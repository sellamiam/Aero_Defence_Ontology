"""
Tests for FastAPI Application REST & SPARQL Endpoints.
"""

import pytest
from fastapi.testclient import TestClient
from api.main import app


@pytest.fixture(scope="module")
def client():
    return TestClient(app)


def test_health(client):
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["triplestore_triples"] > 1000


def test_stats(client):
    response = client.get("/api/v1/stats")
    assert response.status_code == 200
    data = response.json()
    assert "total_triples" in data
    assert "companies_by_country" in data


def test_get_company_profile(client):
    # Test Bombardier (L3842) or GDLS (L0815)
    response = client.get("/api/v1/companies/L0815")
    assert response.status_code == 200
    data = response.json()
    assert data["legal_name"] == "General Dynamics Land Systems-Canada"
    assert data["cage_code"] == "L0815"
    assert data["country"] == "CAN"
    assert "certifications" in data


def test_sparql_endpoint(client):
    query = """
        PREFIX aero: <https://w3id.org/aerospace-defence#>
        SELECT ?name WHERE {
            ?c aero:cageCode "L0429" ;
               aero:legalName ?name .
        }
    """
    response = client.post("/api/v1/sparql", json={"query": query})
    assert response.status_code == 200
    data = response.json()
    assert data["row_count"] >= 1
    assert data["results"][0]["name"] == "CAE Inc."


def test_match_endpoint(client):
    payload = {
        "query_text": "Space-Based Synthetic Aperture Radar SAR satellites",
        "min_trl": 8,
        "top_k": 3,
    }
    response = client.post("/api/v1/match", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert len(data["top_matches"]) > 0
    top = data["top_matches"][0]
    assert "MDA Space" in top["legal_name"]
    assert top["rank"] == 1
