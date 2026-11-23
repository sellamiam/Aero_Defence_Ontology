"""
Tests for Procurement Matching Engine.
"""

import pytest
from matching.engine import MatchingEngine
from matching.models import MatchingCriteria


@pytest.fixture(scope="module")
def engine():
    return MatchingEngine()


def test_matching_benchmarks(engine):
    bench = engine.run_benchmark_scenarios()
    assert bench["all_passed"] is True
    for sc in bench["scenarios"]:
        assert sc["passed"] is True


def test_hard_cgp_filter(engine):
    # Query with CGP required
    crit_cgp = MatchingCriteria(
        query_text="Precision 5-Axis machining for titanium ribs",
        require_controlled_goods=True,
        top_k=20,
    )
    res_cgp = engine.match(crit_cgp)
    assert len(res_cgp.top_matches) > 0
    for m in res_cgp.top_matches:
        assert m.controlled_goods is True


def test_country_filter(engine):
    crit = MatchingCriteria(
        query_text="Combat vehicle design and manufacturing",
        required_country="CAN",
        top_k=10,
    )
    res = engine.match(crit)
    assert len(res.top_matches) > 0
    top = res.top_matches[0]
    assert top.country == "CAN"


def test_leak_proof_geographic_isolation(engine):
    # Query with natural language location constraint "in Ontario"
    crit = MatchingCriteria(
        query_text="Drone motors mid size drones in Ontario",
        top_k=10,
    )
    res = engine.match(crit)
    assert len(res.top_matches) > 0
    for m in res.top_matches:
        assert m.country == "CAN"
        assert m.province == "ON"
        assert m.country != "FRA"
        assert m.country != "GBR"
