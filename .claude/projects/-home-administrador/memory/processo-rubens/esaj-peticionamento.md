# e-SAJ Peticionamento — Regras Aprendidas (atualizado 03/04/2026)

## STATUS CADASTRAMENTO e-SAJ (03/04/2026 14:00)
| # | Peticao | Codigo | UUID | Sistema | Status |
|---|---------|--------|------|---------|--------|
| 1 | Gratuidade | 8014 | 34d92458-317d-442e-bce1-de683015ee67 | petpg 1G | **AGUARDANDO ASSINATURA E ENVIO (17)** |
| 2 | Manifestacao | 8014 | 367961d0-d381-4764-95bc-f341f713bb76 | petpg 1G | **AGUARDANDO ASSINATURA E ENVIO (17)** |
| 3 | Excecao Pre-Exec | 8318 | 56d85a2a-2dd6-446c-96cf-be1b24fc4fee | petpg 1G | **AGUARDANDO ASSINATURA E ENVIO (17)** |
| 4 | Impugnacao 525 | 8045 | fb2ddc4d-bcdf-4007-ab25-5856c0fad397 | petpg 1G | Em cadastramento (14) - CLASSE ERRADA |
| 5 | Agravo Instrumento | 2023 | ad6f4159-49b1-481a-b8bb-2776f1209857 | **petsg 2G** | **AGUARDANDO ASSINATURA E ENVIO (17)** |
| 6 | Rescisoria | 47 | - | petsg 2G | NAO CADASTRADA (prazo ate 01/07/2027) |

## DOCUMENTOS CADASTRADOS POR PETICAO
### 1-Gratuidade (6 docs) - COMPLETA + CNH
- [Peticao 9500] PETICAO_GRATUIDADE_V2_20260402.pdf (134KB otimizado)
- [Justica Gratuita 9503] DECLARACAO_HIPOSSUFICIENCIA_WAGNER_20260402.pdf (39KB)
- [Justica Gratuita 9503] DECLARACAO_HIPOSSUFICIENCIA_VIVIANE_20260402.pdf (38KB)
- [Docs Sigilosos 9898] NU_240542121_01ABR2026_01ABR2026.pdf (18KB) - Extrato Wagner
- [Docs Sigilosos 9898] NU_642549898_01ABR2026_01ABR2026.pdf (18KB) - Extrato Viviane
- [Docs Sigilosos] CNH_WAGNER_E_VIVIANE_20260403.pdf (75KB) - CNH casal

### 2-Manifestacao (2 docs) - COMPLETA + CNH
- [Peticao 9500] MANIFESTACAO_CONTRADICAO_20260402.pdf (29KB)
- [Documento] CNH_WAGNER_E_VIVIANE_20260403.pdf (75KB) - CNH casal

### 3-Excecao (2 docs) - COMPLETA + CNH
- [Peticao 9500] EXCECAO_PRE_EXECUTIVIDADE_20260402.pdf (53KB)
- [Documento] CNH_WAGNER_E_VIVIANE_20260403.pdf (75KB) - CNH casal

### 4-Impugnacao (1 doc) - INCOMPLETA (classe errada)
- [Peticao 9500] IMPUGNACAO_CUMPRIMENTO_20260402.pdf (93KB)
- PROBLEMA: Classe 8045 (38045-Impugnacao ao Cumprimento da Sentenca) sob "Peticoes Diversas"
- CORRETO SERIA: Classe 229 (Incidente Processual)

### 5-Agravo 2G (2 docs) - COMPLETA + CNH
- [Peticao] AGRAVO_INSTRUMENTO_20260403.pdf (152KB - nome Viviane corrigido)
- 4 partes: Wagner+Viviane (Agravantes), Wilson+Sonia (Agravados)
- Liminar: S, Justica Gratuita: S
- Assunto principal: 7691 Inadimplemento
- Outros: 8843 Assistencia Judiciaria Gratuita

