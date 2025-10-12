# Coding: UTF-8

# Copyright (C) 2025 Michał Prędki
# Licensed under the GNU General Public License v3.0.
# Full text of the license can be found in the LICENSE file in the repository.

from .base import BaseCommand


class ExportReportCommand(BaseCommand):
    def execute(self, report_params):
        if not self.can_execute():
            return

        print(report_params)

    def can_execute(self) -> bool:
        return True
