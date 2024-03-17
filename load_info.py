import os
import json
import spotipy
import requests
from time import time
from spotify_genres import generate_genres_list, find_genre
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.exceptions import SpotifyException


client_id = 'b57f0441009e4576bd35fb6a36cce302'
client_secret = '2239ed9d1133428bb7b8333c04922424'
# client_id = 'a35f2af546ee4562b6fb53de3dcfcd3c'
# client_secret = '4f814bb60ea24a60b10d4aa81acbc6a3'
url = 'https://accounts.spotify.com/api/token'
scope = "user-read-playback-state,user-modify-playback-state,user-top-read"
playlist_link = "https://open.spotify.com/playlist/37i9dQZF1DWZBCPUIUs2iR?si=94471ac501d34470"
separator = ','
target_genre = 'country'

codes = []
n = 0

os.environ['SPOTIPY_CLIENT_ID'] = client_id
os.environ['SPOTIPY_CLIENT_SECRET'] = client_secret

keys_dict = {
    -1: "-",
    0: "C",
    1: "C#/Db",
    2: "D",
    3: "D#/Eb",
    4: "E",
    5: "F",
    6: "F#/Gb",
    7: "G",
    8: "G#/Ab",
    9: "A",
    10: "A#/Bb",
    11: "B"
}

main_genres = {
    "blues": 0,
    "classical": 0,
    "country": 0,
    "electronic": 0,
    "folk/acoustic": 0,
    "hip hop": 0,
    "jazz": 0,
    "latin": 0,
    "metal": 0,
    "pop": 0,
    "r&b": 0,
    "rock": 0,
    "undefined": 0
}

playlist_id = playlist_link[34:56:]
t1 = time()
auth_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(auth_manager=auth_manager)
generate_genres_list()
if os.path.exists("songs_in_db.json"):
    with open("songs_in_db.json", "r") as f:
        try:
            songs_in_db = json.load(f)
        except json.decoder.JSONDecodeError:
            songs_in_db = []
else:
    songs_in_db = []


def get_genre(song_genres):
    if not song_genres:
        return []
    main_genre_list = []
    for g in song_genres:
        main_genre = find_genre(g)
        if (not main_genre == 'undefined') and (main_genre not in main_genre_list):
            main_genre_list.append(main_genre)

    if target_genre == '' or (len(main_genre_list) > 0 and main_genre_list[0] == target_genre):
        for i in main_genre_list:
            main_genres[i] += 1
        return '*'.join(main_genre_list)
    else:
        return ''


def write_info(song, f, tracks_features):
    artist = sp.artist(song['artists'][0]['uri'])
    genre = get_genre(artist['genres'])

    if genre == '':
        return

    print(song['name'])
    f.write(f"https://open.spotify.com/track/{song['id']}{separator}")  # link
    f.write(f"{artist['name']}{separator}{song['name']}{separator}{genre}{separator}")

    secs = round(song['duration_ms'] / 1000)
    mins = int(secs / 60)
    a = ""
    if secs % 60 < 10: a = "0"
    f.write(f"{mins}:{a}{secs % 60}{separator}")

    tf = tracks_features[(n % 100) - 1]  # it's track features, guy, chill...
    if tf['mode'] == 1:
        mode = "Major"
    else:
        mode = "Minor"
    f.write(
        f"{round(tf['tempo'])}{separator}{keys_dict[tf['key']]} {mode}{separator}{song['popularity']}{separator}{round(tf['valence'], 2)}{separator}"
        f"{round(tf['danceability'], 2)}{separator}{round(tf['energy'], 2)}{separator}{round(tf['acousticness'], 2)}{separator}"
        f"{round(tf['instrumentalness'], 2)}{separator}{round(tf['liveness'], 2)}{separator}{round(tf['speechiness'], 2)}{separator}"
        f"{song['explicit']}")

    f.write("\n")


# ############### TO-DO ###############
# 1. properties - done
# 2. keys list - done
# 3. genres list - done
# 4. clean code - done i guess
# 5. stats - done
# 6. tests - will work out
# 7. check if already in db - done
# 8. multiple genres - done
# 9. wait until spotify unlocks me or idk - done
# 10. more - country - done
#  - folk/acoustic
#  - jazz - done
# ############### * * * ############### ale ja dobra w to programowanie jestem


# with open("songs.txt", "r") as f:
#     t = f.readlines()

with open("songs_info.txt", "a") as f:
    # f.write("Link;Autor;Tytuł;Rodzaj;Duration;Tempo(BPM);Key;Popularity;Happiness;Danceability;Energy;Acousticness;"
    #         "Instrumentalness;Liveness;Speechiness;Explicit\n")

    playlist = sp.playlist(playlist_id)
    pl_length = playlist["tracks"]["total"]
    print(pl_length)

    offset = 0
    while pl_length > 0:
        ids = []
        playlist = sp.playlist_tracks(playlist_id, offset=offset)
        offset += 100
        for song in playlist["items"]:
            ids.append(song["track"]["id"])
        try:
            tracks_features = sp.audio_features(tracks=ids)
            # print(tracks_features)
        except Exception as e:
            print(e)

        # print({f'offset: {offset}'})
        for song in playlist["items"]:
            n += 1
            if n % 20 == 0:
                print(n, song['track']['name'])
            # print(json.dumps(song, indent=4))
            # print(song["track"]["id"])
            if song["track"]["id"] in songs_in_db:
                continue
            # print(f"{item['track']['name']} {item['track']['artists'][0]['name']}")
            try:
                write_info(song["track"], f, tracks_features)
                songs_in_db.append(song["track"]["id"])
            except UnicodeEncodeError:
                print(f"dziwne znaczki detected: {song['track']['name']}")
        # print(pl_length)
        pl_length -= 100

    # for query in t:
    #     song = sp.search(query.strip(), 1, 0, type="track")["tracks"]["items"][0]
    #     write_info(song, f)

t2 = time()
print(f"czas dla n = {n}: {t2 - t1}")
with open("songs_in_db.json", "w") as f:
    json.dump(songs_in_db, f)
print(main_genres)
