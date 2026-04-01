# eSIM Cloud Bridge — Product Details

## CONCEPT
First BYOE (Bring Your Own eSIM) cloud platform.
Use your eSIM on any device without a phone — SMS, calls, 2FA.

## REPOS
- **Code (PRIVATE)**: github.com/ElromEvedElElyon/esim-cloud-bridge
- **Landing (PUBLIC)**: github.com/ElromEvedElElyon/esim-cloud-bridge-site
- **LIVE**: https://elromevedelelyon.github.io/esim-cloud-bridge-site/

## MARKET GAP
- NINGUEM oferece "Traga Seu Proprio eSIM" na nuvem
- Crypton.sh/Twilio/Google Voice = numeros DELES, nao seus
- Mercado eSIM: $16B ate 2027
- 9 bilhoes de dispositivos eSIM ate 2030

## PRICING
- Free: $0 (10 SMS/mes)
- Personal: $4.99/mo (unlimited SMS, Telegram forward)
- Pro: $14.99/mo (SMS + Voice WebRTC + API)
- Business: $49.99/mo (10 eSIMs, team dashboard)

## TECH STACK
- Backend: Python FastAPI / Node.js
- Frontend: React/Next.js (landing already deployed)
- Modem: Quectel RM520N-GL ($40) com eUICC, ModemManager + lpac
- Voice: Asterisk + chan_dongle / WebRTC
- SMS Gateway: ModemManager/mmcli + custom forwarder
- Notifications: Telegram Bot, Email, Webhooks

## KEY TOOLS (from research)
- **Sigmo**: Web UI for cellular modems on Linux (Go, Vue3)
- **lpac**: CLI eSIM profile management (C)
- **EasyLPAC**: GUI frontend for lpac (Go) — 620 stars
- **OpenRSP**: Blockchain-powered eSIM provisioning
- **Soprani.ca eSIM Adapter**: $39.99 physical eUICC card for desktop
- **sysmoEUICC1**: Developer eUICC card
- **chan_dongle**: Asterisk module for voice via USB modems

## HARDWARE NEEDED (for real MVP)
- 5x Quectel RM520N-GL USB modem: ~$200
- OR cheaper: 5x Huawei E173 (~$50 total used from MercadoLivre)
- Mini-PC or our machine with USB hub

## NUMERO CLARO eSIM
- **+5511966083891** — ativado 23 Mar 2026
- smsProvider registrado como "free-services" (quackr.io)
- Para usar REAL: precisa modem USB celular + eSIM adapter
- OU contatar Claro para reemitir QR code do eSIM

## TWILIO (funcional)
- **SID**: TWILIO_SID_REDACTED
- **Phone**: +13187149390 (SMS+MMS+Voice)
- **Saldo**: $14.34
- **Checker**: `bash ~/twilio-sms-checker.sh`

## TELEGRAM DESKTOP
- Instalado em ~/bin/telegram-desktop
- Registrar com numero Twilio +13187149390
- Script: ~/register-telegram.sh
