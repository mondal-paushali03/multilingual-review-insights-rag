from transformers import MarianTokenizer, MarianMTModel

class Translator:
    def __init__(self, model_name):
        self.tokenizer = MarianTokenizer.from_pretrained(model_name)
        self.model = MarianMTModel.from_pretrained(model_name)

    def to_english(self, text):
        batch = self.tokenizer.prepare_seq2seq_batch([text], return_tensors="pt")
        translated = self.model.generate(**batch)
        return self.tokenizer.decode(translated[0], skip_special_tokens=True)
