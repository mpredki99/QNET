# Coding: UTF-8

# Copyright (C) 2025 Michał Prędki
# Licensed under the GNU General Public License v3.0.
# Full text of the license can be found in the LICENSE file in the repository.

from ..dto.data_transfer_objects import (
    AdjustmentParams,
    OutputParams,
    ReaderParams,
    ReportParams,
)


class MainViewModel:
    def __init__(self, model) -> None:
        self.model = model
        
    def perform_adjustment(
        self,
        reader_params: ReaderParams,
        adjustment_params: AdjustmentParams,
        report_params: ReportParams,
        output_params: OutputParams,
    ):
        print("----- PERFORM_ADJUSTMENT -----\n")
        print(reader_params)
        print(adjustment_params)
        print(report_params)
        print(output_params, '\n')
