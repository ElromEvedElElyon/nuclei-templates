#!/bin/bash
# Script para registrar Telegram com numero Twilio
# 1. Abre Telegram Desktop
# 2. Monitora SMS no Twilio para codigo de verificacao

TWILIO_SID="TWILIO_SID_REDACTED"
TWILIO_TOKEN="5faeec697d87c55680ff3d044a8d363e"
TWILIO_PHONE="+13187149390"

echo "=========================================="
echo "  REGISTRO TELEGRAM — Padrao Bitcoin"
echo "=========================================="
echo ""
echo "NUMERO PARA REGISTRAR: $TWILIO_PHONE"
echo ""
echo "INSTRUCOES:"
echo "1. O Telegram vai abrir"
echo "2. Selecione pais: United States (+1)"
echo "3. Digite o numero: 3187149390"
echo "4. Telegram envia SMS de verificacao"
echo "5. Este script vai capturar o codigo automaticamente"
echo ""
echo "Abrindo Telegram..."
~/bin/telegram-desktop &
TPID=$!

echo ""
echo "Monitorando SMS no Twilio... (Ctrl+C para parar)"
echo ""

LAST_MSG=""
while true; do
    CURRENT=$(curl -s -u "$TWILIO_SID:$TWILIO_TOKEN" \
        "https://api.twilio.com/2010-04-01/Accounts/$TWILIO_SID/Messages.json?To=$TWILIO_PHONE&PageSize=1" \
        | python3 -c "
import sys, json
data = json.load(sys.stdin)
msgs = data.get('messages', [])
if msgs:
    m = msgs[0]
    print(f'{m[\"date_sent\"]}|{m[\"from\"]}|{m[\"body\"]}')
" 2>/dev/null)

    if [ "$CURRENT" != "$LAST_MSG" ] && [ -n "$CURRENT" ]; then
        LAST_MSG="$CURRENT"
        echo "============ NOVO SMS RECEBIDO! ============"
        echo "$CURRENT" | tr '|' '\n'
        echo ""
        # Extrair codigo numerico
        CODE=$(echo "$CURRENT" | grep -oE '[0-9]{4,6}' | head -1)
        if [ -n "$CODE" ]; then
            echo ">>> CODIGO DE VERIFICACAO: $CODE <<<"
            echo ""
        fi
        echo "============================================="
    fi
    sleep 3
done
