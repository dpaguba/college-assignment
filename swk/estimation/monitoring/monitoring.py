"""Goal-question-metric, and the KPIs that come out of it.

The exercise asks for a goal, three questions, and a metric for each. That
order is the method: a metric chosen before the question it answers measures
whatever was easy to collect, and a team then optimises it.

GQM comes from Basili and Rombach. Its whole content is the discipline of the
arrow: goal to question to metric, never the other way round.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Metric:
    """A measurable quantity, with how it is computed from raw data."""

    name: str
    unit: str
    compute: object
    good_direction: str = "up"

    def evaluate(self, data):
        """The value of the metric for a data set."""
        return self.compute(data)

    def improved(self, before, after):
        """Whether a change moved the metric the way the goal wants."""
        first, second = self.evaluate(before), self.evaluate(after)
        return second > first if self.good_direction == "up" else second < first


@dataclass
class Question:
    """One question about the goal, with the metrics that answer it."""

    text: str
    metrics: tuple


@dataclass
class Goal:
    """A GQM tree: one goal, its questions, and their metrics."""

    purpose: str
    object_: str
    viewpoint: str
    questions: tuple = field(default_factory=tuple)

    def evaluate(self, data):
        """Every metric in the tree, evaluated against one data set."""
        results = {}
        for question in self.questions:
            for metric in question.metrics:
                results[metric.name] = metric.evaluate(data)
        return results

    def __str__(self):
        """The goal with its questions and their metrics."""
        lines = [f"Goal: {self.purpose} of {self.object_} from the view of {self.viewpoint}"]
        for index, question in enumerate(self.questions, start=1):
            lines.append(f"  Q{index}: {question.text}")
            for metric in question.metrics:
                lines.append(f"      M: {metric.name} [{metric.unit}, better {metric.good_direction}]")
        return "\n".join(lines)


def onboarding_goal():
    """The exercise's example: improving the conversion rate of app onboarding.

    Three questions, one metric each, and the metrics are deliberately of
    different kinds: a rate, a duration and a count. A tree with three
    variations of the same number answers one question three times.
    """
    completion = Metric(
        "onboarding completion rate", "share",
        lambda data: data["finished"] / data["started"] if data["started"] else 0.0)

    duration = Metric(
        "median time to finish onboarding", "seconds",
        lambda data: data["median_seconds"], good_direction="down")

    dropout = Metric(
        "steps before the largest drop-off", "step number",
        lambda data: max(data["per_step"], key=lambda step: data["per_step"][step]),
        good_direction="down")

    return Goal(
        purpose="improve",
        object_="the conversion rate of mobile app onboarding",
        viewpoint="the product team",
        questions=(
            Question("How many users who start onboarding finish it?", (completion,)),
            Question("How long does finishing take?", (duration,)),
            Question("Where exactly do users give up?", (dropout,)),
        ),
    )


@dataclass
class KPI:
    """A key indicator, with the decision it is supposed to support.

    The second field is the one that matters. An indicator nobody would act on
    differently is a number on a dashboard, not a KPI, and naming the decision
    is the cheapest way to tell the two apart.
    """

    name: str
    supports_decision: str
    compute: object
    target: float = None

    def evaluate(self, data):
        """The current value."""
        return self.compute(data)

    def on_target(self, data):
        """Whether the current value meets the target, if there is one."""
        if self.target is None:
            return None
        return self.evaluate(data) >= self.target


def product_kpis():
    """Three KPIs for steering a mobile app, each tied to a decision."""
    return (
        KPI("activation rate",
            "whether to keep investing in onboarding or move on",
            lambda data: data["activated"] / data["signups"] if data["signups"] else 0.0,
            target=0.4),
        KPI("day 30 retention",
            "whether the product delivers lasting value or only a first impression",
            lambda data: data["retained_30"] / data["cohort"] if data["cohort"] else 0.0,
            target=0.25),
        KPI("crash-free session rate",
            "whether the next sprint goes to features or to stability",
            lambda data: 1 - data["crashes"] / data["sessions"] if data["sessions"] else 1.0,
            target=0.995),
    )


def goodharts_warning(history):
    """Detect a metric being optimised while the goal behind it is not.

    Named after Goodhart's law: a measure that becomes a target stops being a
    good measure. The check is crude and the pattern is real: the indicator
    improves steadily while the outcome it stands for does not move.

    ``history`` is a list of (indicator, outcome) pairs in time order.
    """
    if len(history) < 3:
        return False

    indicators = [item[0] for item in history]
    outcomes = [item[1] for item in history]

    indicator_rising = all(later >= earlier for earlier, later in zip(indicators, indicators[1:]))
    outcome_flat = abs(outcomes[-1] - outcomes[0]) <= 0.05 * max(1e-9, abs(outcomes[0]))

    return indicator_rising and outcome_flat and indicators[-1] > indicators[0]
