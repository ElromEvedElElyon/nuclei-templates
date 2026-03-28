#!/usr/bin/env python3
"""
NEHEMIAS — Security Guardian Agent
Em nome do Senhor Jesus Cristo, nosso Salvador.

Named after Nehemiah who rebuilt the walls of Jerusalem.
This agent guards against credential leaks, unauthorized access,
and ensures all sensitive data stays protected.

Usage:
    python3 nehemias_security_agent.py scan       # Full security scan
    python3 nehemias_security_agent.py guard       # Continuous guard mode (runs every 5 min)
    python3 nehemias_security_agent.py audit-git   # Audit all git repos for leaked credentials
    python3 nehemias_security_agent.py rotate      # Check which credentials need rotation
"""
import os
import sys
import json
import stat
import subprocess
import re
import time
from datetime import datetime, timezone, timedelta
from pathlib import Path

BRT = timezone(timedelta(hours=-3))
HOME = Path.home()
ZION_DIR = HOME / ".zion"
LOG_DIR = ZION_DIR / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)
REPORT_FILE = LOG_DIR / "nehemias_report.json"
ALERT_FILE = LOG_DIR / "nehemias_alerts.json"

# ============================================================
# CREDENTIAL PATTERNS TO DETECT
# ============================================================
CREDENTIAL_PATTERNS = [
    (r'ghp_[A-Za-z0-9]{36}', 'GitHub PAT (classic)'),
    (r'gho_[A-Za-z0-9]{36,}', 'GitHub OAuth Token'),
    (r'github_pat_[A-Za-z0-9_]{82}', 'GitHub PAT (fine-grained)'),
    (r'sk-[A-Za-z0-9]{48}', 'OpenAI API Key'),
    (r'sk-ant-[A-Za-z0-9-]{80,}', 'Anthropic API Key'),
    (r'AKIA[0-9A-Z]{16}', 'AWS Access Key'),
    (r'[a-zA-Z0-9]{16}:[a-zA-Z0-9]{32}', 'Potential API Key:Secret'),
    (r'xoxb-[0-9]{11,13}-[0-9]{11,13}-[a-zA-Z0-9]{24}', 'Slack Bot Token'),
    (r'AC[a-f0-9]{32}', 'Twilio Account SID'),
    (r'vrhyiymomugnqwrs', 'EXPOSED Gmail App Password'),
    (r'ImmElrom2026!Bug#99', 'EXPOSED Immunefi Password'),
    (r'HackenElrom2026!Sec#99', 'EXPOSED HackenProof Password'),
    (r'GuardElrom2026Sec#99', 'EXPOSED Guardian Password'),
    (r'haylaHorse20@@', 'EXPOSED Twitter Password'),
    (r'ProtonElrom2026@Sec99', 'EXPOSED Proton Password'),
]

# Files that MUST have 600 permissions
CRITICAL_FILES = [
    HOME / ".secrets.env",
    HOME / ".git-credentials",
    HOME / ".immunefi_creds",
    HOME / ".proton_creds",
    HOME / ".twilio_creds",
    HOME / ".config/gh/hosts.yml",
    HOME / ".claude/projects/-home-administrador/memory/credentials-secure.md",
]

# Directories that MUST have 700 permissions
CRITICAL_DIRS = [
    HOME / ".ssh",
    HOME / ".claude/secure-backup",
    HOME / ".gnupg",
]

# Patterns that should NEVER appear in git-tracked files
GIT_FORBIDDEN_PATHS = [
    ".claude/projects/",
    ".claude/secure-backup/",
    "*credentials*",
    "*secrets*",
    "*.env",
    "*_creds",
]


def log(msg, level="INFO"):
    ts = datetime.now(BRT).strftime("%Y-%m-%d %H:%M:%S")
    prefix = {"INFO": "+", "WARN": "!", "ALERT": "!!!", "FIX": "*"}
    print(f"[{ts}] [{prefix.get(level, '+')}] {msg}")


def save_report(report):
    report["timestamp"] = datetime.now(BRT).isoformat()
    with open(REPORT_FILE, "w") as f:
        json.dump(report, f, indent=2)
    os.chmod(REPORT_FILE, 0o600)


