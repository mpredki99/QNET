from qgis.PyQt.QtWidgets import QFileDialog

from .window_ui import WindowDialogUI


class WindowDialog(WindowDialogUI):
    def set_input_file(self, input_file_line_edit, input_file_label_text):
        path, _ = QFileDialog.getOpenFileName(self, input_file_label_text)
        if path:
            input_file_line_edit.setText(path)
    
    def switch_free_adjustment(self, state):
        is_enabled = state == 2
        self.free_adjustment_weighting_methods.setEnabled(is_enabled)
        for spin_box in self.free_adjustment_tuning_constants:
            spin_box.setEnabled(is_enabled)

    def weighting_method_changed(self, index, combo_box, tuning_constants_list):
        weighting_method = combo_box.currentText()
        for value in self.weighting_methods.values():
            if value["label"] == weighting_method:
                method_tuning_constants = value["default_c"]
                break
        self._hide_tuning_constants(tuning_constants_list)
        if method_tuning_constants is not None:
            self._show_tuning_constants(method_tuning_constants, tuning_constants_list)

    def set_report_path(self):
        path, _ = QFileDialog.getSaveFileName(self, "Report")
        if path:
            self.report_path.setText(path)

    def report_checkbox_changed(self, state, report_btn):
        report_btn.setEnabled(state == 2)
        self.report_path.setEnabled(state == 2)

    def set_output_mode(self, mode):
        if mode == "temp_layer" and self.output_saving_mode != "temp_layer":
            self.output_saving_mode = mode
            self.output_path.setText("")
        elif mode == "to_file":
            self.output_saving_mode = mode
            self.set_output_path()

    def set_output_path(self):
        path, _ = QFileDialog.getSaveFileName(self, "Wybierz plik wynikowy")
        if path:
            self.output_path.setText(path)

    def perform_adjustment(self):
        # TODO: Pass the adjustment parameters to the module with application core logic
        print("----- PERFORM ADJUSTMENT -----")
        print()

        print("----- Input files -----")
        print("measurements.csv:", self.measurements_file_path.text())
        print("controls.csv", self.controls_file_path.text())
        print()

        print("----- Weighting methods -----")
        print("Observations:", self.obs_weighting_methods.currentText())
        for i, obs_c in enumerate(self.obs_tuning_constants):
            if obs_c.isHidden():
                break
            print(f"c_{i+1}:", obs_c.value())
        print()

        if self.free_adjustment_weighting_methods.isEnabled():
            print("Free adjustment:", self.free_adjustment_weighting_methods.currentText())
        for i, obs_c in enumerate(self.free_adjustment_tuning_constants):
            if obs_c.isHidden():
                break
            print(f"c_{i+1}:", obs_c.value())
        print()

        if self.report_path.isEnabled():
            print("----- Export report -----")
            print("Report path:", self.report_path.text())
        print()

        print("----- Output -----")
        print("Output_mode:", self.output_saving_mode)
        if self.output_saving_mode == "temp_layer":
            print("Temp layer name", self.output_path.text())
        else:
            print("Output file path:", self.output_path.text())
