# Firefox + Extensoes + MCP DevTools

## Firefox Info
- **Versao**: 148.0.2 (Snap)
- **Binario**: /usr/bin/firefox (snap wrapper)
- **Profile path**: /home/administrador/snap/firefox/common/.mozilla/firefox/3gjtnsc5.default
- **Extensions dir**: {profile}/extensions/

## Extensoes Instaladas (24 Mar 2026)

### Ja existiam:
| Extensao | ID | Tamanho |
|----------|----|---------|
| MetaMask | webextension@metamask.io | 29MB |
| Proton VPN | vpn@proton.ch | 2.5MB |
| PT-BR Lang | langpack-pt-BR@firefox.mozilla.org | 457KB |
| New Tab | newtab@mozilla.org | 1.5MB |

### Instaladas nesta sessao (Claude extensions):
| Extensao | ID | Tamanho | Fonte |
|----------|----|---------|-------|
| Super Claude | superclaude@pilotecode.com | 1.9MB | addons.mozilla.org |
| Claude Usage Tracker | claude_usage_tracker@lugia19.com | 2.7MB | addons.mozilla.org |
| Claude Exporter | {25798758-c184-470a-bb5b-9fa76a09d9b5} | 194KB | addons.mozilla.org |
| Claude Helper | claude-helper@merteraslan.github.io | 18KB | addons.mozilla.org |
| Summarize & Translate | extension-summarize-translate-claude@dbstudy.info | 91KB | addons.mozilla.org |

## Como Instalar Extensoes Firefox via CMD (PROCEDIMENTO CONFIRMADO)

```bash
# 1. Baixar XPI do addons.mozilla.org
curl -sL "https://addons.mozilla.org/firefox/downloads/latest/NOME/addon-NOME-latest.xpi" -o /tmp/extensao.xpi

# 2. Extrair ID da extensao do manifest.json
unzip -p /tmp/extensao.xpi manifest.json | python3 -c "
import sys,json
m=json.load(sys.stdin)
print(m.get('browser_specific_settings',{}).get('gecko',{}).get('id','') or
      m.get('applications',{}).get('gecko',{}).get('id',''))
"

# 3. Copiar com nome = ID.xpi para pasta extensions do profile
cp /tmp/extensao.xpi "$PROFILE/extensions/ID_DA_EXTENSAO.xpi"

# 4. Firefox reconhece na proxima inicializacao
```

**IMPORTANTE**: O nome do arquivo .xpi DEVE ser o ID da extensao (ex: `superclaude@pilotecode.com.xpi`)

## MCP Firefox DevTools — Configuracao

### Config atual em ~/.claude.json:
```json
{
  "firefox-devtools": {
    "type": "stdio",
    "command": "npx",
    "args": [
      "firefox-devtools-mcp@latest",
      "--profilePath",
      "/home/administrador/snap/firefox/common/.mozilla/firefox/3gjtnsc5.default",
      "--viewport",
      "1280x720"
    ]
  }
}
```

### Opcoes uteis do firefox-devtools-mcp:
- `--profilePath PATH` — Usa perfil existente (COM extensoes!)
- `--headless` — Sem UI (mais rapido, mas extensoes podem nao funcionar)
- `--viewport WxH` — Tamanho da janela
- `--connectExisting` — Conecta a Firefox ja rodando (precisa --marionette)
- `--startUrl URL` — URL inicial
- `--firefoxPath PATH` — Caminho do Firefox
- `--marionettePort N` — Porta marionette (default 2828)

### Como adicionar via CLI:
```bash
claude mcp add firefox-devtools -s user -- npx firefox-devtools-mcp@latest \
  --profilePath /home/administrador/snap/firefox/common/.mozilla/firefox/3gjtnsc5.default \
  --viewport 1280x720
```

### IMPORTANTE — Limitacoes:
- MCP precisa **reiniciar Claude Code** para reconectar apos mudanca de config
- `--headless` pode NAO carregar extensoes (testar sem headless primeiro)
- NAO rodar Firefox separado ao mesmo tempo (conflito de profile lock)
- Firefox Snap usa paths diferentes: ~/snap/firefox/common/.mozilla/firefox/

## Interacao com MetaMask via MCP

### Fluxo para desbloquear MetaMask:
1. Firefox abre com perfil que tem MetaMask
2. Navegar para `chrome-extension://` ou esperar popup
3. MCP preenche campo de senha
4. MCP clica "Unlock"
5. Screenshot para confirmar

### Para assinar transacoes:
1. Navegar para dApp
2. Conectar wallet (MetaMask popup)
3. MCP clica "Connect"
4. Para assinar: MCP clica "Confirm" no popup MetaMask

## Extensoes Claude Oficiais — NAO EXISTE para Firefox
- Anthropic so tem extensao oficial para Chrome/Edge
- Todas as extensoes Firefox sao da comunidade (third-party)
- Alternativa: Claude Sidebar (sidebar access sem sair da pagina)
