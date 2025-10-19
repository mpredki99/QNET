import os.path

from qgis.PyQt.QtGui import QIcon, QPixmap

ICONS_DIR = os.path.join(os.path.dirname(__file__), "png")


main_icon = QIcon(os.path.join(ICONS_DIR, "QNet.png"))

main_pixmap = QPixmap(os.path.join(ICONS_DIR, "QNet.png"))
qnet_error_pixmap = QPixmap(os.path.join(ICONS_DIR, "QNetError.png"))
qnet_warning_pixmap = QPixmap(os.path.join(ICONS_DIR, "QNetWarning.png"))
qnet_question_pixmap = QPixmap(os.path.join(ICONS_DIR, "QNetQuestion.png"))
qnet_information_pixmap = QPixmap(os.path.join(ICONS_DIR, "QNetInformation.png"))
