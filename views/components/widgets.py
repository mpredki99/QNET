# Coding: UTF-8

# Copyright (C) 2025 Michał Prędki
# Licensed under the GNU General Public License v3.0.
# Full text of the license can be found in the LICENSE file in the repository.

from typing import Any, Iterator, List, Optional, Tuple

from qgis.PyQt.QtCore import QObject, pyqtSignal
from qgis.PyQt.QtGui import QPixmap
from qgis.PyQt.QtWidgets import (
    QAction,
    QComboBox,
    QDoubleSpinBox,
    QMenu,
    QMessageBox,
    QWidget,
)

from ...icons.icons import (
    main_pixmap,
    qnet_error_pixmap,
    qnet_information_pixmap,
    qnet_warning_pixmap,
)
from ...utils.weighting_methods import WEIGHTING_METHODS


class QDoubleSpinBoxList(QObject):
    """
    Container for multiple QDoubleSpinBox widgets.

    Provides a list-like interface for managing and interacting with several
    spin boxes simultaneously. This allows batch configuration, value retrieval,
    and unified signal handling.

    Signals
    -------
    - listValueChanged : tuple
        Emitted when any visible spin box value changes.

    Attributes
    ----------
    _items : list[QDoubleSpinBox]
        List of QDoubleSpinBox widgets contained in this widget.
    """

    listValueChanged = pyqtSignal(tuple)

    def __init__(self, n: int, parent: Optional[QWidget] = None) -> None:
        """
        Initialize a container of QDoubleSpinBox widgets.

        Parameters
        ----------
        n : int
            The number of QDoubleSpinBox widgets to create and store in the list.
        parent : QWidget, optional
            Parent widget for the QDoubleSpinBoxList object and its child spin boxes.
        """
        super().__init__(parent)
        self._items = [QDoubleSpinBox(parent=parent) for _ in range(n)]
        self._bind_spin_boxes()

    def __getattr__(self, name: str) -> Any:
        """Delegate attribute access or method calls to list container or QDoubleSpinBox items."""
        if hasattr(list, name):
            return self._handle_list_method(name)
        if hasattr(QDoubleSpinBox, name):
            return self._handle_spin_box_method(name)
        raise AttributeError(f"{self.__class__.__name__} has no attribute {name}")

    def __len__(self) -> int:
        """Return the number of spin boxes contained."""
        return len(self._items)

    def __iter__(self) -> Iterator[QDoubleSpinBox]:
        """Return iterator over spin boxes."""
        return iter(self._items)

    def __getitem__(self, index: int) -> QDoubleSpinBox:
        """Get spin box at index."""
        return self._items[index]

    def __setitem__(self, index: int, value: QDoubleSpinBox) -> None:
        """Set spin box at index."""
        if not isinstance(value, QDoubleSpinBox):
            raise TypeError(
                f"{self.__class__.__name__} can constains only QDoubleSpinBox objects"
            )
        self._items[index] = value

    def _bind_spin_boxes(self) -> None:
        """Bind valueChanged signal of each spin box to emit_list_value_changed."""
        for sb in self._items:
            sb.valueChanged.connect(self._emit_list_value_changed)

    def _emit_list_value_changed(self, _: float) -> None:
        """Emit listValueChanged signal with current visible spin box values."""
        values = tuple(
            spin_box.value() for spin_box in self._items if spin_box.isVisible()
        )
        self.listValueChanged.emit(values)

    def _handle_list_method(self, name: str) -> Any:
        """Handle list method delegation."""

        def wrapper(*args: Any, **kwargs: Any) -> Any:
            return getattr(self._items, name)(*args, **kwargs)

        attr = getattr(list, name)
        return wrapper if callable(attr) else attr

    def _handle_spin_box_method(self, name: str) -> Any:
        """Handle QDoubleSpinBox method delegation."""

        def wrapper(*args: Any, **kwargs: Any) -> Any:
            return [getattr(sb, name)(*args, **kwargs) for sb in self._items]

        attr = getattr(QDoubleSpinBox, name)
        return wrapper if callable(attr) else attr


