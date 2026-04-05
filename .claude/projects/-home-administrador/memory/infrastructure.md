# Infrastructure — External Compute (Zero Cost, No Credit Card)

## ARCHITECTURE: i3 = Terminal Only, Compute = External

```
LOCAL (i3 3.3GB) ─── Terminal de comando apenas
  │
  ├── GitHub Actions (PUBLIC) ──── AGENTE PRIMARIO
  │   7GB RAM, unlimited mins, cron 5min
  │   Bounty scan, PR monitor, code analysis
  │
  ├── Hugging Face Space (Docker) ── AGENTE PERSISTENTE
  │   2 CPU, 16GB RAM, 48h sleep (UptimeRobot)
  │   Dashboard, API, singularity engine
  │
  ├── Render.com (Free) ──────── WEBHOOK + DASHBOARD
  │   512MB RAM, 750hrs/mo, 15min sleep
  │   Status page, webhook receiver
  │
  ├── Lightning.ai Studio ─────── DEV ENVIRONMENT
  │   4 CPUs, 24/7, full Linux
  │   Development, testing, interactive
  │
  ├── Google Cloud Shell ──────── HEAVY ONE-OFF
  │   60hrs/week, 4GB RAM, 5GB persistent
  │
  ├── Kaggle Notebooks ────────── GPU COMPUTE
  │   30hrs/week P100 GPU, background OK
  │
  └── Google Colab ────────────── BATCH PROCESSING
      12hr sessions, 12GB RAM, T4 GPU
```

## PRIORITY ORDER (Setup)
1. **GitHub Actions** — FIRST (already have account, just create workflows)
2. **Hugging Face Space** — SECOND (16GB RAM, free Docker)
3. **Lightning.ai** — THIRD (4 CPU 24/7 terminal)
4. **Render.com** — FOURTH (webhook receiver)
5. **Oracle Cloud** — ENDGAME (need debit card: Nubank/Inter/C6 virtual)

## ORACLE CLOUD — THE ENDGAME
- 4 ARM CPUs + 24GB RAM + 200GB disk — FOREVER FREE
- Needs Visa/MasterCard debit card ($1-3 hold, refunded)
- Brazilian banks with FREE instant virtual debit: Nubank, Inter, C6, Mercado Pago
- If user gets ANY of these, Oracle replaces ALL other services

## GITHUB ACTIONS AGENT SETUP
- Repo: capybara-agent-cloud (PUBLIC)
- Workflows:
  - bounty-scanner.yml (cron */30, scan GitHub bounties via REST API)
  - pr-monitor.yml (cron */60, check all PRs status)
  - singularity-cycle.yml (cron */15, full execution cycle)
  - revenue-dashboard.yml (daily, generate revenue report)
- State persistence: Commit results to repo data/ dir or use HF datasets

## HUGGING FACE SPACE
- Type: Docker Space
- Content: Singularity Engine + FastAPI dashboard
- Endpoints: /health, /status, /scan, /evolve
- Keep-alive: UptimeRobot (free, 50 monitors, 5min interval)
- State: Save to HF Dataset repo (free, unlimited public)

## TOTAL FREE RESOURCES
| Resource | Source | Amount |
|----------|--------|--------|
| CPU 24/7 | Lightning.ai | 4 CPUs |
| CPU scheduled | GitHub Actions | Unlimited (public) |
| RAM web | Hugging Face | 16 GB |
| RAM web | Render | 512 MB |
| GPU | Kaggle | 30 hrs/week |
| GPU | Colab | 12 hrs/session |
| Shell | Cloud Shell | 60 hrs/week |
| Monitoring | UptimeRobot | 50 monitors free |
