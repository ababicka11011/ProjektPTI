genres = ["blues", "classical", "country", "electronic", "folk_acoustic", "hip_hop", "jazz", "latin", "metal", "pop",
          "rnb", "rock"]

for genre in genres:
    with open(f"genres/{genre}_genres.txt", "r") as f:
        g = f.readlines()

    with open(f"genres/{genre}_genres.txt", "w") as f:
        for i in g:
            l = i.strip().lower()
            print(l)
            # if genre not in l:
            #     f.write(f"{l}\n")
            f.write(f"{l}\n")
