import json
import spotipy
from random import randint


def get_recommendations(sp: spotipy.Spotify, limit: int, time_range: str, seed_tracks=None):
    if seed_tracks is None or seed_tracks == []:
        seed_tracks = []
        top_songs = sp.current_user_top_tracks(limit=20, time_range=time_range)["items"]
        print(len(top_songs))
        # print(json.dumps(top_songs, sort_keys=True, indent=4))
        for i in range(5):
            index = randint(0, 19-i)
            seed_tracks.append(top_songs[index]["id"])

    recoms = sp.recommendations(seed_tracks=seed_tracks, limit=limit)

    with open("recommendations.json", "w") as f:
        json.dump(recoms, f, sort_keys=True, indent=4)

    rec = []
    i = 1
    for song in recoms["tracks"]:
        rec.append((f"{i}. {song['name']}, {song['artists'][0]['name']}", song["uri"]))
        i += 1

    return rec
