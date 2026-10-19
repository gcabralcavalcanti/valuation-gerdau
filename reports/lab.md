# Laboratório econométrico

Valor justo por ação (R$) em cada especificação. Prêmio fixo em 5% quando a dimensão testada não é o prêmio.

| dimension | spec | 2021-02-25 | 2022-02-24 | 2023-03-02 | 2024-02-21 | 2025-02-20 |
|---|---|---|---|---|---|---|
| Beta: regression window | window 5y · beta 10y W raw · ERP 5% · tax effective | 28.0 | 81.1 | 91.1 | 53.7 | 40.1 |
| Beta: regression window | window 5y · beta 2y W raw · ERP 5% · tax effective | 26.1 | 74.9 | 106.7 | 67.6 | 44.6 |
| Beta: regression window | window 5y · beta 3y W raw · ERP 5% · tax effective | 26.9 | 77.8 | 88.8 | 65.7 | 48.7 |
| Beta: regression window | window 5y · beta 5y W raw · ERP 5% · tax effective | 24.6 | 80.6 | 91.4 | 55.1 | 41.5 |
| Beta: return frequency and adjustment | window 5y · beta 5y M raw · ERP 5% · tax effective | 21.2 | 85.7 | 92.3 | 54.8 | 43.5 |
| Beta: return frequency and adjustment | window 5y · beta 5y W blume · ERP 5% · tax effective | 26.9 | 83.2 | 93.2 | 56.2 | 42.4 |
| Beta: return frequency and adjustment | window 5y · beta 5y W raw · ERP 5% · tax effective | 24.6 | 80.6 | 91.4 | 55.1 | 41.5 |
| Equity risk premium | window 5y · beta 5y W raw · ERP 4% · tax effective | 30.5 | 93.1 | 105.1 | 62.5 | 46.2 |
| Equity risk premium | window 5y · beta 5y W raw · ERP 5% · tax effective | 24.6 | 80.6 | 91.4 | 55.1 | 41.5 |
| Equity risk premium | window 5y · beta 5y W raw · ERP 6% · tax effective | 20.4 | 70.9 | 80.7 | 49.2 | 37.7 |
| Equity risk premium | window 5y · beta 5y W raw · ERP 7% · tax effective | 17.1 | 63.1 | 72.1 | 44.4 | 34.5 |
| Equity risk premium | window 5y · beta 5y W raw · ERP historical · tax effective | -261.5 | 1,253.5 | -1,618.6 | 405.6 | 195.2 |
| Estimation window (assumptions and beta) | window 10y · beta 10y W raw · ERP 5% · tax effective | 19.4 | 46.3 | 57.5 | 42.3 | 31.1 |
| Estimation window (assumptions and beta) | window 3y · beta 3y W raw · ERP 5% · tax effective | 31.0 | 88.6 | 123.7 | 87.6 | 26.4 |
| Estimation window (assumptions and beta) | window 5y · beta 5y W raw · ERP 5% · tax effective | 24.6 | 80.6 | 91.4 | 55.1 | 41.5 |
| Estimation window (assumptions and beta) | window 7y · beta 7y W raw · ERP 5% · tax effective | 21.8 | 53.3 | 69.6 | 55.9 | 39.2 |

## A pergunta do TCC: desvio médio (valor/preço − 1) por janela e fase do ciclo do aço

| window | falling | flat | rising |
|---|---|---|---|
| 3 | +190% | +301% | +142% |
| 5 | +181% | +152% | +113% |
| 7 | +137% | +156% | +52% |
| 10 | +92% | +94% | +33% |

## Beta no intervalo de 95% da regressão (cenários do manual do orientador)

| scenario | 2021-02-25 | 2022-02-24 | 2023-03-02 | 2024-02-21 | 2025-02-20 |
|---|---|---|---|---|---|
| β | 24.6 | 80.6 | 91.4 | 55.1 | 41.5 |
| β + 1.96 se | 21.8 | 73.6 | 83.4 | 50.6 | 38.6 |
| β − 1.96 se | 28.1 | 89.0 | 101.0 | 60.5 | 44.9 |

## Leitura

**O que mais move o valor:** A premissa de prêmio de risco de mercado (ERP) domina a amplitude do valor justo: com ERP histórico os valores ficam negativos ou explodem, enquanto ERP de 4% a 7% já move o valor em torno de ±25%. A janela de estimação e a janela de regressão do beta vêm em seguida; a frequência de retorno e o ajuste de Blume quase não alteram o resultado.

- **Equity risk premium** — ERP histórico produz valores absurdos (negativos ou muito acima do preço), tornando essa especificação inutilizável para a pergunta do TCC. Entre 4% e 7%, o valor cai de forma monotônica, mas sem mudar de sinal. (ERP histórico: -261.5 (2021), 1253.5 (2022), -1618.6 (2023), 405.6 (2024), 195.2 (2025); ERP 4%: 30.5 a 105.1; ERP 7%: 17.1 a 72.1; amplitude máxima de 1723.6 em 2023)
- **Estimation window (assumptions and beta)** — A janela de 3 anos gera o valor mais alto em 2023 e a de 10 anos o mais baixo. A amplitude é grande em 2022 e 2023, menor em 2025. (Janela 3y: 31.0 (2021), 88.6 (2022), 123.7 (2023); janela 10y: 19.4, 46.3, 57.5; amplitude: 11.6, 42.3, 66.1, 45.3, 15.1)
- **Beta: regression window** — Dentro da janela de regressão do beta, a variação é moderada. A janela de 2 anos é a mais sensível em 2023, e a de 10 anos é a mais baixa em 2021. (Amplitude: 3.4, 6.2, 17.9, 13.8, 8.7; janela 2y em 2023: 106.7 contra 88.8 da janela 3y)
- **Beta: return frequency and adjustment** — Frequência de retorno e ajuste de Blume quase não alteram o valor; a diferença fica abaixo de R$ 6 em todas as datas. (Amplitude: 5.7, 5.1, 1.8, 1.4, 1.9; mensal em 2021: 21.2 contra semanal 24.6)
- **Thesis question** — A conclusão sobre subvalorização ou sobrevalorização depende do ERP e da janela de estimação, não da escolha de frequência ou ajuste. O intervalo de 95% do beta (±1.96 erro-padrão) não muda o sinal em nenhuma data. (Intervalo beta: 2023 entre 83.4 e 101.0 com central 91.4; 2025 entre 38.6 e 44.9 com central 41.5)

**Opções do autor (ele decide):**

- Fixar ERP em 5% e reportar a sensibilidade a 4% e 7% como faixa — prós: Valores finitos e interpretáveis; a faixa mostra o efeito sem depender de ERP histórico. · contras: Escolha de 5% é arbitrária e precisa de justificativa externa.
- Excluir o ERP histórico e discutir sua instabilidade como resultado — prós: Mostra por que a premissa é frágil e evita leituras enganosas dos valores negativos. · contras: Deixa o leitor sem uma estimativa central alternativa.
- Usar janela de 5 anos como base e reportar 3 e 10 anos como robustez — prós: Janela intermediária e comum na literatura; os extremos ilustram a dependência da janela. · contras: A janela de 3 anos produz valores muito altos em 2023, o que exige discussão.
- Apresentar o intervalo de 95% do beta junto com o ponto central — prós: Mostra a incerteza estatística do beta sem alterar a conclusão de sinal. · contras: A incerteza de ERP e janela é maior que a do beta e pode ficar subestimada.

---
Gerado por `python -m valuation_gerdau lab` · modelo claude-haiku-5-5 · modo demo · chamadas à API 0 · respostas gravadas usadas 7 · custo estimado US$ 0.0000
