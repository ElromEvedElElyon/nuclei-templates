# TapToons — Two Versions
# Em nome do Senhor Jesus Cristo

## Status: LIVE (28 Mar 2026, Session 51 — REPOS FIXED)

### V1 — Pixel Art Edition (Original)
- **LIVE**: https://elromevedelelyon.github.io/taptoons-v1/
- **Repo**: https://github.com/ElromEvedElElyon/taptoons-v1 (PUBLIC, main branch)
- **Local mirror**: ~/taptoons/ (public repo, master branch)
- **Title**: "TapToons v1 - Pixel Art Sounds & Game" (FIXED Session 51)
- **Branding**: "PIXEL ART EDITION v1.0" (was wrongly labeled v2)
- Pixel art 12x16, emojis nos botoes, game Sonic basico
- 1425 linhas, 64KB

### V2.1 — N64 Monster Edition (Qualidade Extrema)
- **LIVE**: https://elromevedelelyon.github.io/taptoons/
- **Repo PUBLIC**: https://github.com/ElromEvedElElyon/taptoons (master branch)
- **Repo PRIVATE**: https://github.com/ElromEvedElElyon/taptoons-v2 (main branch)
- **Local dev**: ~/taptoons-v2/ | **Local public**: ~/taptoons/
- **Title**: "TapToons v2 - Monster Runner N64" (RESTORED Session 51)
- 6 monstros procedurais (Sulley, Mike, Rosie, Drake, Gears, Rex)
- Sonic Green Hill Zone: ceu gradiente, palmeiras, flores, 5 camadas parallax
- Text labels (sem emojis), on-screen game pad, bigger char select
- ~67KB, cache SW v5, 1422 linhas
- **Price**: $0.99 (Stripe + PayPal)

### Session 51 Fix Summary
- v1 repo: Branding corrigido (v2→v1 em title, ver badge, footer)
- v2 public: N64 Monster Edition RESTAURADO (tinha sido revertido para Pixel Art)
- v2 private: 673 linhas uncommitted COMMITADAS (sessao anterior crashou)
- Ambas Pages builds: OK, sites verificados LIVE

## ROI Analysis
- Net per sale: $0.66 (after Stripe/PayPal fees)
- Cost to build: $0
- Comparable: iFart $40K day 1, SlapMac $5K/3 days
- Conservative: $660-$5,000/month

## Architecture (single index.html ~67KB)
- **CSS**: Press Start 2P pixel font, retro palette, CRT scanlines
- **Sounds**: 10 packs x 10 = 100 total, Web Audio API synthesis (10 recipes)
  - FREE: Complaints, Pleas, Cartoon (30 sounds)
  - PREMIUM: Laughs, Screams, Retro Game, Animals, Music, Silly, Weird (70 sounds)
- **Game**: Monster Runner N64 — Sonic-style side-scroller, canvas 400x200
- **Characters**: 6 procedural monsters (M_BODY + ML arrays, drawMonster function)
- **Payment**: Same Stripe LIVE + PayPal links

## Stripe LIVE Config (DO NOT CHANGE)
- Payment Link: https://buy.stripe.com/6oUdR80Vu5pm3S56uV0x20c
- PayPal: https://www.paypal.com/paypalme/PadraoBitcoin/0.99
- Product: prod_UEBT31CtCFl76R | Price: price_1TFj6GCrBH7uXgTeWvYzgDau

## Synthesis Engine (10 recipes)
tone, sweep, burst, formant, repeat, slide, chord, noise, wobble, impact

## Israel Four
- Security audit before deploy
- Capybara engine code scan
- XSS/payment tampering/localStorage abuse checks
