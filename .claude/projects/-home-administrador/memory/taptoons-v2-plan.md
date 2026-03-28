# TapToons — Two Versions
# Em nome do Senhor Jesus Cristo

## Status: LIVE (28 Mar 2026, Session 50)

### V1 — Jogo Simples (Pixel Art)
- **LIVE**: https://elromevedelelyon.github.io/taptoons-v1/
- **Repo**: https://github.com/ElromEvedElElyon/taptoons-v1 (PUBLIC para Pages)
- Pixel art 12x16, emojis nos botoes, game Sonic basico
- 1425 linhas, 64KB

### V2.1 — N64 Monster Edition (Qualidade Extrema)
- **LIVE**: https://elromevedelelyon.github.io/taptoons/
- **Repo**: https://github.com/ElromEvedElElyon/taptoons (PUBLIC para Pages, master)
- **Dev**: https://github.com/ElromEvedElElyon/taptoons-v2 (PRIVATE)
- **Local**: ~/taptoons-v2/index.html
- 6 monstros procedurais (Sulley, Mike, Rosie, Drake, Gears, Rex)
- Sonic Green Hill Zone: ceu gradiente, palmeiras, flores, 5 camadas parallax
- Plataformas pedra com highlight/shadow, grama com laminas
- Rings dourados Sonic com brilho, inimigos Badnik roboticos
- Sem emojis — UI limpa profissional
- ~67KB, cache SW v5
- **Price**: $0.99 (Stripe + PayPal)

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
