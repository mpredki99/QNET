# Coding: UTF-8

# Copyright (C) 2025 Michał Prędki
# Licensed under the GNU General Public License v3.0.
# Full text of the license can be found in the LICENSE file in the repository.

from typing import Literal

from qgis.PyQt.QtWidgets import QCheckBox, QFileDialog, QLineEdit, QWidget

get_file_name_mode = Literal["open", "save"]


def get_file_path_from_dialog_window(
    widget: QWidget,
    window_title: str,
    dir: str,
    file_filter: str,
    mode: get_file_name_mode,
) -> str:
    """Open file dialog and return selected file path."""
    modes = {
        "open": QFileDialog.getOpenFileName,
        "save": QFileDialog.getSaveFileName,
    }
    window_mode = modes.get(mode)

    path, _ = window_mode(widget, window_title, dir, file_filter)
    return path if path else ""


def update_line_edit(line_edit: QLineEdit, new_line_edit_text: str) -> None:
    """Update the line edit if not focused and value changed."""
    if line_edit.hasFocus():
        return  # Skip when user is typing the path manually

    if line_edit.text() == new_line_edit_text:
        return  # Skip if new value is the same as previous one

    line_edit.setText(new_line_edit_text)


def update_checkbox_state(checkbox: QCheckBox, state: int) -> None:
    """Update checkbox to the specified check state."""
    if state == checkbox.checkState():
        return
    checkbox.setCheckState(state)
