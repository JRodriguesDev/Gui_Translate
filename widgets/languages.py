from PySide6.QtWidgets import QFrame, QPushButton, QVBoxLayout, QHBoxLayout, QButtonGroup, QLabel, QProgressBar, QGraphicsColorizeEffect, QStackedLayout, QWidget, QGraphicsDropShadowEffect
from PySide6.QtCore import Slot, Qt, QPropertyAnimation, QEvent
from PySide6.QtGui import QColor, QIcon


with open('./styles/languages.qss', mode='r') as f:
    style = f.read()

class LanguagesWidget(QFrame):
    def __init__(self, main_window):
        super().__init__()
        self.setObjectName('widget')

        self._main_window = main_window
        self._languages = main_window.languages
        self._language_s = ''
        self._language_t = ''
        self._mode = None

        glow_effect = QGraphicsDropShadowEffect(self)
        glow_effect.setBlurRadius(30)
        glow_effect.setOffset(0, 0)
        glow_effect.setColor(QColor(0, 0, 255))

        self._capture_icon = QIcon('./db/images/capture.svg')
        self._stream_icon = QIcon('./db/images/stream.svg')

        self._s_button_group = QButtonGroup()
        self._s_button_group.setExclusive(True)
        self._t_button_group = QButtonGroup()
        self._t_button_group.setExclusive(True)

        self._capture_button = QPushButton(self._capture_icon, '')
        self._stream_button = QPushButton(self._stream_icon, '')
        self._translate_button = QPushButton('Confirmar')

        self._capture_button.setFixedSize(90, 40)
        self._capture_button.setObjectName('button_modes')
        self._capture_button.clicked.connect(self.mode_capture)
        self._stream_button.setFixedSize(90, 40)
        self._stream_button.setObjectName('button_modes')
        self._stream_button.clicked.connect(self.mode_stream)
        self._translate_button.setObjectName('confirm_button')
        self._translate_button.setFixedSize(250, 30)
        self._translate_button.clicked.connect(self.confirm_mode)

        self._main_layout = QVBoxLayout()
        self._title_layout = QVBoxLayout()
        self._languagues_layout = QHBoxLayout()
        self._source_layout = QVBoxLayout()
        self._target_layout = QVBoxLayout()
        self._main_modes_layout = QVBoxLayout()
        self._modes_layout = QHBoxLayout()
        self._title_modes_layout = QVBoxLayout()

        self._title = QLabel('Selecione as linguagens')
        self._progress_bar = QProgressBar()
        self._confirm_button = QPushButton('Confirmar Linguagens')

        self._modes_title = QLabel('Selecione o modo')
        self._modes_progress_bar = QProgressBar()

        self._modes_title.setObjectName('title')
        self._modes_progress_bar.setObjectName('progress_bar')
        self._modes_progress_bar.setTextVisible(False)
        self._modes_progress_bar.setRange(0, 100)
        self._modes_progress_bar.setFixedSize(250, 8)
        self._modes_progress_bar.setValue(50)

        self._animation_mode_bar = QPropertyAnimation(self._modes_progress_bar, b'value', self)
        self._animation_mode_bar.setDuration(300)
        self._animation_mode_bar.finished.connect(self.init_translate)

        self._title.setObjectName('title')
        self._confirm_button.setObjectName('confirm_button')
        self._confirm_button.setFixedSize(250, 30)
        self._confirm_button.installEventFilter(self)
        self._confirm_button.clicked.connect(self.confirm_langs)

        self._progress_bar.setObjectName('progress_bar')
        self._progress_bar.setTextVisible(False)
        self._progress_bar.setRange(0, 100)
        self._progress_bar.setFixedSize(250, 8)

        self._animation_main_bar = QPropertyAnimation(self._progress_bar, b'value', self)
        self._animation_main_bar.setDuration(300)
        self._animation_main_bar.finished.connect(self.swith_mode)

        self._translate_button.installEventFilter(self)

        self._title_modes_layout.addStretch(1)
        self._title_modes_layout.addWidget(self._modes_title, alignment=Qt.AlignmentFlag.AlignCenter)
        self._title_modes_layout.addStretch(0)
        self._title_modes_layout.addWidget(self._modes_progress_bar, alignment=Qt.AlignmentFlag.AlignCenter)
        self._title_modes_layout.addStretch(10)

        self._modes_layout.addWidget(self._capture_button)
        self._modes_layout.setSpacing(1)
        self._modes_layout.addWidget(self._stream_button)

        self._main_modes_layout.addStretch(1)
        self._main_modes_layout.addLayout(self._title_modes_layout)
        self._main_modes_layout.addStretch(3)
        self._main_modes_layout.addLayout(self._modes_layout)
        self._main_modes_layout.addStretch(3)
        self._main_modes_layout.addWidget(self._translate_button, alignment=Qt.AlignmentFlag.AlignCenter)
        self._main_modes_layout.addStretch(1)

        for i, lang in enumerate(self._languages.langs):
            s_button = QPushButton(lang)
            t_button = QPushButton(lang)

            s_button.setObjectName('lang_button')
            t_button.setObjectName('lang_button')

            s_button.setCheckable(True)
            t_button.setCheckable(True)

            s_button.setFixedSize(250, 30)
            t_button.setFixedSize(250, 30)

            self._s_button_group.addButton(s_button, i)
            self._t_button_group.addButton(t_button, i)

            self._source_layout.addWidget(s_button)
            self._source_layout.setSpacing(15)
            self._target_layout.addWidget(t_button)
            self._target_layout.setSpacing(15)

        self._title_layout.addStretch(1)
        self._title_layout.addWidget(self._progress_bar, alignment=Qt.AlignmentFlag.AlignCenter)
        self._title_layout.addStretch(0)
        self._title_layout.addWidget(self._title, alignment=Qt.AlignmentFlag.AlignCenter)
        self._title_layout.addStretch(10)

        self._languagues_layout.addLayout(self._source_layout)
        self._languagues_layout.addLayout(self._target_layout)

        self._main_layout.addStretch(1)
        self._main_layout.addLayout(self._title_layout)
        self._main_layout.addStretch(5)
        self._main_layout.addLayout(self._languagues_layout)
        self._main_layout.addStretch(1)
        self._main_layout.addWidget(self._confirm_button, alignment=Qt.AlignmentFlag.AlignCenter)
        self._main_layout.addStretch(2)

        self._s_button_group.buttonClicked.connect(self.s_language)
        self._t_button_group.buttonClicked.connect(self.t_language)

        self._main_widget = QWidget()
        self._main_widget.setLayout(self._main_layout)
        self._main_modes_widget = QWidget()
        self._main_modes_widget.setLayout(self._main_modes_layout)

        self._stacks_layouts = QStackedLayout()
        self._stacks_layouts.addWidget(self._main_widget)
        self._stacks_layouts.addWidget(self._main_modes_widget)

        self.setLayout(self._stacks_layouts)
        self._stacks_layouts.setCurrentIndex(0)

        self._colorize_effect_confirm_btn = QGraphicsColorizeEffect(self._confirm_button)
        self._confirm_button.setGraphicsEffect(self._colorize_effect_confirm_btn)
        self._confirm_button_animation = QPropertyAnimation(self._colorize_effect_confirm_btn, b'color', self)
        self._confirm_button_animation.setDuration(250)

        self._colorize_effect_translate_btn = QGraphicsColorizeEffect(self._translate_button)
        self._translate_button.setGraphicsEffect(self._colorize_effect_translate_btn)
        self._translate_button_animation = QPropertyAnimation(self._colorize_effect_translate_btn, b'color', self)
        self._translate_button_animation.setDuration(250)

        self._progress_bar.setGraphicsEffect(glow_effect)
        self._modes_progress_bar.setGraphicsEffect(glow_effect)
        self.setStyleSheet(style)

    def eventFilter(self, watched, event):
        if watched == self._confirm_button:
            if event.type() == QEvent.Enter:
                self._confirm_button_animation.setStartValue(QColor(0, 0, 255))
                self._confirm_button_animation.setEndValue(QColor(255, 0, 0))
                self._confirm_button_animation.start()
                return True
            elif event.type() == QEvent.Leave:
                self._confirm_button_animation.setStartValue(QColor(255, 0, 0))
                self._confirm_button_animation.setEndValue(QColor(0, 0, 255))
                self._confirm_button_animation.start()
                return True

        if watched == self._translate_button:
            if event.type() == QEvent.Enter:
                self._translate_button_animation.setStartValue(QColor(0, 0, 255))
                self._translate_button_animation.setEndValue(QColor(255, 0, 0))
                self._translate_button_animation.start()
                return True
            elif event.type() == QEvent.Leave:
                self._translate_button_animation.setStartValue(QColor(255, 0, 0))
                self._translate_button_animation.setEndValue(QColor(0, 0, 255))
                self._translate_button_animation.start()
                return True

        return super().eventFilter(watched, event)

    @property
    def all_keys(self):
        self._languages.ocr_keys

    @Slot()
    def s_language(self, btn):
        self._language_s = btn.text()

    @Slot()
    def t_language(self, btn):
        self._language_t = btn.text()
    
    @property
    def get_langs(self):
        return self._language_t, self._language_s
    
    @Slot()
    def mode_capture(self):
        self._mode =self._main_window.switch_capture_widget

    @Slot()
    def mode_stream(self):
        self._mode = self._main_window.switch_stream_widget

    @Slot()
    def confirm_langs(self):
        if self._language_s and self._language_t:
            self._animation_main_bar.setStartValue(0)
            self._animation_main_bar.setEndValue(50)
            self._animation_main_bar.start()

    @Slot()
    def confirm_mode(self):
        if self._mode:
            self._animation_mode_bar.setStartValue(50)
            self._animation_mode_bar.setEndValue(100)
            self._animation_mode_bar.start()

    @Slot()
    def swith_mode(self):
        self._stacks_layouts.setCurrentIndex(1)

    @Slot()
    def init_translate(self):
        if self._language_s and self._language_t:
            keys = {'lang_s': self._languages.get_keys(self._language_s)['key_ocr'], 'lang_t': self._languages.get_keys(self._language_t)['key_llm']}
            self._main_window.show_tray_icon()
            self._mode(keys)
            self._progress_bar.setValue(0)
            self._stacks_layouts.setCurrentIndex(0)