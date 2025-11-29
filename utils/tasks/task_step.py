# Coding: UTF-8

# Copyright (C) 2025 Michał Prędki
# Licensed under the GNU General Public License v3.0.
# Full text of the license can be found in the LICENSE file in the repository.

from typing import Callable, Optional
from dataclasses import dataclass

from ...models.results.result import Result


@dataclass
class TaskStep:
    """
    Represents a single step to be executed by a QNetBackgroundTask.

    A TaskStep holds a reference to a model function that will be executed as part of 
    the task. Optionally, it can also reference a preparation function that runs just
    before the model function. Additionaly, defines flags indicate whether to skip 
    execution of this step and whether to emit a signal upon successful completion.

    Attributes
    ----------
    - model_func : Callable[[], Result]
        The model function that will be executed in this step.
    - skip : bool, optional
        If True, this step is skipped during task execution. Defaults to False.
    - prepare_func : Callable[[], None], optional
        An optional function to run before model_func to set up any preconditions.
    - emit_signal : bool, optional
        If True, the result signal for this step will be emitted on success. Errors and
        warnings will always emit signals regardless of this value. Defaults to True.
    """
    
    model_func: Callable[[], Result]
    skip: bool = False
    prepare_func: Optional[Callable[[], None]] = None
    emit_signal: bool = True
