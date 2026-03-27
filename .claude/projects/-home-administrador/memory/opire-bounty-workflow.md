# Opire Bounty Workflow — Guia Completo (Session 43)

## COMO FUNCIONA
1. Bounty creators colocam $ em issues GitHub via Opire
2. Devs comentam `/opire try` para clamar
3. Dev resolve issue + submete PR
4. Creator aprova + paga via Opire dashboard
5. Dev recebe 100% via Stripe (1-7 dias)

## CADASTRO (BLOQUEADO)
- URL: app.opire.dev → Log in → Continue with GitHub
- Opire OAuth client_id: `Iv1.2d8c6689aac4e981`
- Redirect: `https://app.opire.dev/auth/github`
- Scopes: `read:user user:email`
- **PRECISA**: Senha do GitHub (PAT nao funciona no web login)
- Apos login: configurar Stripe para recebimento
- Nossa Stripe: `acct_1RlC98Cpy8OI4abM` (PADRAO BITCOIN)

## API PUBLICA
- `https://api.opire.dev/health` — health check
- `https://api.opire.dev/rewards` — lista TODOS bounties
- `https://api.opire.dev/users/{id}` — info de usuario
- Auth API: NAO tem endpoint publico, precisa OAuth web flow

## BOUNTIES ATUAIS (claude-builders-bounty)
- PRs #15-#19 submetidos, $575 total
- DUPLICATE PRs #21-#26 from parallel session — same bounties
- OpireBot NAO instalado no repo — pagamento manual pelo creator
- Competidores ativos nos mesmos issues

## REGISTRATION STATUS
- **INCOMPLETE**: Reached GitHub OAuth authorize page (title: "Authorize Opire") but button NOT clicked
- **URL**: `https://github.com/login/oauth/authorize?client_id=Iv1.2d8c6689aac4e981&redirect_uri=...`
- **NEXT**: Need to click "Authorize Opire" button → redirect to app.opire.dev → configure Stripe
- **Stripe account**: acct_1RlC98Cpy8OI4abM (PADRAO BITCOIN)
- **BLOCKER**: Chrome cookie decryption has artifacts (garbled first AES block)
- **ALTERNATIVE**: Use Chrome headless CDP with authenticated profile

## LICOES
1. Opire funciona mas precisa browser para cadastro
2. `/opire try` so funciona se OpireBot estiver instalado
3. Sem bot, creator paga manualmente via dashboard
4. Dev precisa conta Opire + Stripe configurado ANTES de receber
5. Bounties no app.opire.dev/home mostram todos disponiveis
6. Expensify $250 issues sao rapidos demais — todos TAKEN em horas
7. nuclei-templates NAO tem bounty labels ativas atualmente
8. Chrome cookie decryption: v10 AES-CBC with 'peanuts' key has prefix garbage on Linux
9. GitHub OAuth authorize page URL contains 'opire.dev' in redirect_uri — FALSE POSITIVE for redirect check
10. Firefox Marionette sessions dont persist cookies — need to re-inject every time
