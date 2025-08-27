def calculate(process):
    n = len(process)
    process.sort(key=lambda x: x[1])
    FT, WT, TAT, RT = [], [], [], []
    time = 0
    gant_chart = []
    
    for x in range(n):
        pid, at, bt = process[x]
        
        if time < at:
            gant_chart.append(("idle",time, at))
            time = at
        rt = time
        ft = time + bt
        
        tat = rt - at
        wt = ft - at
        
        FT.append(ft)
        WT.append(wt)
        TAT.append(tat)
        RT.append(rt)

        gant_chart.append((f"P{pid}", time, ft))
        time = at
    for x in gant_chart:
        print(x)
    

file = open("config.txt", "r").read().split("<cut>")
p = file[1].strip().splitlines()
n = file[0].strip().split("=")[1].strip()
process = []
for idx, x in enumerate(p):
    parts = x.strip().split()
    at, bt = int(parts[0]),int(parts[1])
    process.append((idx+1,at,bt))
calculate(process)