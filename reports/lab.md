# Laboratório econométrico

Valor justo por ação (R$) em cada especificação; o resto fica como no modelo do TCC.

| dimension | spec | 2021-02-25 | 2022-02-24 | 2023-03-02 | 2024-02-21 | 2025-02-20 |
|---|---|---|---|---|---|---|
| Beta: regression window | window 5y · beta 10y W raw · ERP us_mature + country · kd rating_spread · tax effective | 28.7 | 73.7 | 87.1 | 53.7 | 40.7 |
| Beta: regression window | window 5y · beta 2y W raw · ERP us_mature + country · kd rating_spread · tax effective | 26.8 | 68.6 | 100.8 | 67.4 | 45.6 |
| Beta: regression window | window 5y · beta 3y W raw · ERP us_mature + country · kd rating_spread · tax effective | 27.7 | 71.1 | 85.1 | 65.6 | 50.1 |
| Beta: regression window | window 5y · beta 5y W raw · ERP us_mature + country · kd rating_spread · tax effective | 25.4 | 73.4 | 87.3 | 55.1 | 42.3 |
| Beta: return frequency and adjustment | window 5y · beta 5y M raw · ERP us_mature + country · kd rating_spread · tax effective | 22.0 | 77.5 | 88.1 | 54.7 | 44.4 |
| Beta: return frequency and adjustment | window 5y · beta 5y W blume · ERP us_mature + country · kd rating_spread · tax effective | 27.6 | 75.5 | 88.9 | 56.1 | 43.2 |
| Beta: return frequency and adjustment | window 5y · beta 5y W raw · ERP us_mature + country · kd rating_spread · tax effective | 25.4 | 73.4 | 87.3 | 55.1 | 42.3 |
| Cost of capital method | window 5y · beta 5y W raw · ERP 5% · kd book · tax effective | 24.6 | 80.6 | 91.4 | 55.1 | 41.5 |
| Cost of capital method | window 5y · beta 5y W raw · ERP brazil_historical · kd book · tax effective | -261.5 | 1,253.5 | -1,618.6 | 405.6 | 195.2 |
| Cost of capital method | window 5y · beta 5y W raw · ERP us_mature + country · kd book · tax effective | 22.3 | 68.3 | 82.4 | 50.6 | 37.4 |
| Cost of capital method | window 5y · beta 5y W raw · ERP us_mature + country · kd rating_spread · tax effective | 25.4 | 73.4 | 87.3 | 55.1 | 42.3 |
| Cost of capital method | window 5y · beta 5y W raw · ERP us_mature · kd rating_spread · tax effective | 30.8 | 88.9 | 99.8 | 60.5 | 46.4 |
| Equity risk premium | window 5y · beta 5y W raw · ERP 4% + country · kd rating_spread · tax effective | 29.1 | 82.6 | 97.5 | 62.4 | 48.2 |
| Equity risk premium | window 5y · beta 5y W raw · ERP 5% + country · kd rating_spread · tax effective | 23.6 | 72.4 | 85.5 | 55.0 | 43.2 |
| Equity risk premium | window 5y · beta 5y W raw · ERP 6% + country · kd rating_spread · tax effective | 19.6 | 64.3 | 76.0 | 49.1 | 39.1 |
| Equity risk premium | window 5y · beta 5y W raw · ERP 7% + country · kd rating_spread · tax effective | 16.6 | 57.7 | 68.3 | 44.3 | 35.7 |
| Equity risk premium | window 5y · beta 5y W raw · ERP us_mature + country · kd rating_spread · tax effective | 25.4 | 73.4 | 87.3 | 55.1 | 42.3 |
| Estimation window (assumptions and beta) | window 10y · beta 10y W raw · ERP us_mature + country · kd rating_spread · tax effective | 19.6 | 41.6 | 53.7 | 41.4 | 30.0 |
| Estimation window (assumptions and beta) | window 3y · beta 3y W raw · ERP us_mature + country · kd rating_spread · tax effective | 33.3 | 79.2 | 118.8 | 92.7 | 30.2 |
| Estimation window (assumptions and beta) | window 5y · beta 5y W raw · ERP us_mature + country · kd rating_spread · tax effective | 25.4 | 73.4 | 87.3 | 55.1 | 42.3 |
| Estimation window (assumptions and beta) | window 7y · beta 7y W raw · ERP us_mature + country · kd rating_spread · tax effective | 23.1 | 49.1 | 65.4 | 55.4 | 39.0 |

## A pergunta do TCC: desvio médio (valor/preço − 1) por janela e fase do ciclo do aço

| window | falling | flat | rising |
|---|---|---|---|
| 3 | +193% | +324% | +127% |
| 5 | +176% | +152% | +100% |
| 7 | +129% | +154% | +46% |
| 10 | +82% | +90% | +23% |

## Beta no intervalo de 95% da regressão (cenários do manual do orientador)

