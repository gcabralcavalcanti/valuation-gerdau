# Revisora de premissas

## Premissas usadas (janela de 5 anos)

| assumption | 2021-02-25 | 2022-02-24 | 2023-03-02 | 2024-02-21 | 2025-02-20 |
|---|---|---|---|---|---|
| Capex / revenue | 0.035 | 0.036 | 0.042 | 0.052 | 0.060 |
| D&A / revenue | 0.055 | 0.048 | 0.044 | 0.044 | 0.043 |
| EBIT margin | 0.074 | 0.117 | 0.148 | 0.159 | 0.165 |
| Revenue growth | 0.001 | 0.158 | 0.174 | 0.083 | 0.111 |
| Tax rate | 0.118 | 0.165 | 0.220 | 0.259 | 0.235 |
| Working capital / revenue | 0.181 | 0.176 | 0.179 | 0.184 | 0.199 |

## Onde cada premissa está no histórico da própria Gerdau (percentil; 0 = mínimo, 1 = máximo)

| assumption | 2021-02-25 | 2022-02-24 | 2023-03-02 | 2024-02-21 | 2025-02-20 |
|---|---|---|---|---|---|
| Capex / revenue | 0.18 | 0.17 | 0.38 | 0.50 | 0.73 |
| D&A / revenue | 0.55 | 0.25 | 0.23 | 0.29 | 0.20 |
| EBIT margin | 0.45 | 0.92 | 0.85 | 0.86 | 0.87 |
| Revenue growth | 0.27 | 0.75 | 0.77 | 0.64 | 0.73 |
| Tax rate | 0.64 | 0.58 | 0.62 | 0.79 | 0.73 |
| Working capital / revenue | 0.27 | 0.17 | 0.15 | 0.36 | 0.40 |

## Tornado em 2025-02-20 (valor base R$ 31.01, preço R$ 16.43)

| assumption | range_source | low | high | value_at_low | value_at_high | swing |
|---|---|---|---|---|---|---|
| EBIT margin | Gerdau p10–p90 | 0.049 | 0.186 | 0.282 | 36.603 | 36.321 |
| Capex / revenue | Gerdau p10–p90 | 0.031 | 0.083 | 41.188 | 23.275 | 17.913 |
| Revenue growth | Gerdau p10–p90 | -0.139 | 0.223 | 21.024 | 36.582 | 15.558 |
| Tax rate | Gerdau p10–p90 | 0.000 | 0.275 | 39.915 | 29.321 | 10.594 |
| D&A / revenue | Gerdau p10–p90 | 0.037 | 0.060 | 28.911 | 36.813 | 7.902 |
| Equity risk premium | test range 4%–7% | 0.040 | 0.070 | 34.239 | 27.146 | 7.093 |
| Terminal growth | test range ± 1 p.p. | 0.049 | 0.069 | 28.881 | 33.554 | 4.673 |
| Working capital / revenue | Gerdau p10–p90 | 0.174 | 0.255 | 32.250 | 28.184 | 4.066 |
| Beta | 95% interval of the regression | 0.966 | 1.304 | 33.006 | 29.216 | 3.790 |
| Country risk premium | test range 1.5%–4% | 0.015 | 0.040 | 31.753 | 29.466 | 2.287 |
| Credit spread | test range 1%–3% | 0.010 | 0.030 | 31.337 | 29.911 | 1.426 |

## Ciclo do aço em cada data (FRED WPU101, só o que era público na data)

| date | steel_month | steel_ppi | steel_yoy | steel_vs_10y_avg | phase |
|---|---|---|---|---|---|
| 2021-02-25 | 2020-12 | 230.700 | 0.113 | 0.041 | rising |
| 2022-02-24 | 2021-12 | 433.252 | 0.878 | 0.881 | rising |
| 2023-03-02 | 2023-01 | 323.534 | -0.236 | 0.316 | falling |
| 2024-02-21 | 2023-12 | 325.503 | 0.009 | 0.273 | flat |
| 2025-02-20 | 2024-12 | 288.188 | -0.115 | 0.093 | falling |

## Perguntas prováveis da banca

**1. Por que a margem EBIT vai de 7,4% em 2021 a 16,5% em 2025, quando o histórico da Gerdau tem mediana de 8,1% e p90 de 18,6%? Você está assumindo que o pico do ciclo é o novo normal?** (EBIT margin)
- Por que é perigosa: A margem é a premissa de maior peso no tornado (swing de R$ 36,3), e a data de 2025 está no percentil 0,87, em região de ciclo alto. Se a margem reverter à mediana, o valor cai drasticamente.
- Números: Margem 2025 = 16,5% (percentil 0,87); mediana histórica 8,1%; p10–p90 = 4,9%–18,6%; valor em 4,9% = R$ 0,28 vs base R$ 31,01 e em 18,6% = R$ 36,60.
- Resposta curta: A margem foi limitada ao p10–p90 histórico, mas a base usa 16,5%, acima da mediana. Reconheço que o resultado é muito sensível a essa premissa e apresento o cenário com margem mediana como teste de robustez.

