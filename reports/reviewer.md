# Revisora de premissas

## Premissas usadas (janela de 5 anos)

| assumption | 2021-02-25 | 2022-02-24 | 2023-03-02 | 2024-02-21 | 2025-02-20 |
|---|---|---|---|---|---|
| Capex / revenue | 0.035 | 0.036 | 0.042 | 0.052 | 0.060 |
| Cost of debt | 0.107 | 0.111 | 0.128 | 0.136 | 0.154 |
| D&A / revenue | 0.055 | 0.048 | 0.044 | 0.044 | 0.043 |
| EBIT margin | 0.074 | 0.117 | 0.148 | 0.159 | 0.165 |
| Revenue growth | 0.001 | 0.158 | 0.174 | 0.083 | 0.111 |
| Tax rate | 0.118 | 0.165 | 0.220 | 0.259 | 0.235 |
| Working capital / revenue | 0.181 | 0.176 | 0.179 | 0.184 | 0.199 |

## Onde cada premissa está no histórico da própria Gerdau (percentil; 0 = mínimo, 1 = máximo)

| assumption | 2021-02-25 | 2022-02-24 | 2023-03-02 | 2024-02-21 | 2025-02-20 |
|---|---|---|---|---|---|
| Capex / revenue | 0.18 | 0.17 | 0.38 | 0.50 | 0.73 |
| Cost of debt | 0.64 | 0.83 | 0.77 | 0.79 | 0.80 |
| D&A / revenue | 0.55 | 0.25 | 0.23 | 0.29 | 0.20 |
| EBIT margin | 0.45 | 0.92 | 0.85 | 0.86 | 0.87 |
| Revenue growth | 0.27 | 0.75 | 0.77 | 0.64 | 0.73 |
| Tax rate | 0.64 | 0.58 | 0.62 | 0.79 | 0.73 |
| Working capital / revenue | 0.27 | 0.17 | 0.15 | 0.36 | 0.40 |

## Tornado — 2025-02-20 (valor base R$ 41.54, preço R$ 16.43)

| assumption | range_source | low | high | value_at_low | value_at_high | swing |
|---|---|---|---|---|---|---|
| EBIT margin | Gerdau p10–p90 | 0.049 | 0.186 | 1.234 | 48.885 | 47.651 |
| Capex / revenue | Gerdau p10–p90 | 0.031 | 0.083 | 54.900 | 31.399 | 23.501 |
| Revenue growth | Gerdau p10–p90 | -0.139 | 0.223 | 27.582 | 49.376 | 21.794 |
| Cost of debt | Gerdau p10–p90 | 0.076 | 0.177 | 54.047 | 38.917 | 15.131 |
| Tax rate | Gerdau p10–p90 | 0.000 | 0.275 | 51.806 | 39.539 | 12.267 |
| Equity risk premium | test range 4%–7% | 0.040 | 0.070 | 46.152 | 34.506 | 11.646 |
| D&A / revenue | Gerdau p10–p90 | 0.037 | 0.060 | 38.793 | 49.160 | 10.367 |
| Terminal growth | test range ± 1 p.p. | 0.049 | 0.069 | 37.745 | 46.363 | 8.618 |
| Beta | 95% interval of the regression | 0.966 | 1.304 | 44.884 | 38.636 | 6.248 |
| Working capital / revenue | Gerdau p10–p90 | 0.174 | 0.255 | 42.955 | 38.337 | 4.618 |

## Ciclo do aço em cada data (FRED WPU101, só o que era público na data)

| date | steel_month | steel_ppi | steel_yoy | steel_vs_10y_avg | phase |
|---|---|---|---|---|---|
| 2021-02-25 | 2020-12 | 230.700 | 0.113 | 0.041 | rising |
| 2022-02-24 | 2021-12 | 433.252 | 0.878 | 0.881 | rising |
| 2023-03-02 | 2023-01 | 323.534 | -0.236 | 0.316 | falling |
| 2024-02-21 | 2023-12 | 325.503 | 0.009 | 0.273 | flat |
| 2025-02-20 | 2024-12 | 288.188 | -0.115 | 0.093 | falling |

## Perguntas prováveis da banca

**1. Por que a margem EBIT de 16,5% em 2025 está no percentil 87 da própria Gerdau, e não é um pico de ciclo que vai reverter?** (EBIT margin)
- Por que é perigosa: A margem atual está acima da mediana histórica de 8,1% e perto do p90 de 18,6%, e o valor do modelo é muito sensível a ela (swing de R$ 47,65 no tornado).
- Números: EBIT margin 2025 = 0,165; mediana 2010–2024 = 0,081; p90 = 0,186; percentil 0,87; ciclo do aço 2025 = falling, steel_vs_10y_avg 0,093.
- Resposta curta: A margem está alta em relação ao histórico, por isso usei o intervalo p10–p90 para testar. Reconheço que um ciclo em queda pode reduzir a margem, e isso aparece como cenário de baixa no tornado.

