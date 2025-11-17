from models.translator import Translator
from models.sentiment import SentimentAnalyzer
from models.classifier import DepartmentClassifier
from models.embedding_store import EmbeddingStore
from services.sop_retriever import SOPRetriever
from models.rag_generator import ActionGenerator

from services.google_sheets import GoogleSheetsClient
from services.trello_client import TrelloClient
from services.email_notifier import EmailNotifier

from config.settings import *

def process_review(review_text):
    translator = Translator(TRANSLATION_MODEL)
    sentiment_model = SentimentAnalyzer(SENTIMENT_MODEL)
    dept_classifier = DepartmentClassifier(CLASSIFICATION_MODEL)

    store = EmbeddingStore()
    retriever = SOPRetriever(store)
    rag = ActionGenerator(RAG_LLM)

    sheets = GoogleSheetsClient()
    trello = TrelloClient()
    email = EmailNotifier()

    # Step 1 — Translate
    text_en = translator.to_english(review_text)

    # Step 2 — Sentiment
    sentiment = sentiment_model.classify(text_en)

    # Step 3 — Department Classification
    department = dept_classifier.classify(text_en)

    # Step 4 — RAG Retrieval
    top_sops = retriever.retrieve(text_en, top_k=3)
    sop_context = "\n".join([f"{s['department']}: {s['action']} (Score: {s['score']:.2f})" for s in top_sops])

    # Step 5 — Generate Action
    action_json = rag.generate(text_en, sentiment, department, sop_context)

    # Step 6 — Push to Sheets, Trello & Email
    sheets.push(action_json)
    trello.create_card(department, action_json["next_action"], review_text)
    email.notify(department, action_json["next_action"])

    return action_json


if __name__ == "__main__":
    sample = "मेरी डिलीवरी 5 दिन लेट थी और पैकेज डैमेज था।"
    print(process_review(sample))
