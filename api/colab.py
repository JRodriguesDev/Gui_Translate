from PySide6.QtCore import QObject, Signal, Slot
import requests
from dotenv import load_dotenv
import os

load_dotenv()

class ColabApi(QObject):
    _url = os.getenv('NGROK_KEY')
    finished = Signal(dict)

    def __init__(self):
        super().__init__(),
        self._lists = None
        self._key_lang = None

    @property
    def lists(self):
        return self._lists
    
    @lists.setter
    def lists(self, value):
        self._lists = value

    @property
    def keys(self):
        return self._key_lang
    
    @keys.setter
    def keys(self, value):
        self._key_lang = value

    @Slot(dict)
    def translate(self):
        texts = []
        rects = []
        for item in self.lists:
            texts.append({'text': item['text'], 'lang': self.keys})
            rects.append(item['rect'])

        response = requests.post(f'{self._url}/translate', json={'items': texts})
        print(response.json())
        self.finished.emit({'response': response.json(), 'rects': rects})
