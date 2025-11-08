# Coding: UTF-8

# Copyright (C) 2025 Michał Prędki
# Licensed under the GNU General Public License v3.0
# Full text of the license can be found in the LICENSE file in the repository.

from typing import Generic, Optional, TypeVar

from ..view_models.base_view_models import BaseViewModel

# Type variable used to define a generic ViewModel type
ViewModelType = TypeVar("ViewModelType", bound=BaseViewModel)


class BaseView(Generic[ViewModelType]):
    """
    Generic base class for all View components in the QNET plugin.

    This class provides a foundation for implementing ViewModel binding logic
    across all user interface components. It defines a consistent interface for
    connecting UI widgets to their corresponding ViewModels.

    Attributes
    ----------
    - _view_model : ViewModelType, optional
        Reference to the associated ViewModel instance.

    Properties
    ----------
    - view_model : Getter and setter for the ViewModel reference. When a ViewModel is
        assigned, the view automatically binds widgets and signals.
    """

    def __init__(self) -> None:
        """
        Initialize the BaseView and set the initial ViewModel reference to None.
        """
        self._view_model: Optional[ViewModelType] = None

    @property
    def view_model(self) -> Optional[ViewModelType]:
        """Get the current view model."""
        return self._view_model

    @view_model.setter
    def view_model(self, view_model: Optional[ViewModelType]) -> None:
        """Set the view model and bind widgets and signals if it's not None."""
        self._view_model = view_model
        if self._view_model is None:
            return

        self.bind_widgets()
        self.bind_view_model_signals()

    def bind_widgets(self) -> None:
        """Bind UI widgets to event handlers."""
        raise NotImplementedError(
            f"{self.__class__.__name__} must implement bind_widgets()"
        )

    def bind_view_model_signals(self) -> None:
        """Bind ViewModel signals to UI update methods."""
        raise NotImplementedError(
            f"{self.__class__.__name__} must implement bind_view_model_signals()"
        )


class BaseViewSection(BaseView[ViewModelType]):
    """
    Base class for section-level views in the QNET plugin.

    This class extends `BaseView` to automatically trigger `reset_state()` on the
    ViewModel when it is assigned.

    Properties
    ----------
    - view_model : Extends the base property setter to include automatic ViewModel state
        reset after binding.
    """

    @BaseView.view_model.setter
    def view_model(self, view_model: Optional[ViewModelType]) -> None:
        """Set the view model and reset its state after binding if it's not None."""
        BaseView.view_model.fset(self, view_model)
        if not self._view_model:
            return
        self._view_model.reset_state()
