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

## Tornado em 2025-02-20 (valor base R$ 42.30, preço R$ 16.43)

| assumption | range_source | low | high | value_at_low | value_at_high | swing |
|---|---|---|---|---|---|---|
| EBIT margin | Gerdau p10–p90 | 0.049 | 0.186 | 1.302 | 49.767 | 48.465 |
| Capex / revenue | Gerdau p10–p90 | 0.031 | 0.083 | 55.885 | 31.983 | 23.902 |
| Revenue growth | Gerdau p10–p90 | -0.139 | 0.223 | 28.051 | 50.296 | 22.245 |
| Tax rate | Gerdau p10–p90 | 0.000 | 0.275 | 54.517 | 40.003 | 14.514 |
| Equity risk premium | test range 4%–7% | 0.040 | 0.070 | 48.221 | 35.699 | 12.522 |
| D&A / revenue | Gerdau p10–p90 | 0.037 | 0.060 | 39.503 | 50.047 | 10.544 |
| Terminal growth | test range ± 1 p.p. | 0.049 | 0.069 | 38.365 | 47.315 | 8.950 |
| Beta | 95% interval of the regression | 0.966 | 1.304 | 45.918 | 39.178 | 6.740 |
| Working capital / revenue | Gerdau p10–p90 | 0.174 | 0.255 | 43.723 | 39.067 | 4.656 |
| Country risk premium | test range 1.5%–4% | 0.015 | 0.040 | 43.634 | 39.607 | 4.027 |
| Credit spread | test range 1%–3% | 0.010 | 0.030 | 42.889 | 40.377 | 2.511 |

## Ciclo do aço em cada data (FRED WPU101, só o que era público na data)

| date | steel_month | steel_ppi | steel_yoy | steel_vs_10y_avg | phase |
|---|---|---|---|---|---|
| 2021-02-25 | 2020-12 | 230.700 | 0.113 | 0.041 | rising |
| 2022-02-24 | 2021-12 | 433.252 | 0.878 | 0.881 | rising |
| 2023-03-02 | 2023-01 | 323.534 | -0.236 | 0.316 | falling |
| 2024-02-21 | 2023-12 | 325.503 | 0.009 | 0.273 | flat |
| 2025-02-20 | 2024-12 | 288.188 | -0.115 | 0.093 | falling |

## Perguntas prováveis da banca

**1. Por que a margem EBIT de 16,5% em 2025 é sustentável se está no percentil 87 do histórico da própria Gerdau, muito acima da mediana de 8,1%?** (EBIT margin)
- Por que é perigosa: A margem atual está perto do topo do ciclo; se ela reverter à mediana, o valor cai drasticamente, e o tornado mostra que essa é a premissa de maior impacto (swing de R$ 48,47).
- Números: Margem 2025 = 0,165 (percentil 0,87); mediana 2010–2024 = 0,081; p90 = 0,186; faixa testada p10–p90 = 0,049–0,186; valor com 0,049 = R$ 1,30 vs R$ 49,77 com 0,186.
- Resposta curta: Reconheço que a margem está alta e é a premissa mais sensível; por isso mostro o cenário de reversão ao p10 (R$ 1,30) e o valor base de R$ 42,30 deve ser lido como condicional ao ciclo atual.

**2. Se o capex/receita subiu de 3,5% para 6,0% e já está no percentil 73, você está assumindo que esse investimento gera crescimento ou apenas que a empresa precisa gastar mais?** (Capex / revenue)
- Por que é perigosa: Capex elevado reduz o FCFF; se não houver contrapartida em crescimento ou margem, o valor estará subestimado, e a sensibilidade é a segunda maior do tornado.
- Números: Capex/receita 2025 = 0,060 (percentil 0,73); mediana histórica = 0,054; p10–p90 = 0,031–0,083; valor com 0,031 = R$ 55,89 e com 0,083 = R$ 31,98 (swing R$ 23,90).
- Resposta curta: O capex atual está acima da mediana, mas dentro da faixa histórica; mantenho a premissa e mostro que, se o investimento for de manutenção/expansão já capitalizada, o valor pode estar conservador, como indica o cenário p10.

