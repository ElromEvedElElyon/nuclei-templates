# X/Twitter — Politica, Algoritmo e Crescimento (Pesquisa 25 Mar 2026)

## ALGORITMO X (Open Source Jan 2026 — Grok-powered)
### Formula de Engagement Score
```
Likes × 1 + Retweets × 20 + Replies × 13.5 + Profile Clicks × 12 + Link Clicks × 11 + Bookmarks × 10
```
- **Retweets valem 20x um like**
- **Replies valem 13.5x um like**
- Time decay: perde ~50% visibilidade a cada 6 horas
- **Primeiros 30 minutos sao CRITICOS** — engagement rapido = distribuicao ampla

### Premium vs Free
- Premium ($8/mo): **4-8x mais distribuicao** para mesmo conteudo
- Links externos: **30-50% penalidade** sem Premium (desde Mar 2026)
- Blue check = mais trust + prioridade em replies

## ERROR 226 (Spam Flag)
### Triggers
- IPs de datacenter (AWS, Hetzner, etc.) = flagged IMEDIATAMENTE
- Automacao (twikit, Selenium, Puppeteer)
- Timing mecanico (intervalos fixos)
- Re-login frequente via scripts
- Conteudo identico/repetido

### FIX (Sequencia Exata)
1. Login MANUAL no Chrome GUI (nao headless)
2. Scrollar feed 10-15 min, curtir 3-5 posts
3. Postar 1 tweet manualmente
4. Extrair cookies frescos (auth_token, ct0, kdt) do DevTools
5. **PARAR toda automacao por 24-72h**
6. Retomar com delays RANDOMICOS (60-180s, NAO fixo 55s)

## ERROR 344 (Daily Limit)
- Free: ~600 posts/dia (pode ser reduzido se flagged)
- Premium: ~6,000/dia
- Reset: meia-noite UTC
- MAX 50 posts por janela de 30 min

## SHADOW BAN — Tipos
1. **Search Suggestion Ban**: username nao aparece no autocomplete
2. **Search Ban**: tweets nao aparecem na busca
3. **Ghost Ban**: replies escondidas (precisa clicar "show more")
4. **For You Exclusion**: fora do feed algoritmico

### Como Verificar @opencllaw
- https://shadowban.yuzurisa.com/ (melhor tool, sem login)
- https://hisubway.online/shadowban/
- Teste manual: buscar em aba anonima

## MELHORES PRATICAS PARA ALCANCE
### Frequencia
- **Sweet spot: 3-5 tweets/dia** (individual)
- Tech/crypto: 4-6/dia
- MAX 2-3 posts por janela de 30 min
- **60+ min entre posts** para dar tempo de engagement

### Horarios (Global)
- **Melhor dia: Quarta** (depois Terca, Quinta)
- **Piores: Sabado e Sexta**
- **Melhor horario: 9AM-3PM** (timezone do usuario)
- Crypto: 7-10PM tambem funciona

### Formato (Ranking de Engagement)
1. **Video nativo** — 10x mais shares que texto
2. **Threads** — 2.4-3x mais engagement
3. **Imagens** — 2.3x mais engagement
4. **GIFs** — 55% boost
5. **Texto puro** — menor alcance mas pode viralizar
6. **Links externos** — SUPRIMIDO sem Premium

### Estrategias de Engagement
- **Responder TODA reply** (+8% engagement por post)
- **Threads para conteudo profundo** — algoritmo re-promove
- **Fazer perguntas** — replies valem 13.5x likes
- **Quote tweet seus proprios posts** para re-injetar
- **Engajar em threads de perfis grandes** ANTES de postar
- **NUNCA "post and ghost"** — ficar ativo 30-60 min apos postar

### O que MATA o Alcance
- Links externos (sem Premium)
- Hashtag stuffing (>2-3 por tweet)
- Posts identicos/repetidos
- Intervalos mecanicos fixos
- Replies spam ("great post", "dm me")
- Follow/unfollow rapido

## MULTI-ACCOUNT
### Politica Oficial: ate 10 contas por pessoa
### Regras
- Cada conta = proposito DISTINTO
- NAO interagir entre contas proprias
- NAO duplicar conteudo
- NAO manipular trending

### Operacao Segura
1. **Browser profiles separados** (Firefox Containers ou antidetect)
2. **IP separado por conta** (residential proxy ou VPN distinto)
3. **Horarios diferentes** por conta
4. **Temas diferentes** por conta
5. **NUNCA curtir/RT suas proprias contas**
6. **Emails e telefones separados** por conta

## DETECCAO DE AUTOMACAO
- IP classification (datacenter = flagged)
- Browser fingerprint (canvas, WebGL, fonts, timezone)
- Timing analysis (ML detecta ritmos nao-humanos)
- Interaction graph (cluster de contas que so interagem entre si)
- Topic velocity (1 tema com consistencia mecanica = flag)
