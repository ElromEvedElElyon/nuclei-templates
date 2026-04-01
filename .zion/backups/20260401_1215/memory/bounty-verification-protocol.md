# Protocolo de Verificação de Bounties — OURO NO COFRE
# Em nome do Senhor Jesus Cristo
# Session 42 — 27 Mar 2026
# REGRA ABSOLUTA: ZERO TRABALHO GRÁTIS

## CHECKLIST OBRIGATÓRIO — ANTES DE QUALQUER TRABALHO

### FASE 1: VERIFICAÇÃO DA PLATAFORMA (5 min)
- [ ] A plataforma está na LISTA APROVADA abaixo?
- [ ] Se NÃO está na lista: pesquisar "platform name payout reviews" + "platform name scam"
- [ ] Verificar último pagamento público (Open Collective, Twitter, etc.)
- [ ] Verificar se a plataforma tem escrow/garantia de pagamento
- [ ] **RED FLAG**: Sem evidência de pagamentos = NÃO TRABALHAR

### FASE 2: VERIFICAÇÃO DO PROJETO/BOUNTY (5 min)
- [ ] O projeto tem atividade recente? (PRs mergeados nos últimos 30 dias)
- [ ] O bounty tem valor FIXO em USD? (não tokens obscuros)
- [ ] O pagamento é via método verificável? (Stripe/USDC/BTC, NÃO "tokens próprios")
- [ ] Existem OUTROS contribuidores que foram pagos? (verificar PRs mergeados + comments)
- [ ] **RED FLAG**: >60 dias sem merge de PR externo = PROJETO MORTO

### FASE 3: VERIFICAÇÃO DA NOSSA CONTA (3 min)
- [ ] Temos conta ATIVA e VERIFICADA na plataforma?
- [ ] Wallet/Stripe está configurado para recebimento?
- [ ] KYC está completo (se necessário)?
- [ ] Email de recebimento está correto?
- [ ] **BLOQUEIO**: Se conta não existe = CRIAR PRIMEIRO, trabalhar DEPOIS

### FASE 4: ESTIMATIVA DE ROI (2 min)
- [ ] Valor do bounty: $___
- [ ] Tempo estimado: ___ horas
- [ ] $/hora estimado: $___
- [ ] Competição: quantos outros estão tentando?
- [ ] **MÍNIMO**: $50/hora estimado OU bounty > $500
- [ ] **REJEITAR**: Se < $25/hora estimado

### FASE 5: VERIFICAÇÃO PÓS-TRABALHO
- [ ] Submissão confirmada na plataforma?
- [ ] Recibo/screenshot salvo?
- [ ] Wallet de pagamento verificada no profile?
- [ ] Prazo de pagamento anotado?

## LISTA APROVADA — PLATAFORMAS QUE PAGAM (Verificado Mar 2026)

### TIER S — CONFIRMADO, ALTA CONFIANÇA
| Plataforma | Pagamento | Total Pago | Método | Nota |
|-----------|-----------|-----------|--------|------|
| **Immunefi** | 2-8 semanas | $100M+ | USDC/ETH on-chain | KYC obrigatório. Risco: scope disputes |
| **Code4rena** | 4-8 semanas | $10M+ | USDC/ETH | Competitivo. Paga winners garantido |
| **HackerOne** | 1-4 semanas | $300M+ | Stripe/PayPal/Bank | Maior plataforma. Transparente |
| **Algora** | Instant on merge | — | Stripe escrow | Pre-funded. AutoPay. 100% ao dev |
| **huntr.com** | Mensal (dia 25) | — | Stripe Connect | AI/ML focus. Protect AI backing |

### TIER A — PROVAVELMENTE PAGA
| Plataforma | Pagamento | Total Pago | Método | Nota |
|-----------|-----------|-----------|--------|------|
| **HackenProof** | 48h withdrawal | $15.7M+ | USDC Base/BTC/ETH | Web3 focus. 3% commission |
| **ProjectDiscovery** | Variável | — | Programa próprio | $50-$250/template nuclei |
| **Intigriti** | 1-4 semanas | — | Bank transfer | Forte na Europa |
| **Opire** | Via Stripe | — | Stripe | 0% fee ao dev |
| **Gitcoin** | Variável | $60M+ | Crypto | Grants + bounties |

### TIER B — USAR COM CAUTELA
| Plataforma | Risco | Nota |
|-----------|-------|------|
| **DoraHacks** | Médio | Hackathons. Verificar prize pool funding |
| **Superteam Earn** | Médio | Solana ecosystem. Verificar deadline + prizes |
| **Colosseum** | Médio | Hackathons Solana. Prizes reais mas competitivo |

