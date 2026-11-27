"""
Tests for Data Harvesters across Canada, USA, UK, and EU.
"""

import pytest
from harvesters.canada_harvester import CanadaHarvester
from harvesters.uk_harvester import UKHarvester
from harvesters.eu_harvester import EUHarvester
from harvesters.usa_harvester import USAHarvester
from pipeline.extractor import RDFTripleExtractor
from pipeline.validator import OntologyValidator


def test_canada_harvester(tmp_path):
    harvester = CanadaHarvester()
    harvester.output_dir = tmp_path
    records = harvester.harvest(limit=25)
    assert len(records) == 25
    for r in records:
        assert r["country"] == "CAN"
        assert r["legal_name"]
        assert r["cage_code"].startswith("L")
        assert len(r["capabilities"]) >= 1
        assert "certifications" in r


def test_uk_harvester(tmp_path):
    harvester = UKHarvester()
    harvester.output_dir = tmp_path
    records = harvester.harvest(limit=25)
    assert len(records) == 14
    for r in records:
        assert r["country"] == "GBR"
        assert r["legal_name"]
        assert r["cage_code"].startswith("K")


def test_eu_harvester(tmp_path):
    harvester = EUHarvester()
    harvester.output_dir = tmp_path
    records = harvester.harvest(limit=25)
    assert len(records) == 14
    for r in records:
        assert len(r["country"]) == 3
        assert r["legal_name"]
        assert len(r["capabilities"]) >= 1


def test_usa_harvester(tmp_path):
    harvester = USAHarvester(output_dir=tmp_path)
    records = harvester.harvest(limit=25)
    assert len(records) == 25
    for r in records:
        assert r["country"] == "USA"
        assert r["legal_name"]
        assert r["cage_code"]
        assert len(r["province"]) == 2
        assert len(r["capabilities"]) >= 1
        assert "certifications" in r


def test_usa_shacl_conformance(tmp_path):
    harvester = USAHarvester(output_dir=tmp_path)
    records = harvester.harvest(limit=25)
    extractor = RDFTripleExtractor()
    validator = OntologyValidator()
    g = extractor.build_rdf_graph(records, include_schema=False)
    conforms, report_text, _ = validator.validate_instances(g)
    assert conforms is True, f"USA SHACL validation failed:\n{report_text}"
