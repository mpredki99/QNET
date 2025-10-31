# Coding: UTF-8

# Copyright (C) 2025 Michał Prędki
# Licensed under the GNU General Public License v3.0
# Full text of the license can be found in the LICENSE file in the repository.

from typing import Generic, Optional, TypeVar

from ..view_models.base_view_model import BaseViewModel

ViewModelType = TypeVar("ViewModelType", bound=BaseViewModel)


class BaseView(Generic[ViewModelType]):
    """
    Generic base class for all views in the MVVM architecture.

    Provides common functionality for view-model binding and eliminates
    code duplication across view implementations.
    """

    def __init__(self) -> None:
        self._view_model: Optional[ViewModelType] = None

    @property
    def view_model(self) -> Optional[ViewModelType]:
        """Get the current view model."""
        return self._view_model

    @view_model.setter
    def view_model(self, view_model: Optional[ViewModelType]) -> None:
        """Set the view model and bind widgets and signals if it's not None."""
        self._view_model = view_model
        if not self._view_model:
            return

        self.bind_widgets()
        self.bind_view_model_signals()

    def bind_widgets(self):
        """Bind UI widgets to their respective handlers."""
        raise NotImplementedError(
            f"{self.__class__.__name__} must implement bind_widgets()"
        )

    def bind_view_model_signals(self):
        """Bind view model signals to UI update methods."""
        raise NotImplementedError(
            f"{self.__class__.__name__} must implement bind_view_model_signals()"
        )


class BaseViewSection(BaseView[ViewModelType]):
    """
    Generic base class for all views in the MVVM architecture.

    Provides common functionality for view-model binding and eliminates
    code duplication across view implementations.
    """

    @BaseView.view_model.setter
    def view_model(self, view_model: Optional[ViewModelType]) -> None:
        """Set the view model and bind widgets and signals if it's not None."""
        BaseView.view_model.fset(self, view_model)
        if not self._view_model:
            return
        self._view_model.reset_state()