| scenario | 2021-02-25 | 2022-02-24 | 2023-03-02 | 2024-02-21 | 2025-02-20 |
|---|---|---|---|---|---|
| β | 25.4 | 73.4 | 87.3 | 55.1 | 42.3 |
| β + 1.96 se | 22.6 | 67.5 | 80.2 | 50.6 | 39.2 |
| β − 1.96 se | 28.8 | 80.2 | 95.8 | 60.4 | 45.9 |

## Leitura

**O que mais move o valor:** O método de custo de capital (Cost of capital method) é a dimensão que mais move o valor justo, sobretudo pelo prêmio de risco Brasil histórico, que gera valores negativos e extremos. Entre as premissas plausíveis, o prêmio de risco (ERP) vem em seguida, e a janela de estimação é a terceira. A escolha de frequência e ajuste do beta quase não altera o resultado.

- **Cost of capital method** — Com ERP brasileiro histórico, o valor fica negativo em 2021 e 2023 e dispara em 2022; as amplitudes são enormes e tornam o resultado inutilizável para a pergunta do TCC. Usando ERP us_mature + country, o valor cai para a faixa de 37 a 82 R$ por ação, sem inversão de sinal. (ERP brazil_historical: 2021 −261,5; 2022 1253,5; 2023 −1618,6; 2024 405,6; 2025 195,2 (amplitude até 1718,4 em 2023). Com us_mature + country e kd book: 22,3; 68,3; 82,4; 50,6; 37,4.)
- **Equity risk premium** — Cada ponto de ERP desloca o valor de forma relevante e monotônica: ERP maior reduz o valor justo em todas as datas. A variação entre 4% e 7% é grande, e o resultado de us_mature + country fica entre os extremos. (Em 2023 (ERP 4% a 7%): 97,5 a 68,3, amplitude 29,2. Em 2022: 82,6 a 57,7, amplitude 24,8. Em 2025: 48,2 a 35,7, amplitude 12,5.)
- **Estimation window (assumptions and beta)** — A janela de estimação altera o valor de forma importante, mas com padrão irregular: a janela de 10 anos produz os valores mais baixos em quase todas as datas, e a de 3 anos os mais altos. Em 2025 a janela de 3 anos destoa das demais. (Em 2023 (janelas 3y a 10y): 118,8 a 53,7, amplitude 65,1. Em 2022: 79,2 a 41,6, amplitude 37,6. Em 2025: 30,2 a 42,3, amplitude 12,3 (janela 3y em 30,2; 5y em 42,3).)
- **Beta: regression window** — A janela de regressão do beta move o valor, mais em 2023 e 2024 do que nas demais datas. O resultado depende do ponto do ciclo: na fase de alta (2023) a diferença é maior. (Em 2023 (beta 2y a 10y): 100,8 a 85,1, amplitude 15,7. Em 2024: 67,4 a 53,7, amplitude 13,8. Em 2021: amplitude 3,3.)
- **Beta: return frequency and adjustment** — A frequência de retornos e o ajuste de Blume quase não mudam o valor; é a dimensão mais estável. Diferenças só aparecem em 2021 e 2022. (Amplitude: 5,6 em 2021; 4,2 em 2022; 1,6 em 2023; 1,4 em 2024; 2,1 em 2025. Em 2025: mensal 44,4, semanal raw 42,3, Blume 43,2.)

**Opções do autor (ele decide):**

- Usar ERP us_mature + country como base, reportando ERP 4% a 7% como sensibilidade — prós: Evita o resultado instável do ERP brasileiro histórico e mostra como a premissa de risco-país move o valor. · contras: Torna o intervalo de valor mais largo e exige justificar o ERP escolhido.
- Tratar o ERP brazil_historical como caso excluído, descrito apenas no texto — prós: Explica por que o método gera valores negativos e extremos, sem contaminar a conclusão. · contras: Pode ser visto como descarte seletivo se não houver argumento metodológico explícito.
- Reportar a janela de estimação de 5 anos como referência, com 3 e 10 anos como faixa — prós: Mantém o resultado central em uma janela usual e mostra a dependência da janela. · contras: A janela de 10 anos e a de 3 anos dão valores muito distantes em 2023, o que enfraquece a faixa.
- Usar o intervalo de 95% do beta como faixa principal de incerteza da pergunta do TCC — prós: Traz uma medida estatística direta: em 2023 o valor vai de 80,2 a 95,8, e em 2025 de 39,2 a 45,9. · contras: Captura só a incerteza do beta, não a das outras premissas, que são maiores.

---
Gerado por `python -m valuation_gerdau lab` · modelo claude-haiku-5-5 · modo demo · chamadas à API 0 · respostas gravadas usadas 7 · custo estimado US$ 0.0000

Texto da IA: todo número foi conferido contra as tabelas que ela recebeu (nenhum inventado), mas um número real ainda pode aparecer ligado à data errada; confira nas tabelas acima.
