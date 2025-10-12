# Coding: UTF-8

# Copyright (C) 2025 Michał Prędki
# Licensed under the GNU General Public License v3.0.
# Full text of the license can be found in the LICENSE file in the repository.

from qgis.PyQt.QtCore import QObject, pyqtSignal

from .input_files_view_model import InputFilesViewModel
from .output_view_model import OutputViewModel
from .report_view_model import ReportViewModel
from .weighting_methods_view_model import WeightingMethodsViewModel


class MainViewModel(QObject):
    """
    Main view model for the QNET plugin.

    Coordinates and manages the interaction between all view models corresponding to UI sections,
    such as input files, weighting methods, report options, and output options. Acts as the
    central point for invoking processes like adjustment calculation and output/export tasks,
    and provides the data and logic backbone for the main dialog.
    """

    def __init__(
        self,
        model,
        input_files_view_model=InputFilesViewModel(),
        weighting_methods_view_model=WeightingMethodsViewModel(),
        report_view_model=ReportViewModel(),
        output_view_model=OutputViewModel(),
    ) -> None:
        super().__init__()

        self.model = model
        self.input_files_view_model = input_files_view_model
        self.weighting_methods_view_model = weighting_methods_view_model
        self.report_view_model = report_view_model
        self.output_view_model = output_view_model

    def perform_adjustment(self) -> None:
        """Perform the network adjustment and export results."""
        self.input_files_view_model.import_dataset()
        self.weighting_methods_view_model.perform_adjustment()
        self.report_view_model.export_report()
        self.output_view_model.export_output_file()
