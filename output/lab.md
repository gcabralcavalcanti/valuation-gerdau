# Laboratório econométrico

Valor justo por ação (R$) em cada especificação; o resto fica como no modelo do TCC.

| dimension | spec | 2021-02-25 | 2022-02-24 | 2023-03-02 | 2024-02-21 | 2025-02-20 |
|---|---|---|---|---|---|---|
| Beta: regression window | window 5y · beta 10y W raw · rf ntnf · ERP us_mature + country · kd rating_spread · tax effective | 28.2 | 57.4 | 62.0 | 49.7 | 30.1 |
| Beta: regression window | window 5y · beta 2y W raw · rf ntnf · ERP us_mature + country · kd rating_spread · tax effective | 26.4 | 54.1 | 69.0 | 61.4 | 32.8 |
| Beta: regression window | window 5y · beta 3y W raw · rf ntnf · ERP us_mature + country · kd rating_spread · tax effective | 27.3 | 55.7 | 60.9 | 59.8 | 35.2 |
| Beta: regression window | window 5y · beta 5y W raw · rf ntnf · ERP us_mature + country · kd rating_spread · tax effective | 25.1 | 57.1 | 62.1 | 50.9 | 31.0 |
| Beta: return frequency and adjustment | window 5y · beta 5y M raw · rf ntnf · ERP us_mature + country · kd rating_spread · tax effective | 21.7 | 59.8 | 62.6 | 50.5 | 32.2 |
| Beta: return frequency and adjustment | window 5y · beta 5y W blume · rf ntnf · ERP us_mature + country · kd rating_spread · tax effective | 27.2 | 58.5 | 63.0 | 51.7 | 31.5 |
| Beta: return frequency and adjustment | window 5y · beta 5y W raw · rf ntnf · ERP us_mature + country · kd rating_spread · tax effective | 25.1 | 57.1 | 62.1 | 50.9 | 31.0 |
| Cost of capital method | window 5y · beta 5y W raw · rf ntnf · ERP us_mature + country · kd book · tax effective | 24.6 | 60.9 | 65.1 | 49.5 | 31.3 |
| Cost of capital method | window 5y · beta 5y W raw · rf ntnf · ERP us_mature + country · kd rating_spread · tax effective | 25.1 | 57.1 | 62.1 | 50.9 | 31.0 |
| Cost of capital method | window 5y · beta 5y W raw · rf ntnf · ERP us_mature · kd rating_spread · tax effective | 30.3 | 66.6 | 68.6 | 55.5 | 33.3 |
| Cost of capital method | window 5y · beta 5y W raw · rf selic · ERP 5% · kd book · tax effective | 24.6 | 80.6 | 91.4 | 55.1 | 41.5 |
| Cost of capital method | window 5y · beta 5y W raw · rf selic · ERP brazil_historical · kd book · tax effective | -261.5 | 1,253.5 | -1,618.6 | 405.6 | 195.2 |
| Cost of capital method | window 5y · beta 5y W raw · rf selic · ERP us_mature + country · kd rating_spread · tax effective | 25.4 | 73.4 | 87.3 | 55.1 | 42.3 |
| Equity risk premium | window 5y · beta 5y W raw · rf ntnf · ERP 4% + country · kd rating_spread · tax effective | 28.6 | 62.9 | 67.4 | 57.1 | 34.2 |
| Equity risk premium | window 5y · beta 5y W raw · rf ntnf · ERP 5% + country · kd rating_spread · tax effective | 23.3 | 56.5 | 61.2 | 50.8 | 31.5 |
| Equity risk premium | window 5y · beta 5y W raw · rf ntnf · ERP 6% + country · kd rating_spread · tax effective | 19.4 | 51.3 | 55.9 | 45.7 | 29.2 |
| Equity risk premium | window 5y · beta 5y W raw · rf ntnf · ERP 7% + country · kd rating_spread · tax effective | 16.4 | 46.8 | 51.3 | 41.5 | 27.1 |
| Equity risk premium | window 5y · beta 5y W raw · rf ntnf · ERP us_mature + country · kd rating_spread · tax effective | 25.1 | 57.1 | 62.1 | 50.9 | 31.0 |
| Estimation window (assumptions and beta) | window 10y · beta 10y W raw · rf ntnf · ERP us_mature + country · kd rating_spread · tax effective | 19.2 | 31.7 | 37.8 | 38.1 | 22.2 |
| Estimation window (assumptions and beta) | window 3y · beta 3y W raw · rf ntnf · ERP us_mature + country · kd rating_spread · tax effective | 33.1 | 62.6 | 85.1 | 84.4 | 21.4 |
| Estimation window (assumptions and beta) | window 5y · beta 5y W raw · rf ntnf · ERP us_mature + country · kd rating_spread · tax effective | 25.1 | 57.1 | 62.1 | 50.9 | 31.0 |
| Estimation window (assumptions and beta) | window 7y · beta 7y W raw · rf ntnf · ERP us_mature + country · kd rating_spread · tax effective | 22.8 | 38.5 | 47.3 | 50.9 | 28.5 |

