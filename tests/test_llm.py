"""The API wrapper: schema checks, retry, recording cache, call cap, demo mode. A fake client stands in for the API."""
import json
from types import SimpleNamespace

import pytest

from valuation_gerdau import llm as llm_mod
from valuation_gerdau.llm import LLM, BudgetExceeded, NoRecording

SCHEMA = {"type": "object", "additionalProperties": False, "required": ["x"], "properties": {"x": {"type": "number"}}}


class FakeMessages:
    def __init__(self, answers):
        self.answers = list(answers)
        self.calls = []

    def create(self, **kw):
        self.calls.append(kw)
        text = self.answers.pop(0)
        return SimpleNamespace(stop_reason="end_turn", content=[SimpleNamespace(type="text", text=text)],
                               usage=SimpleNamespace(input_tokens=100, output_tokens=10))


def make(tmp_path, answers, max_calls=5):
    m = LLM(mode="demo", max_calls=max_calls, recordings=tmp_path / "rec", log_dir=tmp_path / "logs")
    m.mode = "live"
    m._client = SimpleNamespace(messages=FakeMessages(answers))
    return m


def test_valid_answer_is_recorded_and_reused(tmp_path):
    m = make(tmp_path, ['{"x": 1}'])
    assert m.ask("t", "sys", "p", SCHEMA) == {"x": 1}
    assert m.ask("t", "sys", "p", SCHEMA) == {"x": 1}          # same request: no second call
    assert len(m._client.messages.calls) == 1 and m.cache_hits == 1
    # the request carries the cost controls
    kw = m._client.messages.calls[0]
    assert kw["model"] == "claude-haiku-5-5" and kw["max_tokens"] <= 2000
    assert kw["output_config"]["format"]["schema"] == SCHEMA


def test_schema_failure_retries_with_feedback(tmp_path):
    m = make(tmp_path, ['{"x": "one"}', '{"x": 1}'])
    assert m.ask("t", "sys", "p", SCHEMA) == {"x": 1}
    assert "rejected by the checker" in m._client.messages.calls[1]["messages"][0]["content"]


def test_semantic_check_failure_raises_after_retries(tmp_path):
    m = make(tmp_path, ['{"x": 1}', '{"x": 1}'])
    with pytest.raises(ValueError):
        m.ask("t", "sys", "p", SCHEMA, check=lambda a: ["x must be 2"] if a["x"] != 2 else [])
    assert not list((tmp_path / "rec").glob("*.json"))      # bad answers are never recorded


def test_call_cap(tmp_path):
    m = make(tmp_path, ['{"x": 1}', '{"x": 2}'], max_calls=1)
    m.ask("a", "sys", "p1", SCHEMA)
    with pytest.raises(BudgetExceeded):
        m.ask("b", "sys", "p2", SCHEMA)


def test_demo_mode_replays_or_stops(tmp_path, monkeypatch):
    monkeypatch.setattr(llm_mod, "_load_key", lambda: None)
    live = make(tmp_path, ['{"x": 3}'])
    live.ask("t", "sys", "p", SCHEMA)
    demo = LLM(mode="auto", recordings=tmp_path / "rec", log_dir=tmp_path / "logs")
    assert demo.mode == "demo"
    assert demo.ask("t", "sys", "p", SCHEMA) == {"x": 3}
    with pytest.raises(NoRecording):
        demo.ask("t", "sys", "another prompt", SCHEMA)


def test_log_is_json_lines_with_tokens(tmp_path):
    m = make(tmp_path, ['{"x": 1}'])
    m.ask("t", "sys", "p", SCHEMA)
    lines = [json.loads(l) for l in m.log_path.read_text(encoding="utf-8").splitlines()]
    assert lines[0]["input_tokens"] == 100 and lines[0]["source"] == "api"
    assert m.cost_usd() == pytest.approx((100 * 0.10 + 10 * 0.50) / 1e6)
