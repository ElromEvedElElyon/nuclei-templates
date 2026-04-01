# KDP Automation — Lessons & Patterns (Session 67)
# NUNCA DELETAR — Base para publicar MYTHOS em 193 idiomas

## FERRAMENTAS
- **kdp_nav.py v2.0**: CDP client melhorado (~/kdp_nav.py)
- **kdp_publish_lang.py**: Automação multi-idioma (~/kdp_publish_lang.py)
- **Chrome CDP**: Port 9222, user-data-dir ~/.chrome-kdp

## ERROS CRITICOS E CORRECOES (Session 67)

### 1. Checkbox customizado React (MAIS IMPORTANTE)
- **ERRO**: Procurou `input[type=checkbox]` — NÃO encontrou os checkboxes de confirmação
- **CAUSA**: KDP usa `<div role="checkbox">` com `aria-checked="true/false"` (React custom)
- **FIX**: `document.querySelectorAll('[role="checkbox"]')` + `.click()`
- **REGRA**: SEMPRE usar `cdp.check_role_checkboxes()` ANTES de Save & Continue na page Content
- **QUANTIDADE**: Page Content tem DOIS checkboxes role=checkbox (AI + manuscrito)

### 2. Campo CPF preenchido errado
- **ERRO**: Usou index 0 para preencher CPF → preencheu campo SkipElement (errado)
- **CAUSA**: Campos input listados por index, primeiro visível não era o campo CPF
- **FIX**: Usar `input[name="BRCPF"]` (seletor por nome)
- **REGRA**: NUNCA preencher por index. SEMPRE usar `fill_field_by_name()` ou `fill_field_by_id()`

### 3. Navegação React SPA
- **ERRO**: Clicar em links `<a>` do sidebar não funcionou (React intercepta)
- **CAUSA**: React SPA usa onClick handlers, não navegação tradicional
- **FIX**: TreeWalker para encontrar nó de texto e clicar no parentElement
- **REGRA**: Usar `cdp.click_by_text("texto exato")` para navegar em SPAs

### 4. URLs KDP incorretas
- **ERRO**: `/en_US/account/taxinterview` retornou 404
- **CAUSA**: KDP mudou estrutura de URLs, agora em `account.kdp.amazon.com`
- **URLs CORRETAS**:
  - Bookshelf: `https://kdp.amazon.com/pt_BR/bookshelf`
  - Details: `https://kdp.amazon.com/pt_BR/title-setup/kindle/{ASIN}/details`
  - Content: `https://kdp.amazon.com/pt_BR/title-setup/kindle/{ASIN}/content`
  - Pricing: `https://kdp.amazon.com/pt_BR/title-setup/kindle/{ASIN}/pricing`
  - Account: `https://account.kdp.amazon.com/`
  - Tax: `https://account.kdp.amazon.com/tax-info`
  - New eBook: `https://kdp.amazon.com/pt_BR/title-setup/kindle/new/details`

### 5. Fluxo sequencial obrigatório
- **ERRO**: Tentou publicar direto da page Pricing sem completar Content
- **CAUSA**: KDP exige que cada etapa seja completada em ordem
- **REGRA**: Details → Content (com checkboxes) → Pricing → Publish
- **VALIDACAO**: "Conclua esta etapa antes de continuar" = algum checkbox faltando

### 6. Página demora para carregar (React lazy)
- **ERRO**: Tentou interagir antes da página carregar
- **CAUSA**: React usa lazy loading, elementos não existem imediatamente
- **FIX**: `cdp.wait_for_element()` ou `cdp.wait_for_text()` antes de interagir
- **REGRA**: SEMPRE esperar pelo menos 3-5s após navigate(), usar wait_for_*

### 7. Input React não detecta setValue direto
- **ERRO**: `el.value = "x"` não dispara change no React
- **FIX**: Usar `Object.getOwnPropertyDescriptor(HTMLInputElement.prototype, 'value').set`
  seguido de `dispatchEvent(new Event('input', {bubbles: true}))`
- **REGRA**: SEMPRE usar fill_field_by_name() que já faz isso automaticamente

### 8. Formato de preço locale
- **ERRO**: "Use um formato de preço de 0,00" (formato brasileiro com vírgula)
- **CAUSA**: KDP brasil usa vírgula como separador decimal
- **FIX**: DEVE usar "6,66" (vírgula) — "6.66" gera erro de formato
- **REGRA**: Usar CDP Input.insertText para digitar preço + Tab para blur
- **CAMPO US**: `input[name="data[digital][channels][amazon][US][price_vat_inclusive]"]`

