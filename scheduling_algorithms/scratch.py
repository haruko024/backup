
file = open("config.txt","r").read().split("<cut>")
p = file[0].split("=")[1].strip()
proc = file[1].strip().splitlines()

processes = []
for x in proc:
    parts = x.strip().split()
    formatted = int(parts[0]), int(parts[1])
    processes.append(formatted)

print((processes))