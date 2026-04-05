# Repository Blacklist — Dead Repos (Do NOT Submit PRs)
# Last updated: Session 109 (3 Apr 2026)

## RULE: Before ANY PR, run:
## `gh pr list --repo OWNER/REPO --state merged --limit 5`
## If 0 external merges → SKIP. Do not waste time.

---

## BLACKLISTED REPOS

### 1. claude-builders-bounty/claude-builders-bounty
- **Status**: DEAD — 0 merges out of 440+ open PRs EVER
- **Our PRs**: 5 open (#19, #367, #368, #369, #370)
- **Evidence**: `gh pr list --repo claude-builders-bounty/claude-builders-bounty --state merged --limit 5` returns EMPTY
- **Reason**: Repo collects submissions but never reviews or merges. Pure time sink.
- **Action**: Do NOT submit more PRs. Consider closing existing ones.

### 2. 1712n/dn-institute
- **Status**: DEAD for external bounty contributors — last external merge was Jun 2024 (JediFaust, SorryBro28)
- **Our PRs**: 10 open (#694-#703)
- **Evidence**: Only maintainer merges since mid-2024. No bounty PRs merged.
- **Reason**: Maintainer-only merge pattern. External PRs rot indefinitely.
- **Action**: Do NOT submit more PRs. Existing 10 PRs are dead weight.

### 3. Good Angel Network
- **Status**: CLOSED program
- **Evidence**: Bounty program shut down
- **Reason**: No active bounty program to pay out
- **Action**: Skip entirely

### 4. projectdiscovery/nuclei-templates (CONDITIONAL)
- **Status**: HOSTILE to AI-generated content
- **Our PRs**: 2 open (#15676, #15701)
- **Evidence**: PRs get labeled "AI-generated" and deprioritized/rejected
- **Reason**: Maintainers actively filter AI-generated templates
- **Action**: Only submit if manually crafted AND tested. AI-generated = auto-reject.

---

## REPOS WITH LOW MERGE PROBABILITY (MONITOR)

### 5. rohitdash08/FinMind
- **Our PRs**: 1 open (#644)
- **Status**: Unknown merge rate. Monitor.

### 6. ANAVHEOBA/PrivacyLayer
- **Our PRs**: 2 open (#117, #118)
- **Status**: Unknown merge rate. Monitor.

### 7. sorosave-protocol/frontend
- **Our PRs**: 3 open (#130, #131, #132)
- **Status**: Active repo but workspace dependency issues. Monitor.

---

## HEALTHY REPOS (OK TO SUBMIT)

### Awesome lists (merge regularly):
- punkpeye/awesome-mcp-servers — Active, reviews PRs
- TensorBlock/awesome-mcp-servers — Active
- badkk/awesome-crypto-mcp-servers — Active
- docker/mcp-registry — Active, official

### Bug bounty platforms (pay for findings):
- Immunefi — Pays. #72086 ESCALATED.
- Code4rena — Pays. 2 HIGH submitted.
- Guardian/LimitBreak — Pays. 16 findings submitted.

### Hackathons:
- solanabr/solana-glossary — Active competition
- nosana-ci/agent-challenge — Active, PR #18 open
- Colosseum Frontier — Starting Apr 6

---

## PR INVENTORY (3 Apr 2026)

### Dead repos (waste): 15 PRs
- claude-builders-bounty: 5 PRs
- dn-institute: 10 PRs

### Active repos: 20+ PRs
- awesome-mcp-servers (various): 8 PRs
- awesome-crypto-mcp-servers: 4 PRs
- docker/mcp-registry: 1 PR
- nuclei-templates: 2 PRs (conditional)
- solana-glossary: 1 PR
- nosana-ci: 1 PR
- PrivacyLayer: 2 PRs
- sorosave: 3 PRs
- FinMind: 1 PR
- bounty-hunter-test: 1 PR
