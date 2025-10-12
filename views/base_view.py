# Coding: UTF-8

# Copyright (C) 2025 Michał Prędki
# Licensed under the GNU General Public License v3.0.
# Full text of the license can be found in the LICENSE file in the repository.


class BaseView:
    """This class provides a template for binding widgets and view model signals."""

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
