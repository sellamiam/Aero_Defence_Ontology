# Aerospace & Defence (A&D) Enterprise Knowledge Graph Ontology & Strategic Matching Platform

An elite, enterprise-grade **Knowledge Graph Ontology**, **Multi-Criteria Procurement Matching Engine**, and **Strategic Consortium Builder** for the Aerospace & Defence industrial ecosystems of **Canada** (~1,000 enterprises), the **United Kingdom**, and the **European Union**.

Engineered to the highest defence & intelligence standards (aligning with **BFO 2020 Upper Ontology**, **NATO Codification / NCS STANAG**, **Canadian Key Industrial Capabilities [KICs]**, and **Industrial & Technological Benefits [ITB] Offset Policies**).

---

## Executive Feature Highlights

1. **Upper Ontology Architecture**:
   - Mapped to **Basic Formal Ontology (BFO 2020)** and **Unified Architecture Framework (UAF)**.
   - Rigorous multi-tier supply chain traceability (`Tier-0 Prime -> Tier-1 Subsystem -> Tier-2 Specialist -> SME`).
   - Strategic material dependency tracking (Titanium, Carbon Fiber, Gallium Nitride [GaN], Rare Earths).
2. **Leak-Proof Hybrid Procurement Matching Engine**:
   - Zero-leak geographic and regional filtering (Canadian provinces, UK clusters, EU member states).
   - Natural language intent parsing and automatic defence taxonomy / acronym expansion.
   - Dynamic weight normalization eliminating score inflation.
3. **Strategic Teaming & Consortium Builder**:
   - Automatically assembles winning **Lead Prime + Tier-1 + SME** teaming consortia for multi-billion-dollar defence programs.
   - Maximizes Canadian Content Value (CCV) and calculates official ITB R&D multipliers (up to 5x for Canadian SMEs).
4. **C-Suite Strategic Intelligence Dossier Generator**:
   - Generates classified-style strategic intelligence briefings on any contractor by CAGE/NCAGE code.
5. **Interactive Executive Web Command Dashboard**:
   - Live visual knowledge graph canvas (`Vis.js`), real-time procurement matching simulator, and SPARQL 1.1 terminal served at `http://127.0.0.1:8000/`.

---

## System Architecture

```
                                  +-------------------------------------------------------+
                                  |   Executive Command Center & Interactive Web UI (/)   |
                                  +-------------------------------------------------------+
                                                             |
                                           REST API (FastAPI) & SPARQL 1.1
                                                             |
                                  +-------------------------------------------------------+
                                  |     Hybrid Procurement Matching & Consortium Engine   |
                                  |  (Semantic Vector Cosine + Leak-Proof Graph Filters)  |
                                  +--------------------------+----------------------------+
                                                             |
                                  +--------------------------+----------------------------+
                                  |                                                       |
                +------------------------------------+               +------------------------------------+
                |   Rust Oxigraph RDF Triplestore    |               |    Semantic Vector & Index Store   |
                |   (32,624 Triples | SPARQL 1.1)    |               |  (1,117 Dense Capability Vectors)  |
                +-----------------+------------------+               +-----------------+------------------+
                                  |                                                       |
                                  +--------------------------+----------------------------+
                                                             |
                                        +--------------------+--------------------+
                                        |   Entity Resolution & Corporate Graph   |
                                        | (CAGE/DUNS, Multinational Hierarchy)    |
                                        +--------------------+--------------------+
                                                             |
                                        +--------------------+--------------------+
                                        |     Orchestrated Multi-Agent Swarm      |
                                        | (Canada, UK, EU Regional Harvesters)    |
                                        +-----------------------------------------+
```

---

## 1. Quick Start Guide for Executives & Demonstrations

### Start the Executive Web Command Dashboard
```bash
python3 main.py serve --host 127.0.0.1 --port 8000
```
Open your browser to:
👉 **`http://127.0.0.1:8000/`** (Interactive Command Center & Visual Graph Network)
👉 **`http://127.0.0.1:8000/docs`** (Interactive OpenAPI / Swagger Documentation)

---

## 2. CLI Command Reference

### A. Leak-Proof Procurement Matching
```bash
# Drone electric motors in Ontario (100% leak-proof, zero foreign bleed)
python3 main.py match "Drone motors mid size drones in Ontario"

# Canadian Patrol Aircraft Depot Maintenance (Filtered by CGP and AS9100D)
python3 main.py match "Maritime patrol aircraft depot-level overhaul and structural life extension" \
  --country CAN \
  --cgp \
  --certs AS9100D,CGP_Canada \
  --min-trl 8
```

### B. Strategic Consortium & Teaming Generator
Assembles a winning joint venture consortium for a major defence tender:
```bash
python3 main.py consortium "Canadian Future Aircrew Training Program" \
  --caps "Flight simulation Level D,Turboprop engine MRO,Special mission avionics"
```

### C. Executive Strategic Intelligence Dossier
Compiles a C-suite strategic intelligence briefing:
```bash
# General Dynamics Land Systems-Canada
python3 main.py dossier L0815

# CAE Inc.
python3 main.py dossier L0429

# MDA Space Ltd.
python3 main.py dossier L0642
```
*Dossiers are automatically saved as Markdown files in `data/dossier_<CAGE>.md`.*

### D. Direct SPARQL 1.1 Analytical Queries
```bash
python3 main.py sparql "
  PREFIX aero: <https://w3id.org/aerospace-defence#>
  SELECT ?country (COUNT(DISTINCT ?c) AS ?suppliers) WHERE {
    ?c a aero:Company ;
       aero:headquartersCountry ?country .
  } GROUP BY ?country ORDER BY DESC(?suppliers)
"
```

---

## 3. Running Automated Test Suite

```bash
PYTHONPATH=. pytest -v tests/
```
All 14 tests verify schema integrity, SHACL conformance, geographic leak proofing, matching accuracy, and REST API endpoints.
