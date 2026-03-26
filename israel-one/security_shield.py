#!/usr/bin/env python3
"""
Security Shield — Real security scanning for ZION infrastructure.
Em nome do Senhor Jesus Cristo, nosso Salvador.
Replaces broken ~/security_shield.py cron target.

Usage:
    python3 security_shield.py scan    # Full scan
    python3 security_shield.py quick   # Quick port check only
"""
import os, sys, subprocess, json, stat
from datetime import datetime, timezone, timedelta
from pathlib import Path

BRT = timezone(timedelta(hours=-3))
LOG_DIR = Path.home() / ".zion" / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)
REPORT = LOG_DIR / "security_report.json"

def log(msg):
    ts = datetime.now(BRT).strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{ts}] {msg}")

def scan_ports():
    """Check for unexpected listening ports."""
    try:
        r = subprocess.run(["ss", "-tlnp"], capture_output=True, text=True, timeout=5)
        lines = [l for l in r.stdout.splitlines() if "LISTEN" in l]
        expected = {"8777", "2828"}  # dashboard, firefox marionette
        alerts = []
        for line in lines:
            port = line.split(":")[1].split()[0] if ":" in line else ""
            if port and port not in expected and int(port) > 1024:
                alerts.append(f"Unexpected port {port}: {line.strip()[:80]}")
        return {"ports": len(lines), "alerts": alerts}
    except Exception as e:
        return {"ports": -1, "alerts": [str(e)]}

def check_permissions():
    """Check critical files have safe permissions."""
    fixes = 0
    critical = [
        Path.home() / ".secrets.env",
        Path.home() / ".git-credentials",
        Path.home() / ".immunefi_creds",
        Path.home() / ".proton_creds",
        Path.home() / ".twilio_creds",
    ]
    for f in critical:
        if f.exists():
            mode = oct(f.stat().st_mode)[-3:]
            if mode != "600":
                f.chmod(0o600)
                fixes += 1
                log(f"FIXED {f.name} {mode}->600")
    # SSH keys
    ssh_dir = Path.home() / ".ssh"
    if ssh_dir.exists():
        for key in ssh_dir.glob("id_*"):
            if not key.name.endswith(".pub"):
                mode = oct(key.stat().st_mode)[-3:]
                if mode != "600":
                    key.chmod(0o600)
                    fixes += 1
    return {"fixes": fixes}

def check_processes():
    """Check for suspicious processes."""
    try:
        r = subprocess.run(["ps", "aux", "--no-headers"], capture_output=True, text=True, timeout=5)
        suspicious = []
        bad_patterns = ["miner", "xmrig", "cryptonight", "stratum", "nmap"]
        for line in r.stdout.splitlines():
            lower = line.lower()
            for pattern in bad_patterns:
                if pattern in lower:
                    suspicious.append(line.strip()[:100])
        return {"clean": len(suspicious) == 0, "suspicious": suspicious}
    except Exception as e:
        return {"clean": False, "suspicious": [str(e)]}

def check_chrome_count():
    """Warn if too many Chrome processes (OOM risk)."""
    try:
        r = subprocess.run(["pgrep", "-c", "chrome"], capture_output=True, text=True, timeout=3)
        count = int(r.stdout.strip()) if r.returncode == 0 else 0
        return {"chrome_count": count, "alert": count > 10}
    except:
        return {"chrome_count": 0, "alert": False}

def full_scan():
    log("=== Security Scan ===")
    results = {}

    results["ports"] = scan_ports()
    log(f"Port scan: {results['ports']['ports']} listening, {len(results['ports']['alerts'])} alerts")

    results["permissions"] = check_permissions()
    log(f"File permissions: {results['permissions']['fixes']} fixed")

    results["processes"] = check_processes()
    log(f"Process check: {'clean' if results['processes']['clean'] else 'SUSPICIOUS FOUND'}")

    results["chrome"] = check_chrome_count()
    if results["chrome"]["alert"]:
        log(f"WARNING: {results['chrome']['chrome_count']} Chrome processes (OOM risk)")

    results["timestamp"] = datetime.now(BRT).isoformat()
    with open(REPORT, "w") as f:
        json.dump(results, f, indent=2)
    log(f"SCAN COMPLETE — report saved")
    return results

if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "scan"
    if cmd == "scan":
        full_scan()
    elif cmd == "quick":
        r = scan_ports()
        log(f"Quick: {r['ports']} ports, {len(r['alerts'])} alerts")
    else:
        print(f"Usage: {sys.argv[0]} scan|quick")
