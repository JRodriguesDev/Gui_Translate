from PySide6.QtWidgets import QFrame, QLabel, QVBoxLayout, QPushButton, QGraphicsDropShadowEffect
from PySide6.QtCore import Slot, Qt, QRect, QPoint
from PySide6.QtGui import QPainter, QColor, QGuiApplication
import os

with open('./styles/capture.qss', mode='r', encoding='utf-8') as f:
    styles = f.read()

class CaptureWidget(QFrame):
    def __init__(self, main_window):
        super().__init__()
        self._main_window = main_window
        self._main_window._key_listen._hotkey_clicked.connect(self.init_capture)
        self._main_window._key_listen._mode_switched.connect(self.multiple_mode)
        

        self._is_capturing = False
        self._multiple_select = False
        self._selected_rects = []
        self._translated_labels = []

        self._translate_button = QPushButton('Iniciar Traduçao', self)
        self._translate_button.hide()
        self._translate_button.clicked.connect(self.init_translate)

        self._start_point = QPoint()
        self._end_point = QPoint()
        self._is_drawning = False

        self._label = QLabel(f'Modo de Multipla captura: {self._multiple_select}', self)
        self._label.setObjectName('label')
        self._label.move(10, 10)

        self.setStyleSheet(styles)

    @property
    def multiple_selected(self):
        return self._multiple_select

    @multiple_selected.setter
    def multiple_selected(self, value):
        self._multiple_select = value

    @Slot()
    def multiple_mode(self):
        if self.multiple_selected:
            self.multiple_selected = False
            self._label.setText(f'Modo de Multipla captura: {self.multiple_selected}')
            return
        
        if not self.multiple_selected:
            self.multiple_selected = True
            self._label.setText(f'Modo de Multipla captura: {self.multiple_selected}')

    @Slot()
    def init_capture(self):
        if self._is_capturing:
            self._main_window._key_listen.swith_mode_off()
            self._main_window.show_tray_icon()
            self._is_capturing = False   
            return

        if not self._is_capturing:
            self._main_window.capture_mode()
            self._is_capturing = True
        
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._start_point = event.position().toPoint()
            self._is_drawning = True
            [os.remove(os.path.join('./db/temp/capture', f)) for f in os.listdir('./db/temp/capture')]
    
    def mouseMoveEvent(self, event):
        if self._is_drawning:
            self._end_point = event.position().toPoint()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._end_point = event.position().toPoint()
            self._is_drawning = False
            self.show_translate_button()
            self.update()
            current_rect = QRect(self._start_point, self._end_point).normalized()
            if self._multiple_select:
                self._selected_rects.append(current_rect)
            else:
                self._selected_rects = [current_rect]

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor(0, 0, 0, 100))

        if self._is_drawning:
            current_rect = QRect(self._start_point, self._end_point).normalized()
            painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_Clear)
            painter.fillRect(current_rect, QColor(0, 0 ,0))

        for rect in self._selected_rects:
            painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_Clear)
            painter.fillRect(rect, QColor(0, 0 ,0))

        painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceOver)
        painter.setPen(QColor(0, 0, 255))

        if self._is_drawning:
            current_rect = QRect(self._start_point, self._end_point).normalized()
            painter.drawRect(current_rect)

        for rect in self._selected_rects:
            painter.drawRect(rect)

    def show_translate_button(self):
        if not self._multiple_select:
            rect = QRect(self._start_point, self._end_point).normalized()
            button_x = rect.x() + (rect.width() - self._translate_button.width()) / 2
            button_y = rect.y() + rect.height() + 10
            if button_y + self._translate_button.height() > self.height():
                button_y = rect.y() - self._translate_button.height() - 10
        else:
            button_w = self._translate_button.width()
            button_h = self._translate_button.height()
            button_x = (self.width() - button_w) / 2
            button_y = self.height() - button_h - 10

        self._translate_button.move(int(button_x), int(button_y))
        self._translate_button.show()

    @Slot()
    def init_translate(self):
        for i, rect in enumerate(self._selected_rects):
            screen = QGuiApplication.primaryScreen()
            screen_shot = screen.grabWindow(0, rect.x(), rect.y(), rect.width(), rect.height())
            screen_shot.save(f'./db/temp/capture/{i}.png')
        
        self._main_window._threads_ok.connect(self.show_translated)
        self._main_window.extract_capture_text()

    @Slot(dict)
    def show_translated(self, signal):
        #self._main_window._llm_thread.end_task()
        self._main_window._api_thread.end_task()
        for label in self._translated_labels:
            label.deleteLater()
        self._translated_labels.clear()
        res = signal.get('response')['translations']
        for i, text in enumerate(res):
            rect = self._selected_rects[i]
            #rect.moveTo(rect)
            label = QLabel(self)
            label.setStyleSheet('background-color: black; color:white; font-size: 18px')
            label.setWordWrap(True)
            label.setFixedWidth(rect.width())
            label.setGeometry(rect)
            label.setText(text)
            label.adjustSize()
            label.show()
            self._translated_labels.append(label)

