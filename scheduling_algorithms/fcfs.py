from typing import List, Dict, Tuple

def fcfs(processes: List[Dict], show_steps: bool = True) -> Dict:
    """
    FCFS scheduler with detailed stats + formulas.
    Each process: {"pid": "P1", "AT": 0, "BT": 3}
    """
    # --- validation ---
    for p in processes:
        if p["AT"] < 0 or p["BT"] <= 0:
            raise ValueError(f"Invalid times for {p['pid']}: AT>=0 and BT>0 required")

    # stable sort by arrival time
    indexed = [(i, p["pid"], p["AT"], p["BT"]) for i, p in enumerate(processes)]
    indexed.sort(key=lambda x: (x[2], x[0]))

    # --- simulation ---
    time = 0
    timeline: List[Tuple[str, int, int]] = []
    rows = []

    if show_steps:
        print("== FCFS – Step by Step ==")

    for _, pid, at, bt in indexed:
        if time < at:
            if show_steps:
                print(f"Time {time}–{at}: CPU IDLE")
            timeline.append(("IDLE", time, at))
            time = at

        st = time                        # start time
        ct = st + bt                     # completion time (finish time)
        wt = st - at                     # waiting time
        tat = ct - at                    # turnaround time
        rt = st - at                     # response time (same as WT in FCFS)

        if show_steps:
            print(f"\n{pid}:")
            print(f"  ST  = max(previous CT, AT) = max({time}, {at}) = {st}")
            print(f"  CT  = ST + BT = {st} + {bt} = {ct}")
            print(f"  WT  = ST - AT = {st} - {at} = {wt}")
            print(f"  TAT = CT - AT = {ct} - {at} = {tat}")
            print(f"  RT  = ST - AT = {st} - {at} = {rt}")

        rows.append({
            "PID": pid, "AT": at, "BT": bt,
            "ST": st, "CT": ct, "WT": wt, "TAT": tat, "RT": rt
        })
        timeline.append((pid, st, ct))
        time = ct

    # --- aggregates ---
    n = len(rows)
    tbt = sum(r["BT"] for r in rows)                    # total burst time (busy time)
    tft = timeline[-1][2] if timeline else 0            # finish time (makespan = last CT)
    busy_time = sum(e - s for (lab, s, e) in timeline if lab != "IDLE")
    cpu_util = (busy_time / tft * 100) if tft > 0 else 0
    throughput = (n / tft) if tft > 0 else 0

    avg_wt = sum(r["WT"] for r in rows) / n
    avg_tat = sum(r["TAT"] for r in rows) / n

    # --- queue order ---
    order = [pid for (_, pid, _, _) in indexed]
    print("\n== Ready Queue Order by Arrival ==")
    print(" → ".join(order))

    # --- Gantt chart ---
    print("\n== Gantt Chart ==")
    def seg_w(a, b): return max(1, int(round(b - a)))
    top = mid = bot = ""
    for label, s, e in timeline:
        w = seg_w(s, e)
        top += "+" + "-" * w
        mid += "|" + label.center(w)
        bot += "+" + "-" * w
    top += "+\n"; mid += "|\n"; bot += "+"
    times_line = []
    for i, (_, s, e) in enumerate(timeline):
        if i == 0: times_line.append(str(s))
        times_line.append(str(e))
    print(top + mid + bot)
    print(" ".join(t for t in times_line) + " -> Total Finish Time (TFT)")

    print("""
Arrival Time (AT)            Burst Time (BT)
Completion Time (CT)         Waiting Time (WT)            
Turnaround Time (TAT)        Response Time (RT)         
Total Finish Time (TFT)      Total Burst Time (TBT)    
N = Number of Processes
    """)

    # --- table ---
    print("\n== Results ==")
    header = f"{'PID':<5}{'AT':>5}{'BT':>5}{'CT':>6}{'RT':>6}{'TAT':>7}{'WT':>6}"
    print(header); print("-" * len(header))
    for r in rows:
        print(f"{r['PID']:<5}{r['AT']:>5}{r['BT']:>5}{r['CT']:>6}{r['RT']:>6}{r['TAT']:>7}{r['WT']:>6}")
    print("-" * len(header))

    # --- formulas + answers ---
    print("\n== Formulas & Final Results ==")
    print(f"AWT  = ΣWT / N  = {sum(r['WT'] for r in rows)} / {n} = {avg_wt:.2f}")
    print(f"ATAT = ΣTAT / N = {sum(r['TAT'] for r in rows)} / {n} = {avg_tat:.2f}")
    print(f"TBT  = ΣBT      = {tbt}")
    print(f"TFT  = last CT  = {tft}")
    print(f"CPU Utilization = Busy / TFT * 100 = {busy_time}/{tft} * 100 = {cpu_util:.2f}%")
    print(f"Throughput = N / TFT = {n}/{tft} = {throughput:.4f}")

    print("\n===========================================================")
    print("           Programmed By : Paul Mendoza")
    print("===========================================================\n")

    return {
        "table": rows,
        "avg_wt": avg_wt,
        "avg_tat": avg_tat,
        "timeline": timeline,
        "TBT": tbt,
        "TFT": tft,
        "cpu_utilization_pct": cpu_util,
        "throughput": throughput,
        "order": order,
    }


if __name__ == "__main__":
    # ----- interactive input -----
    print("""
===========================================================
   First Come, First Serve (FCFS) Scheduling Algorithm
   With Step-by-Step Computation, Gantt Chart & Metrics
   Code By : Paul Mendoza
===========================================================
""")
    n = int(input("Enter number of processes: "))
    processes = []
    for i in range(n):
        at = int(input(f"Enter Arrival Time (AT) for P{i+1}: "))
        bt = int(input(f"Enter Burst Time (BT) for P{i+1}: "))
        processes.append({"pid": f"P{i+1}", "AT": at, "BT": bt})
    fcfs(processes)
