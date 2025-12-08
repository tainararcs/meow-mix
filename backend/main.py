import services.gemini as gemini
import services.spotify as spotify
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse 
from pydantic import BaseModel                      # Requerido por class PlaylistRequest
import urllib.parse                                 # Requerido por login_spotify *
import requests

# 
REDIRECT_URI = 'http://127.0.0.1:8000/callback'

app = FastAPI()

# Libera o React (localhost:5173)
app.add_middleware( CORSMiddleware, allow_origins=['*'], allow_credentials=True, allow_methods=['*'], allow_headers=['*'], )

class PlaylistRequest(BaseModel):
    '''
    Modelo de entrada vindo do front-end (do formulário).
    '''
    mood: list[str]
    timeOfDay: list[str]
    goal: list[str]
    genres: list[str]
    rhythm: list[str]
    novelty: list[str]
    languages: list[str]
    limit: int
    obs: str | None = None
    access_token: str | None = None
    refresh_token: str | None = None

# Frontend -> /login -> Spotify -> /callback -> volta para Frontend -> chama /generate

@app.post('/generate')
async def generate_playlist(payload: PlaylistRequest) -> dict:
    '''
    Cria a playlist
    '''

    access_token = payload.access_token      # Token do usuário.
    refresh_token = payload.refresh_token    # Token.

    # Obtém info do usuário real.
    user = spotify.get_user_profile(access_token)
    print('User: ', user, '\n')

    if 'error' in user and user['error']['status'] == 401:
        access_token = spotify.refresh_access_token(refresh_token)['access_token']
        print('Token expirado. Foi renovado para: ', access_token, '\n')
        # access_token = new_tokens['access_token']
        user = spotify.get_user_profile(access_token) # Tenta novamente

    suggestions = await gemini.generate_playlist_suggestions(payload)
    suggestions = suggestions[0]
    # print('Sugestões: ', suggestions)

    playlist = spotify.create_playlist(user['id'], suggestions['playlist_name'], access_token)
    spotify.add_tracks_playlist(playlist['id'], suggestions['tracks'], access_token)

    print('Link', playlist['url'], '\n')
    return {'playlist_url': playlist['url']}


@app.get('/login')
def login_spotify() -> dict:  
    ''' 
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
def spotify_callback(code: str) -> dict:
    '''
    '''

    if not code:
        return {'error': 'No authorization code returned'}

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
        print('Erro ao obter tokens:', tokens)
        return RedirectResponse(url='http://localhost:5173/?error=auth_failed')
    
    access_token = tokens['access_token']
    refresh_token = tokens['refresh_token']

    # Redireciona ao frontend com token.
    redirect_url = f'http://localhost:5173/?access_token={access_token}&refresh_token={refresh_token}'
    return {'url': redirect_url}   
