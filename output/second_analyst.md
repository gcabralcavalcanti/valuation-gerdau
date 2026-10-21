# Segunda analista

**Reconciliação planilha × CVM (dados abertos, DFP consolidada):** 130 de 130 linhas batem (tolerância 0,5%), exercícios 2015–2024.

## Valor justo por ação (R$) com uma escolha diferente por vez
Base: modelo do TCC desde 21/10 (rf = NTN-F − EMBI; custo da dívida = NTN-F + spread Baa; ke com prêmio maduro + λ × EMBI). Cada linha muda uma escolha.

| variant | 2021-02-25 | 2022-02-24 | 2023-03-02 | 2024-02-21 | 2025-02-20 |
|---|---|---|---|---|---|
| All three | 25.47 | 55.55 | 59.36 | 48.85 | 30.20 |
| Cost of debt = interest on debt (DFC) | 30.98 | 69.28 | 73.63 | 58.89 | 39.27 |
| EBIT without equity income | 24.91 | 56.14 | 59.71 | 47.97 | 28.70 |
| No country risk (lambda = 0) | 30.35 | 66.64 | 68.55 | 55.51 | 33.29 |
| Statutory tax 34% | 21.33 | 47.98 | 53.19 | 45.35 | 26.42 |
| Thesis model (21/10) | 25.06 | 57.13 | 62.13 | 50.88 | 31.01 |

## Custo da dívida usado

| variant | 2021-02-25 | 2022-02-24 | 2023-03-02 | 2024-02-21 | 2025-02-20 |
|---|---|---|---|---|---|
| All three | 0.067 | 0.067 | 0.067 | 0.067 | 0.067 |
| Cost of debt = interest on debt (DFC) | 0.067 | 0.067 | 0.067 | 0.067 | 0.067 |
| EBIT without equity income | 0.103 | 0.134 | 0.152 | 0.124 | 0.159 |
| No country risk (lambda = 0) | 0.103 | 0.134 | 0.152 | 0.124 | 0.159 |
| Statutory tax 34% | 0.103 | 0.134 | 0.152 | 0.124 | 0.159 |
| Thesis model (21/10) | 0.103 | 0.134 | 0.152 | 0.124 | 0.159 |

## Parecer

Reconciliação com a CVM bate em 130 de 130 linhas, sem divergências. Os valores justos do modelo da tese variam de 25,06 a 62,13 por ação. Escolhas de custo da dívida e de lambda geram as maiores variações; o prêmio-país é o principal driver do valor justo.

- **Reconciliação com a CVM**: Nenhuma divergência entre planilha e CVM. Números: 130 de 130 linhas batem (tolerância 0,5%).. Causa provável: Não há diferença identificada na base. Ação sugerida: Manter a reconciliação como evidência de consistência da base; nenhuma ação corretiva necessária.
- **No country risk (lambda = 0)**: Remover o risco-país do ke aumenta o valor justo em todas as datas. Números: Variação de +21,1% (2021), +16,6% (2022), +10,3% (2023), +9,1% (2024), +7,4% (2025). Custo da dívida do modelo da tese: 10,3%, 13,4%, 15,2%, 12,4%, 15,9%.. Causa provável: Lambda multiplica o EMBI+ no ke; com lambda zero, o ke cai e o valor justo sobe, com maior efeito nos anos de EMBI mais alto. Ação sugerida: Justificar a escolha de lambda pela fatia da receita no Brasil e testar a faixa do prêmio-país (1,5%–4%) explicitamente no texto.
- **Cost of debt = interest on debt (DFC)**: Trocar o custo da dívida pela despesa de juros da DFC eleva o valor justo, e o custo fica fixo em 6,7% em todas as datas. Números: Variação de +23,6% (2021), +21,3% (2022), +18,5% (2023), +15,7% (2024), +26,6% (2025). Custo da dívida do modelo da tese: 10,3% a 15,9%, contra 6,7% na variante.. Causa provável: A despesa de juros da DFC é despesa e não custo de captação atual; o modelo da tese usa NTN-F + spread Baa − Treasury, que captura o custo atual. Ação sugerida: Manter o custo de mercado como base e apresentar a variante DFC apenas como sensibilidade, explicando que ela subestima o custo de captação.
- **EBIT without equity income**: Excluir o resultado de equivalência patrimonial do EBIT reduz o valor justo, com efeito crescente ao longo do tempo. Números: Variação de −0,6% (2021), −1,7% (2022), −3,9% (2023), −5,7% (2024), −7,4% (2025).. Causa provável: Parte do lucro operacional vem de participações não consolidadas no EBIT; retirá-la reduz o fluxo operacional projetado. Ação sugerida: Documentar a fronteira entre EBIT operacional e equivalência patrimonial e justificar a inclusão ou exclusão.
- **Statutory tax 34%**: Usar a alíquota estatutária de 34% no lugar da alíquota efetiva reduz o valor justo. Números: Variação de −14,9% (2021), −16,0% (2022), −14,4% (2023), −10,9% (2024), −14,8% (2025). Tax rate efetiva da tese: 11,8%, 16,5%, 22,0%, 25,9%, 23,5%.. Causa provável: A alíquota efetiva da Gerdau fica abaixo de 34% por benefícios e incentivos fiscais; a estatutária ignora esse efeito. Ação sugerida: Justificar a alíquota efetiva com os incentivos fiscais identificados no 20-F e reportar a sensibilidade à estatutária.

---
Gerado por `python -m valuation_gerdau second_analyst` · modelo claude-haiku-5-5 · modo demo · chamadas à API 0 · respostas gravadas usadas 6 · custo estimado US$ 0.0000

Texto da IA: todo número foi conferido contra as tabelas que ela recebeu (nenhum inventado), mas um número real ainda pode aparecer ligado à data errada; confira nas tabelas acima.
