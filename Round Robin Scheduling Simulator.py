import matplotlib.pyplot as plt
from tabulate import tabulate

processes = [("P1", 10, 0), ("P2", 5, 1), ("P3", 8, 2)]
time_quantum = 3

def round_robin_scheduling(processes, time_quantum):
    n = len(processes)
    burst_times = {proc[0]: proc[1] for proc in processes}
    arrival_times = {proc[0]: proc[2] for proc in processes}

    remaining_burst_times = burst_times.copy()

    time = 0
    gantt_chart = []
    waiting_times = {proc[0]: 0 for proc in processes}
    turnaround_times = {proc[0]: 0 for proc in processes}
    completion_times = {proc[0]: 0 for proc in processes}
    ready_queue = []
    completed = 0

    while completed < n:
        for proc in processes:
            if proc[0] not in ready_queue and proc[2] <= time and remaining_burst_times[proc[0]] > 0:
                ready_queue.append(proc[0])

        if not ready_queue:
            time += 1
            continue

        current_proc = ready_queue.pop(0)
        gantt_chart.append((current_proc, time))

        execution_time = min(time_quantum, remaining_burst_times[current_proc])
        remaining_burst_times[current_proc] -= execution_time
        time += execution_time

        for proc in processes:
            if proc[0] in ready_queue:
                waiting_times[proc[0]] += execution_time

        if remaining_burst_times[current_proc] > 0:
            ready_queue.append(current_proc)
        else:
            completed += 1
            completion_times[current_proc] = time
            turnaround_times[current_proc] = time - arrival_times[current_proc]

    return gantt_chart, waiting_times, turnaround_times, completion_times

gantt_chart, waiting_times, turnaround_times, completion_times = round_robin_scheduling(processes, time_quantum)

avg_tat = sum(turnaround_times.values()) / len(processes)
avg_wt = sum(waiting_times.values()) / len(processes)

table = []
for proc in processes:
    proc_id = proc[0]
    arrival_time = proc[2]
    burst_time = proc[1]
    completion_time = completion_times[proc_id]
    turnaround_time = turnaround_times[proc_id]
    waiting_time = waiting_times[proc_id]
    table.append([proc_id, arrival_time, burst_time, completion_time, turnaround_time, waiting_time])

headers = ["Process", "Arrival Time", "Burst Time", "Completion Time", "Turnaround Time", "Waiting Time"]
print(tabulate(table, headers=headers, tablefmt="pretty"))

print(f"\nAverage Turnaround Time: {avg_tat:.2f} ms")
print(f"Average Waiting Time: {avg_wt:.2f} ms")

# Print the Gantt Chart (for reference)
print("\nGantt Chart:", gantt_chart)

def plot_gantt_chart(gantt_chart, time_quantum):
    fig, gnt = plt.subplots()
    gnt.set_ylim(0, 5)
    max_time = max(t[1] for t in gantt_chart) + 3
    gnt.set_xlim(0, max_time)
    gnt.set_xlabel('Time (ms)', fontsize=15,labelpad=10)
    gnt.set_ylabel('Processes', fontsize=15)

    x_ticks = range(0, max_time + 1, 1)
    gnt.set_xticks(x_ticks)

    yticks = [5]
    ylabels = ['']
    gnt.set_yticks(yticks)
    gnt.set_yticklabels(ylabels)

    # Colors for each process
    colors = {"P1": "lightblue", "P2": "lightgreen", "P3": "lightcoral"}

    gnt.grid(True, axis='x', linestyle='--', alpha=0.5, zorder=0)

    for i, (proc, start_time) in enumerate(gantt_chart):
        if i < len(gantt_chart) - 1:
            end_time = gantt_chart[i + 1][1]
        else:
            end_time = start_time + time_quantum
        duration = end_time - start_time

        gnt.broken_barh([(start_time, duration)], (2, 1), facecolors=colors[proc], edgecolor='black')

        gnt.text(start_time + duration / 2, 2.5, proc, ha='center', va='center', color='black', fontsize=10, zorder=2)

    plt.title('Round Robin Scheduling Gantt Chart', fontsize=18, fontweight='bold')
    plt.show()

plot_gantt_chart(gantt_chart, time_quantum)