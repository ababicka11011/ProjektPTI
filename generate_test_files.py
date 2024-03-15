import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

client_id = 'b57f0441009e4576bd35fb6a36cce302'
client_secret = 'ed55deb9332f42229bc2096215df6bb8'
url = 'https://accounts.spotify.com/api/token'
scope = "user-read-playback-state,user-modify-playback-state,user-top-read"

os.environ['SPOTIPY_CLIENT_ID'] = client_id
os.environ['SPOTIPY_CLIENT_SECRET'] = client_secret

auth_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(auth_manager=auth_manager)

playlist = sp.playlist_tracks("37zwhMsLdsyqJQT2S9PDfr")
n = playlist["total"]
print(n)

with open("testfile02.txt", "w") as f:
    for item in playlist["items"]:
        #print(f"{item['track']['name']} {item['track']['artists'][0]['name']}")
        try:
            f.write(f"{item['track']['name']} {item['track']['artists'][0]['name']}\n")
        except UnicodeEncodeError:
            print("dziwne znaczki detected")

    o = 100
    while n > 100:
        o+=100
        playlist = sp.playlist_tracks("37zwhMsLdsyqJQT2S9PDfr", offset=o)
        for item in playlist["items"]:
            # print(f"{item['track']['name']} {item['track']['artists'][0]['name']}")
            try:
                f.write(f"{item['track']['name']} {item['track']['artists'][0]['name']}\n")
            except UnicodeEncodeError:
                print("dziwne znaczki detected")
        n-=100

    # with open("playlist.json", "w") as f:
#     json.dump(playlist, f, sort_keys=True, indent=4)
# print(json.dumps(playlist, sort_keys=True, indent=4))


