# === agent.py ===
import json, time, socket, requests, subprocess, sys, platform
from pathlib import Path
from datetime import datetime

CONFIG_FILE = Path("config/config.json")
COMMANDS_URL = None

# === Konfiguration laden === 
if not CONFIG_FILE.exists():
    raise FileNotFoundError("❌ config/config.json fehlt!")

with CONFIG_FILE.open() as f:
    config = json.load(f)

CLIENT_ID = config.get("client_id", socket.gethostname())
API_URL = config.get("api_url")
INTERVAL = config.get("interval", 60)
COMMANDS_URL = API_URL.replace("/status", "/commands")

# === Hilfsfunktionen ===
def send_status():
    data = {
        "client_id": CLIENT_ID,
        "hostname": socket.gethostname(),
        "ip": get_ip(),
        "uptime": get_uptime(),
        "modules": detect_modules(),
        "info": get_sysinfo()
    }
    try:
        r = requests.post(API_URL, json=data, timeout=5)
        print(f"[INFO] Status gesendet ({r.status_code})")
    except Exception as e:
        print(f"[ERROR] Status senden fehlgeschlagen: {e}")

def get_commands():
    try:
        r = requests.get(COMMANDS_URL, params={"client_id": CLIENT_ID}, timeout=5)
        return r.json().get("commands", [])
    except Exception as e:
        print(f"[ERROR] Commands abrufen fehlgeschlagen: {e}")
        return []

def handle_command(cmd):
    name = cmd.get("cmd")
    args = cmd.get("args")
    print(f"[CMD] Empfangen: {name} ({args})")
    if name == "reboot":
        subprocess.run(["sudo", "reboot"])
    elif name == "update":
        subprocess.run(["sudo", "apt", "update"])
        subprocess.run(["sudo", "apt", "upgrade", "-y"])
    elif name == "install_kits":
        return install_kits(args)
    else:
        print(f"[WARN] Unbekannter Befehl: {name}")

def install_kits(repo_url):
    print("[INFO] kITs-Installation wird gestartet ...")
    kits_path = Path("/opt/kITs")
    if not kits_path.exists():
        subprocess.run(["git", "clone", repo_url, str(kits_path)])
        subprocess.run(["pip3", "install", "-r", f"{kits_path}/requirements.txt"])
        setup_systemd_service()
        return "✅ kITs installiert"
    else:
        subprocess.run(["git", "-C", str(kits_path), "pull"])
        subprocess.run(["systemctl", "restart", "kits.service"])
        return "🔁 kITs aktualisiert"

def setup_systemd_service():
    print("[INFO] systemd-Dienst für kITs wird erstellt ...")
    service = f"""
[Unit]
Description=kITs System
After=network.target

[Service]
ExecStart=/usr/bin/python3 /opt/kITs/kits_main.py
WorkingDirectory=/opt/kITs
Restart=always

[Install]
WantedBy=multi-user.target
"""
    Path("/etc/systemd/system/kits.service").write_text(service)
    subprocess.run(["systemctl", "daemon-reexec"])
    subprocess.run(["systemctl", "enable", "--now", "kits.service"])

# === Infos erfassen ===
def get_ip():
    try:
        result = subprocess.run(["ip", "route", "get", "1.1.1.1"], capture_output=True, text=True)
        return result.stdout.split("src")[-1].split()[0].strip()
    except:
        return "unknown"

def get_uptime():
    try:
        with open("/proc/uptime") as f:
            seconds = float(f.readline().split()[0])
            return f"{int(seconds // 3600)}h {(int(seconds) % 3600) // 60}min"
    except:
        return "unknown"

def detect_modules():
    mods = {}
    if Path("/opt/kITs").exists():
        mods["kits"] = True
    return mods

def get_update_status():
    try:
        result = subprocess.run(["apt", "list", "--upgradeable"], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True, timeout=10)
        lines = result.stdout.splitlines()
        count = len([l for l in lines if "/" in l and "Listing..." not in l])
        return f"{count} Paket(e) können aktualisiert werden" if count else "System ist aktuell"
    except Exception as e:
        return f"Fehler: {e}"

def get_sysinfo():
    return {
        "os": platform.platform(),
        "kernel": platform.release(),
        "python": f"{sys.version_info.major}.{sys.version_info.minor}",
        "ip": get_ip(),
        "update_status": get_update_status(),
        "time": datetime.now().isoformat()
    }

# === Hauptloop ===
print(f"🛰️  Agent gestartet als {CLIENT_ID}")
while True:
    send_status()
    commands = get_commands()
    for cmd in commands:
        handle_command(cmd)
    time.sleep(INTERVAL)
