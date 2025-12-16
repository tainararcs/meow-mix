import requests
import base64
import dotenv
import os


dotenv.load_dotenv()

# Identificador da aplicação no Spotify
CLIENT_ID = os.getenv('CLIENT_ID')

# Chave secreta da aplicação no Spotify
CLIENT_SECRET = os.getenv('CLIENT_SECRET')

# Escopos de permissão solicitados ao usuário no login do Spotify
# Definem quais ações a aplicação pode realizar em nome do usuário
SCOPES = 'playlist-modify-public playlist-modify-private user-read-private ugc-image-upload'


def refresh_access_token(refresh_token: str) -> dict:
    '''
        Renova o Access Token do Spotify utilizando um Refresh Token válido sem exigir que o usuário faça login novamente.

        Args:
            refresh_token (str): Refresh Token fornecido pelo Spotify durante o fluxo de autenticação OAuth.

        Returns:
            Dict[str, Any]: Dicionário JSON retornado pela API do Spotify contendoo novo token de acesso.
    '''
    # Endpoint do Spotify para renovação de tokens OAuth
    url = 'https://accounts.spotify.com/api/token'

    data = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    }

    response = requests.post(url, data=data)
    return response.json()


def fetch_web_api(endpoint: str, token_access: str, method='GET', body=None) -> dict:
    '''
        Acessa a API do Spotify.

        - endpoint: string com o caminho da API (ex: 'v1/me/top/tracks').
        - method: GET, POST, PUT, DELETE.
        - body: corpo JSON quando houver envio de dados (POST/PUT).

        
        Executa requisições HTTP para a Web API do Spotify.
        Centraliza o acesso à API do Spotify.

        Args:
            endpoint (str): Caminho do endpoint da API do Spotify, sem a URL base. Exemplo: 'v1/me'.
            token_access (str): Access token OAuth 2.0 do usuário
            method (str, opcional): Método HTTP a ser utilizado na requisição.
            body (dict | None, opcional): Corpo da requisição em formato JSON.

        Returns:
            dict: Resposta da API do Spotify já convertida para JSON.

        Raises:
            requests.RequestException: Caso ocorra erro de rede ou falha na execução da requisição.
    '''
    url = f'https://api.spotify.com/{endpoint}'

    headers = {
        'Authorization': f'Bearer {token_access}',
        'Content-Type': 'application/json',
    }

    if method.upper() == 'GET':
        response = requests.get(url, headers=headers)
    else:
        response = requests.request(method, url, headers=headers, json=body)

    return response.json()


def get_user_profile(access_token: str) -> dict:
    '''
        Obtém as informações do perfil do usuário autenticado no Spotify pelo endpoint `/v1/me`.
        
        Args:
            access_token (str): Token de acesso OAuth fornecido pelo Spotify.

        Returns:
            Dict[str, Any]: Dicionário JSON retornado pela API do Spotify com os dados do perfil do usuário.
    '''
    # Endpoint do Spotify que retorna o perfil do usuário autenticado.
    endpoint = 'v1/me'

    # print("\nEscopos do token:", result.headers.get('X-Spotify-Token-Scopes'))
    return fetch_web_api(endpoint, access_token)


def define_playlist_cover(token_access: str, playlist_id: str, mood_tag: str) -> None:
    '''
        Define a imagem de capa de uma playlist no Spotify.
        A imagem é obtida a partir da API pública Cataas (imagens de gatos),
        utilizando uma tag de humor para gerar uma capa temática.

        Args:
            token_access (str): Access token OAuth 2.0 do usuário.
            playlist_id (str): ID da playlist que terá a capa atualizada.
            mood_tag (str): Tag usada para buscar uma imagem temática.
    '''
    # Endpoint da API do Spotify para upload da capa da playlist
    url_spotify = f'https://api.spotify.com/v1/playlists/{playlist_id}/images'
    
    # Endpoint da API Cataas para obter uma imagem temática
    url_cat = f'https://cataas.com/cat/{mood_tag}?type=square'

    # Baixa uma imagem aleatória de gato com base na tag
    cat_image = requests.get(url_cat)
    print('Foto', cat_image)

    # Converte para base64 
    base64_image = base64.b64encode(cat_image.content).decode('utf-8').replace('\n', '')
    
    headers = {
        'Authorization': f'Bearer {token_access}',
        'Content-type': 'image/jpeg'
    }

    # Troca a capa da playlist no spotify.
    resp = requests.put(url_spotify, headers=headers, data=base64_image)

    if resp.status_code not in (200, 202):
        print('\nErro no upload da img:', resp.status_code, resp.text)


