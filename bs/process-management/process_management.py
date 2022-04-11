"""Processes: fork, exec, wait, and what happens when they are misused.

`fork` returns twice, which is the single strangest thing in the UNIX
interface and the source of every question about it. In the parent it returns
the child's process id; in the child it returns zero. Both then continue from
the same line with the same memory contents, and the return value is the only
way either of them can tell which it is.

`exec` replaces the image and keeps everything else: the process id, the open
files, the working directory. That separation, one call to create a process and
another to give it a program, is what makes shell redirection possible: the
child changes its own file descriptors between the two.

`wait` is the third piece, and its purpose is bookkeeping. A terminated process
keeps its exit status until someone reads it, and until then it is a **zombie**
holding a slot in the process table.
"""

from __future__ import annotations

INIT = 1
"""The process every orphan is adopted by."""


def fork_result(parent_pid, child_pid):
    """What `fork` returns in each of the two processes.

    Zero in the child and the child's id in the parent, which is asymmetric on
    purpose: the child can always find its parent with `getppid`, and the
    parent has no other way to learn the child's id.
    """
    return {"parent": child_pid, "child": 0}


def fork_bomb_generations(generations):
    """How many processes exist after each generation of `for (;;) fork();`.

    Every process in a generation forks, so the count doubles. Ten generations
    reach 1024 and twenty reach a million, which is why the loop takes seconds
    to make a machine unusable and why process limits exist.
    """
    return [2 ** generation for generation in range(generations + 1)]


class Tree:
    """A process tree, tracking parents, states and reaping."""

    def __init__(self):
        """Start with only the init process."""
        self.next_pid = 2
        self.parents = {INIT: None}
        self.states = {INIT: "running"}

    def spawn(self, parent):
        """Create a child of a process, or of init when none is given."""
        pid = self.next_pid
        self.next_pid += 1
        self.parents[pid] = parent if parent is not None else INIT
        self.states[pid] = "running"
        return pid

    def exit(self, pid):
        """Terminate a process, reparenting its children and reaping if orphaned.

        A terminated process becomes a zombie until its parent waits for it.
        If its parent is init, the reaping is automatic, because init waits in
        a loop and does nothing else. That is the whole reason init exists as
        process 1.
        """
        for child, parent in self.parents.items():
            if parent == pid and self.states[child] != "reaped":
                self.parents[child] = INIT
                if self.states[child] == "zombie":
                    self.states[child] = "reaped"

        self.states[pid] = "zombie"
        if self.parents[pid] == INIT:
            self.states[pid] = "reaped"

    def wait(self, pid):
        """Reap one terminated child, returning its id, or `None`."""
        for child, parent in self.parents.items():
            if parent == pid and self.states.get(child) == "zombie":
                self.states[child] = "reaped"
                return child
        return None

    def state(self, pid):
        """The state of a process."""
        return self.states[pid]

    def parent(self, pid):
        """The current parent of a process, which changes when it is orphaned."""
        return self.parents[pid]

    def zombies(self):
        """Every process waiting to be reaped.

        A long-running program that forks without waiting accumulates these and
        eventually cannot create processes at all, having filled the table with
        entries holding nothing but exit statuses.
        """
        return [pid for pid, state in self.states.items() if state == "zombie"]


def exec_image(state, image):
    """Replace a process's program while keeping its identity.

    The process id, the open file descriptors and the working directory
    survive. That is what makes `fork`, adjust the descriptors, `exec` the
    standard way to run a program with its output redirected, and it is why
    redirection is a property of the shell rather than of the program.
    """
    return {**state, "image": image}


def shell_effect(command):
    """What a shell does with a redirection or a pipe.

    `ls -l > sort` runs **one** program and sends its output to a **file**
    named `sort`, overwriting it. `ls -l | sort` runs **two** programs and
    connects the first's output to the second's input.

    They look alike and share almost nothing: the first creates a file called
    sort, the second runs the sorting program. The exercise asks for exactly
    this distinction, and the trap is that the file in the first case is named
    after the program in the second.
    """
    if ">" in command:
        left, _, target = command.partition(">")
        return {"kind": "redirect", "target": target.strip(),
                "runs": [left.strip()]}

    if "|" in command:
        parts = [part.strip() for part in command.split("|")]
        return {"kind": "pipe", "target": None, "runs": parts}

    return {"kind": "simple", "target": None, "runs": [command.strip()]}


def fork_versus_vfork():
    """The difference between the two calls, and what is left of it.

    `vfork` was an optimisation for the case where the child immediately calls
    `exec`: it borrows the parent's address space and suspends the parent until
    the child execs or exits. Copying the page tables was expensive, and
    skipping it mattered.

    Copy-on-write made `fork` almost as cheap, since the pages are shared until
    one side writes and the child usually writes nothing before `exec`. What is
    left of `vfork` today is a marginal saving and a large footgun: the child
    shares the parent's stack, so returning from the function that called it
    corrupts the parent.
    """
    return {
        "fork": "copies the address space, lazily through copy-on-write",
        "vfork": "borrows it and suspends the parent until exec or _exit",
        "still different": "marginally, and only before an immediate exec",
    }
