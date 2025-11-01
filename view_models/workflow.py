# Coding: UTF-8

# Copyright (C) 2025 Michał Prędki
# Licensed under the GNU General Public License v3.0.
# Full text of the license can be found in the LICENSE file in the repository.

from dataclasses import dataclass, field
from typing import Callable, List, Optional

from ..models.results.result import Result, ResultStatus


@dataclass
class Workflow:
    """
    Workflow represents a step or a collection of steps in a sequence of actions to be performed,
    typically involving model operations and emitting corresponding signals. Each Workflow instance
    contains a function to execute (model_func), a signal emitter (signal_emitor) to notify about
    the result, and can optionally be skipped or have a preparation function executed before the main
    action. Workflows can be chained using add_step to form a tree of operations executed in order,
    with each step running only if the previous did not result in an error.
    """

    model_func: Callable[[], Result]
    signal_emitor: Callable[[Result], None]
    skip: bool = False
    prepare_func: Optional[Callable[[], None]] = None

    steps: List["Workflow"] = field(default_factory=list, init=False)

    def add_step(self, step: "Workflow") -> "Workflow":
        """Add a workflow step to the sequence."""
        self.steps.append(step)
        return self

    def run(self) -> bool:
        """Run this workflow step and all chained steps."""
        if not self._run_self(self):
            return False

        if not self.steps:
            return True

        for step in self.steps:
            if not step.run():
                return False
        return True

    @staticmethod
    def _run_self(step: "Workflow") -> bool:
        """Run a single workflow step, handling preparation and skipping."""
        if step.skip:
            return True

        if step.prepare_func:
            step.prepare_func()

        result = step.model_func()
        step.signal_emitor(result)
        return result.status != ResultStatus.ERROR
