from transformers import MarianMTModel, MarianTokenizer
import torch

class TranslationService:
    def __init__(self):
        self.models = {}
        self.tokenizers = {}
        self.language_codes = {
            'hindi': 'hi',
            'tamil': 'ta',
            'telugu': 'te',
            'marathi': 'mr',
            'bengali': 'bn'
        }
        self.model_names = {
            'hindi': 'Helsinki-NLP/opus-mt-en-hi',
            'tamil': 'Helsinki-NLP/opus-mt-en-ta',
            'telugu': 'Helsinki-NLP/opus-mt-en-te',
            'marathi': 'Helsinki-NLP/opus-mt-en-mr',
            'bengali': 'Helsinki-NLP/opus-mt-en-bn'
        }

    def load_model(self, language):
        if language not in self.models:
            model_name = self.model_names[language]
            self.tokenizers[language] = MarianTokenizer.from_pretrained(model_name)
            self.models[language] = MarianMTModel.from_pretrained(model_name)

    def translate(self, text, target_language):
        try:
            self.load_model(target_language)
            tokenizer = self.tokenizers[target_language]
            model = self.models[target_language]

            inputs = tokenizer(text, return_tensors="pt", padding=True)
            with torch.no_grad():
                translated = model.generate(**inputs)
            
            translated_text = tokenizer.decode(translated[0], skip_special_tokens=True)
            return translated_text
        except Exception as e:
            print(f"Translation error: {str(e)}")
            return None

translation_service = TranslationService()