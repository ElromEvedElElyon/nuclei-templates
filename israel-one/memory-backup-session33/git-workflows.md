# Git & GitHub — Melhores Praticas Confirmadas

## GitHub CLI (gh) — Comandos Essenciais
```bash
# Ver TODOS PRs abertos
gh search prs --author=ElromEvedElElyon --state=open --limit=40

# Push arquivo via API (bypassa workflow scope errors)
gh api repos/OWNER/REPO/contents/PATH --method PUT \
  -f message="msg" -f content="$(base64 -w0 FILE)" -f sha="SHA"

# Checar sha antes de atualizar
gh api repos/OWNER/REPO/contents/PATH --jq '.sha'

# Claim bounty
gh issue comment ISSUE_URL --body "I'd like to work on this"

# Pingar maintainer
gh pr comment PR_URL --body "Gentle ping for review"

# Ver Gists
gh gist list && gh gist edit GIST_ID
```

## Nuclei-Templates — Processo de Contribuicao
1. Fork + branch do upstream/main
2. Adicionar APENAS arquivo(s) do template (NADA pessoal!)
3. `verified: true` requer evidencia real de teste
4. Tags: incluir `authenticated` se CVE requer auth (CVSS PR:L)
5. Matchers: usar `and` (nao `or`) para evitar false positives
6. Neo bot review automatico em minutos — enderecar TODOS os findings
7. Commit + push no branch atualiza PR automaticamente
8. **LICAO**: Nunca misturar commits pessoais (backup, memory) no branch do PR!

## PR #15676 Licao Critica
- Branch tinha 69 arquivos pessoais de backup
- Neo bot flaggou, merge bloqueado
- FIX: `git checkout -b clean-branch FETCH_HEAD && git cherry-pick COMMIT && git push --force`
- REGRA: branches de PR devem ter SOMENTE arquivos relevantes

## Git Best Practices
- `rm -f ~/.git/index.lock` se lock file aparecer
- Backup antes de tarefas arriscadas
- FUNDING.yml: se push falha (workflow scope), usar `gh api` PUT
- Pre-commit hooks falham → NUNCA `--amend` (cria novo commit)
- Force push para branch de PR e OK (atualiza PR)
- Force push para main NUNCA

## Fork Workflow
```bash
git remote add upstream URL_ORIGINAL
git fetch upstream main
git checkout -b feature upstream/main
# ... trabalhar ...
git push origin feature
gh pr create --repo ORIGINAL_OWNER/REPO
```
