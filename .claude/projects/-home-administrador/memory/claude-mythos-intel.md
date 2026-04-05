# Claude Models — ESTADO REAL (5 Apr 2026)

## MODELOS DISPONIVEIS NA API (CONFIRMADO)

| Modelo | ID | Input/MTok | Output/MTok | Context | Max Output |
|--------|-----|-----------|-------------|---------|------------|
| **Opus 4.6** | claude-opus-4-6 | $5 | $25 | 1M | 128K |
| **Sonnet 4.6** | claude-sonnet-4-6 | $3 | $15 | 1M | 64K |
| **Haiku 4.5** | claude-haiku-4-5-20251001 | $1 | $5 | 200K | 64K |

### Legacy (ainda disponíveis)
- Sonnet 4.5 (claude-sonnet-4-5-20250929)
- Opus 4.5 (claude-opus-4-5-20251101)
- Opus 4.1 (claude-opus-4-1-20250805)
- Sonnet 4.0 (claude-sonnet-4-20250514)
- Opus 4.0 (claude-opus-4-20250514)
- Haiku 3 — DEPRECATED, retira 19 Apr 2026

## MYTHOS / CAPYBARA — REAL MAS NAO DISPONIVEL

- **Status**: Em teste INTERNO com early-access customers
- **Confirmado por**: Fortune leak (27 Mar 2026), ~3000 docs internos vazados
- **Tier**: Capybara (ACIMA de Opus em capacidade e custo)
- **Capacidades reportadas**: Step change em cybersecurity, code gen, reasoning
- **Release date**: NAO DEFINIDA (pode ser Oct 2026 alinhado ao IPO)
- **API access**: ZERO. Nenhum model ID publico. NAO existe na API.
- **Pricing estimado**: $10-20 input / $50-100 output per MTok
- **ACAO**: Monitorar announcements. NAO gastar tempo tentando acessar.

## OPORTUNIDADES REAIS DE ACESSO ANTECIPADO
- **HackerOne Anthropic Bug Bounty**: https://forms.gle/3ocTorSkkuvcGePn9 (até $25K/jailbreak)
- **Anthropic Fellows 2026**: Cohort May/Jul, $15.4K/mes + $15K compute
  - https://job-boards.greenhouse.io/anthropic/jobs/5023394008

## MCP mythos-edge — REALIDADE
- Localizado em: ~/israel-four/mcp/mythos_mcp_server.py
- **NAO** conecta a nenhum modelo Mythos. Usa Opus 4.6 (modelo atual desta sessao).
- security_audit e vuln_scan = prompts rodando no modelo ATUAL, nao em Mythos.
- mythos_scan = scraper que verifica site da Anthropic por novos modelos.
- **Util como**: Scanner de novidades + wrapper de audit usando modelo atual.
- **NAO é**: Acesso a Capybara/Mythos.
