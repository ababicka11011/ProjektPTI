keys_dict = {
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

with open("keys.txt", "w") as f:
    f.write("(")
    for key in keys_dict.values():
        if key == 'B':
            f.write(f"(\"{key} Major\"),")
            f.write(f"(\"{key} Minor\")")
        else:
            f.write(f"(\"{key} Major\"),")
            f.write(f"(\"{key} Minor\"),")
    f.write(")")