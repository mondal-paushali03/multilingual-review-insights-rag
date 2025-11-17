import json, re, numpy as np
from transformers import pipeline

class ActionGenerator:
    def __init__(self, model_name):
        self.pipe = pipeline(
            "text-generation",
            model=model_name,
            tokenizer=model_name,
            device_map="auto",
            max_new_tokens=256,
            temperature=0.2,
        )

    def generate(self, review, sentiment, department, sop_context):
        prompt = f"""
SOP CONTEXT:
{sop_context}

REVIEW: {review}
SENTIMENT: {sentiment}
DEPARTMENT: {department}

Generate JSON with fields:
department, next_action, reason_summary, confidence
"""

        result = self.pipe(prompt)[0]["generated_text"]

        match = re.search(r"\{.*\}", result, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(0))
            except:
                pass

        return {
            "department": department,
            "next_action": "Follow SOP to resolve issue.",
            "confidence": 0.50,
            "reason_summary": "Generated fallback due to parsing error."
        }
