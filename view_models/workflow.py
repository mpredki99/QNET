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
    Represents an executable step or a chain of dependent actions in the QNET plugin.

    Each Workflow encapsulates a model function to execute, an associated signal
    emitter to handle the result, and optional logic to prepare or skip the step.
    Workflows can be chained to form sequential execution flows, with each step
    proceeding only if the previous one completes without error.

    Attributes
    ----------
    - model_func : Callable[[], Result]
        The function performing the main operation for this workflow step.
    - signal_emitor : Callable[[Result], None]
        The callback responsible for emitting signals based on the result status.
    - skip : bool, optional
        If True, the step is skipped during execution. Defaults to False.
    - prepare_func : Callable[[], None], optional
        Function executed before model_func to prepare any required context.
    - steps : List[Workflow]
        List of subsequent workflow steps to be executed sequentially.
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
        if not Workflow._run_self(self):
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
