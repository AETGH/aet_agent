import json, time, socket, requests
from pathlib import Path

# === Konfiguration laden ===
CONFIG_FILE = Path("/app/config/config.json")
if not CONFIG_FILE.exists():
    raise FileNotFoundError(f"Config file not found: {CONFIG_FILE}")

config = json.loads(CONFIG_FILE.read_text())

CLIENT_ID = config.get("client_id", socket.gethostname())
API_URL = config["api_url"]
INTERVAL = config.get("interval", 60)

# === Hauptloop ===
while True:
    data = {
        "client_id": CLIENT_ID,
        "hostname": socket.gethostname(),
        "ip": "auto-detect",  # TODO
        "uptime": "todo",
        "modules": {"agent": True},
        "info": {"cpu": "todo"}
    }
    try:
        requests.post(API_URL, json=data, timeout=3)
        print(f"✅ Sent status for {CLIENT_ID}")
    except Exception as e:
        print(f"❌ Error: {e}")
    time.sleep(INTERVAL)
