from PySide6.QtWidgets import QStackedWidget
from widgets.start import StartWidget
from widgets.languages import LanguagesWidget
from widgets.capture import CaptureWidget
from widgets.stream_capture import StreamCapture
from widgets.loading import LoadingWidget

class Stacks_Widgets(QStackedWidget):
    def __init__(self, main_window):
        super().__init__()
        self.addWidget(LoadingWidget(main_window))
        self.addWidget(StartWidget(main_window))
        self.addWidget(LanguagesWidget(main_window))
        self.addWidget(CaptureWidget(main_window))
        self.addWidget(StreamCapture(main_window))

    def switch_widget(self, i):
        self.setCurrentIndex(i)