### 9. CKEditor para descrição (Session 68)
- **ERRO**: innerHTML no iframe não sincroniza com CKEditor interno
- **CAUSA**: KDP usa CKEditor dentro de iframe para campo descrição
- **FIX**: `CKEDITOR.instances.editor1.setData(html)` + `ed.updateElement()` + `ed.fire("change")`
- **REGRA**: SEMPRE usar CKEditor API, NUNCA innerHTML direto

### 10. React role="radio" AI disclosure (Session 68)
- **ERRO**: `element.click()`, `dispatchEvent(new MouseEvent("click"))` NÃO funcionam
- **CAUSA**: React usa synthetic events, não responde a JS nativo em role="radio"
- **FIX**: CDP `Input.dispatchMouseEvent` com coordenadas reais do `getBoundingClientRect()`
- **REGRA**: Para role="radio" e role="checkbox" sempre usar CDP mouse events

### 11. AI tool name fields (Session 68)
- **ERRO**: Native input value setter + dispatchEvent não triggera React validation
- **CAUSA**: React input tem onChange handler que só responde a eventos reais de teclado
- **FIX**: CDP `Input.dispatchMouseEvent` (click) → `Input.dispatchKeyEvent` (Ctrl+A) → `Input.insertText` (texto) → `Input.dispatchKeyEvent` (Tab/blur)
- **REGRA**: Para inputs React que não respondem ao setter nativo, usar CDP Input.insertText

### 12. CDPClient.send() syntax (Session 68)
- **ERRO**: `cdp.send('method', key=value)` → TypeError
- **CAUSA**: CDPClient.send() aceita (method, params=None) onde params é dict
- **FIX**: `cdp.send('Input.dispatchMouseEvent', {'type': 'mousePressed', 'x': x, 'y': y, ...})`
- **REGRA**: SEMPRE usar dict para params, NUNCA kwargs

## FLUXO KDP PARA 193 IDIOMAS

### Pré-requisitos (JÁ FEITOS)
- [x] Conta KDP ativa (standardbitcoin.io@gmail.com)
- [x] W-8BEN validado (Ref A03730261AJ26J8KT5R0R)
- [x] Banco adicionado (*****218)
- [x] Chrome CDP rodando (~/.chrome-kdp, port 9222)
- [x] 22 EPUBs prontos em ~/capybara-bible/dist/
- [x] Capa universal: cover_1600x2560.jpg

### Para cada idioma novo:
1. `python3 kdp_publish_lang.py PT` (ou qualquer código)
2. Script navega: New eBook → Details → Content → Pricing → Publish
3. Cada publicação leva ~3-5 minutos com automação
4. Esperar 72h para revisão da Amazon por idioma

### Ordem de publicação (por tamanho de mercado):
1. EN ✅ PUBLICADO (30 Mar 2026) — ASIN A1M3B0MAA1KRQ
2. PT ⏳ EM ANDAMENTO (Pricing page) — ASIN AXQR3EQ9UQXCU
2. ES → FR → DE → IT → RU
3. ZH → JA → KO → HI → AR
4. NL → TR → SV → PL → VI → TH → ID
5. UK → RO → CS
6. Traduzir + publicar 170 idiomas restantes progressivamente

### Para idiomas que ainda NÃO têm EPUB:
1. Traduzir manuscrito: `python3 translate_pipeline.py --lang XX`
2. Gerar EPUB: `python3 build_epub.py XX`
3. Gerar PDF: `python3 build_pdf.py XX`
4. Publicar: `python3 kdp_publish_lang.py XX`

## CONTA KDP
- **Email**: standardbitcoin.io@gmail.com
- **Senha**: HaylaHorse20@
- **ASIN EN**: A1M3B0MAA1KRQ (PUBLICADO — em revisão desde 30 Mar)
- **ASIN PT**: AXQR3EQ9UQXCU (rascunho, bloqueado banco)
- **ASIN ES**: A2BLSW5PLF9EF7 (rascunho — Details incompleto: FALTAM CATEGORIAS)
- **Tipo**: Pessoa Física (PF)
- **Nome**: WAGNER RUBENS DO NASCIMENTO MOURA
- **CPF**: 22398943852
- **W-8BEN**: Ref A03730261AJ26J8KT5R0R (30% retenção US)
- **Banco**: Brasil *****218
- **Tax**: PROCESSADO (email 30 Mar confirmou)

