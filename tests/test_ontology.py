"""
Tests for W3C OWL 2 Ontology Schema and SHACL Constraint Conformance.
"""

import pytest
from pipeline.validator import OntologyValidator
from pipeline.extractor import RDFTripleExtractor


def test_schema_integrity():
    validator = OntologyValidator()
    report = validator.verify_schema_integrity()
    assert report["is_valid"] is True
    assert report["classes"] >= 30
    assert report["object_properties"] >= 10
    assert report["data_properties"] >= 10
    assert report["total_triples"] >= 300


def test_shacl_sample_conformance():
    validator = OntologyValidator()
    extractor = RDFTripleExtractor()
    import json
    with open("data/processed/normalized_companies.json") as f:
        sample = json.load(f)[:25]

    sample_graph = extractor.build_rdf_graph(sample)
    conforms, report_text, _ = validator.validate_instances(sample_graph)
    assert conforms is True, f"SHACL validation failed:\n{report_text}"