**3. Como você justifica crescimento de receita de 11,1% em 2025 se a própria fase do aço é de queda (steel_yoy = -11,5%)?** (Revenue growth)
- Por que é perigosa: Crescer acima do ciclo de preços do aço sem base operacional explícita pode superestimar o fluxo; o crescimento aparece como terceiro maior swing.
- Números: Crescimento 2025 = 0,111 (percentil 0,73); p10 = -0,139; mediana = 0,052; p90 = 0,223; steel_yoy 2025 = -0,115; fase = falling; valor com -0,139 = R$ 28,05 e com 0,223 = R$ 50,30.
- Resposta curta: A premissa reflete a média de longo prazo da fase de expansão recente, não o ciclo de preços de 2024; reconheço o risco e mostro que o valor cai para R$ 28,05 no cenário de contração.

**4. Por que usar 23,5% de alíquota efetiva quando o histórico da Gerdau tem mediana de 15,8% e mínimo zero?** (Tax rate)
- Por que é perigosa: Alíquota efetiva muito volátil (incentivos, prejuízos fiscais, JCP) pode distorcer o FCFF; a premissa atual está acima da mediana e o swing é relevante.
- Números: Tax rate 2025 = 0,235 (percentil 0,73); mediana = 0,158; p10 = 0,000; p90 = 0,275; valor com 0,000 = R$ 54,52 e com 0,275 = R$ 40,00 (swing R$ 14,51).
- Resposta curta: Uso a alíquota efetiva recente por refletir a carga atual, e o limite de 0–34% evita valores absurdos; a faixa p10–p90 mostra que o efeito é moderado.

**5. Por que o prêmio maduro de 5% (ou 4%–7%) é adequado, e como a escolha afeta o ke?** (Equity risk premium)
- Por que é perigosa: A faixa é de teste, não dado observado; combinada com beta e prêmio-país, eleva ou reduz o ke de forma direta e pode mudar a conclusão do valuation.
- Números: Faixa testada 4%–7%; valor com 0,040 = R$ 48,22 e com 0,070 = R$ 35,70 (swing R$ 12,52); preço de mercado R$ 16,43.
- Resposta curta: Trato o prêmio como premissa de teste; mesmo no extremo de 4% o valor fica acima do preço de mercado, o que indica que a conclusão de subvalorização é robusta a essa escolha.

**6. Por que a janela de 5 anos é suficiente para estimar as premissas, dado que o ciclo do aço dura mais de 5 anos?** (Janela de estimação)
- Por que é perigosa: Janela curta captura apenas parte do ciclo; as premissas de 2021 a 2025 podem refletir um período atípico (pico de 2021–2022), enviesando margens e crescimento.
- Números: Datas de 2021 a 2025; steel_vs_10y_avg em 2022 = 0,881 (fase rising); em 2025 = 0,093; histórico completo 2010–2024 usado para percentis.
- Resposta curta: A janela de 5 anos é a que o modelo usa para premissas operacionais, mas os percentis são calculados sobre 2010–2024, o que ancora as premissas no ciclo completo; reconheço o risco de viés do período recente.

**7. Por que o custo da dívida usa Selic futura + spread Baa menos Treasury, e não a despesa financeira contábil?** (Cost of debt)
- Por que é perigosa: O custo contábil inclui variação cambial e não reflete o custo marginal atual; a escolha altera o WACC, mas o swing associado ao spread de crédito é pequeno (R$ 2,51), o que precisa ser explicado.
- Números: Credit spread faixa testada 1%–3%; valor com 0,010 = R$ 42,89 e com 0,030 = R$ 40,38 (swing R$ 2,51); valor base R$ 42,30.
- Resposta curta: O custo marginal de captação é a referência correta para o WACC; o spread tem impacto pequeno no valor, então a escolha do custo contábil não mudaria a conclusão de forma relevante.

---
Gerado por `python -m valuation_gerdau reviewer` · modelo claude-haiku-5-5 · modo demo · chamadas à API 0 · respostas gravadas usadas 8 · custo estimado US$ 0.0000

Texto da IA: todo número foi conferido contra as tabelas que ela recebeu (nenhum inventado), mas um número real ainda pode aparecer ligado à data errada; confira nas tabelas acima.
