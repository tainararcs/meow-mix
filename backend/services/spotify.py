import requests

# ID do usuário no Spotify.
CLIENT_ID = '' # USER_ID
CLIENT_SECRET = ''
SCOPES = "playlist-modify-public playlist-modify-private user-read-private"


def get_user_profile(access_token):
    '''
    '''
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    result = requests.get("https://api.spotify.com/v1/me", headers=headers)
    return result.json()


def refresh_access_token(refresh_token):
    url = "https://accounts.spotify.com/api/token"

    data = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    }

    response = requests.post(url, data=data)
    return response.json()


def fetch_web_api(endpoint, token, method='GET', body=None):
    '''
        Acessa a API do Spotify.

        - endpoint: string com o caminho da API (ex: 'v1/me/top/tracks').
        - method: GET, POST, PUT, DELETE.
        - body: corpo JSON quando houver envio de dados (POST/PUT).

        Retorna: JSON da resposta da API.
    '''
    url = f'https://api.spotify.com/{endpoint}'

    # Cabeçalhos exigidos pelo Spotify.
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json',
    }

    # Execução da requisição
    if method.upper() == 'GET':
        response = requests.get(url, headers=headers)
    else:
        response = requests.request(method, url, headers=headers, json=body)

    return response.json()


def create_playlist(user_id, name, token, description="", public=False):
    '''
        Cria uma playlist para um usuário.
        Endpoint: POST https://api.spotify.com/v1/users/{user_id}/playlists

        Retorna dados da playlist criada.
    '''
    endpoint = f"v1/users/{user_id}/playlists"

    body = {
        "name": name,
        "description": description,
        "public": public,
    }

    playlist = fetch_web_api(endpoint, token, method="POST", body=body)

    return {
        "id": playlist["id"],
        "url": playlist["external_urls"]["spotify"]
    }


def search_track_uri(title_music, artist_music, token):
    """
        Pesquisa uma música pelo nome e artista e retorna sua URI real do Spotify.
    """
    query = f"{title_music} {artist_music}".replace(" ", "%20")
    endpoint = f"v1/search?q={query}&type=track&limit=1"
    
    track_uri = fetch_web_api(endpoint, token)
    return track_uri['tracks']['items'][0]['uri']


def add_tracks_playlist(playlist_id, tracks_suggestions, token):
    """
        Adiciona músicas à playlist.
        Endpoint: POST https://api.spotify.com/v1/playlists/{playlist_id}/tracks
        
        track_uris: lista de URIs no formato: "spotify:track:ID"
    """
    endpoint = f"v1/playlists/{playlist_id}/tracks"

    uris = []

    for track in tracks_suggestions:
        uri = search_track_uri(track['title'], track['artist'], token)
        uris.append(uri) if uri else print('Música ', track['title'], ' não encontrada')

    body = { "uris": uris }

    return fetch_web_api(endpoint, token, method="POST", body=body)
