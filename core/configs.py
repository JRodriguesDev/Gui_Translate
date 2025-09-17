import json

with open('./config.json', mode='r') as f:
    langs = json.load(f)[0]['Languages']

class Languages:
    _langs = langs
    def __init__(self):
        pass
    

    @property
    def ocr_keys(self):
        all_keys = []
        for key in self._langs:
            all_keys += key['key_ocr']

        return all_keys

    @property
    def langs(self):
        return [lang['name'] for lang in self._langs]
    
    def get_keys(self, lang_selected):
        for lang in self._langs:
            if lang['name'] == lang_selected:
                return {'key_ocr': lang['key_ocr'], 'key_llm': lang['key_llm']}



