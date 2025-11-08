# Coding: UTF-8

# Copyright (C) 2025 Michał Prędki
# Licensed under the GNU General Public License v3.0.
# Full text of the license can be found in the LICENSE file in the repository.

from typing import Literal

from qgis.PyQt.QtWidgets import QCheckBox, QComboBox, QFileDialog, QLineEdit, QWidget


def get_file_path_from_dialog(
    widget: QWidget,
    window_title: str,
    dir: str,
    file_filter: str,
    mode: Literal["open", "save"],
) -> str:
    """
    Open a file dialog and return the selected file path.

    Opens a QFileDialog in either open or save mode, based on the provided mode.
    Returns the absolute file path selected by the user, or an empty string if
    the dialog is cancelled or an invalid mode is specified.

    Parameters
    ----------
    - widget: QWidget
        Parent widget for the file dialog.
    - window_title : str
        Title displayed on the file dialog window.
    - dir: str
        Initial directory path for the file dialog.
    - file_filter: str
        File type filter.
    - mode : Literal["open", "save"]
        Mode of the dialog — either "open" for loading files or "save" for saving output.

    Returns
    -------
    str
        Selected file path or an empty string if cancelled.
    """
    window_modes = {
        "open": QFileDialog.getOpenFileName,
        "save": QFileDialog.getSaveFileName,
    }
    window_mode = window_modes.get(mode)

    if not window_mode:
        return ""

    path, _ = window_mode(widget, window_title, dir, file_filter)
    return path if path else ""


def update_line_edit(line_edit: QLineEdit, line_edit_text: str) -> None:
    """
    Update the text in a QLineEdit widget if is not focused and the new text differs
    from the current value.

    Parameters
    ----------
    - line_edit : QLineEdit
        The line edit widget to update.
    - line_edit_text : str
        The new text value to set.
    """
    if line_edit.hasFocus():
        return  # Skip when user is typing the path manually

    if line_edit.text() == line_edit_text:
        return  # Skip if new value is the same as previous one

    line_edit.setText(line_edit_text)


def update_checkbox_state(checkbox: QCheckBox, state: int) -> None:
    """
    Update a checkbox to the specified check state if different from the current one.

    Parameters
    ----------
    - checkbox : QCheckBox
        The checkbox widget to update.
    - state : int
        The target check state.
    """
    if state == checkbox.checkState():
        return
    checkbox.setCheckState(state)


def update_combo_box_text(combo_box: QComboBox, text: str) -> None:
    """
    Update the current text of a combo box if it differs from the existing one.

    Parameters
    ----------
    - combo_box : QComboBox
        The combo box widget to update.
    - text : str
        The target text to set as the current selection.
    """
    if text == combo_box.currentText():
        return

    index = combo_box.findText(text)
    if index != -1:
        combo_box.setCurrentIndex(index)
