from PySide6.QtWidgets import QSystemTrayIcon, QMenu, QApplication
from PySide6.QtGui import QIcon
from PySide6.QtCore import Slot

class SystemTrayIcon(QSystemTrayIcon):
    def __init__(self, window):
        super().__init__()
        self.setIcon(QIcon('./db/images/tradutor.png'))
        self._menu = QMenu()
        self._show_action = self._menu.addAction('Show')
        self._quit_action = self._menu.addAction('Quit')
        self._show_action.triggered.connect(window.show_window)
        self._quit_action.triggered.connect(self.exit_window)
        self.setContextMenu(self._menu)

    def show_tray(self):
        self.show()

    @Slot()
    def hidden_tray(self):
        self.hide()

    @Slot()
    def exit_window(self):
        QApplication.instance().quit()