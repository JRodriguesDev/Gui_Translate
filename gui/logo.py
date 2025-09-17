from PySide6.QtWidgets import QFrame, QVBoxLayout, QLabel, QGraphicsDropShadowEffect
from PySide6.QtSvg import QSvgRenderer
from PySide6.QtGui import QPixmap, QColor
from PySide6.QtCore import Qt, QPropertyAnimation

class Logo(QFrame):
    def __init__(self):
        super().__init__()
        self.setFixedSize(175, 175)
        
        self._logo_label = QLabel()

        self._layout = QVBoxLayout(self)
        self._layout.addWidget(self._logo_label, alignment=Qt.AlignmentFlag.AlignCenter)

        pixmap = QPixmap('./db/images/logo.svg')
        scaled_pixmap = pixmap.scaled(150, 150, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        self._logo_label.setPixmap(scaled_pixmap)

        self._glow_effect = QGraphicsDropShadowEffect(self)
        self._glow_effect.setBlurRadius(40)
        self._glow_effect.setOffset(5, 5)
        self._glow_effect.setColor(QColor(0, 0, 255))

        self._logo_label.setGraphicsEffect(self._glow_effect)

        self._animation = QPropertyAnimation(self._glow_effect, b'color', self)
        self._animation.setDuration(500)

    def enterEvent(self, event):
        self._animation.setStartValue(self._glow_effect.color())
        self._animation.setEndValue(QColor(255, 0, 0))
        self._animation.start()

        super().enterEvent(event)

    def leaveEvent(self, event):
        self._animation.setStartValue(self._glow_effect.color())
        self._animation.setEndValue(QColor(0, 0, 255))
        self._animation.start()

        super().leaveEvent(event)