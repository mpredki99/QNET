from qgis.PyQt.QtWidgets import (
    QDialog, 
    QVBoxLayout, 
    QHBoxLayout, 
    QLineEdit, 
    QPushButton, 
    QFileDialog, 
    QLabel, 
    QFormLayout, 
    QComboBox, 
    QMenu, 
    QAction, 
    QCheckBox,
    QDoubleSpinBox
)


class WindowDialog(QDialog):

    weighting_methods = {
        "ordinary": {"label": "Ordinary", "default_c": None}, 
        "weighted": {"label": "Weighted", "default_c": None},
        "huber": {"label": "Huber", "default_c": (1.345,)},
        "slope": {"label": "Slope", "default_c": (2, 2)},
        "hampel": {"label": "Hampel", "default_c": (1.7, 3.4, 8.5)},
        "danish": {"label": "Danish", "default_c": (2.5,)},
        "epanechnikov": {"label": "Epanechnikov", "default_c": (3.674, 2)},
        "tukey": {"label": "Tukey", "default_c": (4.685, 2)},
        "jacobi": {"label": "Jacobi", "default_c": (4.687, 1)},
        "exponential": {"label": "Exponential", "default_c": (2, 2)},
        "sigma": {"label": "Sigma", "default_c": (2, 2)},
        "error_func": {"label": "Error function", "default_c": (1.414, 2)},
        "cauchy": {"label": "Cauchy", "default_c": (2.385, 2)},
        "t": {"label": "T", "default_c": (1, 2)},
        "bell": {"label": "Bell", "default_c": (1, 1)},
        "chain": {"label": "Chain Curve", "default_c": (1,)},
        "andrews": {"label": "Andrews", "default_c": (4.207,)},
        "wave": {"label": "Wave", "default_c": (2.5,)},
        "half_wave": {"label": "Half-wave", "default_c": (2.5,)},
        "wigner": {"label": "Wigner", "default_c": (3.137,)},
        "ellipse_curve": {"label": "Ellipse", "default_c": (2.5,)},
        "trim": {"label": "Trim", "default_c": (2.5,)},
    }

    def __init__(self):
        super().__init__()
        self.setWindowTitle("QNET")

        self.measurements_file_path = None
        self.controls_file_path = None
        self.obs_weighting_methods = None
        self.obs_tuning_constants = []
        self.free_adjustment_weighting_methods = None
        self.free_adjustment_tuning_constants = []
        self.report_path = None
        self.output_saving_mode = None
        self.output_path = None

        main_layout = QVBoxLayout()

        data_input_layout = self._prepare_data_input_layout()
        main_layout.addLayout(data_input_layout)

        select_weighting_methods_layout = self._prepare_weighting_methods_layout()
        main_layout.addLayout(select_weighting_methods_layout)

        report_layout = self._prepare_report_layout()
        main_layout.addLayout(report_layout)

        data_output_layout = self._prepare_data_output_layout()
        main_layout.addLayout(data_output_layout)

        ok_button = self._prepare_ok_button()
        main_layout.addWidget(ok_button)

        self.resize(430, 285) 

        self.setLayout(main_layout)

    def _prepare_data_input_layout(self):
        data_input_form_layout = QFormLayout()

        measurements_file_row_label, measurements_file_input_layout = self._prepare_input_file_layout(
            "measurements_file_path",
            "Select measurements.csv file"
        )
        data_input_form_layout.addRow(measurements_file_row_label)
        data_input_form_layout.addRow(measurements_file_input_layout)

        controls_file_row_label, controls_file_input_layout = self._prepare_input_file_layout(
            "controls_file_path",
            "Select controls.csv file"
        )
        data_input_form_layout.addRow(controls_file_row_label)
        data_input_form_layout.addRow(controls_file_input_layout)

        return data_input_form_layout

    def _prepare_input_file_layout(self, attr_name, input_file_label_text):
        input_file_layout = QHBoxLayout()
        
        setattr(self, attr_name, QLineEdit())
        input_file_path_widget = getattr(self, attr_name)

        browse_file_button = QPushButton("...")
        browse_file_button.clicked.connect(lambda: self.set_input_file(input_file_path_widget, input_file_label_text))
        
        input_file_layout.addWidget(input_file_path_widget, stretch=1)
        input_file_layout.addWidget(browse_file_button, stretch=0)

        return QLabel(input_file_label_text + ":"), input_file_layout
    
    def _prepare_weighting_methods_layout(self):
        select_weighting_methods_form_layout = QFormLayout()

        select_weighting_methods_row_layout = QHBoxLayout()

        obs_weighting_methods_layout = self._prepare_obs_weighting_methods_layout()
        select_weighting_methods_row_layout.addLayout(obs_weighting_methods_layout, stretch=1)

        ctrl_weighting_methods_layout = self._prepare_free_adjustment_weighting_methods_layout()
        select_weighting_methods_row_layout.addLayout(ctrl_weighting_methods_layout, stretch=1)

        select_weighting_methods_form_layout.addRow(select_weighting_methods_row_layout)

        return select_weighting_methods_form_layout
    
    def _prepare_obs_weighting_methods_layout(self):
        weighting_methods_layout = QFormLayout()

        select_weighting_methods_label = QLabel("Observations weighting methods")
        obs_tuning_constants_layout = self._prepare_tuning_constants_layout(self.obs_tuning_constants)
        self.obs_weighting_methods = self._prepare_weighting_methods_combo_box(self.obs_tuning_constants)

        weighting_methods_layout.addRow(select_weighting_methods_label)
        weighting_methods_layout.addRow(self.obs_weighting_methods)
        weighting_methods_layout.addRow(obs_tuning_constants_layout)
        
        return weighting_methods_layout

    def _prepare_free_adjustment_weighting_methods_layout(self):
        free_adjustment_weighting_methods_layout = QFormLayout()

        select_weighting_methods_label = QLabel("Free adjustment weighting methods")
        
        weighting_methods_combo_box_layout = QHBoxLayout()
        
        free_adjustment_checkbox = QCheckBox()
        free_adjustment_checkbox.stateChanged.connect(self.switch_free_adjustment)
        
        free_adjustment_tuning_constants_layout = self._prepare_tuning_constants_layout(self.free_adjustment_tuning_constants)

        self.free_adjustment_weighting_methods = self._prepare_weighting_methods_combo_box(self.free_adjustment_tuning_constants)
        self.free_adjustment_weighting_methods.setEnabled(False)

        weighting_methods_combo_box_layout.addWidget(free_adjustment_checkbox, stretch=0)
        weighting_methods_combo_box_layout.addWidget(self.free_adjustment_weighting_methods, stretch=1)

        free_adjustment_weighting_methods_layout.addRow(select_weighting_methods_label)
        free_adjustment_weighting_methods_layout.addRow(weighting_methods_combo_box_layout)
        free_adjustment_weighting_methods_layout.addRow(free_adjustment_tuning_constants_layout)

        return free_adjustment_weighting_methods_layout
    
    def _prepare_weighting_methods_combo_box(self, tuning_constants_list):
        weighting_methods_combo_box = QComboBox()
        weighting_methods_combo_box.addItems([value["label"] for value in self.weighting_methods.values()])
        weighting_methods_combo_box.currentIndexChanged.connect(lambda index: self.weighting_method_changed(index, weighting_methods_combo_box, tuning_constants_list))

        return weighting_methods_combo_box
    
    def _prepare_tuning_constants_layout(self, tuning_constants_list):
        tuning_constants_layout = QHBoxLayout()
        for _ in range(3):
            spin_box = QDoubleSpinBox()
            spin_box.setDecimals(3)
            spin_box.setRange(0, 100.0)
            spin_box.setSingleStep(0.01)
            spin_box.hide()
            tuning_constants_list.append(spin_box)
            tuning_constants_layout.addWidget(spin_box)

        return tuning_constants_layout
    
    def _hide_tuning_constants(self, tuning_constants_list):
        for spin_box in tuning_constants_list:
            spin_box.hide()
    
    def _show_tuning_constants(self, method_tuning_constants, tuning_constants_list):
        for spin_box, c in zip(tuning_constants_list, method_tuning_constants):
            spin_box.setValue(c)
            spin_box.show()
    
    def _prepare_report_layout(self):
        report_form_layout = QFormLayout()
        
        report_label = QLabel("Report:")

        report_path_layout = QHBoxLayout()

        self.report_path = QLineEdit()
        self.report_path.setEnabled(False)

        report_btn = QPushButton("...")
        report_btn.setEnabled(False)
        report_btn.clicked.connect(self.set_report_path)

        report_checkbox = QCheckBox()
        report_checkbox.stateChanged.connect(lambda state: self.report_checkbox_changed(state, report_btn))

        report_path_layout.addWidget(report_checkbox, stretch=0)
        report_path_layout.addWidget(self.report_path, stretch=1)
        report_path_layout.addWidget(report_btn, stretch=0)

        report_form_layout.addRow(report_label)
        report_form_layout.addRow(report_path_layout)
        
        return report_form_layout
    

    def _prepare_data_output_layout(self):
        data_output_form_layout = QFormLayout()

        data_output_label = QLabel("Select output path:")
        output_path_layout = QHBoxLayout()

        self.output_path = QLineEdit()
        self.output_path.setPlaceholderText("[Temporary layer]")

        output_saving_mode_btn = QPushButton("...")
        self.output_saving_mode = "temp"
        
        output_saving_mode_menu = QMenu()

        qmenu_actions = self._define_output_mode_actions()

        for action in qmenu_actions:
            output_saving_mode_menu.addAction(action)
        
        output_saving_mode_btn.setMenu(output_saving_mode_menu)
        
        output_path_layout.addWidget(self.output_path)
        output_path_layout.addWidget(output_saving_mode_btn)

        data_output_form_layout.addRow(data_output_label)
        data_output_form_layout.addRow(output_path_layout)

        return data_output_form_layout
    
    def _define_output_mode_actions(self):
        temp_layer_mode_action = self._define_output_mode_action("temp_layer", "Temporary layer")
        to_file_mode_action = self._define_output_mode_action("to_file", "To file")

        return temp_layer_mode_action, to_file_mode_action

    def _define_output_mode_action(self, action_mode, action_name):
        action = QAction(action_name, self)
        action.triggered.connect(lambda: self.set_output_mode(action_mode))
        
        return action
    
    def _prepare_ok_button(self):
        ok_button = QPushButton("OK")
        ok_button.clicked.connect(self.perform_adjustment)
        return ok_button
    
    # Signals handling ------------------------------------------------------

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
