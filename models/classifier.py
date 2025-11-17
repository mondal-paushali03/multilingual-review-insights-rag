from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

class DepartmentClassifier:
    def __init__(self, model_name):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

    def classify(self, text):
        prompt = f"Classify business department for: {text}"
        tokens = self.tokenizer(prompt, return_tensors="pt")
        out = self.model.generate(**tokens, max_new_tokens=20)
        return self.tokenizer.decode(out[0], skip_special_tokens=True)
