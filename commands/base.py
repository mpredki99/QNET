# Coding: UTF-8

# Copyright (C) 2025 Michał Prędki
# Licensed under the GNU General Public License v3.0.
# Full text of the license can be found in the LICENSE file in the repository.

from abc import ABC, abstractmethod


class BaseCommand(ABC):
    """
    Abstract base class for all command classes in the QNET plugin.
    Provides the interface for executing commands and checking if they can be executed.
    """

    @abstractmethod
    def execute(self, *args, **kwargs):
        """Execute the command with the given arguments."""
        pass

    @abstractmethod
    def can_execute(self) -> bool:
        """Determine whether the command can be executed."""
        pass
