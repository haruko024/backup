import tkinter as tk
import threading
import time
import os

def clear():
    if os.name == "nt":
        _ = os.system("cls")
    else:
        _ = os.system("clear")
    
def fcfs():
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
        THROUGHPUT = n / TBT  
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
        print("="*100)
        print(f"Number of Process = {n}")
        print(f"Waiting Time (WT) = FT - AT")
        print(f"Turn Around Time (TAT) = RT - AT")
        print("-"*80)
        print(f"Total Burst Time (TBT) = {TBT}     # Sum of BT")
        print(f"Total Finish Time (TFT) = {TFT}    # Last FT")
        print("-"*80)
        print(f"Average Turnaround Time (ATAT) = sum(TAT) / #process = \t\t{sum(TAT)} / {n} = {ATAT:.2f}")
        print(f"Average Waiting Time (AWT) = sum(WT) / #process = \t\t{sum(WT)} / {n} = {AWT:.2f}")
        print(f"CPU Utilization = (TBT / TFT)* 100 = \t\t\t\t({TBT} / {TFT}) * 100 = {CPU_UTIL:.2f}%")
        print(f"Throughput = #process / TBT = \t\t\t\t\t{n} / {TBT} = {THROUGHPUT:.4f} or {THP:.2f}%")
        print("="*100)
        print("MASAYA KANA BOI?")

        root = tk.Tk()
        root.title("FCFS Scheduling - Gantt Chart")
        try:
            root.iconbitmap("assets/icon.ico")
        except:
            pass 

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
        try:
            root.iconbitmap("assets/icon.ico")
        except:
            pass 

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
        try:
            root.iconbitmap("assets/icon.ico")
        except:
            pass 

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
        question = input("Second Question, Pogi ba talaga si Fafa Paul [Y/n]: ")
        if question.lower() == "y":
            threading.Thread(target=fcfs_scheduling, args=(processes,)).start()
            threading.Thread(target=show_process_table, args=(processes,)).start()
        else:
            print("Bahala ka! walang sagot!.")
            print("Retrying..")
            time.sleep(2)
            return main()

    def main():
        clear()
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
    if __name__ == "__main__":
        main()

def ps():
    print("--- Priority Scheduling ---")
    print("Future Update..")
    time.sleep(3)
    return main()

def srt():
    print("--- Shortest Remaining Time ---")
    print("Future Update..")
    time.sleep(3)
    return main()

def sjt():
    print("--- Shortest Job First ---")
    print("Future Update..")
    time.sleep(3)
    return main()

def rrs():
    print("--- Round Robin Scheduling ---")
    print("Future Update..")
    time.sleep(3)
    return main()

def mqs():
    print("--- Multilevel Queue Scheduling ---")
    print("Future Update..")
    time.sleep(3)
    return main()


def main():
    while True:
        print("\n--- SCHEDULING ALGORITMS v1.0---")
        print("Options:")
        print("[1] First Come First Serve")
        print("[2] Priority Scheduling")
        print("[3] Shortest Remaining Time")
        print("[4] Shortest Job First")
        print("[5] Round Robin Scheduling")
        print("[6] Multilevel Queue Scheduling")
        print("[q] Quit")
        command = input("\nSelect Option: ")
        if command == "1" or command == "01":
            clear()
            fcfs()
            break
        elif command == "2" or command == "02":
            clear()
            ps()
            break
        elif command == "3" or command == "03":
            clear()
            srt()
            break
        elif command == "4" or command == "04":
            clear()
            sjt()
            break
        elif command == "5" or command == "05":
            clear()
            rrs()
            break
        elif command == "6" or command == "06":
            clear()
            mqs()
            break
        elif command.lower() == "q":
            break
        else:
            print("Invalid command.")
            print("Retrying..")
            time.sleep(2)
            clear()


if __name__ == "__main__":
    while True:
        command = input("Pogi ba si FAFA Paul? [Y/n]: ")
        if command.lower() == "y":
            clear()
            main()
            break
        print("Be Honest! Kasi!.")
    
