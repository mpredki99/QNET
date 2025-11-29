# Coding: UTF-8

# Copyright (C) 2025 Michał Prędki
# Licensed under the GNU General Public License v3.0.
# Full text of the license can be found in the LICENSE file in the repository.

"""
========================================================================================
Icons
========================================================================================

This module centralizes access to all QNET plugin icons. Icons are stored as QIcon or 
QPixmap objects for convenient reuse throughout the plugin.

Structure
---------
All icons are stored in the local `png/` directory. This module exposes both:
- QIcon objects — typically used for window or action icons
- QPixmap objects — typically used in message dialogs or labels

Exposed Icons
-------------
- main_icon : QIcon used as the primary plugin icon
- main_pixmap : Pixmap version of the main icon
- qnet_error_pixmap : Pixmap for error messages
- qnet_warning_pixmap : Pixmap for warning messages
- qnet_question_pixmap : Pixmap for confirmation dialogs
- qnet_information_pixmap : Pixmap for informational messages

========================================================================================
"""

from pathlib import Path

from qgis.PyQt.QtGui import QIcon, QPixmap

ICONS_DIR = Path(__file__).parent.joinpath("png")

# Icons ================================================================================
main_icon = QIcon(str(ICONS_DIR.joinpath("QNet.png")))

# Pixmaps ==============================================================================
main_pixmap = QPixmap(str(ICONS_DIR.joinpath("QNet.png")))
qnet_error_pixmap = QPixmap(str(ICONS_DIR.joinpath("QNetError.png")))
qnet_warning_pixmap = QPixmap(str(ICONS_DIR.joinpath("QNetWarning.png")))
qnet_question_pixmap = QPixmap(str(ICONS_DIR.joinpath("QNetQuestion.png")))
qnet_information_pixmap = QPixmap(str(ICONS_DIR.joinpath("QNetInformation.png")))
