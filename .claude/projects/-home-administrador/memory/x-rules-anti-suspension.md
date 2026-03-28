# Regras do X/Twitter — Anti-Suspensao (28 Mar 2026)
# LEITURA OBRIGATORIA ANTES DE QUALQUER POSTAGEM

## STATUS ATUAL
- **@opencllaw**: SUSPENSA (28 Mar 2026) — conta PERDIDA
- **@standardbitcoin**: ATIVA — usar esta conta AGORA
- **TODOS os sentinels/agents de tweet**: DESLIGADOS
- **Crontab**: Sentinels DESABILITADOS no reboot

## REGRAS ABSOLUTAS — VIOLAR = SUSPENSAO PERMANENTE

### 1. NUNCA AUTOMATIZAR ENGAJAMENTO
- **PROIBIDO**: Auto-like, auto-retweet, auto-follow, auto-unfollow
- **PROIBIDO**: Engagement pods, troca de likes, servicos de followers
- **PROIBIDO**: Qualquer script que interage com tweets de OUTROS
- **PERMITIDO**: Apenas POSTAR conteudo proprio via API/OAuth

### 2. NUNCA USAR BROWSER AUTOMATION SEM OAuth
- **PROIBIDO**: Headless Chrome, Selenium, Puppeteer logando com senha
- **PROIBIDO**: curl_cffi simulando browser (o que tweet_now.py fazia!)
- **PROIBIDO**: Roubar cookies do browser e usar em scripts
- **PERMITIDO**: Apenas apps autorizados via OAuth oficial do X
- **PERMITIDO**: API oficial do X com rate limits respeitados

### 3. NUNCA SPAM
- **PROIBIDO**: Conteudo duplicado ou substancialmente similar
- **PROIBIDO**: Mesmo tweet em multiplas contas
- **PROIBIDO**: Usar hashtags trending para manipular visibilidade
- **PROIBIDO**: Mensagens em massa (DMs, replies, mentions)
- **PROIBIDO**: Postar links repetitivos sem contexto

### 4. LIMITES DE POSTAGEM
- **MAXIMO**: 8-10 tweets/dia para conta nova/reativada
- **MAXIMO**: 15-20 tweets/dia para conta estabelecida (>6 meses)
- **INTERVALO MINIMO**: 90-180 segundos RANDOMICOS entre posts
- **NUNCA**: Intervalos fixos (55s, 60s, etc = deteccao de bot)
- **NUNCA**: Picos subitos de volume (0 tweets/dia → 15 = flag)

### 5. WARMUP OBRIGATORIO
- Conta nova/reativada: 1-3 tweets/dia na primeira semana
- Semana 2: 3-5 tweets/dia
- Semana 3: 5-8 tweets/dia
- Semana 4+: 8-15 tweets/dia MAX
- SEMPRE: Navegar no feed 5-10 min antes de postar

### 6. CONTEUDO QUE CAUSA SUSPENSAO
- Ameacas, violencia, terrorismo
- Assedio, bullying, discriminacao
- Impersonacao (usar logo/nome de outro)
- Venda de bens/servicos ilegais
- Conteudo de exploracao infantil
- Coordinated inauthentic behavior

## POR QUE @opencllaw FOI SUSPENSA

Provaveis causas (baseado na analise):
1. **Browser automation (curl_cffi + Safari fingerprint)** = NAO e OAuth
2. **Postagem automatica a cada 55-90 min 24/7** = padrao de bot
3. **62 tweets na fila com conteudo similar** = spam/repetitivo
4. **IP de datacenter/residencial fixo** = flag
5. **Zero engajamento organico** (so postava, nao interagia)
6. **Multiplos logins automaticos** por dia

## POR QUE CAIO (@0xCVYH) NAO E SUSPENSO

1. **Conteudo UNICO e substantivo** — cada tweet tem dados reais
2. **Produtos proprios geram conteudo** (gotas.social, orquestr.ai, caioexplica.ai)
3. **Engajamento REAL** — replies, bookmarks = algoritmo favorece
4. **Mix de idiomas** (56% PT, 44% EN) — nao parece bot
5. **Autoridade de builder** — share de codigo, PRs, metricas reais
6. **Nao usa browser automation** — usa ferramentas OAuth autorizadas
7. **Premium/verificado** — 4-8x mais distribuicao, mais confianca

## COMO USAR @standardbitcoin COM SEGURANCA

### Fase 1: Warmup (Dias 1-7)
- Login MANUAL no browser (Chrome/Firefox GUI)
- Navegar feed 10 min, like manual 3-5 posts relevantes
- Postar 1-2 tweets/dia MANUALMENTE
- Conteudo: dados reais (TapToons stats, nuclei PRs, builder log)
- ZERO automacao

### Fase 2: Semi-auto (Dias 8-14)
- Usar APENAS ferramentas OAuth autorizadas (Buffer, Typefully)
- 3-5 tweets/dia
- Intervalos de 3-4 horas entre posts
- Conteudo variado (nunca template)

### Fase 3: Escala (Dia 15+)
- 5-10 tweets/dia MAX
- Cada tweet UNICO com dados reais
- Interagir manualmente (reply a 2-3 pessoas/dia)
- Monitorar impressoes e engagement rate

### REGRAS DE CONTEUDO (Estilo Caio)
- ZERO emojis, ZERO hashtags, ZERO "!"
- Lead com dados/produto, nunca com "I" ou "we"
- Fragmentos curtos OK ("ship or sleep")
- Terminar com predicao, acao, ou take contrario
- Vocabulario: ship, sovereign, build, deploy, output, receipts
- PROIBIDO: excited, thrilled, LFG, WAGMI, game-changing, innovative

### 7 PILARES DE CONTEUDO
1. Data Expose [PT] — numeros reais + insight (MAIS engagement)
2. Tool Reveal [PT] — feature + "Open source." + frase filosofica
3. Builder Raw [EN] — max 15 palavras, fragmento cru
4. Ultra-Short [EN] — 2-5 palavras, lowercase, curiosidade
5. News + Take [EN/PT] — noticia + perspectiva builder
6. DeFi Analysis [PT] — tecnico com cadeia causa-efeito
7. Builder Log [PT] — metricas reais do dia + "Zero reunioes. So output."

## FERRAMENTAS SEGURAS (OAuth)
- **Buffer**: buffer.com — scheduling gratis ate 3 canais
- **Typefully**: typefully.com — drafts + scheduling
- **X API oficial**: developer.x.com (precisa aplicar para acesso)
- **NUNCA MAIS**: curl_cffi, twikit, selenium, headless chrome

## CHECKLIST ANTES DE POSTAR
- [ ] Conteudo e UNICO? (nao template)
- [ ] Tem dados reais? (numeros, links, commits)
- [ ] Nao repete tweet recente? (verificar ultimos 7 dias)
- [ ] Intervalo > 90 min do ultimo post?
- [ ] Esta dentro do limite diario? (max 10)
- [ ] Usa vocabulario on-brand? (sem emojis/hashtags)
- [ ] Ferramenta e OAuth autorizada?
