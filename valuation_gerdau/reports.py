"""Markdown reports (Portuguese: they are written for the thesis author) plus the raw tables in JSON."""

from __future__ import annotations

import json

import pandas as pd

from . import config


def _pct(x):
    return "" if x is None or pd.isna(x) else f"{x:+.1%}"


def _md(df: pd.DataFrame, floatfmt="{:,.2f}") -> str:
    df = df.copy()
    for c in df.columns:
        if pd.api.types.is_float_dtype(df[c]):
            df[c] = df[c].map(lambda v: "" if pd.isna(v) else floatfmt.format(v))
    cols = [str(c) for c in df.columns]
    lines = ["| " + " | ".join(cols) + " |", "|" + "---|" * len(cols)]
    lines += ["| " + " | ".join(str(v) for v in r) + " |" for r in df.itertuples(index=False)]
    return "\n".join(lines)


def _write(name: str, text: str, data: dict, run_info: dict):
    config.REPORTS.mkdir(parents=True, exist_ok=True)
    footer = (
        f"\n\n---\nGerado por `python -m valuation_gerdau {name}` · modelo {run_info['model']} · "
        f"modo {run_info['mode']} · chamadas à API {run_info['api_calls']} · respostas gravadas usadas "
        f"{run_info['recorded_answers_used']} · custo estimado US$ {run_info['estimated_cost_usd']:.4f}\n"
        f"\nTexto da IA: todo número foi conferido contra as tabelas que ela recebeu (nenhum inventado), mas um "
        f"número real ainda pode aparecer ligado à data errada; confira nas tabelas acima.\n"
    )
    (config.REPORTS / f"{name}.md").write_text(text + footer, encoding="utf-8")
    (config.REPORTS / f"{name}.json").write_text(
        json.dumps(data, ensure_ascii=False, indent=1, default=str), encoding="utf-8"
    )


def auditor(rows, golden_score, run_info):
    df = pd.DataFrame(rows)
    ok = (df["status"] == "match").sum()
    table = df.assign(diff=df["diff"].map(_pct), quote=df["quote"].str.slice(0, 70))[
        ["fiscal_year", "metric", "spreadsheet", "document", "diff", "status", "page", "quote"]
    ]
    text = (
        f"# Auditora de dados\n\nPlanilha × releases de resultados do 4º trimestre (SEC, exhibit 99). "
        f"**{ok} de {len(df)} números batem** (tolerância 1%). Cada número traz a página e a linha copiada "
        f"do documento; o código confere que a linha está mesmo na página citada.\n\n"
        f"Acerto da extração contra os números conferidos à mão pelo autor (golden set): "
        f"**{golden_score['correct']}/{golden_score['cases']}**.\n\n{_md(table, '{:,.1f}')}\n\n"
        f"Fontes: " + " · ".join(sorted({f"[{r['fiscal_year']}]({r['source']})" for r in rows}))
    )
    _write("auditor", text, {"rows": rows, "golden": golden_score}, run_info)


def analyst(res, run_info):
    recon, alt, memo = res["reconciliation"], res["alternatives"], res["memo"]
    ok = (recon["status"] == "match").sum()
    fv = alt.pivot_table(index="variant", columns="date", values="fair_value").round(2).reset_index()
    kd = alt.pivot_table(index="variant", columns="date", values="Cost of debt").round(3).reset_index()
    text = (
        f"# Segunda analista\n\n**Reconciliação planilha × CVM (dados abertos, DFP consolidada):** "
        f"{ok} de {len(recon)} linhas batem (tolerância 0,5%), "
        f"exercícios {recon['year'].min()}–{recon['year'].max()}.\n\n"
        f"## Valor justo por ação (R$) com uma escolha diferente por vez\n"
        f"Base: modelo do TCC desde 19/10 (custo da dívida = Selic esperada + spread Baa; ke com prêmio maduro + "
        f"λ × EMBI). Cada linha muda uma escolha.\n\n{_md(fv)}\n\n"
        f"## Custo da dívida usado\n\n{_md(kd, '{:.3f}')}\n"
    )
    if memo:
        text += f"\n## Parecer\n\n{memo['summary']}\n\n" + "\n".join(
            f"- **{f['topic']}** — {f['what_differs']} Números: {f['numbers']}. Causa provável: "
            f"{f['likely_cause']} Ação sugerida: {f['suggested_action']}"
            for f in memo["findings"]
        )
    _write(
        "second_analyst",
        text,
        {"reconciliation": recon.to_dict("records"), "alternatives": alt.to_dict("records"), "memo": memo},
        run_info,
    )


