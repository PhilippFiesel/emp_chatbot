import json
import base64
from connection import Connection

UNITY_IP = "127.0.0.1"
UNITY_TX_PORT = 8820  


class UnityConversationConnector:
    def __init__(self):
        self.conn = Connection(UNITY_IP, UNITY_TX_PORT)
        self.conv_id = 0

    def send_emotion(self, emotion: str, value: float, text: str):
        pdu = {
            "type": "conversation",
            "id": self.conv_id,
            "emotion": emotion,
            "emotionValue": value,
            "text": text,
            "state": "speaking",
            "interrupt": False
        }

        self.conv_id += 1

        encoded = base64.b64encode(
            json.dumps(pdu).encode("utf-8")
        )

        self.conn.send(encoded)

        print("→ UNITY:", pdu)
    
    def send_mute(self, muted: bool):
        pdu = {
            "type": "mute",
            "muted": muted
        }

        encoded = base64.b64encode(
            json.dumps(pdu).encode("utf-8")
        )

        self.conn.send(encoded)
        print("→ UNITY MUTE:", pdu)

