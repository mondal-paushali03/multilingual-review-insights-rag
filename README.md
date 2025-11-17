# 🧠 AI Customer Feedback RAG Pipeline

<img width="250" height="350" alt="53aac6f2-8210-4443-87cd-85a77f797f1d" src="https://github.com/user-attachments/assets/539bb000-051c-4cc8-a4df-efba4cfb4c9f" />


A multilingual AI pipeline that processes customer reviews end-to-end and generates **actionable next steps** for business teams using RAG, FAISS, and automation tools.

---

## 🚀 What This Does

The system automatically:

* Translates multilingual reviews (Helsinki-NLP)
* Detects sentiment (RoBERTa)
* Classifies department (Flan-T5)
* Retrieves relevant SOPs using FAISS vector search
* Generates next actions via a lightweight LLM (Phi-3)
* Sends results to Trello, Google Sheets & email

This turns raw feedback into **structured, actionable insights**.

---

## 🧩 Core Components

* **Translation** → English normalization
* **Sentiment Analysis** → negative / neutral / positive
* **Department Classification** → Logistics, Support, Finance, etc.
* **FAISS Retrieval** → fast SOP matching
* **RAG Generator** → next step recommendation
* **Integrations** → Trello, Sheets, email

---

## 📦 Installation

```bash
pip install -r requirements.txt
```

---

## ▶️ Run the Pipeline

```bash
python main.py
```

---

## 📄 Example Output

```json
{
  "department": "Logistics",
  "sentiment": "negative",
  "next_action": "Initiate replacement and notify customer.",
  "reason": "Matched SOP for delayed and damaged deliveries.",
  "confidence": 0.89
}
```

---

## 📁 Project Structure

```
.
├── config/
├── models/
├── services/
├── data/
├── main.py
└── requirements.txt
```

---

## 🧱 Tech Stack

* SentenceTransformers
* FAISS
* Transformers (Helsinki-NLP, RoBERTa, Flan-T5, Phi-3)
* Trello API
* Google Sheets API

---

## ✨ Why This Project?

A compact demonstration of:

* Practical NLP
* Vector search (FAISS)
* RAG-style reasoning
* Workflow automation
* Real-world business use cases

---

## 👩‍💻 Author

**Paushali Mondal**

---

