file2 = open("config.txt", "r", encoding="utf-8").read().split('@')
temp = file2[0].split("=")[1].strip()
cont = file2[1].split("=")[1].strip()

print(cont)