**2. Como você justifica crescimento de receita de 11,1% em 2025 se o ciclo do aço está em queda (steel_yoy -11,5%, fase falling)?** (Revenue growth)
- Por que é perigosa: O crescimento usado fica no percentil 0,73 e acima da mediana histórica de 5,2%, o que descola a projeção do ciclo setorial observado.
- Números: Crescimento 2025 = 11,1% (percentil 0,73); mediana histórica 5,2%; p90 22,3%; steel_yoy 2024-12 = -11,5%; valor em -13,9% = R$ 21,02 vs R$ 36,58 em 22,3%.
- Resposta curta: O crescimento de 11,1% reflete a média recente da própria empresa, mas admito que o ciclo indica desaceleração. O tornado mostra que o intervalo p10–p90 move o valor em cerca de R$ 15, o que deve ser comunicado como incerteza.

**3. Por que a alíquota efetiva sobe de 11,8% para 23,5% e por que não usar 34%, a alíquota nominal brasileira?** (Tax rate)
- Por que é perigosa: A alíquota efetiva oscila muito e a escolha afeta o valor. Além disso, a série histórica tem mínimo zero, o que pode refletir benefícios fiscais temporários.
- Números: Tax rate 2025 = 23,5% (percentil 0,73); mediana histórica 15,8%; p90 27,5%; valor em 0% = R$ 39,92 e em 27,5% = R$ 29,32; limite do cálculo 0–34%.
- Resposta curta: Usei a alíquota efetiva observada, limitada a 0–34%, pois reflete benefícios e juros sobre capital próprio. Mostro que o valor varia cerca de R$ 10 entre os extremos do p10–p90 e que o uso de 34% reduziria o valor.

**4. Capex de 6,0% da receita em 2025, no percentil 0,73, é investimento de expansão ou manutenção? Como isso afeta o FCFF?** (Capex / revenue)
- Por que é perigosa: Capex alto reduz o FCFF, mas também pode gerar crescimento; a banca pode questionar se a premissa é coerente com o crescimento e a margem assumidos.
- Números: Capex 2025 = 6,0% (percentil 0,73); mediana histórica 5,4%; p10–p90 = 3,1%–8,3%; valor em 3,1% = R$ 41,19 vs R$ 23,28 em 8,3%; D&A 2025 = 4,3%.
- Resposta curta: O capex acima da D&A indica expansão, o que é coerente com o crescimento usado. Reconheço o risco de dupla contagem entre crescimento alto e capex elevado e mostro o intervalo de R$ 18 no tornado.

**5. Por que o prêmio maduro de 5% e o lambda vinculado ao EMBI não estão contabilizando o risco-país duas vezes?** (Equity risk premium)
- Por que é perigosa: O ke soma prêmio maduro, beta e lambda × EMBI, e a taxa rf já desconta o EMBI. Uma banca pode alegar dupla contagem do risco-país.
- Números: Prêmio maduro faixa 4%–7%; swing no tornado = R$ 7,09 (value_at_low R$ 34,24; value_at_high R$ 27,15); rf = NTN-F − EMBI; prêmio-país faixa 1,5%–4% com swing R$ 2,29.
- Resposta curta: rf é a NTN-F menos o EMBI, então o risco-país sai da taxa livre e volta via lambda × EMBI no ke, sem dupla contagem. Mostro que a sensibilidade ao prêmio maduro é de R$ 7, e que o risco-país tem efeito menor.

**6. A janela de 5 anos é suficiente para capturar a dinâmica do aço? Por que as datas de 2021 e 2022 incluem o boom pós-pandemia?** (Janela de estimação)
- Por que é perigosa: O período inclui o auge de 2021–2022 (steel_vs_10y_avg de 0,88 em 2022) e pode inflar as premissas de margem e crescimento.
- Números: Ciclo: 2022 steel_vs_10y_avg = 0,881 (phase rising); 2025 = 0,093 (falling); margem 2021 = 7,4% vs 2022 = 11,7%; janela de 5 anos em todas as datas.
- Resposta curta: A janela de 5 anos mistura fases de alta e de queda, mas as premissas mudam muito entre 2021 e 2022 justamente pelo ciclo. Reconheço que a estimação é sensível à janela e proponho testar janelas alternativas como robustez.

**7. Por que o custo da dívida usa NTN-F mais spread Baa menos Treasury, e não a despesa financeira contábil da DRE?** (Cost of debt)
- Por que é perigosa: A definição muda de Selic + spread para NTN-F + spread em 20/10. Sem explicar a troca, a banca pode questionar a comparabilidade entre datas e o efeito cambial.
- Números: Cost of debt usa NTN-F + spread Baa − Treasury 10a; spread teste 1%–3% com swing de R$ 1,43 (R$ 31,34 em 1% e R$ 29,91 em 3%); custo contábil = despesa financeira total (inclui variação cambial) / dívida média.
- Resposta curta: Uso o custo de captação atual por ser prospectivo, enquanto o custo contábil mistura variação cambial e dívidas antigas. Mostro que o efeito do spread é pequeno (R$ 1,43) e que a troca de metodologia em 20/10 foi documentada.

---
Gerado por `python -m valuation_gerdau reviewer` · modelo claude-haiku-5-5 · modo demo · chamadas à API 0 · respostas gravadas usadas 8 · custo estimado US$ 0.0000

Texto da IA: todo número foi conferido contra as tabelas que ela recebeu (nenhum inventado), mas um número real ainda pode aparecer ligado à data errada; confira nas tabelas acima.