def save_alert(alert):
    alerts = []
    if ALERT_FILE.exists():
        try:
            alerts = json.loads(ALERT_FILE.read_text())
        except:
            alerts = []
    alert["timestamp"] = datetime.now(BRT).isoformat()
    alerts.append(alert)
    # Keep last 100 alerts
    alerts = alerts[-100:]
    ALERT_FILE.write_text(json.dumps(alerts, indent=2))
    os.chmod(ALERT_FILE, 0o600)


# ============================================================
# SCAN FUNCTIONS
# ============================================================

def check_file_permissions():
    """Ensure critical files have safe permissions."""
    results = {"checked": 0, "fixed": 0, "alerts": []}

    for f in CRITICAL_FILES:
        if f.exists():
            results["checked"] += 1
            mode = oct(f.stat().st_mode)[-3:]
            if mode != "600":
                os.chmod(f, 0o600)
                results["fixed"] += 1
                log(f"FIXED permissions: {f.name} ({mode} -> 600)", "FIX")

    for d in CRITICAL_DIRS:
        if d.exists():
            results["checked"] += 1
            mode = oct(d.stat().st_mode)[-3:]
            if mode != "700":
                os.chmod(d, 0o700)
                results["fixed"] += 1
                log(f"FIXED permissions: {d.name} ({mode} -> 700)", "FIX")

    return results


def check_git_tracking():
    """Ensure no sensitive files are tracked by git."""
    results = {"repos_checked": 0, "violations": []}

    # Check all git repos in home directory
    git_dirs = []
    for d in HOME.iterdir():
        if d.is_dir() and (d / ".git").exists():
            git_dirs.append(d)
    # Also check home itself
    if (HOME / ".git").exists():
        git_dirs.append(HOME)

    for repo_dir in git_dirs:
        results["repos_checked"] += 1
        try:
            r = subprocess.run(
                ["git", "ls-files", "--cached"],
                capture_output=True, text=True, timeout=10,
                cwd=str(repo_dir)
            )
            for line in r.stdout.splitlines():
                line_lower = line.lower()
                if any(p.replace("*", "") in line_lower for p in GIT_FORBIDDEN_PATHS):
                    violation = {
                        "repo": repo_dir.name,
                        "file": line,
                        "severity": "CRITICAL"
                    }
                    results["violations"].append(violation)
                    log(f"GIT VIOLATION: {repo_dir.name}/{line}", "ALERT")
        except Exception as e:
            pass

    return results


def scan_for_credentials():
    """Scan git-tracked files for credential patterns."""
    results = {"files_scanned": 0, "leaks": []}

    git_dirs = []
    for d in HOME.iterdir():
        if d.is_dir() and (d / ".git").exists():
            git_dirs.append(d)
    if (HOME / ".git").exists():
        git_dirs.append(HOME)

    for repo_dir in git_dirs:
        try:
            r = subprocess.run(
                ["git", "ls-files", "--cached"],
                capture_output=True, text=True, timeout=10,
                cwd=str(repo_dir)
            )
            for filepath in r.stdout.splitlines():
                full_path = repo_dir / filepath
                if not full_path.exists() or full_path.stat().st_size > 500000:
                    continue
                if full_path.suffix in ('.yaml', '.yml', '.md', '.json', '.py', '.js', '.sh', '.txt', '.env'):
                    results["files_scanned"] += 1
                    try:
                        content = full_path.read_text(errors='ignore')
                        for pattern, desc in CREDENTIAL_PATTERNS:
                            if re.search(pattern, content):
                                leak = {
                                    "repo": repo_dir.name,
                                    "file": filepath,
                                    "type": desc,
                                    "severity": "CRITICAL"
                                }
                                results["leaks"].append(leak)
                                log(f"CREDENTIAL LEAK: {desc} in {repo_dir.name}/{filepath}", "ALERT")
                    except:
                        pass
        except:
            pass

    return results


