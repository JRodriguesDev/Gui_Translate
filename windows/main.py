from PySide6.QtWidgets import QMainWindow
from PySide6.QtCore import Slot, Qt, Signal
from stacks.stacks import Stacks_Widgets
from gui.tray_icon import SystemTrayIcon
from core.keyboard import KeyboardListen
from core.threads import OcrThread, ApiThread
from api.colab import ColabApi
from ia.models import EasyOcr
from core.configs import Languages
from gui.transiction import Transiction

class MainWindow(QMainWindow):
    _threads_ok = Signal(dict)

    def __init__(self):
        super().__init__()
        self._languages = Languages()
        self._key_listen = KeyboardListen()
        self._tray_icon = SystemTrayIcon(self)
        self._api_thread = ApiThread()
        self._colab_api = ColabApi()
        self._ocr = EasyOcr()
        #self._llm_translated = TranslateModel()
        #self._llm_thread = LLMThread(self._llm_translated)
        self._manager_transition = Transiction()
        self._ocr_thread = OcrThread(self._ocr)
        self._progress_bar = 0
        self._loading_widget = None
        self._previous_geometry = None
        self._current_widget = 0
        self.setWindowTitle('GUI Translator')
        self.setFixedSize(600, 450)
        self._stacks_widgets = Stacks_Widgets(self)
        self.setCentralWidget(self._stacks_widgets)
        self._stacks_widgets.setCurrentIndex(1)

        #self._manager_transition._finished.connect(self.end_transition)

    def closeEvent(self, event):
        self._current_widget = self._stacks_widgets.currentIndex()
        self.hide()
        event.ignore()
        self.window_geometry = self.geometry()
        self.show_tray_icon()

    @property
    def window_geometry(self):
        return self._previous_geometry

    @window_geometry.setter
    def window_geometry(self, value):
        self._previous_geometry = value
    
    @property
    def languages(self):
        return self._languages

    def set_loading_widget(self, widget):
        self._loading_widget = widget

    def progress_bar_max(self):
        size = [len(self._languages.ocr_keys)]
        return sum(size)
    
    def full_size(self):
        self.showMaximized()

    def active_transparency_window(self):
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)

    def deactive_transparency_window(self):
        self.setAttribute(Qt.WA_TranslucentBackground, False)
        self.setWindowFlags(Qt.Window)

    def show_tray_icon(self):
        self.hide()
        self._tray_icon.show_tray()

    def hidden_tray_icon(self):
        self.show()

    def show_window(self):
        self._key_listen.reset_stream_off()
        self._tray_icon.hidden_tray()
        self.stop_keyboard()
        self._stacks_widgets.setCurrentIndex(self._current_widget)
        self.deactive_transparency_window()
        self.show()
        self.setGeometry(self.window_geometry)
    
    @Slot()
    def swith_widget(self, i):
        self.window_geometry = self.geometry()
        self._stacks_widgets.setCurrentIndex(i)
        #old_widget = self._stacks_widgets.currentWidget()
        #new_widget = self._stacks_widgets.widget(i)
        #self._manager_transition.start_transiticion(old_widget, new_widget)

    @Slot()
    def end_transition(self):
        new_widget = self._manager_transition._new_widget
        old_widget = self._manager_transition._old_widget


        old_widget.setGraphicsEffect(None)
        new_widget.setGraphicsEffect(None)

    def switch_capture_widget(self, keys):
        self._current_widget = 2
        self._ocr.keys = keys['lang_s']
        self._colab_api.keys = keys['lang_t']
        #self._llm_translated.keys = keys['lang_t']
        self._window_geometry = self.geometry()
        self._stacks_widgets.setCurrentIndex(3)
        self.show_tray_icon()
        self._key_listen.init_capture()

    def switch_stream_widget(self, keys):
        self._current_widget = 2
        self._ocr.keys = keys['lang_s']
        self._colab_api.keys = keys['lang_t']
        #self._llm_translated.keys = keys['lang_t']
        self._window_geometry = self.geometry()
        self._stacks_widgets.setCurrentIndex(4)
        self.show_tray_icon()
        self._key_listen.init_capture()

    def capture_mode(self):
        self._key_listen.swith_mode()
        self.hidden_tray_icon()
        self.show()
        self.active_transparency_window()
        self.full_size()

    def stop_keyboard(self):
        self._key_listen.stop_hotkey()

    def install_all_models(self):
        self._ocr.all_keys = self._languages.ocr_keys
        #self._ocr._progress_model.connect(self._loading_widget.update_state)
        #self._ocr._finished_model.connect(self._loading_widget.update_progress)
        self._ocr_thread._task_end_install.connect(self.finish_install)
        self._ocr_thread.start_task_install()
        #self._llm_translated._progress.connect(self._loading_widget.update_state)
        #self._llm_translated._finished_install.connect(self._loading_widget.update_progress)
        #self._llm_thread._task_end_install.connect(self._loading_widget.finish_loading)

    def finish_install(self):
        self._ocr_thread.end_task()
        print('doownload terminado')

    def extract_capture_text(self):
        self._ocr_thread._task.connect(self.text_translate)
        self._ocr_thread.start_task_capture()

    def extract_stream_text(self):
        self._ocr_thread._task.connect(self.text_translate)
        self._ocr_thread.start_task_stream()

    @Slot(dict)
    def text_translate(self, signal):
        self._ocr_thread.end_task()
        lists = signal.get('list')
        #self._llm_translated.lists = lists
        #self._llm_thread._task.connect(self._threads_ok)
        #self._llm_thread.start_task_translate()
        #API na nuvem
        self._colab_api.lists = lists
        self._api_thread._task.connect(self._threads_ok)
        self._api_thread.start_task(self._colab_api)