## BLOQUEIO UNICO: CERTIFICADO ICP-BRASIL
- 5 peticoes prontas (status 17) mas SEM certificado digital
- API /api/certificado/ retorna [] (nenhum certificado)
- NECESSARIO: e-CPF (A1 ou A3) + extensao Web Signer do Chrome/Firefox

## PRAZOS CRITICOS
- Pagamento art. 523: **08/04/2026** (3 dias uteis de 02/04)
- Impugnacao art. 525: **30/04/2026** (18 dias uteis)
- Rescisoria: ate 01/07/2027

## REGRA FUNDAMENTAL: CADA PECA = UM PROTOCOLO SEPARADO

## CODIGOS CORRETOS PARA ESTE PROCESSO
| Peca | Tipo | Codigo e-SAJ | Classe e-SAJ | Instancia |
|------|------|-------------|-------------|-----------|
| Gratuidade | Intermediaria | 8014 | Peticao Intermediaria | 1G petpg |
| Manifestacao | Intermediaria | 8014 | Peticao Intermediaria | 1G petpg |
| Excecao Pre-Exec | Intermediaria | 8318 | Excecao Pre-Executividade | 1G petpg |
| Impugnacao 525 | Intermediaria | 229* | Incidente Processual | 1G petpg |
| Agravo | **INICIAL** | 2023 | 202-Agravo de Instrumento | **2G petsg** |
| Rescisoria | **INICIAL** | 47 | Acao Rescisoria | **2G petsg** |

*Nota: Impugnacao foi cadastrada como 8045 (38045) sob Peticoes Diversas - INCORRETO.
O correto e 229 como Incidente Processual. Precisa recriar.

## SISTEMAS e-SAJ
- **1G**: esaj.tjsp.jus.br/petpg/ (intermediaria, incidentes)
- **2G**: esaj.tjsp.jus.br/petsg/ (iniciais 2G: Agravo, Rescisoria)
- API 1G: /petpg/api/peticoes/{userId}/{uuid}?instancia=PG
- API 2G: /petsg/api/peticoes/{userId}/{uuid}?instancia=SG
- **PUT retorna 405 no petsg** - dados do 2G sao salvos via POST no salvar

## REGRAS TECNICAS APRENDIDAS (e-SAJ Angular)

### Dropdowns ui-select (1G petpg)
- **CRITICO**: focusser.click() NAO ABRE o dropdown! Usar ArrowDown OBRIGATORIAMENTE
- Sequencia: `focusser.focus()` → `focusser.dispatchEvent(new KeyboardEvent('keydown', {key: 'ArrowDown', keyCode: 40, bubbles: true}))`
- Input busca: `.ui-select-search` fica visivel SOMENTE apos ArrowDown
- IDs importantes: `selectAssuntoPrincipal`, `selectOutrosAssuntos`
- CUIDADO: se dois dropdowns abertos, digita no errado!

### Dropdowns ui-select (2G petsg)
- Mesmo sistema Angular ui-select mas SEM focusser funcional
- Abrir via toggle.click() + search.value + input event
- Alguns dropdowns (Estado civil, Nacionalidade) NAO abrem com JS simples
- Solucao: preencher dados criticos e clicar finalize - campos opcionais sao aceitos

### Campo CPF com ui-mask
- NAO aceita ClipboardEvent paste
- FUNCIONA: CDP `Input.dispatchKeyEvent` para cada digito
- Auto-popula nome, RG, endereco do cadastro do TJ-SP

### Campo Processo com ui-mask (9999999-99.9999.\8.\2\6.9999)
- ClipboardEvent paste FUNCIONA para numero de processo
- Focar no input, dispatchEvent com clipboardData

### Spinner bloqueante
- `<div id="loadFeedback" class="spinner--fullpage spinner--fullpage--show">`
- Remover: `sp.classList.remove('spinner--fullpage--show'); sp.style.display = 'none';`
- APLICAR APOS CADA OPERACAO que faz requisicao