def check_ports():
    """Check for unexpected listening ports."""
    try:
        r = subprocess.run(["ss", "-tlnp"], capture_output=True, text=True, timeout=5)
        lines = [l for l in r.stdout.splitlines() if "LISTEN" in l]
        expected = {"8777", "2828", "9222", "9223"}  # dashboard, marionette, CDP ports
        alerts = []
        for line in lines:
            parts = line.split()
            for part in parts:
                if ":" in part:
                    port = part.rsplit(":", 1)[-1]
                    if port.isdigit() and port not in expected and int(port) > 1024:
                        alerts.append(f"Unexpected port {port}")
        return {"total_ports": len(lines), "unexpected": alerts}
    except Exception as e:
        return {"total_ports": -1, "unexpected": [str(e)]}


def check_gitignore():
    """Ensure .gitignore has all required security patterns."""
    results = {"repos_checked": 0, "missing_patterns": []}

    required_patterns = [".claude/", "*credentials*", "*.env", "*_creds", "*secrets*"]

    git_dirs = []
    for d in HOME.iterdir():
        if d.is_dir() and (d / ".git").exists():
            git_dirs.append(d)
    if (HOME / ".git").exists():
        git_dirs.append(HOME)

    for repo_dir in git_dirs:
        results["repos_checked"] += 1
        gitignore = repo_dir / ".gitignore"
        if gitignore.exists():
            content = gitignore.read_text()
            for pattern in required_patterns:
                if pattern not in content and pattern.lstrip("/") not in content:
                    results["missing_patterns"].append({
                        "repo": repo_dir.name,
                        "pattern": pattern
                    })
        else:
            results["missing_patterns"].append({
                "repo": repo_dir.name,
                "pattern": "NO .gitignore FILE!"
            })

    return results


def check_remote_exposure():
    """Check if any remote branches have .claude files."""
    results = {"remotes_checked": 0, "exposed": []}

    git_dirs = []
    if (HOME / ".git").exists():
        git_dirs.append(HOME)
    for d in HOME.iterdir():
        if d.is_dir() and (d / ".git").exists():
            git_dirs.append(d)

    for repo_dir in git_dirs[:10]:  # Limit to avoid timeout
        try:
            r = subprocess.run(
                ["git", "remote", "-v"],
                capture_output=True, text=True, timeout=5,
                cwd=str(repo_dir)
            )
            remotes = set()
            for line in r.stdout.splitlines():
                parts = line.split()
                if len(parts) >= 2 and "(fetch)" in line:
                    remotes.add(parts[0])

            for remote in remotes:
                results["remotes_checked"] += 1
                r2 = subprocess.run(
                    ["git", "ls-remote", "--heads", remote],
                    capture_output=True, text=True, timeout=15,
                    cwd=str(repo_dir)
                )
                for line in r2.stdout.splitlines():
                    sha, ref = line.split("\t")
                    branch = ref.replace("refs/heads/", "")
                    try:
                        r3 = subprocess.run(
                            ["git", "cat-file", "-e", f"{remote}/{branch}:.claude/projects/-home-administrador/memory/credentials-secure.md"],
                            capture_output=True, timeout=5,
                            cwd=str(repo_dir)
                        )
                        if r3.returncode == 0:
                            results["exposed"].append({
                                "repo": repo_dir.name,
                                "remote": remote,
                                "branch": branch,
                                "severity": "CRITICAL"
                            })
                            log(f"REMOTE EXPOSURE: {repo_dir.name}/{remote}/{branch}", "ALERT")
                    except:
                        pass
        except:
            pass

    return results


# ============================================================
# MAIN COMMANDS
# ============================================================

