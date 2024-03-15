import os
import json
import webbrowser
import spotipy
import spotipy.util as util
from spotipy import SpotifyOAuth, SpotifyClientCredentials
from spotipy.exceptions import SpotifyException
from recommendations import get_recommendations

client_id = 'b57f0441009e4576bd35fb6a36cce302'
client_secret = 'ed55deb9332f42229bc2096215df6bb8'
url = 'https://accounts.spotify.com/api/token'
scope = "user-read-playback-state,user-modify-playback-state,user-top-read"

os.environ['SPOTIPY_CLIENT_ID'] = client_id
os.environ['SPOTIPY_CLIENT_SECRET'] = client_secret
os.environ['SPOTIPY_REDIRECT_URI'] = 'http://localhost:3000'
print(os.environ.get('SPOTIPY_REDIRECT_URI'))

# username = sys.argv[1]
# annababicka?si=2ec7fb07bdf24f7d
username = "Niuń"

# auth = SpotifyOAuth(
#         redirect_uri="http://localhost:8080",
#         username=username,
#         scope=scope
#     )

# spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
# spotify = spotipy.Spotify(auth_manager = SpotifyOAuth(client_id = '', client_secret = '', redirect_uri = ''))

# auth.get_auth_response(open_browser=False)

try:
    token = util.prompt_for_user_token(username, scope=scope)
except:
    os.remove(f".cache-{username}")
    token = util.prompt_for_user_token(username, scope=scope)

spotify = spotipy.Spotify(auth=token)
print(spotify.me())  # Just for cache
