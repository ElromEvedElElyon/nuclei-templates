#!/bin/bash
# Twilio SMS Inbox Checker — Padrao Bitcoin
# Numero: +1 318-714-9390
# Uso: bash ~/twilio-sms-checker.sh [limit]

SID="TWILIO_SID_REDACTED"
TOKEN="5faeec697d87c55680ff3d044a8d363e"
PHONE="+13187149390"
LIMIT="${1:-20}"

echo "=== TWILIO SMS INBOX — $PHONE ==="
echo "Saldo: $(curl -s -u "$SID:$TOKEN" "https://api.twilio.com/2010-04-01/Accounts/$SID/Balance.json" | python3 -c "import sys,json; print(json.load(sys.stdin).get('balance','?'))" 2>/dev/null) USD"
echo ""

curl -s -u "$SID:$TOKEN" \
  "https://api.twilio.com/2010-04-01/Accounts/$SID/Messages.json?To=$PHONE&PageSize=$LIMIT" \
  | python3 -c "
import sys, json
data = json.load(sys.stdin)
msgs = data.get('messages', [])
if not msgs:
    print('Nenhum SMS recebido.')
else:
    print(f'{len(msgs)} mensagens:')
    print('-' * 60)
    for m in msgs:
        print(f\"Data: {m['date_sent']}\")
        print(f\"De: {m['from']}\")
        print(f\"Status: {m['status']}\")
        print(f\"Texto: {m['body']}\")
        print('-' * 60)
" 2>/dev/null
