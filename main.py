import os
import json
import webbrowser
import spotipy
import spotipy.util as util
from spotipy.exceptions import SpotifyException
from recommendations import get_recommendations


def get_token():
    try:
        token = util.prompt_for_user_token(username, scope=scope, cache_path="C:/Users/hp/PycharmProjects/PTI_test/cache")
    except:
        os.remove(f".cache-{username}")
        token = util.prompt_for_user_token(username, scope=scope, cache_path="C:/Users/hp/PycharmProjects/PTI_test/cache")

    spotify = spotipy.Spotify(auth=token)
    return spotify


def get_time_range():
    time_range = input("Your choice: ")
    print()
    if time_range == "s":
        time_range = "short_term"
    elif time_range == "l":
        time_range = "long_term"
    else:
        time_range = "medium_term"

    return time_range


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
username = input("Your username: ")

spotify = get_token()

user = spotify.current_user()
genres = spotify.recommendation_genre_seeds()
# print(json.dumps(user, sort_keys=True, indent=4))
with open("genres.json", "w") as f:
    json.dump(genres, f, sort_keys=True, indent=4)

displayName = user['display_name']
followers = user['followers']['total']
recoms = get_recommendations(spotify, 10, "short_term")
# print(displayName)

# Device control
devices = spotify.devices()
# pprint(devices)
with open("dev.json", "w") as f:
    json.dump(devices, f, sort_keys=True, indent=4)
device = devices['devices'][0]

while True:
    print()
    print(f">>> Welcome to Spotipy {displayName}!")
    print(f">>> You have {followers} followers.")
    print()
    print(f"Recommendations for {displayName}:")

    # for r in recoms:
    #     print(r[0])

    print()
    print("1 - Search for an artist")
    print("2 - Play a song")
    print("3 - Pause a song")
    print("4 - I wanna listen something random")
    print("5 - Change volume")
    print("6 - Change device")
    print("0 - exit")
    print()
    choice = input("Your choice: ")

    # Search for the artist
    if choice == "1":
        print()
        searchQuery = input("Ok, what's their name?: ")
        print()

        # Get search results
        searchResults = spotify.search(searchQuery, 1, 0, "artist")
        print(json.dumps(searchResults, sort_keys=True, indent=4))

        # Artist details
        artist = searchResults['artists']['items'][0]
        print(artist['name'])
        print(str(artist['followers']['total']) + " followers")
        if len(artist['genres']) > 0:
            print(artist['genres'])
        print()
        webbrowser.open(artist['images'][0]['url'])
        artistID = artist['id']

        # Album and track details
        trackURIs = []
        trackArt = []
        z = 0

        # Extract album data
        albumResults = spotify.artist_albums(artistID)
        albumResults = albumResults['items']

        for item in albumResults:
            print("ALBUM " + item['name'])
            albumID = item['id']
            albumArt = item['images'][0]['url']

            # Extract track data
            trackResults = spotify.album_tracks(albumID)
            trackResults = trackResults['items']

            for track_item in trackResults:
                print(str(z) + ": " + track_item['name'])
                trackURIs.append(track_item['uri'])
                trackArt.append(albumArt)
                z += 1
            print()

        # See album art
        while True:
            songSelection = input("Enter a small number to see the album art associated with it (x to exit): ")
            if songSelection == "x":
                break
            webbrowser.open(trackArt[int(songSelection)])

    elif choice == "2":
        print()
        searchQuery = input("Ok, what's it's name?: ")
        print()

        # Get search results
        searchResults = spotify.search(searchQuery, 1, 0, "track")
        track = searchResults["tracks"]["items"][0]["uri"]
        print(track)

        # get audio features - saved to features.json
        trackFeatures = spotify.audio_features(tracks=[track])
        song = searchResults["tracks"]["items"][0]
        with open("song.json", "w") as f:
            json.dump(song, f, sort_keys=True, indent=4)

        # Change track - do przetestowania
        # spotify.start_playback(device['id'], uris=[track])

        try:
            song_radio = get_recommendations(spotify, 20, "medium_range", [song['uri']])
        except SpotifyException:
            spotify = get_token()
            song_radio = get_recommendations(spotify, 20, "medium_range", [song['uri']])
        playback_queue = [x[1] for x in song_radio]
        playback_queue.insert(0, song['uri'])
        try:
            spotify.start_playback(device['id'], uris=playback_queue)
        except SpotifyException:
            spotify = get_token()


    elif choice == "3":
        devices = spotify.devices()
        print(device['is_active'])
        try:
            spotify.pause_playback()
        except:
            spotify.start_playback()

    elif choice == "4":
        print("What time range do you want to use?")
        print("Type \"s\" for short (approx. a month), \"m\" for medium (approx. 6 months), \"l\" for long (all time)")
        print("Default is medium term")
        time_range = get_time_range()

        try:
            recoms = get_recommendations(spotify, 10, time_range)
        except SpotifyException:
            spotify = get_token()
            recoms = get_recommendations(spotify, 10, time_range)

        print(f"Your recommendations:")

        for r in recoms:
            print(f"{r[0]}")
        print()
        print("Type 1 to play one of these songs, 2 if you want to find similar songs:")
        ch = int(input("Your choice: "))
        print()

        if ch == 1:
            print("Type the number of the song you want to play")
            song_num = int(input("Your choice: "))
            print()

            print(recoms[song_num - 1][1][15::])
            try:
                song_radio = get_recommendations(spotify, 20, "medium_range", [recoms[song_num - 1][1]])
            except SpotifyException:
                spotify = get_token()
                song_radio = get_recommendations(spotify, 20, "medium_range", [recoms[song_num - 1][1]])
            playback_queue = [x[1] for x in song_radio]
            playback_queue.insert(0, recoms[song_num - 1][1])
            try:
                spotify.start_playback(device['id'], uris=playback_queue)
            except SpotifyException:
                spotify = get_token()

        elif ch == 2:
            pass

    elif choice == "5":
        if not device['supports_volume']:
            print("Your device does not support volume control")
            print()
            continue

        vol = int(input("Enter volume percent: "))
        print()

        spotify.volume(vol)

    elif choice == "6":  # do przetestowania (działa)
        devices = spotify.devices()
        with open("dev.json", "w") as f:
            json.dump(devices, f, sort_keys=True, indent=4)

        print("Available devices:")
        i = 1
        for dev in devices['devices']:
            print(f"{i}. {dev['name']}, {dev['type']}")
            i += 1
        i = int(input("Choose your device: "))
        device = devices['devices'][i - 1]

        try:
            spotify.start_playback(device_id=device["id"])
        except SpotifyException:
            pass

    # End the program
    if choice == "0":
        print("exit")
        if device["supports_volume"]:
            spotify.volume(100)
        break

# print(json.dumps(VAR, sort_keys=True, indent=4))
