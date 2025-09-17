from PySide6.QtCore import QPropertyAnimation, QByteArray, QSequentialAnimationGroup
from PySide6.QtWidgets import QGraphicsOpacityEffect, QWidget
from PySide6.QtCore import QObject, Signal, Slot

class Transiction(QObject):
    _finished = Signal()

    def __init__(self):
        super().__init__()
        self._duration = 900

    def start_transiticion (self, old_widget, new_widget):
        self._old_widget = old_widget
        self._new_widget = new_widget
        
        self._fade_out_effect = QGraphicsOpacityEffect(self)
        self._fade_in_effect = QGraphicsOpacityEffect(self)
        self._fade_out_anim = QPropertyAnimation(self._fade_out_effect, b'opacity', self)
        self._fade_in_anim = QPropertyAnimation(self._fade_in_effect, b'opacity', self)

        self._fade_out_anim.setDuration(self._duration)
        self._fade_out_anim.setStartValue(1.0)
        self._fade_out_anim.setEndValue(0.0)

        self._fade_in_anim.setDuration(self._duration)
        self._fade_in_anim.setStartValue(0.0)
        self._fade_in_anim.setEndValue(1.0)

        self._fade_out_anim.finished.connect(self.start_fade_in)
        self._fade_in_anim.finished.connect(self._finished.emit)

        self._new_widget.setGraphicsEffect(self._fade_in_effect)
        self._new_widget.setVisible(True)
        self._fade_out_anim.start()

    @Slot()
    def start_fade_in(self):
        self._old_widget.setVisible(False)
        self._fade_in_anim.start()




