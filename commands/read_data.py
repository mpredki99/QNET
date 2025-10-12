# Coding: UTF-8

# Copyright (C) 2025 Michał Prędki
# Licensed under the GNU General Public License v3.0.
# Full text of the license can be found in the LICENSE file in the repository.

from os import path

from .base import BaseCommand


class ReadDataCommand(BaseCommand):
    def execute(self, input_files_params):
        if not self.can_execute(input_files_params):
            return
        print(input_files_params)
        return input_files_params

    def can_execute(self, input_files_params) -> bool:
        if not path.isfile(input_files_params.measurements_file_path):
            return True  # False
        if not path.isfile(input_files_params.controls_file_path):
            return True  # False
        return True
