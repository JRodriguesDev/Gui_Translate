from PySide6.QtWidgets import QFrame, QLabel, QVBoxLayout, QPushButton
from PySide6.QtCore import Qt, Slot

with open('./styles/start.qss', mode='r') as f:
    style = f.read()

class StartWidget(QFrame):
    def __init__(self, main_window):
        super().__init__()
        self._main_window = main_window
        self.setStyleSheet(style)
        self.setObjectName('widget')
        self._title = QLabel('GUI Translate')
        self._title.setObjectName('title')
        self._button = QPushButton("Iniciar")
        self._button.setObjectName('button')
        self._layout = QVBoxLayout()
        self._layout.addStretch(3)
        self._layout.addWidget(self._title, alignment=Qt.AlignCenter)
        self._layout.addStretch(1.8)
        self._layout.addWidget(self._button, alignment=Qt.AlignCenter)
        self._layout.addStretch(4)
        self.setLayout(self._layout)
        self._button.clicked.connect(self.install_and_continue)

    @Slot()
    def install_and_continue(self):
        print('instalando e verificando Modelo OCR')
        self._main_window.install_all_models()
        self._main_window.swith_widget(2)


