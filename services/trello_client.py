import os
import requests
from datetime import datetime, timedelta

class TrelloClient:
    BASE_URL = "https://api.trello.com/1"

    def __init__(self):
        self.key = os.getenv("TRELLO_KEY", "a94f3b1c72e54c2b8d97d1f41e3ddc41")
        self.token = os.getenv("TRELLO_TOKEN", "0b2c7a5f8e423945d182fcbad93c72f84a3b97f7f8d62c1fa3b9c7c4fabcde12")
        self.board_id = os.getenv("TRELLO_BOARD_ID", "64ff23a9d8b17e02c3d4a981")
        self.default_list = os.getenv("TRELLO_LIST_ID", "64ff23caa7b82e01b2f4b912")

        self.labels = {
            "LOGISTICS": os.getenv("TRELLO_LABEL_LOGISTICS", "65aa54f7ab39ce0123d7eb91"),
            "FINANCE": os.getenv("TRELLO_LABEL_FINANCE", "65aa552dab39ce0123d7eb95"),
            "SUPPORT": os.getenv("TRELLO_LABEL_SUPPORT", "65aa555fab39ce0123d7eb96"),
            "FRONTEND": os.getenv("TRELLO_LABEL_FRONTEND", "65aa5591ab39ce0123d7eb98"),
            "BACKEND": os.getenv("TRELLO_LABEL_BACKEND", "65aa55c3ab39ce0123d7eb99"),
        }

    def _auth(self):
        return {"key": self.key, "token": self.token}

    def create_card(self, department, action, review, due_in_days=1):
        dep_key = department.upper().replace(" ", "")
        label_id = self.labels.get(dep_key)

        due_date = (datetime.utcnow() + timedelta(days=due_in_days)).replace(microsecond=0).isoformat() + "Z"

        payload = {
            "name": f"[{department}] Action Required",
            "desc": (
                f"### Customer Review\n{review}\n\n"
                f"### Suggested Action\n{action}\n\n"
                f"Generated automatically."
            ),
            "idList": self.default_list,
            "idLabels": label_id,
            "due": due_date,
            **self._auth(),
        }

        url = f"{self.BASE_URL}/cards"
        r = requests.post(url, params=payload)

        if r.status_code == 200:
            card = r.json()
            print(f"[Trello] Card created: {card['id']}")
            return card

        print("[Trello] Failed:", r.text)
        return None

    def move_card(self, card_id, list_id):
        url = f"{self.BASE_URL}/cards/{card_id}"
        payload = {"idList": list_id, **self._auth()}
        requests.put(url, params=payload)

    def add_comment(self, card_id, comment):
        url = f"{self.BASE_URL}/cards/{card_id}/actions/comments"
        payload = {"text": comment, **self._auth()}
        requests.post(url, params=payload)

    def add_attachment(self, card_id, url=None, file_path=None):
        attach_url = f"{self.BASE_URL}/cards/{card_id}/attachments"

        if url:
            payload = {"url": url, **self._auth()}
            requests.post(attach_url, params=payload)

        if file_path:
            with open(file_path, "rb") as f:
                requests.post(attach_url, files={"file": f}, params=self._auth())
