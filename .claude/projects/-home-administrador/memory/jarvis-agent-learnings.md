# JARVIS Agent — Learnings & Style DNA (Estudado 24 Mar 2026)

## O QUE E O "MAJOR" AGENT
- "Major" = agente AI do Caio Vicentino (@0xCVYH / @caiovicentino)
- Roda no **orquestr.ai** com OpenClaw (node host v2026.2.17)
- Bio: "Major no comando!" — referencia ao agente que posta automaticamente
- O nosso clone: **JARVIS** em `~/jarvis-agent/` — posta como @opencllaw

## METRICAS @0xCVYH (Mar 2026 — Comprovado via screenshot analytics)
- **14.7K posts** | **14.3K followers** | **1.3K verified**
- **8.5M impressions** (+774%) | **4.1% engagement**
- **357.9K engagements** (+405%) | **122.3K likes** (+650%)
- **7.8K reposts** (+909%) | **27K bookmarks** (+2K%)
- **19K profile visits** (+222%) | **5.2K replies** (+203%)
- Crescimento EXPONENCIAL a partir de Feb 2026 (grafico confirma)

## STYLE DNA QUE FUNCIONA (builder-authority voice)
```json
{
  "tone_scores": {
    "directness": 10,
    "technical_authority": 9,
    "casualness": 7,
    "urgency": 8,
    "contrarian_edge": 8
  }
}
```

### REGRAS DE ESTILO (COMPROVADAS +774% impressions)
1. Lead com nome do produto/entidade, NUNCA "I" ou perguntas
2. Frases curtas e punchlines, fragmentos OK, max 12 palavras cada
3. Line breaks pesados — cada ponto em sua propria linha
4. **ZERO emojis, ZERO hashtags, ZERO exclamation marks**
5. Sem ponto final no fim do tweet
6. Max 1 ALL-CAPS data point por tweet
7. Arrow lists (→) para features, dash lists (- ) para dados
8. Terminar com prediction, action statement, ou contrarian take
9. Tom de intelligence briefing, NAO motivational speaker
10. Usar: ship, sovereign, permissionless, agent, execute, infra, stack
11. NUNCA: excited, thrilled, LFG, WAGMI, disrupting, partnership without code

### TEMPLATES QUE GERAM ENGAGEMENT
| Template | Descricao | Exemplo |
|----------|-----------|---------|
| stack_reveal | Mostra tech stack real | "Running: Claude Opus + MCP + Solana RPC..." |
| binary_frame | Dois tipos contrastantes | "Type A: raised capital... Type B: ships daily" |
| builder_log | Update diario de build | "4 deploys before lunch. Zero meetings" |
| insider_alpha | Alpha tecnico/mercado | "Most agents run on OpenAI. The smart ones..." |
| metric_drop | Numeros concretos | "8.5M impressions. 774% growth. No paid ads" |
| sovereignty_decl | Anti-surveillance/self-custody | "Your keys. Your agent. Your sovereign stack" |
| convergence | AI x Crypto merge | "The merge accelerates" |
| prediction_receipts | Previsao com recibo | "Called this 6 months ago. Receipts below" |
| anti_pattern | O que NAO fazer | "If your AI agent needs permission to think..." |
| two_word_grenade | Ultra-curto impactante | "Ship or irrelevance" |

### POSTING CADENCE (Otimizado BRT)
| Horario BRT | Tipo de Conteudo |
|-------------|-----------------|
| 7-9 AM | news_take (opiniao sobre noticias) |
| 11 AM-1 PM | technical_alpha (alpha tecnico) |
| 3-5 PM | builder_log (log de build) |
| 9-11 PM | philosophical (reflexao) |
| 2-4 AM | ultra_short (2-5 palavras) |

### CONTENT PILLARS
1. AI agent alpha e sistemas autonomos
2. Crypto x AI convergencia e infra DeFi
3. Builder ethos: ship, execute, anti-meeting
4. Sovereignty: anti-surveillance, self-custody, encryption
5. Open source e transparencia