def lab(res, run_info):
    grid, ci, hyp, summ = res["grid"], res["beta_ci"], res["hypothesis"], res["summary"]
    by = grid.pivot_table(index=["dimension", "spec"], columns="date", values="fair_value").round(1).reset_index()
    ci_table = ci.pivot_table(index="scenario", columns="date", values="fair_value").round(1).reset_index()
    text = (
        f"# Laboratório econométrico\n\nValor justo por ação (R$) em cada especificação; o resto fica como no "
        f"modelo do TCC.\n\n{_md(by, '{:,.1f}')}\n\n"
        f"## A pergunta do TCC: desvio médio (valor/preço − 1) por janela e fase do ciclo do aço\n\n"
        f"{_md(hyp.round(3).reset_index(), '{:+.0%}')}\n\n"
        f"## Beta no intervalo de 95% da regressão (cenários do manual do orientador)\n\n"
        f"{_md(ci_table, '{:,.1f}')}\n"
    )
    if summ:
        text += (
            f"\n## Leitura\n\n**O que mais move o valor:** {summ['what_moves_value_most']}\n\n"
            + "\n".join(f"- **{f['dimension']}** — {f['finding']} ({f['numbers']})" for f in summ["findings"])
            + "\n\n**Opções do autor (ele decide):**\n\n"
            + "\n".join(
                f"- {o['option']} — prós: {o['pros']} · contras: {o['cons']}" for o in summ["options_for_the_author"]
            )
        )
    _write(
        "lab",
        text,
        {
            "grid": grid.to_dict("records"),
            "beta_ci": ci.to_dict("records"),
            "hypothesis": hyp.reset_index().to_dict("records"),
            "summary": summ,
        },
        run_info,
    )


def reviewer(res, run_info):
    hist, torn, cyc, qs = res["history"], res["tornado"], res["cycle"], res["questions"]
    used = hist.pivot_table(index="assumption", columns="date", values="used").round(3).reset_index()
    pct = hist.pivot_table(index="assumption", columns="date", values="percentile_of_used").round(2).reset_index()
    t = torn[["assumption", "range_source", "low", "high", "value_at_low", "value_at_high", "swing"]]
    text = (
        f"# Revisora de premissas\n\n## Premissas usadas (janela de 5 anos)\n\n{_md(used, '{:.3f}')}\n\n"
        f"## Onde cada premissa está no histórico da própria Gerdau (percentil; 0 = mínimo, 1 = máximo)\n\n"
        f"{_md(pct)}\n\n## Tornado — {torn['date'].iloc[0]} (valor base R$ {torn['base_value'].iloc[0]:.2f}, "
        f"preço R$ {torn['price'].iloc[0]:.2f})\n\n{_md(t, '{:,.3f}')}\n\n"
        f"## Ciclo do aço em cada data (FRED WPU101, só o que era público na data)\n\n"
        f"{_md(cyc.round(3), '{:,.3f}')}\n"
    )
    if qs:
        text += "\n## Perguntas prováveis da banca\n\n" + "\n\n".join(
            f"**{i}. {q['question']}** ({q['assumption']})\n- Por que é perigosa: {q['why_it_is_risky']}\n"
            f"- Números: {q['numbers_for_the_answer']}\n- Resposta curta: {q['suggested_answer']}"
            for i, q in enumerate(qs["questions"], 1)
        )
    _write(
        "reviewer",
        text,
        {
            "history": hist.to_dict("records"),
            "tornado": torn.to_dict("records"),
            "cycle": cyc.to_dict("records"),
            "questions": qs,
        },
        run_info,
    )
