import tkinter as tk
import threading
import time
def fcfs_scheduling(processes):
    n = len(processes)
    processes.sort(key=lambda x: x[1])  

    FT, WT, TAT, RT = [], [], [], []
    gantt_chart = []
    time = 0

    for x in range(n):
        pid, at, bt = processes[x]

        if time < at:
            gantt_chart.append(("Idle", time, at))
            time = at  

        rt = time  
        ft = time + bt  

        tat = rt - at  
        wt = ft - at  

        FT.append(ft)
        RT.append(rt)
        TAT.append(tat)
        WT.append(wt)

        gantt_chart.append((f"P{pid}", time, ft))
        time = ft 

    TBT = sum([p[2] for p in processes])
    TFT = FT[-1]
    AWT = sum(WT) / n
    ATAT = sum(TAT) / n
    CPU_UTIL = (TBT / TFT) * 100
    THROUGHPUT = n / TFT  
    THP = THROUGHPUT * 100
    print("\nPID | AT | BT | FT | WT | RT | TAT")

    combined = []
    for i in range(n):
        combined.append((
            processes[i][0],  # PID
            processes[i][1],  # AT
            processes[i][2],  # BT
            FT[i],
            WT[i],
            RT[i],
            TAT[i]
        ))

    combined.sort(key=lambda x: x[0])

    for entry in combined:
        print(f"{entry[0]:3} | {entry[1]:2} | {entry[2]:2} | {entry[3]:2} | {entry[4]:2} | {entry[5]:2} | {entry[6]:2}")


    # print("\nPID | AT | BT | FT | WT | RT | TAT")
    # for i in range(n):
    #     print(f"{processes[i][0]:3} | {processes[i][1]:2} | {processes[i][2]:2} | {FT[i]:2} | {WT[i]:2} | {RT[i]:2} | {TAT[i]:2}")
    print("")
    print("="*50)
    print(f"Number of Process = {n}")
    print(f"Waiting Time (WT) = FT - AT")
    print(f"Turn Around Time (TAT) = RT - AT")
    print("-"*40)
    print(f"Total Burst Time (TBT) = {TBT}     # Sum of BT")
    print(f"Total Finish Time (TFT) = {TFT}    # Last FT")
    print("-"*40)
    print(f"Average Turnaround Time (ATAT) = sum(TAT) / #process = {sum(TAT)} / {n} = {ATAT:.2f}")
    print(f"Average Waiting Time (AWT) = sum(WT) / #process = {sum(WT)} / {n} = {AWT:.2f}")
    print(f"CPU Utilization = (TBT / TFT)* 100 = ({TBT} / {TFT}) * 100 = {CPU_UTIL:.2f}%")
    print(f"Throughput = #process / TFT = {n} / {TFT} = {THROUGHPUT:.4f} or {THP:.2f}%")
    print("="*50)
    print("MASAYA KANA BOI?")

    root = tk.Tk()
    root.title("FCFS Scheduling - Gantt Chart")
    root.iconbitmap("assets/icon.ico")

    width = 1300
    height = 120
    scale = width // (TFT +1) 

    canvas = tk.Canvas(root, height=height, width=width, bg="white")
    canvas.pack(fill="both", expand=True)

    x_start = 20

    for task in gantt_chart:
        label, start, end = task
        x1 = x_start + start * scale
        x2 = x_start + end * scale
        canvas.create_rectangle(x1, 30, x2, 70, fill="skyblue", outline="black")
        canvas.create_text((x1 + x2) // 2, 50, text=label)
        canvas.create_text(x1, 75, text=str(start))
    canvas.create_text(x2, 75, text=str(end))

    threading.Thread(target=show_summary_table, args=(processes, FT, WT, RT, TAT, AWT, ATAT,)).start()
    root.mainloop()
    
def show_summary_table(processes, FT, WT, RT, TAT, AWT, ATAT):
    root = tk.Toplevel()
    root.title("FCFS Summary Table")
    root.iconbitmap("assets/icon.ico")

    headers = ["PID", "FT", "AT", "WT", "RT", "AT", "TAT"]
    for col, h in enumerate(headers):
        label = tk.Label(root, text=h, font=("Arial", 12, "bold"), borderwidth=2, relief="groove", bg="lightgray")
        label.grid(row=0, column=col, sticky="nsew")

    n = len(processes)

    combined = []
    for i in range(n):
        pid = processes[i][0]
        at = processes[i][1]
        bt = processes[i][2]
        ft = FT[i]
        wt = WT[i]
        rt = RT[i]
        tat = TAT[i]
        combined.append((pid, ft, at, wt, rt, at, tat))

    combined.sort(key=lambda x: x[0])  # Sort by PID

    for row, entry in enumerate(combined, start=1):
        for col, value in enumerate(entry):
            tk.Label(root, text=str(value), borderwidth=2, relief="groove").grid(row=row, column=col, sticky="nsew")

    # Show AWT and ATAT
    tk.Label(root, text="AWT", font=("Arial", 12, "bold"), bg="yellow", borderwidth=2, relief="groove").grid(row=n+1, column=4, sticky="nsew")
    tk.Label(root, text=f"{AWT:.1f}", font=("Arial", 12), bg="yellow", borderwidth=2, relief="groove").grid(row=n+1, column=5, sticky="nsew")

    tk.Label(root, text="ATAT", font=("Arial", 12, "bold"), bg="yellow", borderwidth=2, relief="groove").grid(row=n+2, column=4, sticky="nsew")
    tk.Label(root, text=f"{ATAT:.1f}", font=("Arial", 12), bg="yellow", borderwidth=2, relief="groove").grid(row=n+2, column=5, sticky="nsew")

def show_process_table(processes):
    root = tk.Tk()
    root.title("Process Queue")
    root.iconbitmap("assets/icon.ico")

    at_label = tk.Label(root, text="AT", font=("Arial", 12, "bold"), borderwidth=2, relief="groove")
    at_label.grid(row=0, column=0, sticky="nsew")

    bt_label = tk.Label(root, text="BT", font=("Arial", 12, "bold"), borderwidth=2, relief="groove")
    bt_label.grid(row=2, column=0, sticky="nsew")

    arrival_times = [p[1] for p in processes]
    burst_times = [p[2] for p in processes]

    processes_sorted = sorted(processes, key=lambda x: x[1])

    for idx, (pid, at, bt) in enumerate(processes_sorted, start=1):
        p_label = tk.Label(root, text=f"P{pid}", font=("Arial", 12), borderwidth=2, relief="groove")
        p_label.grid(row=1, column=idx, sticky="nsew")

        at_time_label = tk.Label(root, text=str(at), font=("Arial", 12), borderwidth=2, relief="groove")
        at_time_label.grid(row=0, column=idx, sticky="nsew")

        bt_time_label = tk.Label(root, text=str(bt), font=("Arial", 12), borderwidth=2, relief="groove")
        bt_time_label.grid(row=2, column=idx, sticky="nsew")

    root.mainloop()
    

def main1(processes):
    print("""
                                                        ███████╗ ██████╗███████╗███████╗
First Come First Serve (FCFS) Scheduling Algorithms     ██╔════╝██╔════╝██╔════╝██╔════╝    
            August 21, 2025                             █████╗  ██║     █████╗  ███████╗         
        Code by Paul Mendoza                            ██╔══╝  ██║     ██╔══╝  ╚════██║
                v1.0                                    ██║     ╚██████╗██║     ███████║
                                                        ╚═╝      ╚═════╝╚═╝     ╚══════╝
""")
    question = input("Pogi ba si Fafa Paul [Y/n]: ")
    if question.lower() == "y":
        threading.Thread(target=fcfs_scheduling, args=(processes,)).start()
        threading.Thread(target=show_process_table, args=(processes,)).start()
    else:
        print("Bahala ka! walang sagot!.")

def main():
    err = False
    processes = []
    file = open("config.txt","r").read().split("<cut>")
    num_processes = int(file[0].split("=")[1].strip())
    proc = file[1].strip().splitlines()
    for idx, x in enumerate(proc):
        if num_processes != len(proc):
            err = True
            print("Error: Number of processes is not equal to number of lines!. Check the (config.txt)")
            print("Exiting..")
            time.sleep(5)
            break
        else:
            parts = x.strip().split()
            at, bt = int(parts[0]), int(parts[1])
            processes.append((idx + 1, at, bt))
    if not err == True:
        main1(processes)

# num_processes = int(input("Enter number of processes: "))
# for i in range(1, num_processes + 1):
#     at = int(input(f"Enter Arrival Time of P{i}: "))
#     bt = int(input(f"Enter Burst Time of P{i}: "))
#     processes.append((i, at, bt))


if __name__ == "__main__":
    main()
    
    