### LISTA NEGRA — NÃO TRABALHAR
| Plataforma | Razão | Última Verificação |
|-----------|-------|-------------------|
| **dn-institute (1712n)** | 12 MESES sem merge, 30+ PRs unreviewed, 0 evidência de pagamento | Mar 2026 |
| **RustChain** | PRs fechados, token sem valor, projeto morto | Mar 2026 |
| **PrivacyLayer (ANAVHEOBA)** | SCAM confirmado, 404 on API | Mar 2026 |
| **sorosave-protocol** | 404 on API, provavelmente morto | Mar 2026 |
| **FinMind (rohitdash08)** | Sem bounty label | Mar 2026 |

## ERROS COMETIDOS — NUNCA REPETIR

### Erro 1: Trabalhar sem verificar pagamento
- **nuclei-templates**: 11 PRs criados ANTES de verificar se issue #7549 tinha bounty tag
- **Resultado**: $0. Horas de trabalho perdidas
- **Lição**: SEMPRE verificar bounty tag ANTES de criar qualquer PR

### Erro 2: Assumir que labels = pagamento
- **dn-institute**: Labels "$500", "$1000" existem, mas 12 meses sem merge
- **Resultado**: 10 PRs ($3,100+ potencial) que provavelmente NUNCA serão pagos
- **Lição**: Labels NÃO são garantia. Verificar MERGES RECENTES + PAGAMENTOS CONFIRMADOS

### Erro 3: Trabalhar em projeto morto
- **RustChain**: 16 PRs criados para $18 em token sem valor
- **Resultado**: Todos PRs fechados. Perda total de tempo.
- **Lição**: Verificar atividade do maintainer nos últimos 30 dias

### Erro 4: Criar conta DEPOIS de trabalhar
- **Algora**: Fizemos /claim sem ter conta Algora
- **HackenProof**: Encontramos findings sem ter conta ativa
- **Lição**: CRIAR CONTA + VERIFICAR PAGAMENTO **antes** de qualquer trabalho

### Erro 5: Não diversificar fontes de renda
- **100% bounties** é arriscado — competitivo, tempo longo de pagamento
- **Lição**: Combinar bounties + hackathons + freelance + produtos

## PROCESSO DE DECISÃO RÁPIDO

```
NOVO BOUNTY APARECEU?
  ↓
PLATAFORMA NA LISTA APROVADA?
  → NÃO → Pesquisar 5 min → Evidência de pagamento? → NÃO → REJEITAR
  → SIM ↓
PROJETO ATIVO? (merges nos últimos 30 dias)
  → NÃO → REJEITAR (provavelmente morto)
  → SIM ↓
BOUNTY > $100 E $/hora > $50?
  → NÃO → REJEITAR (não vale o tempo)
  → SIM ↓
TEMOS CONTA ATIVA + WALLET CONFIGURADA?
  → NÃO → CRIAR CONTA PRIMEIRO
  → SIM ↓
TRABALHAR!
```

## PRIORIDADE ATUAL (27 Mar 2026)

### P0 — DINHEIRO REAL, PLATAFORMA VERIFICADA
1. **Immunefi #71022** $1K-$100K — ESCALATED, aguardando ZKsync (TIER S)
2. **C4 Chainlink** $65K — Aguardando resultado (TIER S)
3. **huntr.com** — REGISTRAR + submeter AI/ML vulns (TIER S)

### P1 — PLATAFORMA BOA, PRECISA SETUP
4. **Algora bounties** — Criar conta + buscar bounties REAIS com escrow (TIER S)
5. **HackenProof** — Ativar conta + build rep + NEAR findings (TIER A)
6. **ProjectDiscovery templates** — $50-$250/template via programa DELES (TIER A)

### P2 — HACKATHONS (prize pool confirmado)
7. **Colosseum Frontier** $50K+ — Registrar, Apr 6
8. **INITIATE** $25K — DoraHacks, Apr 15

### SKIP — Não investir mais tempo
- dn-institute (12 meses morto)
- nuclei-templates via issue #7549 ($0)
- RustChain (fechado)

## REVISÃO MENSAL
- No dia 1 de cada mês: revisar esta lista
- Atualizar LISTA NEGRA com novos scams descobertos
- Atualizar LISTA APROVADA com novas plataformas verificadas
- Calcular ROI real: $ recebido / horas investidas
