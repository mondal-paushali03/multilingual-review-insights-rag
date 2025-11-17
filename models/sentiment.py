from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

class SentimentAnalyzer:
    def __init__(self, model_name):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_name)

    def classify(self, text):
        inputs = self.tokenizer(text, return_tensors="pt")
        outputs = self.model(**inputs)
        scores = torch.softmax(outputs.logits, dim=1)[0]

        labels = ["negative", "neutral", "positive"]
        return labels[scores.argmax().item()]
