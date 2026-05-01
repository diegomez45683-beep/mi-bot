import json
import requests
from websocket import create_connection

# ==== TUS DATOS ====
API_KEY = "ptlc_EuAhetIt7WSQ9mULPuqTFgP4uSlYBKdA07CoA4XD1ZZ"
PANEL_URL = "https://kineticpanel.net/server/74f11b03/console"
SERVER_ID = "74f11b03"
DISCORD_WEBHOOK = "https://discord.com/api/webhooks/1499854152732250213/oD1Ood69RC2IDi-8fVeEUXtwQ53DRPOBDhrbK-H7LzSeF4RwtbtI5w7axcIZm8BWrYyl"
# ===================

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Accept": "Application/Application/vnd.pterodactyl.v1+json"
}

# Obtener token websocket
url = f"{PANEL_URL}/api/client/servers/{SERVER_ID}/websocket"
r = requests.get(url, headers=headers)
data = r.json()["data"]

socket_url = data["socket"]
token = data["token"]

ws = create_connection(socket_url)

# auth websocket
auth_payload = {
    "event": "auth",
    "args": [token]
}
ws.send(json.dumps(auth_payload))

print("Conectado a consola...")

while True:
    result = ws.recv()
    data = json.loads(result)

    if data.get("event") == "console output":
        texto = "".join(data["args"])

        print(texto)

        texto_lower = texto.lower()

        if any(x in texto_lower for x in ["joined", "connected", "disconnected", "left"]):
            requests.post(DISCORD_WEBHOOK, json={
                "content": f"🚛 Evento servidor:\n```{texto}```"
            })