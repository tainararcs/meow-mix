from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel # Requerido por class PlaylistRequest

import services.gemini as gemini
import services.spotify as spotify
import urllib.parse
import requests

# 
REDIRECT_URI = "http://127.0.0.1:8000/callback"

app = FastAPI()

# Libera o React (localhost:5173)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelo de entrada vindo do front-end (do formulário).
class PlaylistRequest(BaseModel):
    mood: list[str]
    time: list[str]
    goal: list[str]
    genres: list[str]
    rhythm: list[str]
    novelty: list[str]
    languages: list[str]
    limit: int
    obs: str | None = None
    access: str  
    refresh: str

# Frontend -> /login -> Spotify -> /callback -> volta para Frontend -> chama /generate

@app.post('/generate')
async def generate_playlist(payload: PlaylistRequest):
    access = payload.access   # Token do usuário.
    refresh = payload.refresh  # 

    # Obtém info do usuário real.
    user = spotify.get_user_profile(access)
    print('User: ', user)

    if "error" in user and user["error"]["status"] == 401:
        print("Token expirado. Renovando…")
        new_tokens = spotify.refresh_access_token(refresh)
        access = new_tokens["access_token"]
        
        # tenta novamente:
        user = spotify.get_user_profile(access)

    user_id = user["id"]

    suggestions = await gemini.generate_playlist_suggestions(payload)
    suggestions = suggestions[0]
    print('Sugestões: ', suggestions)

    playlist = spotify.create_playlist(user_id, suggestions['name_playlist'], access)
    spotify.add_tracks_playlist(playlist["id"], suggestions['tracks'], access)

    print('Link', playlist["url"])
    return {"playlist_url": playlist["url"]}


@app.get("/login")
def login_spotify():
    params = {
        "client_id": spotify.CLIENT_ID,
        "response_type": "code",
        "redirect_uri": REDIRECT_URI,
        "scope": spotify.SCOPES,
    }    

    url = "https://accounts.spotify.com/authorize?" + urllib.parse.urlencode(params)
    return {"url": url}


@app.get("/callback")
def spotify_callback(code: str):
    if not code:
        return {"error": "No authorization code returned"}

    token_url = "https://accounts.spotify.com/api/token"
    
    body = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "client_id": spotify.CLIENT_ID,
        "client_secret": spotify.CLIENT_SECRET,
    }

    response = requests.post(token_url, data=body)
    tokens = response.json()

    access = tokens["access_token"]
    refresh = tokens["refresh_token"]

    # Redireciona ao frontend com token.
    redirect = (
        f"http://localhost:5173/?access_token={access}"
        f"&refresh_token={refresh}"
    )

    return {"url": redirect}