**2. Por que o capex/receita de 6,0% está no percentil 73, acima da mediana de 5,4%, e isso é sustentável na perpetuidade?** (Capex / revenue)
- Por que é perigosa: O swing é de R$ 23,50, e um capex elevado persistente reduz o FCFF; além disso, a premissa interage com o crescimento terminal.
- Números: Capex/revenue 2025 = 0,060; mediana histórica = 0,054; p90 = 0,083; percentil 0,73; valor com baixo capex = R$ 54,90; com alto capex = R$ 31,40.
- Resposta curta: O capex subiu de 3,5% para 6,0% no período, então usei a mediana histórica como referência e o p10–p90 para o teste. Justifico que o investimento recente em expansão ainda pesa, mas reconheço a incerteza.

**3. Com crescimento de receita de 11,1% no último ano, por que assumir que a janela de 5 anos mantém esse ritmo?** (Revenue growth)
- Por que é perigosa: O crescimento recente está no percentil 73 e o swing é de R$ 21,79; uma média de 5 anos pode estar inflada pelo ciclo de recuperação.
- Números: Revenue growth 2025 = 0,111; mediana histórica = 0,052; p90 = 0,223; p10 = -0,139; swing = R$ 21,79; ciclo do aço em queda (steel_yoy -0,115).
- Resposta curta: O crescimento usado vem da janela de 5 anos, que inclui 2021–2022 de alta. O teste p10–p90 mostra que o valor depende fortemente disso, e cenários de queda estão cobertos pela faixa.

**4. O custo da dívida de 15,4% inclui variação cambial e derivativos; isso não distorce o WACC?** (Cost of debt)
- Por que é perigosa: Cost of debt de 15,4% está acima da mediana de 10,7% e no percentil 80; a definição usa despesa financeira total, não só juros, e o swing é de R$ 15,13.
- Números: Cost of debt 2025 = 0,154; mediana histórica = 0,107; p90 = 0,177; percentil 0,80; despesa de juros (DFC) não está nesta tabela, então não é comparável diretamente.
- Resposta curta: Uso a despesa financeira total da DRE por ser o custo econômico efetivo, mas reconheço que variação cambial infla o número. Por isso o teste p10–p90 cobre valores menores.

**5. Por que a alíquota efetiva de 23,5% é usada, sendo que o limite legal é 34%?** (Tax rate)
- Por que é perigosa: A alíquota efetiva oscila (0,118 em 2021, 0,259 em 2024) e o percentil atual é 0,73; a faixa do histórico vai de 0,000 a 0,317.
- Números: Tax rate 2025 = 0,235; mediana histórica = 0,158; p90 = 0,275; limite do modelo 0–34%; swing = R$ 12,27.
- Resposta curta: A alíquota efetiva reflete benefícios e prejuízos fiscais, então uso o valor observado e o intervalo histórico. Mantenho o limite de 34% como teto metodológico.

**6. Por que o prêmio de mercado está em 5% se a faixa de teste é 4%–7%, sem dado observado?** (Equity risk premium)
- Por que é perigosa: O prêmio é um julgamento não observado; o swing é de R$ 11,65 e o valor muda de R$ 46,15 para R$ 34,51 na faixa.
- Números: Prêmio testado = 5%; faixa 4%–7%; valor em 4% = R$ 46,15; valor em 7% = R$ 34,51; preço de mercado = R$ 16,43.
- Resposta curta: 5% é o ponto central da faixa de teste, não um dado. Mostro o valor em toda a faixa e deixo explícito que a conclusão depende dessa escolha.

**7. O beta de 1,0 a 1,3 vem de uma regressão com janela curta; ela representa o risco atual da Gerdau?** (Beta)
- Por que é perigosa: A estimativa tem intervalo de confiança de 95% e a janela de estimação pode não refletir mudanças de alavancagem; o swing é de R$ 6,25.
- Números: Beta intervalo 95% = 0,966 a 1,304; valor em beta 0,966 = R$ 44,88; em beta 1,304 = R$ 38,64; valor base = R$ 41,54.
- Resposta curta: Uso o intervalo de confiança da regressão para medir a incerteza do beta. O impacto no valor é menor que o do prêmio e do crescimento, o que indica robustez relativa.

---
Gerado por `python -m valuation_gerdau reviewer` · modelo claude-haiku-5-5 · modo demo · chamadas à API 0 · respostas gravadas usadas 8 · custo estimado US$ 0.0000
