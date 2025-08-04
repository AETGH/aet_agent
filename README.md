# aet_agent – Der Agent, der nur einem dient 🤖  
*The humble servant of the aet_dashboard*

---

## 🇩🇪 Deutsch

**aet-agent** ist ein kleiner, Docker-fähiger Python-Client, der regelmäßig Statusdaten an den [`aet_dashboard`](https://github.com/AETGH/aet_dashboard) sendet.

Er läuft auf entfernten Systemen (z. B. Raspberry Pi, Server, VMs) und übermittelt:

- 🖥️ Hostname & Client-ID
- 🌐 IP-Adresse & Uptime
- ⚙️ Aktive Module
- 📊 Systeminformationen

> Seine Mission:  
> **Berichten. Lauschen. Gehorchen.**

Er führt über das Dashboard auf Wunsch Befehle aus wie:
- 🔁 Update
- 🔄 Neustart
- 📤 Logs senden

### 🔧 Konfiguration

Die Datei `config/config.json` enthält die Steuerdaten:

``` json
{
  "client_id": "pi-backup",
  "api_url": "http://dashboard.local:7080/api/status",
  "interval": 60
}
```


🇬🇧 English
aet-agent is a lightweight Docker-based Python client that regularly reports status to the aet-dashboard.

It runs on remote systems (e.g. Raspberry Pi, servers, VMs) and transmits:

🖥️ Hostname & client ID
🌐 IP address & uptime
⚙️ Active modules
📊 System info

Its mission:
Report. Listen. Obey.
It can also execute remote commands via the dashboard such as:

🔁 Update
🔄 Reboot
📤 Send logs
🔧 Configuration
All settings are provided via config/config.json:

``` json
{
  "client_id": "pi-backup",
  "api_url": "http://dashboard.local:7080/api/status",
  "interval": 60
}
```

🐳 Verwendung / Usage
🔨 Build
bash
Kopieren
Bearbeiten
docker build -t aet-agent .
🚀 Start
``` bash
docker run -d \
  -v $(pwd)/config:/app/config \
  --restart unless-stopped \
  --name aet_agent \
  aet_agent
```
🔁 Update
``` bash
docker pull AETGH/aet_agent
docker stop aet_agent
docker rm aet_agent
docker run -d ...
```

Made with ☕, 🐧 and a little bit of 🧠 by [-@-].
