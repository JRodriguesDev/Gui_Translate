from PySide6.QtWidgets import QFrame, QVBoxLayout, QProgressBar, QLabel, QGraphicsDropShadowEffect
from PySide6.QtCore import Qt, Slot, Signal, QPropertyAnimation, QPoint
from PySide6.QtGui import QColor
from gui.logo import Logo

with open('./styles/loading.qss', mode='r', encoding='utf-8') as f:
    styles = f.read()

class LoadingWidget(QFrame):
    def __init__(self, main_window):
        super().__init__()
        self._main_window = main_window
        self._log_frames = []

        self._logo = Logo()
        self._main_layout = QVBoxLayout(self)
        self._layout = QVBoxLayout()
        self._log_layout = QVBoxLayout()
        self._progress_bar = QProgressBar()

        self._value = 0

        self._progress_bar.setObjectName('main_progress_bar')
        self._progress_bar.setTextVisible(False)
        self._progress_bar.setFixedSize(100, 20)
        self._progress_bar.setRange(0, self._main_window.progress_bar_max())

        self.setObjectName('widget')

        self._main_layout.addLayout(self._layout)
        self._main_layout.addLayout(self._log_layout)

        self._layout.addStretch(2)
        self._layout.addWidget(self._logo, alignment=Qt.AlignmentFlag.AlignCenter)
        self._layout.addStretch(1)
        self._layout.addWidget(self._progress_bar, alignment=Qt.AlignmentFlag.AlignCenter)
        self._layout.addStretch(4)
        
        self.setLayout(self._main_layout)

        self._main_window.set_loading_widget(self)

        glow_effect = QGraphicsDropShadowEffect(self)
        glow_effect.setBlurRadius(30)
        glow_effect.setOffset(0, 0)
        glow_effect.setColor(QColor(0, 0, 255))
        self._progress_bar.setGraphicsEffect(glow_effect)

        self.setStyleSheet(styles)

    @Slot(str)
    def update_state(self, signal):
        if self._log_frames:
            label_height = self._log_frames[0].height() if self._log_frames else 0
            for frame in self._log_frames:
                animation_label = QPropertyAnimation(frame, b'pos', self)
                animation_label.setDuration(400)
                animation_label.setEndValue(QPoint(frame.x(), frame.y() - label_height))
                animation_label.start()

            border_progress_bar = self._log_frames[-1].findChild(QProgressBar)
            animation_progress_bar = QPropertyAnimation(border_progress_bar, b'value', self)
            animation_progress_bar.setDuration(900)
            animation_progress_bar.setStartValue(0)
            animation_progress_bar.setEndValue(100)
            animation_progress_bar.start()

        log_line_widget = QFrame(self)
        log_line_layout = QVBoxLayout(log_line_widget)
        log_line_layout.setContentsMargins(0, 0, 0, 0)
        log_line_layout.setSpacing(0)

        new_label = QLabel(signal)
        new_label.setObjectName('log_label')

        border_progress_bar = QProgressBar()
        border_progress_bar.setObjectName('console_progress_bar')
        border_progress_bar.setRange(0, 100)
        border_progress_bar.setValue(0)
        border_progress_bar.setTextVisible(False)
        border_progress_bar.setFixedHeight(4)

        log_line_layout.addWidget(new_label)
        log_line_layout.addWidget(border_progress_bar)

        log_line_widget.move(8, self.height() - log_line_widget.height())
        log_line_widget.show()
        self._log_frames.append(log_line_widget)

    @Slot()
    def update_progress(self):
        current_value = self._progress_bar.value()
        self._value += 1

        animation = QPropertyAnimation(self._progress_bar, b'value', self)
        animation.setDuration(500)
        animation.setStartValue(current_value)
        animation.setEndValue(self._value)
        animation.start()
"""
    @Slot()
    def finish_loading(self):
        self._loading_complete = False
        border_progress_bar = self._log_frames[-1].findChild(QProgressBar)
        animation = QPropertyAnimation(border_progress_bar, b'value', self)
        animation.setDuration(900)
        animation.setStartValue(0)
        animation.setEndValue(100)
        animation.start()

        self._main_window._ocr_thread.end_task()
        #self._main_window._llm_thread.end_task()
        animation.finished.connect(lambda: self._main_window.swith_widget(1))
        """
