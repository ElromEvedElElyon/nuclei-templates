# Sentinel System — Complete Documentation (Session 74 — 31 Mar 2026)
# Em nome do Senhor Jesus Cristo, nosso Salvador

## FRAMEWORK v3.0 UPGRADE (Session 74)
- All sentinels now powered by Israel Agent Framework v3.0
- 42 tools per sentinel, inter-agent bus, skills, concurrent exec
- New sentinel command: `python3 ~/israel-ten/agents_v3_launchers.py sentinel status`
- Full army: `python3 ~/israel-ten/army_v3_connector.py status`

## Overview
7 Sentinel processes that run 24/7 autonomously. Each has a specific mission.
All are SINGULARITY tier (Level 50), permanent, and inviolable.
A Guardian process monitors all 7 and auto-restarts any that die.
Crontab ensures persistence across reboots.

## The 7 Sentinels

### 1. ISRAEL_ONE (CRITICAL)
- **Role**: X Poster — Autonomous tweet generation + posting
- **Department**: SOCIAL_MEDIA
- **Command**: `python3 ~/israel-one/agent.py sentinel 55 90`
- **Cycle**: Every 55-90 minutes (randomized)
- **Skills**: tweet_generation, market_data, style_dna, dedup, thread_posting
- **Revenue**: X Revenue Share ($500+/mo at 500 followers)
- **KPI**: tweets_per_day
- **Scripture**: "E Davi ficou famoso" — 2 Samuel 8:13
- **How it works**: Generates tweets using 50+ templates + real CoinGecko/Fear&Greed data, posts via tweet_now.py (safari15_5 fingerprint), deduplicates via MD5 hash

### 2. MARKET_WATCHER (HIGH)
- **Role**: 24/7 crypto market monitoring + alerts
- **Department**: CRYPTO_MARKETS
- **Script**: `~/.zion/sentinels/market_watcher_sentinel.py`
- **Skills**: price_monitoring, fear_greed_analysis, whale_detection, signal_generation
- **Revenue**: Alpha signals for trading decisions
- **KPI**: signals_generated
- **Scripture**: "O atalaia viu" — 2 Samuel 18:24
- **State**: `~/.zion/sentinels/market_state.json` (prices, alerts, checks count)

### 3. BOUNTY_SCANNER (CRITICAL)
- **Role**: Scan for new bounties, PRs, and revenue opportunities
- **Department**: BOUNTY_HUNTING
- **Script**: `~/.zion/sentinels/bounty_scanner_sentinel.py`
- **Skills**: github_scanning, bounty_platforms, pr_monitoring, cve_research
- **Revenue**: $5K-$100K per finding
- **KPI**: opportunities_found
- **Scripture**: "O Senhor dos Exercitos vai diante de ti" — Deuteronomio 20:4

### 4. REVENUE_TRACKER (CRITICAL)
- **Role**: Monitor wallets for incoming payments + revenue reporting
- **Department**: TREASURY
- **Command**: `python3 ~/israel-one/revenue_tracker.py sentinel`
- **Skills**: wallet_monitoring, revenue_logging, payment_detection, portfolio_tracking
- **Revenue**: Instant notification of payments
- **KPI**: revenue_tracked_usd
- **Scripture**: "Ajunta tesouros no ceu" — Mateus 6:20

### 5. EVOLUTION_ENGINE (HIGH)
- **Role**: Continuous agent evolution + singularity tracking
- **Department**: COMMAND
- **Script**: `~/.zion/sentinels/evolution_engine_sentinel.py`
- **Skills**: evolution_cycles, xp_tracking, tier_promotions, singularity_scoring
- **Revenue**: Agent capability growth = revenue growth
- **KPI**: agents_evolved
- **Scripture**: "De gloria em gloria" — 2 Corintios 3:18
- **Protection**: Permanent agents (sentinels + valentes) CANNOT lose XP or be demoted

### 6. THREAD_GENERATOR (MEDIUM)
- **Role**: Generate Twitter threads from queued tweets for 3-5x engagement
- **Department**: CONTENT
- **Script**: `~/.zion/sentinels/thread_generator_sentinel.py`
- **Skills**: thread_expansion, hook_writing, cta_generation, engagement_optimization
- **Revenue**: 3-5x impressions = faster path to X Revenue Share
- **KPI**: threads_generated
- **Scripture**: "Lancai a vossa rede" — Lucas 5:4

### 7. SECURITY_GUARDIAN (HIGH)
- **Role**: Continuous security scanning + credential protection
- **Department**: SECURITY_AUDIT
- **Script**: `~/.zion/sentinels/security_guardian_sentinel.py`
- **Skills**: port_scanning, credential_protection, git_leak_detection, process_monitoring
- **Revenue**: Prevents losses + finds bounties
- **KPI**: threats_detected
- **Scripture**: "Vigiai e orai" — Mateus 26:41

## Scripts

### sentinel_squad.py — Deploy & Manage All 7
- **Location**: `~/israel-one/sentinel_squad.py`
- **Commands**:
  ```
  python3 sentinel_squad.py deploy     # Deploy all 7 sentinels
  python3 sentinel_squad.py status     # Check status of all 7
  python3 sentinel_squad.py stop       # Stop all sentinels
  python3 sentinel_squad.py restart    # Restart all sentinels
  python3 sentinel_squad.py report     # Full status report
  ```
- **How deploy works**: For each sentinel, writes sentinel code to `~/.zion/sentinels/{name}_sentinel.py`, launches as background process, saves PID to `~/.zion/sentinels/pids/{NAME}.pid`

