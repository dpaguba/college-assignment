"""CPU scheduling, up to virtual round robin.

A scheduler decides which ready process runs next, and the algorithms differ in
what they optimise. First come first served minimises nothing and is fair in
the weakest sense. Shortest job first minimises average waiting time provably
and needs to know the future. Round robin bounds the response time and hurts
throughput.

**Virtual round robin** is the interesting one, because it fixes a specific
unfairness. A process that blocks for input and output uses only part of its
quantum, then goes to the back of the ready queue like everyone else, so it
gets less CPU than a compute-bound process even though it asked for less. VRR
adds an **auxiliary queue** with priority, holding processes that return from
I/O, and lets them run for the **remainder** of the quantum they gave up.
"""

from __future__ import annotations


class Process:
    """A process with a repeating CPU burst and I/O burst."""

    def __init__(self, name, cpu_burst, io_burst=0, arrival=0):
        """Record the burst lengths and the arrival time."""
        self.name = name
        self.cpu_burst = cpu_burst
        self.io_burst = io_burst
        self.arrival = arrival

    def __repr__(self):
        """The process and its two burst lengths."""
        return f"{self.name}(cpu={self.cpu_burst}, io={self.io_burst})"


def first_come_first_served(processes):
    """Run each process to completion in arrival order."""
    time = 0
    timeline = []
    waiting = []
    turnaround = []

    for process in sorted(processes, key=lambda entry: entry.arrival):
        start = max(time, process.arrival)
        timeline.append({"process": process.name, "start": start,
                         "end": start + process.cpu_burst,
                         "length": process.cpu_burst})
        waiting.append(start - process.arrival)
        turnaround.append(start + process.cpu_burst - process.arrival)
        time = start + process.cpu_burst

    return _summary(timeline, waiting, turnaround)


def shortest_job_first(processes):
    """Run the shortest available job next.

    Provably optimal for average waiting time, and unusable as stated, because
    it needs the burst length before the burst. Real schedulers estimate it
    from the previous bursts, which works because process behaviour is
    predictable over short intervals.
    """
    remaining = sorted(processes, key=lambda entry: (entry.arrival, entry.cpu_burst))
    time = 0
    timeline = []
    waiting = []
    turnaround = []
    pending = list(remaining)

    while pending:
        available = [entry for entry in pending if entry.arrival <= time] or pending[:1]
        process = min(available, key=lambda entry: entry.cpu_burst)
        pending.remove(process)

        start = max(time, process.arrival)
        timeline.append({"process": process.name, "start": start,
                         "end": start + process.cpu_burst,
                         "length": process.cpu_burst})
        waiting.append(start - process.arrival)
        turnaround.append(start + process.cpu_burst - process.arrival)
        time = start + process.cpu_burst

    return _summary(timeline, waiting, turnaround)


def round_robin(processes, quantum):
    """Give each process a fixed slice in turn, with no I/O.

    Bounds the time until a process runs, which is what an interactive system
    needs, at the cost of a context switch per slice. The quantum is the whole
    design: too small and the switching dominates, too large and it degenerates
    into first come first served.
    """
    queue = [(process.name, process.cpu_burst) for process in processes]
    time = 0
    timeline = []
    finished = {}

    while queue:
        name, left = queue.pop(0)
        slice_length = min(quantum, left)
        timeline.append({"process": name, "start": time,
                         "end": time + slice_length, "length": slice_length})
        time += slice_length
        left -= slice_length

        if left:
            queue.append((name, left))
        else:
            finished[name] = time

    waiting = [finished[process.name] - process.cpu_burst for process in processes]
    turnaround = [finished[process.name] for process in processes]
    return _summary(timeline, waiting, turnaround)


def round_robin_with_io(processes, quantum, horizon):
    """Round robin where processes alternate CPU and I/O bursts.

    The unfairness VRR fixes is visible here: a process whose CPU burst is
    shorter than the quantum gives up the rest of it and rejoins at the back,
    so it is scheduled as often as a process that used the whole slice and gets
    proportionally less CPU.
    """
    return _simulate(processes, quantum, horizon, virtual=False)


def virtual_round_robin(processes, quantum, horizon):
    """Round robin with an auxiliary queue for processes returning from I/O.

    The auxiliary queue has **priority** over the main ready queue, and a
    process dispatched from it runs only for the remainder of the quantum it
    gave up when it blocked. Both halves matter: the priority is what
    compensates the I/O-bound process, and the remainder is what stops it from
    getting more than its share.
    """
    return _simulate(processes, quantum, horizon, virtual=True)


def _simulate(processes, quantum, horizon, virtual):
    """The shared simulation of round robin with I/O, with or without the queue."""
    ready = [entry.name for entry in processes]
    auxiliary = []
    blocked = []
    remainder = {entry.name: quantum for entry in processes}
    burst = {entry.name: entry.cpu_burst for entry in processes}
    definition = {entry.name: entry for entry in processes}
    left = {entry.name: entry.cpu_burst for entry in processes}

    time = 0
    timeline = []
    decisions = []
    cpu_time = {entry.name: 0 for entry in processes}
    auxiliary_dispatches = 0

    while time < horizon:
        for entry in list(blocked):
            if entry["until"] <= time:
                blocked.remove(entry)
                if virtual and entry["remainder"] > 0:
                    auxiliary.append(entry["name"])
                else:
                    ready.append(entry["name"])
                remainder[entry["name"]] = entry["remainder"] if virtual else quantum
                left[entry["name"]] = burst[entry["name"]]

        if not ready and not auxiliary:
            time += 1
            continue

        if virtual and auxiliary:
            name = auxiliary.pop(0)
            source = "auxiliary"
            allowance = remainder[name]
            auxiliary_dispatches += 1
        else:
            name = ready.pop(0)
            source = "ready"
            allowance = quantum

        decisions.append({"time": time, "process": name, "source": source,
                          "auxiliary_waiting": bool(auxiliary) or source == "auxiliary"})

        run = min(allowance, left[name], horizon - time)
        if run <= 0:
            continue

        timeline.append({"process": name, "start": time, "end": time + run,
                         "length": run, "source": source})
        cpu_time[name] += run
        time += run
        left[name] -= run

        if left[name] == 0:
            io = definition[name].io_burst
            blocked.append({"name": name, "until": time + io,
                            "remainder": allowance - run})
        else:
            remainder[name] = quantum
            ready.append(name)

    return {"timeline": timeline, "decisions": decisions, "cpu_time": cpu_time,
            "auxiliary_dispatches": auxiliary_dispatches}


def _summary(timeline, waiting, turnaround):
    """Average waiting and turnaround times alongside the timeline."""
    return {
        "timeline": timeline,
        "average_waiting": sum(waiting) / len(waiting) if waiting else 0.0,
        "average_turnaround": sum(turnaround) / len(turnaround) if turnaround else 0.0,
    }


def response_time_bound(processes, quantum):
    """Worst time until a newly ready process runs, under round robin.

    Every other process runs at most one quantum first, so the bound is the
    number of processes times the quantum. That guarantee is what round robin
    is bought for, and it is why the quantum is chosen from the response time
    requirement rather than from throughput.
    """
    return (len(processes) - 1) * quantum
