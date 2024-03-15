import os
import json
import spotipy
from time import time
from spotify_genres import generate_genres_list, find_genre
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.exceptions import SpotifyException

client_id = 'b57f0441009e4576bd35fb6a36cce302'
client_secret = 'ed55deb9332f42229bc2096215df6bb8'
url = 'https://accounts.spotify.com/api/token'
scope = "user-read-playback-state,user-modify-playback-state,user-top-read"

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


def get_genre(song_genres):
    if not song_genres:
        return 'undefined'
    main_genre = ''
    for g in song_genres:
        main_genre = find_genre(g)
        if not main_genre == 'undefined':
            break
    main_genres[main_genre] += 1
    # print(f"{main_genre}, {stop - start}")

    return main_genre
    # for genre in song_genres:
    #     if 'blues' in genre: main_genres.append('blues')
    #     if 'classical' in genre: main_genres.append('classical')
    #     if 'country' in genre: main_genres.append('country')
    #     if 'electro' in genre: main_genres.append('electronic')
    #     if 'house' in genre: main_genres.append('electronic')
    #     if 'tech' in genre: main_genres.append('electronic')
    #     if 'folk' in genre: main_genres.append('folk/acoustic')
    #     if 'hip hop' in genre: main_genres.append('hip hop')
    #     if 'rap' in genre: main_genres.append('hip hop')
    #     if 'metal' in genre: main_genres.append('metal')
    #     if 'pop' in genre: main_genres.append('pop')
    #     if 'r&b' in genre: main_genres.append('r&b')
    #     if 'soul' in genre: main_genres.append('r&b')
    #     if 'rock' in genre: main_genres.append('rock')


t1 = time()
auth_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(auth_manager=auth_manager)
generate_genres_list()

codes = []
n = 0

# ############### TO-DO ###############
# 1. properties - done
# 2. keys list - done
# 3. genres list - done
# 4. clean code
# 5. stats
# 6. tests
# ############### * * * ###############

with open("testfile02.txt", "r") as f:
    t = f.readlines()

with open("songs_info.txt", "w") as f:
    f.write("Link;Autor;Tytuł;Rodzaj;Duration;Tempo(BPM);Key;Popularity;Happiness;Danceability;Energy;Acousticness;"
            "Instrumentalness;Liveness;Speechiness;Explicit\n")

    for query in t:
        n += 1
        if n % 20 == 0:
            print(n)

        song = sp.search(query.strip(), 1, 0, type="track")["tracks"]["items"][0]
        # print(json.dumps(song["name"], sort_keys=True, indent=4))

        f.write("l;")  # link
        artist = sp.artist(song['artists'][0]['uri'])
        genre = get_genre(artist['genres'])
        f.write(f"{artist['name']};{song['name']};{genre};")

        secs = round(song['duration_ms'] / 1000)
        mins = int(secs / 60)
        a = ""
        if secs % 60 < 10: a = "0"
        f.write(f"{mins}:{a}{secs % 60};")

        tf = sp.audio_features(tracks=[song['uri']])[0]  # it's track features, guy, chill...
        # print(json.dumps(tf, sort_keys=True, indent=4))
        if tf['mode'] == 1:
            mode = "Major"
        else:
            mode = "Minor"
        f.write(f"{round(tf['tempo'])};{keys_dict[tf['key']]} {mode};{song['popularity']};{round(tf['valence'], 2)};"
                f"{round(tf['danceability'], 2)};{round(tf['energy'], 2)};{round(tf['acousticness'], 2)};"
                f"{round(tf['instrumentalness'], 2)};{round(tf['liveness'], 2)};{round(tf['speechiness'], 2)};"
                f"{song['explicit']};")

        f.write("\n")

t2 = time()
print(f"czas dla n = {n}: {t2 - t1}")
print(main_genres)
