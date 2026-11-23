"""
Tests for Data Harvesters across Canada, UK, and EU.
"""

import pytest
from harvesters.canada_harvester import CanadaHarvester
from harvesters.uk_harvester import UKHarvester
from harvesters.eu_harvester import EUHarvester


def test_canada_harvester():
    harvester = CanadaHarvester()
    records = harvester.harvest(limit=50)
    assert len(records) == 50
    for r in records:
        assert r["country"] == "CAN"
        assert r["legal_name"]
        assert r["cage_code"].startswith("L")
        assert len(r["capabilities"]) >= 1
        assert "certifications" in r


def test_uk_harvester():
    harvester = UKHarvester()
    records = harvester.harvest(limit=25)
    assert len(records) == 25
    for r in records:
        assert r["country"] == "GBR"
        assert r["legal_name"]
        assert r["cage_code"].startswith("K")


def test_eu_harvester():
    harvester = EUHarvester()
    records = harvester.harvest(limit=25)
    assert len(records) == 25
    for r in records:
        assert len(r["country"]) == 3
        assert r["legal_name"]
        assert len(r["capabilities"]) >= 1
