# Segunda analista

**Reconciliação planilha × CVM (dados abertos, DFP consolidada):** 130 de 130 linhas batem (tolerância 0,5%), exercícios 2015–2024.

## Valor justo por ação (R$) com uma escolha diferente por vez
Prêmio de mercado fixo em 5% (o histórico sai negativo, ponto em aberto no TCC).

| variant | 2021-02-25 | 2022-02-24 | 2023-03-02 | 2024-02-21 | 2025-02-20 |
|---|---|---|---|---|---|
| All three | 25.57 | 77.92 | 88.46 | 55.64 | 43.73 |
| Cost of debt = interest on debt (DFC) | 31.08 | 95.18 | 108.08 | 66.80 | 55.94 |
| EBIT without equity income | 24.48 | 79.24 | 87.91 | 52.01 | 38.52 |
| Statutory tax 34% | 21.02 | 68.75 | 79.26 | 49.48 | 36.04 |
| Thesis choices (ERP 5%) | 24.62 | 80.60 | 91.38 | 55.14 | 41.54 |

## Custo da dívida usado

| variant | 2021-02-25 | 2022-02-24 | 2023-03-02 | 2024-02-21 | 2025-02-20 |
|---|---|---|---|---|---|
| All three | 0.067 | 0.067 | 0.067 | 0.067 | 0.067 |
| Cost of debt = interest on debt (DFC) | 0.067 | 0.067 | 0.067 | 0.067 | 0.067 |
| EBIT without equity income | 0.107 | 0.111 | 0.128 | 0.136 | 0.154 |
| Statutory tax 34% | 0.107 | 0.111 | 0.128 | 0.136 | 0.154 |
| Thesis choices (ERP 5%) | 0.107 | 0.111 | 0.128 | 0.136 | 0.154 |

## Parecer

Reconciliação CVM bate em 130 de 130 linhas. O valor justo é muito sensível à escolha do custo da dívida e da alíquota de imposto. As variantes 'All three' e 'EBIT without equity income' têm efeitos pequenos e variáveis.

- **Cost of debt = interest on debt (DFC)** — Usar a despesa de juros da DFC gera custo da dívida fixo em 6,7% em todas as datas, contra 10,7% a 15,4% na tese. O valor justo sobe em todas as datas. Números: Custo da dívida: 0,067 vs 0,107 (2021) até 0,154 (2025). Variação do valor justo: +26,2% (2021), +18,1% (2022), +18,3% (2023), +21,1% (2024), +34,7% (2025).. Causa provável: A tese inclui variação cambial e perdas com derivativos na despesa financeira da DRE; a DFC captura só a despesa de juros sobre dívidas. Ação sugerida: Justificar no TCC por que a despesa financeira total da DRE é o custo da dívida adotado e mostrar a sensibilidade com a variante da DFC.
- **Statutory tax 34%** — Trocar a alíquota efetiva pela alíquota estatutária de 34% reduz o valor justo em todas as datas. Números: Alíquota efetiva na tese: 0,118 (2021), 0,165 (2022), 0,220 (2023), 0,259 (2024), 0,235 (2025). Variação do valor justo: -14,6%, -14,7%, -13,3%, -10,3%, -13,2%.. Causa provável: A alíquota efetiva está abaixo de 34% em todos os anos, o que eleva o NOPAT e o FCFF na tese. Ação sugerida: Explicar a origem da alíquota efetiva (benefícios fiscais, lucro no exterior) e reportar o resultado com 34% como cenário conservador.
- **EBIT without equity income** — Excluir o resultado de equivalência patrimonial do EBIT reduz o valor justo em todas as datas, com efeito crescente no tempo. Números: Variação do valor justo: -0,6% (2021), -1,7% (2022), -3,8% (2023), -5,7% (2024), -7,3% (2025).. Causa provável: O resultado de equivalência patrimonial passa a pesar mais no EBIT dos anos recentes. Ação sugerida: Manter a escolha da tese, mas documentar o peso da equivalência no EBIT de cada ano.
- **All three** — Combinar as três mudanças produz efeito de sinal alternado: pequena alta em 2021, 2024 e 2025 e pequena queda em 2022 e 2023. Números: Variação do valor justo: +3,8% (2021), -3,3% (2022), -3,2% (2023), +0,9% (2024), +5,3% (2025). Custo da dívida fixo em 6,7%.. Causa provável: Os efeitos do custo da dívida, da alíquota e do EBIT se compensam em graus diferentes ao longo dos anos. Ação sugerida: Apresentar a combinação como teste de robustez e não como cenário central, pois o resultado depende de compensações entre escolhas.
- **Reconciliação com a CVM** — Não há divergência entre a planilha e os dados da CVM. Números: 130 de 130 linhas batem, com tolerância de 0,5%.. Causa provável: Não se aplica; a base reconcilia integralmente. Ação sugerida: Registrar a reconciliação completa como evidência de consistência da base no TCC.

---
Gerado por `python -m valuation_gerdau second_analyst` · modelo claude-haiku-5-5 · modo demo · chamadas à API 0 · respostas gravadas usadas 6 · custo estimado US$ 0.0000