def create_playlist(user_id, name, mood_tag, token_access, description='', public=False) -> dict:
    '''
       Cria uma playlist no Spotify para um usuário e define uma capa personalizada.

        Args:
            user_id (str): ID do usuário do Spotify que será o proprietário da playlist.
            name (str): Nome da playlist a ser criada.
            mood_tag (str): Tag visual que representa o humor da playlist.
            token_access (str): Access token OAuth 2.0 do usuário,
            description (str, opcional): Descrição textual da playlist no Spotify.
            public (bool, opcional): Define se a playlist será pública ou privada.

        Returns:
            dict[str, str]: Dicionário contendo:
                - id (str): ID da playlist criada no Spotify.
                - url (str): URL pública da playlist no Spotify.

        Raises:
            requests.RequestException: Caso ocorra falha na comunicação com a API do Spotify ou no download da imagem da capa.
            KeyError: Caso a resposta da API do Spotify não contenha os campos esperados.
    '''    
    # Endpoint responsável por criar playlists para um usuário específico
    endpoint = f'v1/users/{user_id}/playlists'

    body = {
        'name': name,
        'description': description,
        'public': public,
    }

    # Cria a playlist
    playlist = fetch_web_api(endpoint, token_access, 'POST', body)
    playlist_id = playlist['id']

    # Define uma capa para a playlist
    define_playlist_cover(token_access, playlist_id, mood_tag)

    return {
        'id': playlist_id,
        'url': playlist['external_urls']['spotify']
    }


def search_track_uri(title_music: str, artist_music: str, token_access: str) -> str:
    '''
        Pesquisa uma música no Spotify pelo título e nome do artista.

        Args:
            title_music (str): Título da música a ser pesquisada.
            artist_music (str): Nome do artista da música.
            token_access (str): Access token OAuth 2.0 do usuário.

        Returns:
            str | None: URI da música no formato `spotify:track:<id>` ou None.

        Raises:
            requests.RequestException: Caso ocorra falha na comunicação com a API do Spotify.
    '''
    # Monta a query de busca combinando título e artista
    query = f'{title_music} {artist_music}'.replace(' ', '%20')
    
    # Endpoint de busca da API do Spotify
    endpoint = f'v1/search?q={query}&type=track&limit=1'
    
    track_uri = fetch_web_api(endpoint, token_access)
    items = track_uri.get('tracks', {}).get('items', [])

    if not items:
        return None

    # Retorna o primeiro resultado (mais relevante)
    return items[0]['uri']


def add_tracks_playlist(playlist_id: str, tracks_suggestions: list[dict], token_access: str) -> dict:
    '''
        Adiciona uma lista de músicas a uma playlist do Spotify.

        Para cada música sugerida, a função:
        1. Pesquisa a URI oficial da faixa no Spotify.
        2. Agrupa todas as URIs encontradas.
        3. Envia as URIs para o endpoint de adição de faixas da playlist.

        Args:
            playlist_id (str): ID da playlist que receberá as músicas.
            tracks_suggestions (list[dict]): Lista de músicas sugeridas,
            token_access (str): Access token OAuth 2.0 do usuário.

        Returns:
            dict | None: Resposta JSON da API do Spotify, caso músicas sejam adicionadas ou None.

        Raises:
            requests.RequestException: Caso ocorra falha na comunicação com a API do Spotify.
    '''
    # Endpoint responsável por adicionar músicas à playlist
    endpoint = f'v1/playlists/{playlist_id}/tracks'

    uris = []

    for track in tracks_suggestions:
        uri = search_track_uri(track['title'], track['artist'], token_access)
        uris.append(uri) if uri else print('\nMúsica ', track['title'], ' não encontrada no spotify')

    if not uris:
        print("\nNenhuma música encontrada para adicionar à playlist.")
        return None
    
    body = { 'uris': uris }

    # Envia as músicas para a playlist
    return fetch_web_api(endpoint, token_access, method='POST', body=body)
