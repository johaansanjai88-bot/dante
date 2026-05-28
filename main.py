#!/usr/bin/env python3
"""
dante-monitor — Real-time Dante audio network monitor
GitHub: https://github.com/johaansa/dante-monitor
"""

import argparse
import sys
from core.discovery import DanteDiscovery
from core.monitor import DanteMonitor
from core.routing import RoutingParser
from utils.exporter import Exporter
from utils.logger import get_logger

logger = get_logger(__name__)


def parse_args():
    parser = argparse.ArgumentParser(
        description="🎛️  Dante Audio Network Monitor",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("--discover", action="store_true", help="Discover all Dante devices on network")
    parser.add_argument("--monitor", action="store_true", help="Live monitor device status (Ctrl+C to stop)")
    parser.add_argument("--routing", action="store_true", help="Display audio subscriptions/routing")
    parser.add_argument("--export", metavar="FILE", help="Export device list to CSV or JSON")
    parser.add_argument("--web", action="store_true", help="Launch web dashboard")
    parser.add_argument("--config", default="config.yaml", help="Path to config file (default: config.yaml)")
    return parser.parse_args()


def print_banner():
    print("""
╔══════════════════════════════════════════════════════╗
║         🎛️  DANTE NETWORK MONITOR  v1.0.0            ║
║              github.com/johaansa                     ║
╚══════════════════════════════════════════════════════╝
    """)


def main():
    args = parse_args()
    print_banner()

    if not any(vars(args).values()):
        print("No option selected. Use --help to see available commands.\n")
        print("Quick start:")
        print("  python main.py --discover    # Find all Dante devices")
        print("  python main.py --monitor     # Live status monitoring")
        print("  python main.py --web         # Open web dashboard")
        sys.exit(0)

    discovery = DanteDiscovery(config_path=args.config)

    if args.discover:
        logger.info("Scanning network for Dante devices...")
        devices = discovery.scan()
        if not devices:
            print("❌  No Dante devices found. Check your network/subnet in config.yaml.")
        else:
            print(f"\n✅  Found {len(devices)} device(s):\n")
            print(f"  {'Device':<25} {'IP Address':<18} {'Sample Rate':<12} {'Status'}")
            print(f"  {'-'*65}")
            for d in devices:
                status_icon = "🟢" if d["online"] else "🔴"
                print(f"  {d['name']:<25} {d['ip']:<18} {d.get('sample_rate','--'):<12} {status_icon}")

    elif args.monitor:
        monitor = DanteMonitor(config_path=args.config)
        monitor.run()  # blocking loop

    elif args.routing:
        parser = RoutingParser(config_path=args.config)
        routes = parser.get_subscriptions()
        if not routes:
            print("No active subscriptions found.")
        else:
            print(f"\n📡  Active Subscriptions ({len(routes)}):\n")
            print(f"  {'Receiver Device':<25} {'Rx Channel':<15} ← {'Transmitter':<25} {'Tx Channel'}")
            print(f"  {'-'*80}")
            for r in routes:
                print(f"  {r['rx_device']:<25} {r['rx_channel']:<15}   {r['tx_device']:<25} {r['tx_channel']}")

    elif args.export:
        devices = discovery.scan()
        exporter = Exporter()
        exporter.save(devices, args.export)
        print(f"✅  Exported {len(devices)} devices to {args.export}")

    elif args.web:
        from web.app import create_app
        app = create_app(config_path=args.config)
        print("🌐  Web dashboard running at http://localhost:5000")
        print("    Press Ctrl+C to stop.\n")
        app.run(host="0.0.0.0", port=5000, debug=False)


if __name__ == "__main__":
    main()
