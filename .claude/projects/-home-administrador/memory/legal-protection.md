# Legal Protection — Padrao Bitcoin
# Atualizado: 1 Abr 2026 (Session 90)

## REGRA MASTER: NUNCA ACEITAR TERMOS CEGAMENTE

Antes de qualquer `acceptedCustomTerms: true`, `I agree`, ou equivalente:
1. **LER** todos os termos completos
2. **VERIFICAR** clausulas de risco (ver checklist abaixo)
3. **ALERTAR** usuario sobre riscos encontrados
4. **DOCUMENTAR** o que foi aceito e quando

## CHECKLIST DE CLAUSULAS PREDATORIAS

Recusar automaticamente se encontrar:
- [ ] IP assignment TOTAL sem compensacao proporcional
- [ ] Non-compete que impeca trabalhar em outras plataformas
- [ ] Liability ilimitada para participante (nosso risco > reward)
- [ ] Jurisdicao inacessivel sem arbitragem razoavel
- [ ] Forfeiture em < 90 dias (prazo curto demais)
- [ ] Waiver de class action sem opt-out
- [ ] Unilateral amendment (eles mudam termos quando quiserem)
- [ ] Indemnificacao sem cap (expoe empresa a risco infinito)

## GUARDIAN LIMITBREAK — ANALISE COMPLETA (1 Abr 2026)

### Termos Aceitos (15 clausulas)
- **S.10 IP Assignment**: Findings ACEITOS sao assigned a Limit Break. PADRAO na industria.
- **S.11 Confidencialidade**: Submissions confidenciais. NAO publicar sem autorizacao escrita.
- **S.12 Indemnificacao**: Participante indemnifica Guardian. Liability cap $100. RISCO BAIXO (padrao).
- **S.14 Delaware + Arbitragem**: Binding arbitration. PADRAO para empresas US.
- **S.8 Forfeiture 6 meses**: Rewards nao reivindicados em 6 meses = perdidos. ACEITAVEL.

### VEREDICTO: Termos PADRAO para bug bounty. SEM clausulas predatorias.
### RISCO PRINCIPAL: Administrativo (email descartavel, duplicatas), NAO legal.

### PROBLEMAS IDENTIFICADOS:
1. **16 submissions (8 duplicatas)** — NAO conseguimos deletar (admin only)
2. **Email sharebot.net** — NAO conseguimos atualizar via API (admin only)
3. **Acao necessaria via BROWSER**: Logar no Guardian, atualizar email, contatar suporte

### ACOES PENDENTES:
- [ ] Atualizar email para standardbitcoin.io@gmail.com via browser
- [ ] Contatar Guardian suporte sobre duplicatas (explicar erro tecnico)
- [ ] NAO publicar findings em lugar nenhum (clausula confidencialidade)

## PLATAFORMAS ANALISADAS — STATUS DE TERMOS

| Plataforma | Termos Lidos? | IP Assignment? | Risco |
|-----------|---------------|----------------|-------|
| Guardian | SIM (1 Abr 2026) | SIM (findings aceitos) | BAIXO |
| Code4rena | NAO VERIFICADO | Provavel | VERIFICAR |
| Immunefi | NAO VERIFICADO | Provavel | VERIFICAR |
| HackenProof | NAO VERIFICADO | Desconhecido | VERIFICAR |
| Algora | NAO VERIFICADO | Improvavel (open source) | VERIFICAR |

## REGRAS PARA EMAILS EM PLATAFORMAS

| Tipo de Plataforma | Email Obrigatorio |
|--------------------|--------------------|
| Bug bounty (pagamento) | standardbitcoin.io@gmail.com |
| Hackathons (premio) | standardbitcoin.io@gmail.com |
| Grants (financiamento) | standardbitcoin.io@gmail.com |
| Registro sem pagamento | inteligenciaartificial.now@gmail.com OK |
| Testes/throwaway | Qualquer (mas NUNCA em conta que paga) |