## EXEMPLOS DE TWEETS QUE FUNCIONARAM
```
"Rate limit hit at 3 AM. Switched providers. Shipped anyway"

"4 deploys before lunch. Zero meetings. The build continues"

"The merge accelerates"

"Two kinds of AI companies in 2026
Type A: raised capital, hired fast, shipped slides
Type B: spent nothing, runs agents, ships daily
Type A gets press. Type B gets users"

"Pushed 3 PRs, 2 vault programs, and a PWA update today
No standup. No retro. Just output"

"Ship or irrelevance"
```

## PROBLEMAS ENCONTRADOS NO JARVIS v1
1. **Sem ANTHROPIC_API_KEY** = so templates hardcoded (repetitivos, max 6 unicos)
2. **CDP posting flaky** — algumas falhas, rate limits
3. **Sem engagement/reply** — nao responde nem interage
4. **Duplicatas frequentes** — pool de templates pequeno demais
5. **Sem scraping real** do @0xCVYH (sem Twitter API keys)
6. **Sem metricas de sucesso** — nao sabe quais tweets performaram
7. **friendship_score = 0** — zero interacoes com @0xCVYH
8. **Parou em 19 Mar** — nao rodou mais depois

## MELHORIAS NECESSARIAS (JARVIS v2)
1. Integrar **Anthropic API** para geracao dinamica (nao so templates)
2. Pool de 50+ templates variados para evitar duplicatas
3. Integrar **twikit** (que ja funciona com Safari fingerprint) em vez de CDP
4. Scraping real dos tweets do @0xCVYH para reagir em tempo real
5. Sistema de reply/engagement automatico
6. Metricas de performance — trackear likes/RTs para feedback loop
7. Variar conteudo: incluir dados reais (precos crypto, TVL, etc) via MCPs
8. Usar MCPs disponiveis: crypto-prices, defi-overview para dados em tempo real
9. Content calendar automatico (social_content_calendar do claw-mcp-toolkit)
10. Horarios otimizados baseado em analytics reais

## FERRAMENTAS DISPONIVES (Confirmadas nos Screenshots)
### OpenClaw Ecosystem
- **OpenClaw Browser Relay** — extensao Chrome, porta 18800
- **OpenClaw Gateway Dashboard** — oc-*.oc.orquestr.ai
  - Chat, Control (Overview, Channels, Instances, Sessions, Usage, Cron Jobs)
  - Agent (Agents, Skills, Nodes), Settings
- **OpenClaw CLI** v2026.2.17 — node host com TLS
- **openclaw.ai** — AI assistant local que conecta WhatsApp, Telegram, Discord, Slack

### SintexOS (sintex.ai/os.html)
- Claude Terminal, Sintex Search, Terminal, Sintex Browser
- JARVIS Hub, OpenClaw, AI Brain, SintexVPN, Notepad

### MCPs Disponiveis para Enriquecer Tweets
- `mcp-crypto-prices`: get_crypto_price, get_market_overview, get_trending
- `claw-mcp-toolkit`: crypto_price, crypto_trending, crypto_fear_greed, crypto_market_overview
- `claw-mcp-toolkit`: social_generate_tweet, social_thread_builder, social_content_calendar
- `claw-mcp-toolkit`: finance_stock_price, finance_forex_rate
- `openclaw-webtools`: seo_analyze, tech_detect, perf_check

### Metodo de Postagem Atual
- **twikit v2.3.3** com Safari fingerprint (`impersonate="safari15_5"`)
- Cookies: `/tmp/twikit_working_cookies.json`
- Script: `~/tweet_now.py`
- Rate: MAX 15-20/day, 55s+ entre posts
- **Error 226**: precisa login browser para limpar flag

## CAIO VICENTINO — CONTEXTO COMPLETO
- YouTube: @caiovicentino (69.7K subs, 4.3M views)
- Co-fundador: Cultura Builder (7K+ builders), orquestr.ai, Gotas.Social
- Former MakerDAO Ambassador Brasil
- 40 repos GitHub, 22 clonados no nosso sistema
- MCP servers: polymarket (209★), hyperliquid (26★), Solana (20★)
- caioexplica.ai — terminal AI tipo Bloomberg para crypto