def full_scan():
    """Run all security checks."""
    log("NEHEMIAS Security Scan — Em nome do Senhor Jesus Cristo", "INFO")
    log("=" * 60, "INFO")

    report = {"type": "full_scan", "alerts": 0}

    # 1. File permissions
    log("Checking file permissions...", "INFO")
    perms = check_file_permissions()
    report["permissions"] = perms
    if perms["fixed"] > 0:
        report["alerts"] += perms["fixed"]

    # 2. Git tracking
    log("Checking git tracking...", "INFO")
    git = check_git_tracking()
    report["git_tracking"] = git
    report["alerts"] += len(git["violations"])

    # 3. Credential scan
    log("Scanning for credential leaks...", "INFO")
    creds = scan_for_credentials()
    report["credential_scan"] = creds
    report["alerts"] += len(creds["leaks"])

    # 4. Port check
    log("Checking ports...", "INFO")
    ports = check_ports()
    report["ports"] = ports
    report["alerts"] += len(ports["unexpected"])

    # 5. Gitignore check
    log("Checking .gitignore files...", "INFO")
    gitignore = check_gitignore()
    report["gitignore"] = gitignore
    report["alerts"] += len(gitignore["missing_patterns"])

    # Summary
    log("=" * 60, "INFO")
    log(f"SCAN COMPLETE: {report['alerts']} alerts", "ALERT" if report["alerts"] > 0 else "INFO")
    log(f"  Permissions: {perms['checked']} checked, {perms['fixed']} fixed", "INFO")
    log(f"  Git tracking: {git['repos_checked']} repos, {len(git['violations'])} violations", "INFO")
    log(f"  Credentials: {creds['files_scanned']} files, {len(creds['leaks'])} leaks", "INFO")
    log(f"  Ports: {ports['total_ports']} listening, {len(ports['unexpected'])} unexpected", "INFO")
    log(f"  Gitignore: {gitignore['repos_checked']} repos, {len(gitignore['missing_patterns'])} missing", "INFO")

    save_report(report)
    if report["alerts"] > 0:
        save_alert({"type": "scan", "alerts": report["alerts"]})

    return report


def guard_mode():
    """Continuous guard — runs checks every 5 minutes."""
    log("NEHEMIAS Guard Mode ACTIVATED", "INFO")
    log("Checking every 5 minutes. Ctrl+C to stop.", "INFO")

    while True:
        try:
            report = full_scan()
            if report["alerts"] > 0:
                log(f"GUARD ALERT: {report['alerts']} issues found!", "ALERT")
            time.sleep(300)  # 5 minutes
        except KeyboardInterrupt:
            log("Guard mode stopped.", "INFO")
            break
        except Exception as e:
            log(f"Guard error: {e}", "WARN")
            time.sleep(60)


def audit_git():
    """Audit all git repos for credential exposure on remotes."""
    log("NEHEMIAS Git Audit — Checking ALL remotes for credential exposure", "INFO")
    log("=" * 60, "INFO")

    results = check_remote_exposure()

    log(f"Checked {results['remotes_checked']} remotes", "INFO")
    if results["exposed"]:
        log(f"CRITICAL: {len(results['exposed'])} remote exposures found!", "ALERT")
        for exp in results["exposed"]:
            log(f"  {exp['repo']}/{exp['remote']}/{exp['branch']}", "ALERT")
    else:
        log("No remote credential exposure detected.", "INFO")

    save_report({"type": "git_audit", "results": results})
    return results


def check_rotation():
    """Check which credentials might need rotation."""
    log("NEHEMIAS Credential Rotation Check", "INFO")
    log("=" * 60, "INFO")

    # Check known exposed credentials
    exposed = [
        ("Gmail App Password", "vrhyiymomugnqwrs", "EXPOSED on GitHub (standardbitcoin, nuclei-templates)"),
        ("Immunefi Password", "ImmElrom2026!Bug#99", "EXPOSED on GitHub (nuclei-templates)"),
    ]

    for name, _, reason in exposed:
        log(f"ROTATE NOW: {name} — {reason}", "ALERT")

    log("", "INFO")
    log("Manual rotation required:", "INFO")
    log("  1. Gmail: myaccount.google.com/security → App passwords", "INFO")
    log("  2. Immunefi: bugs.immunefi.com → Settings → Change password", "INFO")
    log("  3. GitHub: Check if PAT was exposed", "INFO")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "scan"

    if cmd == "scan":
        full_scan()
    elif cmd == "guard":
        guard_mode()
    elif cmd == "audit-git":
        audit_git()
    elif cmd == "rotate":
        check_rotation()
    else:
        print(f"Unknown command: {cmd}")
        print("Usage: nehemias_security_agent.py [scan|guard|audit-git|rotate]")
        sys.exit(1)
