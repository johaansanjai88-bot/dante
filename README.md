# 🎛️ dante-monitor

> Real-time Dante audio network monitor — discover devices, view subscriptions, and track channel levels from the command line or web UI.

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=flat)
![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=flat)

---

## 📸 Preview

```
╔══════════════════════════════════════════════════════╗
║           DANTE NETWORK MONITOR — johaansa           ║
╠══════════════════════════════════════════════════════╣
║  Device             IP Address       Status          ║
║  ─────────────────────────────────────────────────  ║
║  Yamaha-QL5         192.168.1.10     🟢 Online       ║
║  AVIO-Dante-IN      192.168.1.21     🟢 Online       ║
║  PowerCore-01       192.168.1.35     🟡 Latency      ║
║  StageTec-A         192.168.1.44     🔴 Offline      ║
╚══════════════════════════════════════════════════════╝
```

---

## ✨ Features

- 🔍 **Auto-discover** all Dante devices on your network via mDNS
- 📡 **Live device status** — online, offline, latency warnings
- 🔗 **View audio subscriptions** — who is receiving from whom
- 📊 **Channel-level monitoring** via Dante Controller API (optional)
- 🌐 **Web dashboard** — browser-based UI for non-technical operators
- 💾 **Export** device list and routing map to JSON/CSV
- 🔔 **Alerts** — get notified when a device drops off the network

---

## 🧰 Requirements

- Python 3.10+
- A network with Dante-enabled devices
- Dante Controller installed (optional, for level metering)
- Packages: see `requirements.txt`

---

## ⚙️ Setup

```bash
# 1. Clone the repo
git clone https://github.com/johaansa/dante-monitor.git
cd dante-monitor

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate       # Mac/Linux
venv\Scripts\activate          # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure your network
cp config.example.yaml config.yaml
nano config.yaml               # Set your subnet, alerts, etc.

# 5. Run the monitor
python main.py
```

---

## 🚀 Usage

### CLI Mode
```bash
# Discover devices on network
python main.py --discover

# Watch live device status
python main.py --monitor

# Export device list to CSV
python main.py --export devices.csv

# Show routing/subscriptions
python main.py --routing
```

### Web Dashboard
```bash
python main.py --web
# Open http://localhost:5000 in your browser
```

---

## 📁 Project Structure

```
dante-monitor/
├── main.py               # Entry point
├── config.yaml           # Your local config (gitignored)
├── config.example.yaml   # Template config
├── requirements.txt      # Python dependencies
├── .gitignore
├── README.md
│
├── core/
│   ├── discovery.py      # mDNS device discovery
│   ├── monitor.py        # Polling & status tracking
│   ├── routing.py        # Subscription/routing parser
│   └── alerts.py         # Alert logic
│
├── web/
│   ├── app.py            # Flask web server
│   ├── templates/
│   │   └── dashboard.html
│   └── static/
│       └── style.css
│
└── utils/
    ├── exporter.py       # CSV/JSON export
    └── logger.py         # Logging helper
```

---

## 🔧 Configuration (`config.yaml`)

```yaml
network:
  subnet: "192.168.1.0/24"
  poll_interval: 5          # seconds between polls

alerts:
  enabled: true
  offline_threshold: 10     # seconds before marking offline
  email: ""                 # optional: your@email.com

web:
  host: "0.0.0.0"
  port: 5000
```

---

## 🗺️ Roadmap

- [ ] SNMP integration for Dante-enabled switches
- [ ] Latency histogram per device
- [ ] Slack/webhook alert integration
- [ ] Multi-subnet support
- [ ] Dark mode web UI

---

## 🤝 Contributing

Pull requests are welcome! Please open an issue first to discuss what you'd like to change.

---

## 📄 License

MIT © [johaansa](https://github.com/johaansa)
