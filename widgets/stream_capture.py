from PySide6.QtWidgets import QFrame, QLabel
from PySide6.QtCore import QPoint, Slot, Qt, QRect
from PySide6.QtGui import QColor, QPainter, QGuiApplication
import time

class StreamCapture(QFrame):
    def __init__(self, main_window):
        super().__init__()
        self._main_window = main_window
        self._list_labels = []
        
        self._is_capturing = False
        self._is_drawning = False

        self._selected_rect = None
        self._selected_area = False

        self._start_point = QPoint()
        self._end_point = QPoint()

        self._main_window._key_listen._hotkey_clicked.connect(self.init_stream)
        self._main_window._key_listen._stream_clicked.connect(self.extract)
        self._main_window._key_listen._reset_clicked.connect(self.reset_area)

    @Slot()
    def init_stream(self):
        if self._is_capturing:
            self._main_window.show_tray_icon()
            self._main_window._key_listen.stop_stream()
            self._is_capturing = False
            return
        
        if not self._is_capturing:
            self._main_window.capture_mode()
            self._is_capturing = True

    @Slot()
    def reset_area(self):
        self._selected_area = False
        self._selected_rect = None
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        if not self._selected_area:
            painter.fillRect(self.rect(), QColor(0, 0, 0, 100))

            if self._is_drawning or (self._start_point != self._end_point):
                current_rect = QRect(self._start_point, self._end_point).normalized()
                painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_Clear)
                painter.fillRect(current_rect, QColor(0, 0, 0))
                painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceOver)
                painter.setPen(QColor(0, 0, 255))
                painter.drawRect(current_rect)

        if self._selected_area:
            painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_Clear)
            painter.fillRect(self.rect(), QColor(0, 0, 0))
            painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceOver)
            painter.setPen(QColor(0, 0, 255))
            painter.drawRect(self._selected_rect)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._start_point = event.position().toPoint()
            self._is_drawning = True

    def mouseMoveEvent(self, event):
        if self._is_drawning:
            self._end_point = event.position().toPoint()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._end_point = event.position().toPoint()
            self._is_drawning = False
            self._selected_rect = QRect(self._start_point, self._end_point).normalized()
            self._selected_area = True
            self._main_window._key_listen.init_stream_hotkey()
            self._main_window._key_listen.reset_stream()

            self.update()

    @Slot()
    def extract(self):
        print('foi')
        screen = QGuiApplication.primaryScreen()
        screen_shot = screen.grabWindow(0, self._selected_rect.x(), self._selected_rect.y(), self._selected_rect.width(), self._selected_rect.height())
        screen_shot.save('./db/temp/streaming/0.png')
        time.sleep(.2)
        self._main_window._threads_ok.connect(self.show_text)
        self._main_window.extract_stream_text()

    @Slot(dict)
    def show_text(self, signal):
        #self._main_window._llm_thread.end_task()
        self._main_window._api_thread.end_task()
        response = {'texts': signal.get('response')['translations'], 'rects': signal.get('rects')}
        [label.deleteLater() for label in self._list_labels]
        self._list_labels.clear()
        for i in range(len(response['texts'])):
            rect = response['rects'][i]
            rect.moveTo(self._selected_rect.x() + rect.x() -40, self._selected_rect.y() + rect.y() -40)
            label = QLabel(self)
            label.setStyleSheet('background-color: black; color: white; font-size: 18px')
            label.setWordWrap(True)
            label.setFixedWidth(rect.width())
            label.setGeometry(rect)
            label.setText(response['texts'][i])
            label.adjustSize()
            label.show()
            self._list_labels.append(label)