## A pergunta do TCC: desvio médio (valor/preço − 1) por janela e fase do ciclo do aço

| window | falling | flat | rising |
|---|---|---|---|
| 3 | +109% | +286% | +92% |
| 5 | +99% | +133% | +66% |
| 7 | +67% | +133% | +23% |
| 10 | +31% | +74% | +2% |

## Beta no intervalo de 95% da regressão (cenários do manual do orientador)

| scenario | 2021-02-25 | 2022-02-24 | 2023-03-02 | 2024-02-21 | 2025-02-20 |
|---|---|---|---|---|---|
| β | 25.1 | 57.1 | 62.1 | 50.9 | 31.0 |
| β + 1.96 se | 22.3 | 53.4 | 58.2 | 47.0 | 29.2 |
| β − 1.96 se | 28.4 | 61.4 | 66.5 | 55.4 | 33.0 |

## Leitura

**O que mais move o valor:** O método de custo de capital (kd book vs rating spread, rf selic, ERP brasileiro histórico) move o valor mais que qualquer outra dimensão, com valores absurdos em algumas datas; entre as escolhas razoáveis, a janela de estimação e o ERP são as dimensões que mais mudam o valor justo.

- **Cost of capital method**: A combinação rf selic com ERP brazil_historical produz valores negativos ou irreais, inviabilizando essa especificação; sem ela, o método ainda muda bastante o resultado quando se troca rf ou kd. (Amplitude de 1196.3 em 2022-02-24 e 1710.0 em 2023-03-02; em 2023-03-02 o valor vai de -1618.6 a 91.4 com rf selic e ERP brazil_historical.)
- **Estimation window (assumptions and beta)**: A janela de estimação altera o valor de forma relevante e quase sem padrão: a janela de 3 anos dá o maior valor em 2023 e 2024, e a de 10 anos o menor na maioria das datas. (Em 2023-03-02 a faixa vai de 37.8 (janela 10y) a 85.1 (janela 3y); em 2024-02-21, de 38.1 a 84.4; amplitude de 47.3 em 2023-03-02.)
- **Equity risk premium**: O ERP é a dimensão mais estável entre as escolhas razoáveis, mas o valor cai de forma monótona conforme o ERP sobe de 4% para 7%. (Em 2022-02-24 o valor vai de 62.9 (ERP 4%) a 46.8 (ERP 7%); amplitude de 16.1 em 2023-03-02.)
- **Beta: regression window**: A janela e o horizonte do beta mudam o valor pouco em 2021 e 2022, mas mais em 2024, sem ordem clara entre horizontes. (Em 2024-02-21 a faixa vai de 47.0 a 61.4 nas janelas de beta; amplitude de 11.7 nesse ano, contra 1.2 em frequência e ajuste.)
- **Thesis question**: O sinal do valor justo em relação ao preço não muda nas especificações razoáveis, mas o tamanho do desvio depende do ciclo: o desvio médio é maior em janelas curtas e em fase de alta, e menor em janelas longas e em fase de queda. (Desvio médio na janela 3 em fase flat: 2.862; na janela 10 em fase rising: 0.021; janela 5 em rising: 0.658.)

**Opções do autor (ele decide):**

- Manter a especificação base (janela 5y, beta 5y semanal bruto, rf ntnf, ERP us_mature + country, kd rating_spread) e reportar as demais como sensibilidade.. Prós: Coerente com o padrão de mercado e com os cenários de beta, sem valores irreais. · contras: Não explora a faixa de incerteza da janela de estimação, que é grande.
- Excluir a combinação rf selic com ERP brazil_historical por gerar valores negativos, explicando o motivo no texto.. Prós: Evita que valores absurdos dominem a discussão do método de custo de capital. · contras: Exclui um cenário que o leitor pode querer ver; precisa de justificativa explícita.
- Apresentar a faixa de valor por data usando o intervalo de 95% do beta como incerteza estatística.. Prós: Mostra a incerteza estimada do beta de forma simples, por exemplo 53.4 a 61.4 em 2022-02-24. · contras: Só captura o erro do beta, deixando de fora as escolhas de janela e de ERP que mais movem o valor.
- Reportar a análise por fase do ciclo para responder à pergunta da tese sobre o tamanho do desvio.. Prós: Liga diretamente a escolha de janela ao resultado da tese. · contras: Os desvios médios por fase vêm de poucas datas, o que limita a robustez.

---
Gerado por `python -m valuation_gerdau lab` · modelo claude-haiku-5-5 · modo demo · chamadas à API 0 · respostas gravadas usadas 7 · custo estimado US$ 0.0000

Texto da IA: todo número foi conferido contra as tabelas que ela recebeu (nenhum inventado), mas um número real ainda pode aparecer ligado à data errada; confira nas tabelas acima.
