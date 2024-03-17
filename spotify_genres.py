from time import time


def binary_search(arr, x):
    low = 0
    high = len(arr) - 1
    mid = 0

    while low <= high:

        mid = (high + low) // 2

        # If x is greater, ignore left half
        if arr[mid] < x:
            low = mid + 1

        # If x is smaller, ignore right half
        elif arr[mid] > x:
            high = mid - 1

        # means x is present at mid
        else:
            return mid

    # If we reach here, then the element was not present
    return -1


# # Test array
# arr = [2, 3, 4, 10, 40]
# x = 10
#
# # Function call
# result = binary_search(arr, x)
#
# if result != -1:
#     print("Element is present at index", str(result))
# else:
#     print("Element is not present in array")


genres = ["blues", "classical", "country", "electronic", "folk/acoustic", "hip hop", "jazz", "latin", "metal",
          "pop", "r&b", "rock"]

subgenres = {
    "blues": [],
    "classical": [],
    "country": [],
    "electronic": [],
    "folk/acoustic": [],
    "hip hop": [],
    "jazz": [],
    "latin": [],
    "metal": [],
    "pop": [],
    "r&b": [],
    "rock": []
}


def generate_genres_list():
    start = time()
    for genre in subgenres.keys():
        if genre == 'folk/acoustic':
            fname = 'folk_acoustic'
        elif genre == 'hip hop':
            fname = 'hip_hop'
        elif genre == 'r&b':
            fname = 'rnb'
        else:
            fname = genre

        with open(f"genres/{fname}_genres.txt") as file:
            t = file.readlines()
            t2 = []
            for i in t: t2.append(i.strip())
            subgenres[genre] = sorted(t2)
            # print(sorted(t2))
        # SpotifyGenres.subgenres[genre] = SpotifyGenres.subgenres[genre].sort()

    stop = time()
    print((stop - start) * 1000)


def find_genre(name):
    main_genre = 'undefined'
    # print(binary_search(SpotifyGenres.subgenres['pop'], name.strip()))
    for genre in subgenres.keys():
        if binary_search(subgenres[genre], name.strip()) >= 0:
            main_genre = genre
            break
    return main_genre


if __name__ == "__main__":
    generate_genres_list()