class WeightingMethodComboBox(QComboBox):
    """
    QComboBox for selecting a weighting method.

    Automatically populates itself with supported methods defined in
    `WEIGHTING_METHODS`. Supports compatibility with both PyQt5 and PyQt6
    signal naming conventions.

    Signals
    -------
    - currentTextChanged: str
        Provides access to the text change signal compatible with PyQt5 and PyQt6.
    """

    def __init__(
        self,
        weighting_methods: Optional[List[str]] = None,
        parent: Optional[QWidget] = None,
    ) -> None:
        """
        Initialize the WeightingMethodComboBox.

        Parameters
        ----------
        weighting_methods : List[str] [optional, default=None]
            List of weighting method names to populate the combo box. If not provided,
            all available methods from `WEIGHTING_METHODS` will be used.
        parent : QWidget, optional
            The parent widget.
        """
        super().__init__(parent)
        self._populate(
            weighting_methods or [method for method in WEIGHTING_METHODS.keys()]
        )

    def _populate(self, weighting_methods: List[str]) -> None:
        """Populate widget with weighting method names."""
        self.addItems(weighting_methods)

    @property
    def currentTextChanged(self) -> pyqtSignal:
        """Provides the currentTextChanged signal, handling compatibility for both PyQt5 and PyQt6."""
        try:
            return super().currentTextChanged
        except AttributeError:
            return super().currentIndexChanged[str]


class SavingModeMenu(QMenu):
    """
    QMenu for selecting the output saving mode.

    Displays actions for QGIS layer available output modes, such as saving to
    a temporary QGIS layer or exporting results to a file.
    """

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        """
        Initialize the SavingModeMenu.

        Parameters
        ----------
        parent : QWidget, optional
            The parent widget.
        """
        super().__init__(parent)
        for action in self._define_output_mode_actions():
            self.addAction(action)

    def _define_output_mode_actions(self) -> Tuple[QAction]:
        """Return a tuple of QAction objects for output modes."""
        return (QAction("Temporary layer", self), QAction("To file", self))


class QNetMessageBox(QMessageBox):
    """
    Base message box class for QNET dialogs.

    Provides a standardized message box layout with QNET-specific icons
    and titles. Serves as a common base for specialized message box types
    such as error, warning, and information dialogs.
    """

    def __init__(
        self,
        title: str,
        text: str,
        icon: QPixmap = main_pixmap,
        parent: Optional[QWidget] = None,
    ) -> None:
        """
        Initialize QNetMessageBox and display it immediately.

        Parameters
        ----------
        - title : str
            Window title displayed in the dialog.
        - text : str
            Main message text to display.
        - icon : QPixmap, default=main_pixmap
            Custom pixmap used as the dialog icon.
        - parent : QWidget, optional
            Parent widget of the message box.
        """
        # Handle both PyQt5 and PyGt6
        try:
            ok_button = QMessageBox.StandardButton.Ok
        except AttributeError:
            ok_button = QMessageBox.Ok
        
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setText(text)
        self.setStandardButtons(ok_button)
        self.setIconPixmap(icon)
        self.exec()


class QNetErrorMessageBox(QNetMessageBox):
    """Error message box with custom QNET error icon."""

    def __init__(self, title: str, text: str, parent: Optional[QWidget] = None) -> None:
        super().__init__(title, text, icon=qnet_error_pixmap, parent=parent)


class QNetWarningMessageBox(QNetMessageBox):
    """Warning message box with custom QNET warning icon."""

    def __init__(self, title: str, text: str, parent: Optional[QWidget] = None) -> None:
        super().__init__(title, text, icon=qnet_warning_pixmap, parent=parent)


class QNetInformationMessageBox(QNetMessageBox):
    """Information message box for QNET with custom QNET information icon."""

    def __init__(self, title: str, text: str, parent: Optional[QWidget] = None) -> None:
        super().__init__(title, text, icon=qnet_information_pixmap, parent=parent)
