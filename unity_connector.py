import json
import base64
from connection import Connection

UNITY_IP = "127.0.0.1"
UNITY_TX_PORT = 8820  # MUSS zum alten Unity-Projekt passen

class UnityConversationConnector:
    def __init__(self):
        self.conn = Connection(UNITY_IP, UNITY_TX_PORT)
        self.conv_id = 0

    def send_emotion(self, emotion: str, value: float):
        pdu = {
            "type": "conversation",
            "id": self.conv_id,
            "emotion": emotion,
            "emotionValue": value,
            "text": "",
            "state": "speaking",
            "interrupt": False
        }

        self.conv_id += 1

        encoded = base64.b64encode(
            json.dumps(pdu).encode("utf-8")
        )

        self.conn.send(encoded)

        print("→ UNITY:", pdu)

