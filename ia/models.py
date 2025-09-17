from PIL import Image
from PySide6.QtCore import QRect, Slot, Signal, QObject
import easyocr
import os

class EasyOcr(QObject):
    _finished_ocr = Signal(dict)
    _finished_install = Signal()
    _progress_model = Signal(str)
    _finished_model = Signal()

    def __init__(self):
        super().__init__()
        self._widget = None
        self._ocr = easyocr
        self._keys_lang = None
        self._all_keys = None

    @property
    def all_keys(self):
        return self._all_keys
    
    @all_keys.setter
    def all_keys(self, value):
        self._all_keys = value

    @property
    def keys(self):
        return self._keys_lang
    
    @keys.setter
    def keys(self, value):
        self._keys_lang = value

    @Slot()
    def install_models(self):
        for key in self.all_keys:
            #self._progress_model.emit(f'Ocr Model: {key}')
            self._ocr.Reader([key], model_storage_directory='./db/models/EasyOcr', download_enabled=True)
            #self._finished_model.emit()
            
        #self._finished_install.emit()

    def extract_text_capture(self):
        json_list = []
        reader = self._ocr.Reader(self.keys, model_storage_directory='./db/models/EasyOcr', download_enabled=True)
        print('aqui?')
        for i, img in enumerate(os.listdir('./db/temp/capture')):
            text = reader.readtext(f'./db/temp/capture/{img}', detail=0, paragraph=True)
            json_list.append({'text': str(text).replace('[', '').replace(']', '').replace(',', ''), 'rect': ''})
        self._finished_ocr.emit({'list': json_list})

    def extract_text_stream(self):
        json_list = []
        reader = self._ocr.Reader(self.keys, model_storage_directory='./db/models/EasyOcr', download_enabled=True)
        texts = reader.readtext('./db/temp/streaming/0.png', detail=1, paragraph=True)     
        for (bbox, text) in texts:
            x_min, y_min = int(bbox[0][0]), int(bbox[0][1])
            x_max, y_max = int(bbox[2][0]), int(bbox[2][1])
            json_list.append({'text': text, 'rect': QRect(x_min, y_min, x_max - x_min, y_max - y_min)})

        self._finished_ocr.emit({'list': json_list})


