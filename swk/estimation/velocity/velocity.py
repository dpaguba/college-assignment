"""Velocity: how much a team finishes per sprint, and what it forecasts.

Story points measure the size of a story, not the hours it takes. Velocity is
story points completed per sprint, and its whole value is that it converts
sizes into dates **empirically**, without anyone having to estimate hours.

The lecture's rule of thumb: velocity settles after about three sprints, and
from then on the planning number should be the **median** of the observed
values, not the mean, because a median is not dragged around by one bad sprint.
"""

from __future__ import annotations

import statistics
from dataclasses import dataclass, field


@dataclass(frozen=True)
class Story:
    """A user story with its estimated size in story points."""

    name: str
    points: int


@dataclass
class Board:
    """The stories, and what happened to each of them per sprint.

    ``planned`` and ``actual`` map ``(story, sprint)`` to hours. A story
    counts as finished in the last sprint where it recorded actual work.
    """

    stories: tuple
    planned: dict = field(default_factory=dict)
    actual: dict = field(default_factory=dict)

    @property
    def sprints(self):
        """Every sprint number that appears on the board."""
        numbers = {sprint for _, sprint in self.planned} | {sprint for _, sprint in self.actual}
        return sorted(numbers)

    def points_of(self, story):
        """The story points of a story by name."""
        return next(item.points for item in self.stories if item.name == story)

    def completed_in(self, sprint):
        """Stories whose last recorded work is in this sprint."""
        finished = []
        for story in self.stories:
            worked = [number for (name, number) in self.actual if name == story.name]
            if worked and max(worked) == sprint:
                finished.append(story.name)
        return sorted(finished)

    def planned_in(self, sprint):
        """Stories that had work planned in this sprint."""
        return sorted(name for (name, number) in self.planned if number == sprint)

    def planned_velocity(self, sprint):
        """Story points the team took into a sprint."""
        return sum(self.points_of(name) for name in self.planned_in(sprint))

    def actual_velocity(self, sprint):
        """Story points the team finished in a sprint.

        Points count only when the story is done. A story half finished at the
        end of a sprint contributes nothing, which is deliberate: partial
        credit would make velocity smooth and useless as a signal.
        """
        return sum(self.points_of(name) for name in self.completed_in(sprint))

    def hours(self, sprint):
        """Planned and actual hours in a sprint, which velocity deliberately ignores."""
        planned = sum(value for (_, number), value in self.planned.items() if number == sprint)
        actual = sum(value for (_, number), value in self.actual.items() if number == sprint)
        return planned, actual

    def table(self):
        """Planned and actual velocity per sprint, with the hours alongside."""
        rows = []
        for sprint in self.sprints:
            planned_hours, actual_hours = self.hours(sprint)
            rows.append({
                "sprint": sprint,
                "planned points": self.planned_velocity(sprint),
                "actual points": self.actual_velocity(sprint),
                "planned hours": planned_hours,
                "actual hours": actual_hours,
                "completed": self.completed_in(sprint),
            })
        return rows

    def burndown(self):
        """Story points remaining after each sprint.

        The chart the exercise asks to be drawn: total scope on the left,
        falling by the actual velocity of each sprint. A flat stretch means a
        sprint that finished nothing, which is what the chart is for.
        """
        remaining = sum(story.points for story in self.stories)
        points = [(0, remaining)]

        for sprint in self.sprints:
            remaining -= self.actual_velocity(sprint)
            points.append((sprint, remaining))

        return points

    def chart(self, width=40):
        """The burndown as text, one row per sprint."""
        points = self.burndown()
        top = max(value for _, value in points) or 1
        rows = []

        for sprint, remaining in points:
            filled = round(width * remaining / top)
            label = "start" if sprint == 0 else f"after {sprint}"
            rows.append(f"  {label:>8} |{'#' * filled}{' ' * (width - filled)}| {remaining}")

        return "\n".join(rows)


def median_velocity(values, window=3):
    """The planning number: the median of the recent sprints.

    The lecture prefers the median to the mean because it is robust: one
    sprint where half the team was ill moves the mean and barely moves the
    median. The window keeps the number responsive to a team that is actually
    speeding up or slowing down.
    """
    if not values:
        return 0
    recent = values[-window:] if len(values) >= window else values
    return statistics.median(recent)


def forecast(board, remaining_points=None, window=3):
    """How many more sprints the remaining scope needs, at the current velocity.

    Returns the number of sprints and the velocity used. The estimate is only
    as good as the assumption that the future looks like the recent past, and
    it says so by reporting the velocity it assumed.
    """
    observed = [board.actual_velocity(sprint) for sprint in board.sprints]
    speed = median_velocity(observed, window)

    if remaining_points is None:
        remaining_points = board.burndown()[-1][1]

    if speed <= 0:
        return None, speed

    import math
    return math.ceil(remaining_points / speed), speed


def problems(board):
    """Signals that the velocity is not trustworthy yet.

    Three checks the lecture's discussion implies: too few sprints to have
    settled, a scattered history, and a systematic gap between what was taken
    in and what came out.
    """
    observed = [board.actual_velocity(sprint) for sprint in board.sprints]
    planned = [board.planned_velocity(sprint) for sprint in board.sprints]
    found = []

    if len(observed) < 3:
        found.append("fewer than three sprints, the velocity has not settled")

    if len(observed) >= 2 and max(observed) > 2 * max(1, min(observed)):
        found.append(f"velocity ranges from {min(observed)} to {max(observed)}, "
                     "so a median hides more than it says")

    committed = sum(planned)
    delivered = sum(observed)
    if committed and delivered < 0.7 * committed:
        found.append(f"only {delivered} of {committed} committed points were finished, "
                     "the team is consistently over-committing")

    return found


EXERCISE_BOARD = Board(
    stories=(Story("U1", 4), Story("U2", 5), Story("U3", 4), Story("U4", 2),
             Story("U5", 5), Story("U6", 5), Story("U7", 2), Story("U8", 5),
             Story("U9", 5), Story("U10", 4)),
    planned={("U1", 1): 80, ("U2", 1): 120, ("U3", 1): 90, ("U4", 1): 40,
             ("U1", 2): 50, ("U5", 2): 120, ("U6", 2): 120, ("U7", 2): 45,
             ("U6", 3): 70, ("U8", 3): 130, ("U9", 3): 130,
             ("U9", 4): 50, ("U10", 4): 100,
             ("U10", 5): 80},
    actual={("U1", 1): 30, ("U2", 1): 150, ("U3", 1): 110, ("U4", 1): 45,
            ("U1", 2): 65, ("U5", 2): 160, ("U6", 2): 60, ("U7", 2): 60,
            ("U6", 3): 80, ("U8", 3): 160, ("U9", 3): 100,
            ("U9", 4): 100, ("U10", 4): 20,
            ("U10", 5): 100},
)
"""The ten stories and five sprints of exercise sheet 2, task 2.2."""
