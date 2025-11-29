# Coding: UTF-8

# Copyright (C) 2025 Michał Prędki
# Licensed under the GNU General Public License v3.0.
# Full text of the license can be found in the LICENSE file in the repository.

from typing import Callable, List, Optional

from qgis.core import QgsTask

from .task_step import TaskStep
from ...models.results.result import Result, ResultStatus


class QNetBackgroundTask(QgsTask):
    """
    Background task executor for running QNET model operations.

    QNetBackgroundTask provides an orchestration layer for multi-step model operations.
    It inherits from `QgsTask` and executes all steps off the QGIS UI thread, keeping 
    the interface responsive.

    The task sequentially executes all steps, tracks intermediate `Result` objects,
    handles cancellation, and stops execution on the first error. All collected
    results remain available for inspection after task completion.
    """
    
    def __init__(self, description: str = ""):
        """
        Initialize the QNetBackgroundTask object.

        Parameters
        ----------
        - description : str, optional
            Task's description.
        """
        super().__init__(description)
        
        self._steps: List[TaskStep] = []
        self._results: List[Result] = []
        
    def steps(self) -> List[TaskStep]:
        """Returns task's steps."""
        return self._steps
        
    def results(self) -> List[Result]:
        """Returns task's result objects."""
        return self._results
        
    def add_step(
        self,
        model_func: Callable[[], Result],
        skip: bool = False,
        prepare_func: Optional[Callable[[], None]] = None,
        emit_signal: bool = True,
    ) -> "QNetBackgroundTask":
        """Add step to the task's steps."""
        step = TaskStep(
            model_func=model_func,
            skip=skip,
            prepare_func=prepare_func,
            emit_signal=emit_signal,
        )
        self._steps.append(step)

        return self

    def run(self) -> bool:
        """Performs the task's operation when started by the QGIS task manager."""
        for step in self.steps():

            if self.isCanceled():
                return False

            if step.skip:
                continue

            if callable(step.prepare_func):
                step.prepare_func()

            result = step.model_func()

            if result.status != ResultStatus.SUCCESS or step.emit_signal:
                self._results.append(result)
                
            if result.status == ResultStatus.ERROR:
                return False

        return True
