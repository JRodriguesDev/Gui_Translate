import keyboard
from PySide6.QtCore import QObject, Signal, Slot

class KeyboardKey:
    def __init__(self):
        pass

class KeyboardListen(QObject):
    _hotkey_clicked = Signal()
    _stream_clicked = Signal()
    _mode_switched = Signal()
    _reset_clicked = Signal()

    def __init__(self):
        super().__init__()
        keyboard.unhook_all()
        self._mode_hotkey = False
        self._stream_hotkey = False
        self._reset_stream_hotkey = False

    @Slot()
    def hotkey_click(self):
        self._hotkey_clicked.emit()


    def init_capture(self):
        keyboard.add_hotkey('alt', self.hotkey_click)

    def swith_mode(self):
        if not self._mode_hotkey:
            keyboard.add_hotkey('m', self.switch_mode_click)
            self._mode_hotkey = True

    def switch_mode_click(self):
        self._mode_switched.emit()

    def swith_mode_off(self):
        if self._mode_hotkey:
            keyboard.remove_hotkey('m')
            self._mode_hotkey = False

    def init_stream_hotkey(self):
        if  not self._stream_hotkey:
            keyboard.add_hotkey('r', self.stream_click)
            self._stream_hotkey = True
    
    def stream_click(self):
        self._stream_clicked.emit()

    def stop_stream(self):
        if self._stream_hotkey:
            keyboard.remove_hotkey('r')
            self._stream_hotkey = False

    def reset_stream(self):
        if not self._reset_stream_hotkey:
            keyboard.add_hotkey('e', self.reset_stream_clicked)
            self._reset_stream_hotkey = True

    def reset_stream_clicked(self):
        self._reset_clicked.emit()

    def reset_stream_off(self):
        if self._reset_stream_hotkey:
            keyboard.remove_hotkey('e')
            self._reset_stream_hotkey = False

    def stop_hotkey(self):
        keyboard.unhook_all()
