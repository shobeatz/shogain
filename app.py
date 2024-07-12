import spotipy
from spotipy.oauth2 import SpotifyOAuth
from flask import Flask, request, url_for, session, redirect

app = Flask(__name__)

app.secret_key = "212121212"
app.config['SESSION_COOKIE_NAME'] = "Shobhit's Cookie"

@app.route('/')
def login():
    sp_oauth = create_spotify_oauth()
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@app.route('/redirect')
def redirectPage():
    return 'redirect'

@app.route('/getTracks')
def get_tracks():
    return "Shobeatz tracks & shit"

def create_spotify_oauth():
    return SpotifyOAuth(
        client_id = "ea47669c3d944a7f8ec4fc4232a4ac11",
        client_secret = "b13f5d79c372416e9726d3246b93a8a1",
        redirect_uri = url_for('redirectPage', _external = True),
        scope = "user-library-read" 
    )