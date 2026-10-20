# Segunda analista

**Reconciliação planilha × CVM (dados abertos, DFP consolidada):** 130 de 130 linhas batem (tolerância 0,5%), exercícios 2015–2024.

## Valor justo por ação (R$) com uma escolha diferente por vez
Base: modelo do TCC desde 19/10 (custo da dívida = Selic esperada + spread Baa; ke com prêmio maduro + λ × EMBI). Cada linha muda uma escolha.

| variant | 2021-02-25 | 2022-02-24 | 2023-03-02 | 2024-02-21 | 2025-02-20 |
|---|---|---|---|---|---|
| All three | 22.41 | 63.68 | 78.14 | 50.15 | 38.00 |
| Cost of debt = interest on debt (DFC) | 27.68 | 78.78 | 95.94 | 60.41 | 48.92 |
| EBIT without equity income | 25.28 | 72.11 | 84.03 | 51.95 | 39.22 |
| No country risk (lambda = 0) | 30.85 | 88.91 | 99.78 | 60.50 | 46.44 |
| Statutory tax 34% | 20.96 | 61.00 | 74.84 | 48.93 | 36.06 |
| Thesis model (19/10) | 25.43 | 73.35 | 87.35 | 55.09 | 42.30 |

## Custo da dívida usado

| variant | 2021-02-25 | 2022-02-24 | 2023-03-02 | 2024-02-21 | 2025-02-20 |
|---|---|---|---|---|---|
| All three | 0.067 | 0.067 | 0.067 | 0.067 | 0.067 |
| Cost of debt = interest on debt (DFC) | 0.067 | 0.067 | 0.067 | 0.067 | 0.067 |
| EBIT without equity income | 0.082 | 0.088 | 0.103 | 0.101 | 0.112 |
| No country risk (lambda = 0) | 0.082 | 0.088 | 0.103 | 0.101 | 0.112 |
| Statutory tax 34% | 0.082 | 0.088 | 0.103 | 0.101 | 0.112 |
| Thesis model (19/10) | 0.082 | 0.088 | 0.103 | 0.101 | 0.112 |

## Parecer

Revisão do valuation FCFF/WACC da Gerdau. Reconciliação com a CVM sem divergências (130 de 130 linhas). O valor justo do modelo da tese varia bastante entre datas e as variantes mudam o resultado em sentidos diferentes.

- **Reconciliação com a CVM**: Nenhuma divergência entre planilha e CVM. Números: 130 de 130 linhas batem, tolerância 0,5%.. Causa provável: Não há divergência identificada. Ação sugerida: Manter a reconciliação como está e registrá-la no TCC.
- **Thesis model (19/10)**: Custo da dívida sobe de 8,2% para 11,2% entre 2021 e 2025, enquanto o valor justo cai de 73,4 para 42,3 em 2022-2025. Números: Custo da dívida: 0,082 a 0,112. Valor justo: 25,4 (2021), 73,4 (2022), 87,3 (2023), 55,1 (2024), 42,3 (2025). Preço: 26,03 a 16,43.. Causa provável: Custo da dívida pela fórmula Selic t+4 + spread Baa − Treasury muda com o cenário de juros, o que move o WACC de 11,6% para 14,2%. Ação sugerida: Explicar no texto a sensibilidade do valor justo ao custo da dívida e mostrar o intervalo de WACC.
- **Cost of debt = interest on debt (DFC)**: Custo da dívida fica em 6,7% em todas as datas, abaixo do modelo da tese, e o valor justo sobe em todas as datas. Números: Custo da dívida: 0,067 fixo. Variação do valor justo: +8,9% (2021), +7,4% (2022), +9,8% (2023), +9,7% (2024), +15,6% (2025).. Causa provável: A linha de despesa de juros da DFC não acompanha a variação da taxa de captação usada na tese. Ação sugerida: Justificar a escolha de usar a despesa da DFC ou manter a fórmula da tese, e apresentar as duas como robustez.
- **EBIT without equity income**: Excluir resultado de equivalência patrimonial reduz o valor justo, com efeito crescente ao longo do tempo. Números: Variação do valor justo: −0,6% (2021), −1,7% (2022), −3,8% (2023), −5,7% (2024), −7,3% (2025).. Causa provável: O peso da equivalência patrimonial no EBIT cresce nos anos mais recentes. Ação sugerida: Reportar o efeito separadamente e discutir se o resultado de coligadas deve entrar no fluxo operacional.
- **No country risk (lambda = 0)**: Zerar o prêmio-país aumenta o valor justo, com efeito que diminui de 2021 a 2025. Números: Variação do valor justo: +21,3% (2021), +21,2% (2022), +14,2% (2023), +9,8% (2024), +9,8% (2025).. Causa provável: O prêmio-país pesa mais quando a fatia da receita no Brasil e o EMBI+ estavam mais altos no início da série. Ação sugerida: Apresentar o cálculo com lambda e sem lambda, deixando claro o efeito do risco Brasil no ke.
- **Statutory tax 34%**: Usar a alíquota estatutária de 34% reduz o valor justo em todas as datas, em relação à alíquota efetiva. Números: Alíquota efetiva: 11,8% (2021), 16,5% (2022), 22,0% (2023), 25,9% (2024), 23,5% (2025). Variação do valor justo: −17,5%, −16,8%, −14,3%, −11,2%, −14,7%.. Causa provável: A alíquota efetiva abaixo de 34% gera benefício fiscal que eleva o FCFF. Ação sugerida: Justificar o uso da alíquota efetiva e documentar a fonte dos benefícios fiscais.

---
Gerado por `python -m valuation_gerdau second_analyst` · modelo claude-haiku-5-5 · modo demo · chamadas à API 0 · respostas gravadas usadas 6 · custo estimado US$ 0.0000

Texto da IA: todo número foi conferido contra as tabelas que ela recebeu (nenhum inventado), mas um número real ainda pode aparecer ligado à data errada; confira nas tabelas acima.
