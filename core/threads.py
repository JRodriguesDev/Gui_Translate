from PySide6.QtCore import QObject, Signal, QThread, Slot

class ApiThread(QObject):
    _task = Signal(dict)

    def __init__(self):
        super().__init__()
        self._thread = QThread()
        self._worker = None

    def start_task(self, instance):
        self._worker = instance
        self._worker.moveToThread(self._thread)
        self._thread.started.connect(self._worker.translate)
        self._worker.finished.connect(self._task)
        self._thread.start()

    def end_task(self):
        self._thread.quit()

class OcrThread(QObject):
    _task = Signal(dict)
    _task_end_install = Signal()

    def __init__(self, instance):
        super().__init__()
        self._thread = QThread()
        self._worker = instance

    def start_task_install(self):
        self._worker.moveToThread(self._thread)
        self._thread.started.connect(self._worker.install_models)
        self._worker._finished_install.connect(self._task_end_install)
        self._thread.start()

    def start_task_capture(self):
        self._worker.moveToThread(self._thread)
        self._thread.started.connect(self._worker.extract_text_capture)
        self._worker._finished_ocr.connect(self._task)
        self._thread.start()

    def start_task_stream(self):
        self._worker.moveToThread(self._thread)
        self._thread.started.connect(self._worker.extract_text_stream)
        self._worker._finished_ocr.connect(self._task)
        self._thread.start()

    def end_task(self):
        self._thread.quit()

class LLMThread(QObject):
    _task_end_install = Signal()
    _task = Signal(dict)

    def __init__(self, instance):
        super().__init__()
        self._thread = QThread()
        self._worker = instance

    @Slot()
    def start_task_translate(self):
        self._worker.moveToThread(self._thread)
        self._thread.started.connect(self._worker.translated)
        self._worker._finished_translate.connect(self._task)
        self._thread.start()

    @Slot()
    def start_task_install(self):
        self._worker.moveToThread(self._thread)
        self._thread.started.connect(self._worker.install_model)
        self._worker._finished_install.connect(self._task_end_install)
        self._thread.start()

    def end_task(self):
        self._thread.quit()

    