### Formulario de partes (2G petsg)
- Abrir: `document.getElementById('adicionar-polo{ativo|passivo}').click()` → dropdown
- Tipo parte: `<button>` dentro do dropdown-menu (NAO <a>!)
- Fechar/salvar parte: `.recolher-edicao-parte` click → `finalizarEdicaoParte()`
- Cancelar: `.cancelar-edidao-parte` click → `cancelarEdicaoParte()`
- Genero: `#campoGeneroMasc` / `#campoGeneroFem` radio buttons

### Salvar peticao (2G petsg)
- Botoes no footer: links <a> com ng-click
- "Salvar para continuar depois" → `salvarRascunhoPeticao()` (mantem status 14)
- "Salvar para protocolar depois" → `salvarPeticaoProntaParaProtocolar()` (avanca p/ 17)
- "Protocolar" → requer certificado ICP-Brasil
- **CRITICO**: Se "Dados para o processo" estiver em modo edicao (clicou "Informar"),
  campos required ficam vazios e BLOQUEIAM o save silenciosamente!
- **NUNCA** clicar "Informar" antes de salvar - dados ja estao no servidor

### Salvar envia POST (nao PUT)
- POST /petsg/api/peticoes/{userId}/{uuid}
- Body contem TODO o JSON da peticao (classe, assuntos, partes, etc.)
- Partes so sao enviadas no momento do POST de save

### Codigos de tipo de parte (2G)
- 15 = Agravante (polo ativo)
- 16 = Agravado (polo passivo)

### Status de peticao
- 14 = Em cadastramento
- 17 = Aguardando assinatura e envio
- 2 = Protocolada

### Tipos de documento digital
- 9500 = Peticao (obrigatorio)
- 9503 = Justica Gratuita
- 9508 = Declaracao
- 9573 = Certidao
- 9574 = Documento
- 9583 = Contrato
- 9586 = Extrato
- 9898 = Documentos Sigilosos

## ERROS A NUNCA REPETIR
1. NAO cadastrar tudo junto (cada peca = 1 protocolo)
2. NAO usar intermediaria para tudo (Agravo/Rescisoria = INICIAL 2G)
3. NAO aceitar sugestao automatica sem verificar codigo
4. NAO esquecer campo Despesas → Gratuidade (petpg)
5. Impugnacao = INCIDENTE (229), nao Peticao Diversa (38045/8045)
6. NAO clicar "Informar" antes de salvar no petsg (reseta campos required)
7. NAO confiar que partes no UI estao salvas - verificar via API apos save
8. NAO tentar PUT no petsg (retorna 405) - usar POST via botao de salvar
9. Dropdown tipo parte no petsg usa BUTTON, nao <a> link
10. Sempre remover spinner apos cada operacao

## PARTES DO PROCESSO
- Agravante/Requerido: Wagner Rubens do Nascimento Moura (CPF 223.989.438-52, OAB 349784)
- Agravante/Requerida: Viviane Suelen da Silva/Moura (CPF 369.094.768-59)
- Agravado/Exequente: Wilson de Abreu Giglio (CPF 051.041.918-69, M, Casado)
- Agravada/Exequente: Sonia Aparecida Nunes de Matos Giglio (CPF 049.269.938-05, F, Casada)

## DADOS DO SISTEMA
- User ID: 486195
- CPF: 223.989.438-52
- OAB/SP: 349.784
- Processo: 0003216-76.2025.8.26.0362
- Codigo interno: A2000QDIS0000
- Principal: A2000EJH30000 (1004287-67.2023.8.26.0362)

## CUSTAS
- Gratuidade/Impugnacao/Excecao/Manifestacao: ZERO
- Agravo: 15 UFESPs = R$576,30 (ou ZERO c/ gratuidade)
- Rescisoria: 2% + 5% (ou ZERO c/ gratuidade)

## CAIXA POSTAL
- 10 protocolos anteriores no processo principal
- Ultima: 09/02/2025 (WPRO.25.00162399-5)
- Nenhum protocolo no cumprimento (0003216) ainda
