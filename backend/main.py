import services.gemini as gemini
import services.spotify as spotify
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse      # Requerido pelo callback
from pydantic import BaseModel                      # Requerido por class PlaylistRequest
import urllib.parse                                 # Requerido para os parâmetros do login
import requests
import os


app = FastAPI()
app.add_middleware( CORSMiddleware, allow_origins=['*'], allow_credentials=True, allow_methods=['*'], allow_headers=['*'], )

# URL de callback chamada pelo Spotify após o login do usuário
REDIRECT_URI = os.getenv("REDIRECT_URI")
FRONTEND_URL = os.getenv("FRONTEND_URL")


class PlaylistRequest(BaseModel):
    '''
        Modelo de entrada recebido do frontend para geração de playlists.
    '''
    mood: list[str]
    timeOfDay: list[str]
    goal: list[str]
    genres: list[str]
    rhythm: list[str]
    novelty: list[str]
    language: list[str]
    limit: int
    obs: str | None = None
    access_token: str | None = None
    refresh_token: str | None = None

# Frontend -> /login -> Spotify -> /callback -> volta para Frontend -> chama /generate

@app.post('/generate')
async def generate_playlist(payload: PlaylistRequest) -> dict:
    '''
        Cria uma playlist personalizada no Spotify com base nas preferências do usuário.
        Utiliza token para identificar o usuário no Spotify ou o renova automaticamente.
        Adiciona as músicas sugeridas à playlist.

        Args:
            payload (PlaylistRequest): Dados enviados pelo front-end.

        Returns:
            dict[str, str]: Objeto contendo a URL da playlist criada no Spotify. No formato:
            { "playlist_url": "<url_da_playlist>" }

        Raises:
            HTTPException: Caso ocorram falhas nas integrações com a API do Spotify ou na geração de sugestões.
    '''
    # Log das preferências recebidas do formulário 
    print('\nPayload:', payload.mood, payload.timeOfDay, payload.goal, payload.genres, payload.rhythm, payload.novelty, payload.language, payload.limit, payload.obs)

    access_token = payload.access_token      
    refresh_token = payload.refresh_token   

    # Obtém info do usuário real
    user = spotify.get_user_profile(access_token)
    print('User:', user)

    if 'error' in user and user['error']['status'] == 401:
        access_token = spotify.refresh_access_token(refresh_token)['access_token']
        print('\nToken expirado foi renovado')
        
        user = spotify.get_user_profile(access_token) # Tenta novamente

    suggestions = await gemini.generate_playlist_suggestions(payload)
    
    print('\nNome da playlist:', suggestions['playlist_name'])
    print('Tag para a capa:', suggestions['tag'])
    print('Musicas sugeridas:', suggestions['tracks'], '\n')

    playlist = spotify.create_playlist(user['id'], suggestions['playlist_name'], suggestions['tag'], access_token)
    spotify.add_tracks_playlist(playlist['id'], suggestions['tracks'], access_token)

    print('Link: ', playlist['url'], '\n')
    return {'playlist_url': playlist['url']}


@app.get('/login')
def login_spotify() -> dict:  
    ''' 
        Inicia o fluxo de autenticação OAuth com o Spotify.
        Endpoint apenas gera a URL de autorização do Spotify contendo os parâmetros necessários.

        Returns:
            dict[str, str]: Objeto contendo a URL de autenticação do Spotify. No formato:
            { "url": "https://accounts.spotify.com/authorize?... " }
    '''
    params = {
        "client_id": spotify.CLIENT_ID,
        "response_type": "code",
        "redirect_uri": REDIRECT_URI,
        "scope": spotify.SCOPES,
    } 

    url = 'https://accounts.spotify.com/authorize?' + urllib.parse.urlencode(params)
    return {'url': url}


@app.get('/callback')
def spotify_callback(code: str) -> RedirectResponse:
    '''
        Callback OAuth do Spotify.
        Endpoint chamado automaticamente pelo Spotify após o usuário autorizar a aplicação.
        Retorna o usuário de volta para o frontend contendo os tokens como parâmetros.

        Args:
            code (str): Authorization code fornecido pelo Spotify após o login do usuário.

        Returns:
            RedirectResponse: Retorna para o frontend em caso de sucesso ou com falha de autenticação.
    '''

    if not code:
        return {'error': 'Nenhum código de autorização retornado'}

    token_url = 'https://accounts.spotify.com/api/token'
    
    body = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "client_id": spotify.CLIENT_ID,
        "client_secret": spotify.CLIENT_SECRET,
    }

    response = requests.post(token_url, data=body)
    tokens = response.json()

    if 'error' in tokens:
        print('\nErro ao obter tokens:', tokens)
        return RedirectResponse(url=f'{FRONTEND_URL}/?error=auth_failed')
    
    access_token = tokens['access_token']
    refresh_token = tokens['refresh_token']

    # Redireciona ao frontend com os tokens.
    redirect_url = f'{FRONTEND_URL}/?access_token={access_token}&refresh_token={refresh_token}'
    return RedirectResponse(redirect_url)
