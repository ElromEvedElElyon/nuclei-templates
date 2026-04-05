# STATUS DA DEFESA — 03/04/2026 (v5.0 AGRAVO 2G COMPLETO)
# Agente LOBO ativo em /home/administrador/agente-lobo/

## SENTENCA (fls. 157/160)
- **Juiz**: Dr. Fochesato, 20/09/2023
- **DISPOSITIVO**: Rescisao contrato + reintegracao posse + custas + honorarios 10% valor causa
- **CONFIRMA ULTRA PETITA**: NAO existe condenacao em R$470.500
- **Gratuidade INDEFERIDA** na sentenca — renovar com provas novas
- **Citacao**: 05/07/2023 (fls. 78)
- **Despacho taxa 2%**: 13/10/2025 "na inercia, cancele-se"

## STATUS PETICOES e-SAJ (03/04/2026 02:00)

| # | Peticao | UUID | Sistema | Status | Docs |
|---|---------|------|---------|--------|------|
| 1 | Gratuidade | 34d92458 | petpg 1G | **17 AGUARDANDO** | 5 OK |
| 2 | Manifestacao | 367961d0 | petpg 1G | **17 AGUARDANDO** | 1 OK |
| 3 | Excecao | 56d85a2a | petpg 1G | **17 AGUARDANDO** | 1 OK |
| 4 | Impugnacao | fb2ddc4d | petpg 1G | 14 EM CADASTRAMENTO | 1 (classe errada) |
| 5 | **Agravo** | ad6f4159 | **petsg 2G** | **17 AGUARDANDO** | 1 OK + 4 partes |
| 6 | Rescisoria | - | petsg 2G | NAO CADASTRADA | - |

### Detalhes Agravo 2G (SUCESSO 03/04/2026)
- Classe: 202 - Agravo de Instrumento (cd_esaj=2023)
- Secao: Direito Privado 1 e Direito Empresarial
- Assunto principal: 7691 - Inadimplemento
- Outros assuntos: 8843 - Assistencia Judiciaria Gratuita
- Liminar: SIM | Justica Gratuita: SIM
- Partes: Wagner+Viviane (Agravantes) | Wilson+Sonia (Agravados)
- Documento: AGRAVO_INSTRUMENTO_20260402.pdf (152KB otimizado, 13 pags)

### Problema Impugnacao (#4)
- Cadastrada como classe 8045 (38045-Impugnacao) sob "Peticoes Diversas"
- CORRETO: classe 229 (Incidente Processual)
- Precisa RECRIAR com classe correta

## BLOQUEIO UNICO: CERTIFICADO ICP-BRASIL
- 4 peticoes prontas (status 17) mas SEM certificado
- Necessario: e-CPF A1 ou A3 + extensao Web Signer

## PDFs GERADOS (6 peticoes)
| Documento | Pags | Tamanho | Arquivo |
|-----------|------|---------|---------|
| Gratuidade V2 | 11 | 28KB | Peticoes/PETICAO_GRATUIDADE_V2_20260402.pdf |
| Manifestacao | 4 | 7KB | Peticoes/MANIFESTACAO_CONTRADICAO_20260402.pdf |
| Excecao | 15 | 23KB | Peticoes/EXCECAO_PRE_EXECUTIVIDADE_20260402.pdf |
| Impugnacao | 38 | 60KB | Peticoes/IMPUGNACAO_CUMPRIMENTO_20260402.pdf |
| Agravo | 13 | 30KB | Peticoes/AGRAVO_INSTRUMENTO_20260402.pdf |
| Rescisoria | 17 | 24KB | Peticoes/ACAO_RESCISORIA_20260402.pdf |

## DOCUMENTOS SUPORTE
| Documento | Pags | Local |
|-----------|------|-------|
| Declaracao Wagner | 2 | Declaracoes/ |
| Declaracao Viviane | 2 | Declaracoes/ |
| Extrato Nubank Wagner | 1 | Extratos/NU_240542121 |
| Extrato Nubank Viviane | 1 | Extratos/NU_642549898 |
| Relatorio DataJud CNJ | 2 | Dados_Processo/ |
| Relatorio Processual | 2 | Dados_Processo/ |

## PRAZOS CRITICOS
- Pagamento art. 523: **08/04/2026** (3 dias uteis)
- Impugnacao art. 525: **30/04/2026** (18 dias uteis)
- Rescisoria: ate **01/07/2027**

## DADOS DAS PARTES
- Wagner: CPF 223.989.438-52, RG 34.273.080-0, OAB/SP 349.784
- Viviane: CPF 369.094.768-59
- Wilson: CPF 051.041.918-69 (Exequente/Agravado)
- Sonia: CPF 049.269.938-05 (Exequente/Agravada)
- Advogada contraria: Maraliza OAB/SP 321.472, tel (19) 99294-9212

## PROXIMOS PASSOS
1. [CRITICO] Instalar certificado ICP-Brasil para protocolar as 4 peticoes prontas
2. [CRITICO] Corrigir Impugnacao: recriar com classe 229 (Incidente Processual)
3. [URGENTE] Coletar DEFIS/DAS/IRPF para comprovar hipossuficiencia
4. [15 DIAS] Protocolar Impugnacao apos intimacao
5. [FUTURO] Cadastrar Rescisoria no petsg 2G (prazo ate 01/07/2027)

## AGENTE LOBO
- Atalho: lobo (em ~/bin/lobo)
- Repo: /home/administrador/agente-lobo/
- API: /home/administrador/agente-lobo/lobo/services/esaj_api.py
- Knowledge: /home/administrador/agente-lobo/lobo/knowledge/
