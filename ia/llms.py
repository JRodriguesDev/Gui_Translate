from huggingface_hub import login
from PySide6.QtCore import QObject, Slot, Signal
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, BitsAndBytesConfig
import torch
import os
from dotenv import load_dotenv
from optimum.onnxruntime import ORTModelForSeq2SeqLM

load_dotenv()

login(os.getenv('HF_TOKEN'))

class TranslateModel(QObject):
    _finished_install = Signal()
    _progress = Signal(str)
    _finished_translate = Signal(dict)

    def __init__(self):
        super().__init__()
        self._lists = None
        self._key_lang = None
        self._model_id = 'google/madlad400-3b-mt'
        self._bits_config = BitsAndBytesConfig(load_in_4bit=True, 
                                        bnb_4bit_quant_type="nf4", 
                                        bnb_4bit_use_double_quant=True, 
                                        bnb_4bit_compute_dtype=torch.bfloat16, 
                                        llm_int8_threshold=6.0, 
                                        llm_int8_enable_fp32_cpu_offload=True)
        
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

    @Slot()
    def install_model(self):
        self._tokenizer = AutoTokenizer.from_pretrained(self._model_id, trust_remote_code=True, cache_dir='./db/tokenizers')
        #self._progress.emit('LLM: madlad400')
        #self._finished_install.emit()

        if torch.cuda.is_available():
            self._progress.emit(f'LLM: madlad400')
            self._model = AutoModelForSeq2SeqLM.from_pretrained(self._model_id, quantization_config=self._bits_config, trust_remote_code=True, device_map='auto', cache_dir='./db/LLMs/madlad')
            self._finished_install.emit()
        else:
            self._progress.emit(f'LLM: madlad400')
            self._model = AutoModelForSeq2SeqLM.from_pretrained(self._model_id, trust_remote_code=True, device_map='cpu', cache_dir='./db/LLMs/madlad')
            self._finished_install.emit()


    def translated(self):
        texts_tanslated = []
        rects = []
        for item in self.lists:
            prompt = f'<2{self.keys}> {item['text']}'
            input_ids = self._tokenizer(prompt, return_tensors='pt').input_ids.to(self._model.device)
            outputs = self._model.generate(input_ids, max_new_tokens=512) 
            text = self._tokenizer.decode(outputs[0], skip_special_tokens=True)
            texts_tanslated.append([text])
            rects.append(item['rect'])
        self._finished_translate.emit({'response': {'translations': texts_tanslated}, 'rects': rects})