## SESSION 78 — LIÇÕES NOVAS (31 Mar 2026)

### 13. KDP Categorias — NÃO é dropdown, é SEARCH INPUT (CORRIGIDO Session 83)
- **ERRO ORIGINAL**: Tentou usar `<select>` e `<option>` para categorias
- **CAUSA REAL**: Os `<select>` na página são para IDIOMA, ROLE AUTOR, FAIXA ETÁRIA, LOJA
- **O CAMPO CATEGORIAS é um INPUT DE BUSCA com autocomplete** (não aparece nos `<select>`)
- **COMO FUNCIONA**: Campo com "Escolha até três categorias" → digitar texto → sugestões aparecem → clicar
- **FIX**: Precisa encontrar o input de categorias, digitar texto como "Computação" ou "Computer",
  esperar sugestões, e clicar na sugestão correta
- **REGRA**: Categorias KDP = search autocomplete, NÃO dropdown. Usar ActionChains para digitar+selecionar

### 14. KDP Validation blocks page advance
- **ERRO**: Clicar "Salvar e continuar" não avança — fica na mesma página
- **CAUSA**: Categoria vazia ou conteúdo adulto não respondido bloqueiam silenciosamente
- **FIX**: Verificar TODOS os campos obrigatórios ANTES de clicar Save
- **CHECKLIST Details**: idioma, título, subtítulo, autor, descrição, categorias(>=1), adulto=Não, launch=agora

### 15. Firefox Marionette vs Chrome CDP
- **Marionette port 2828**: Funciona mas `WebDriver:NewSession` abre nova sessão/tab
- **Chrome CDP port 9222**: Mais estável para KDP mas TIMEOUT em máquina lenta (i3 3.3GB)
- **Selenium+Firefox**: Funciona mas abre NOVA instância sem cookies de login
- **MELHOR APPROACH**: Selenium+Firefox com `opts.profile` apontando para perfil existente

### 16. Firefox profile path (CORRIGIDO Session 83)
- **Snap Firefox**: Perfis em `~/snap/firefox/common/.mozilla/firefox/` (NÃO em `~/.mozilla/firefox/`)
- **Profile encontrado**: `3gjtnsc5.default`
- **Selenium**: `opts.profile = os.path.expanduser("~/snap/firefox/common/.mozilla/firefox/3gjtnsc5.default")`
- **Marionette**: Iniciar Firefox com `-profile /path/to/profile --marionette`

## SCRIPTS
- **kdp_nav.py**: CDP client (Chrome port 9222) — 586 lines, testado Session 67-70
- **kdp_publish_lang.py**: Multi-lang publisher (Chrome CDP) — 446 lines, 22 idiomas
- **kdp_firefox_publish.py**: Firefox/Selenium publisher (NEW Session 78) — Selenium, necessita fix categorias
- **KDP_LISTING_ES/FR/DE/IT/NL.md**: Listings preparados para 5 idiomas

## COMANDOS UTEIS
```bash
# Firefox publisher (NOVO — Session 78)
python3 kdp_firefox_publish.py ES A2BLSW5PLF9EF7

# Chrome CDP (alternativa, precisa Chrome rodando)
google-chrome --remote-debugging-port=9222 \
  --user-data-dir=~/.chrome-kdp \
  --no-first-run --disable-gpu --window-size=1280,900 \
  https://kdp.amazon.com/pt_BR/bookshelf &
python3 kdp_publish_lang.py ES

# Listar idiomas disponíveis
python3 kdp_publish_lang.py --list

# Screenshot via CDP
python3 kdp_nav.py screenshot /tmp/kdp.png
```

## PROXIMOS PASSOS (Session 83 — 1 Abr 2026)
1. **FIX categorias ES**: O input de categorias é autocomplete (digitar+selecionar sugestão)
   - Tentar Marionette/Selenium: find input → send_keys "Computação" → wait → click suggestion
2. **Completar ES**: Details (categorias) → Content → Pricing → Publish
3. **Verificar EN**: >48h em revisão, ASIN retorna 404 — pode demorar mais
4. **Verificar PT banco**: Até ~2 Abr (HOJE ou AMANHÃ)
5. **Publicar FR, DE, IT**: Após ES, mesmo fluxo
6. **Script Marionette**: `~/kdp_marionette_es.py` (novo Session 83, mais leve que Selenium)