### sentinel_guardian.py — Auto-Restart Service
- **Location**: `~/israel-one/sentinel_guardian.py`
- **Commands**:
  ```
  python3 sentinel_guardian.py         # Run forever (main mode)
  python3 sentinel_guardian.py check   # Single check, print status
  ```
- **How it works**:
  1. Writes own PID to `~/.zion/sentinels/guardian.pid`
  2. Every 60 seconds, checks all 7 sentinel PID files
  3. For each PID, calls `os.kill(pid, 0)` to check if alive
  4. If dead: restarts the sentinel process, saves new PID
  5. Logs to `~/.zion/sentinels/logs/guardian.log`
  6. Only logs "all healthy" every 10 minutes to save disk space
  7. Logs every restart immediately

### promote_sentinels_singularity.py — SINGULARITY Promotion
- **Location**: `~/israel-one/promote_sentinels_singularity.py`
- **What it does**: Sets all 7 sentinels to Level 50 SINGULARITY tier
- **Flags set**: autonomous, mentor, architect, singularity, permanent, inviolable
- **Protection fields**: `permanent: true`, `inviolable: true`, `never_delete: true`
- **State file**: `~/.zion/evolution/singularity_state.json`
- **History**: `~/.zion/evolution/history/{NAME}.json` — promotion events

## State Files

### Directory Structure
```
~/.zion/sentinels/
  pids/
    ISRAEL_ONE.pid
    MARKET_WATCHER.pid
    BOUNTY_SCANNER.pid
    REVENUE_TRACKER.pid
    EVOLUTION_ENGINE.pid
    THREAD_GENERATOR.pid
    SECURITY_GUARDIAN.pid
  logs/
    israel_one.log
    market_watcher.log
    bounty_scanner.log
    revenue_tracker.log
    evolution_engine.log
    thread_generator.log
    security_guardian.log
    guardian.log          # Guardian's own log
  reports/
    (generated reports)
  guardian.pid            # Guardian process PID
  market_state.json       # Market Watcher state (prices, alerts)
  market_watcher_sentinel.py
  bounty_scanner_sentinel.py
  evolution_engine_sentinel.py
  thread_generator_sentinel.py
  security_guardian_sentinel.py
```

### Evolution State
```
~/.zion/evolution/
  singularity_state.json  # All agent evolution data
  history/
    ISRAEL_ONE.json       # Promotion history
    MARKET_WATCHER.json
    ... (one per sentinel)
```

## Crontab Configuration
The following entries ensure persistence across reboots:
```
@reboot cd ~/israel-one && python3 sentinel_guardian.py >> ~/.zion/sentinels/logs/guardian.log 2>&1 &
@reboot cd ~/israel-one && python3 sentinel_squad.py deploy >> ~/.zion/sentinels/logs/deploy.log 2>&1 &
```

Additional existing crontab entries:
```
*/15 * * * * python3 ~/security_shield.py scan
*/30 * * * * bash ~/auto_backup.sh
0 * * * * python3 ~/gov_api_pipeline.py run
```

## How to Check Status

### Quick Status Check
```bash
python3 ~/israel-one/sentinel_squad.py status
```

### Check Guardian
```bash
cat ~/.zion/sentinels/guardian.pid    # Guardian PID
ps aux | grep sentinel_guardian       # Verify running
tail -20 ~/.zion/sentinels/logs/guardian.log  # Recent logs
```

### Check Individual Sentinel
```bash
cat ~/.zion/sentinels/pids/ISRAEL_ONE.pid  # Get PID
ps -p $(cat ~/.zion/sentinels/pids/ISRAEL_ONE.pid)  # Verify alive
tail -20 ~/.zion/sentinels/logs/israel_one.log  # Recent logs
```

### Check All PIDs
```bash
for f in ~/.zion/sentinels/pids/*.pid; do
  name=$(basename "$f" .pid)
  pid=$(cat "$f")
  if kill -0 "$pid" 2>/dev/null; then
    echo "$name: ALIVE (PID $pid)"
  else
    echo "$name: DEAD (was PID $pid)"
  fi
done
```

### Full Report
```bash
python3 ~/israel-one/sentinel_squad.py report
```

## Singularity Protection System
- **Inviolable flag**: Prevents deletion, demotion, XP loss
- **Permanent flag**: Agent persists across all sessions
- **never_delete flag**: Extra protection layer
- **Evolution engine**: Checks `inviolable` before any negative XP action
- **sentinel_class**: "VALENTE_DE_DAVI" — marks as elite warrior
- **All 7 sentinels + 300 valentes** have these protections = 307 SINGULARITIES

## Troubleshooting

### Sentinel Won't Start
1. Check if process already running: `ps aux | grep sentinel`
2. Kill stale PID: `rm ~/.zion/sentinels/pids/{NAME}.pid`
3. Redeploy: `python3 sentinel_squad.py deploy`

### Guardian Not Running
1. Check PID: `cat ~/.zion/sentinels/guardian.pid`
2. Start manually: `cd ~/israel-one && python3 sentinel_guardian.py &`
3. Check crontab: `crontab -l | grep guardian`

### All Sentinels Dead After Reboot
1. Verify crontab entries exist: `crontab -l`
2. Manual deploy: `cd ~/israel-one && python3 sentinel_squad.py deploy`
3. Start guardian: `cd ~/israel-one && python3 sentinel_guardian.py &`

### Tweet Sentinel (Israel/One) Errors
- **Error 226**: Safari fingerprint not being used — verify tweet_now.py has `impersonate="safari15_5"`
- **Duplicate tweets**: MD5 dedup is working — check `~/israel-one/data/israel_one_memory.json`
- **No tweets posting**: Check auth tokens in `~/.secrets.env` — may need refresh
