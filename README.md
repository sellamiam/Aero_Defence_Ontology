# Aerospace & Defence (A&D) Enterprise Knowledge Graph Ontology & Strategic Matching Platform

An elite, enterprise-grade **Knowledge Graph Ontology**, **Multi-Criteria Procurement Matching Engine**, and **Strategic Consortium Builder** for the Aerospace & Defence industrial ecosystems across 6 allied and global jurisdictions: **Canada** (1,000 enterprises), the **United Kingdom** (160 enterprises), the **European Union** (220 enterprises across 9 nations), **India** (180 enterprises), **Australia** (120 enterprises), and **New Zealand** (60 enterprises) — totaling **1,740 verified enterprise suppliers** and over **156,000 RDF knowledge triples**.

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

---

## 4. Standalone Multi-Jurisdiction Knowledge Graphs & Simulation Dataset

A high-performance, standalone RDF Turtle (`.ttl`) Knowledge Graph and SPARQL query suite engineered specifically for **external supply chain simulations**, node-swapping algorithms, resilience modeling, and allied sovereign capability matching across 6 jurisdictions.

> [!NOTE]
> **Complete Decoupling & App Stability Guarantee**: The live interactive web application (`python3 main.py serve` on port 8000) operates autonomously on its dedicated database (`data/processed/knowledge_graph.ttl` & `data/graph/oxigraph_db/`). The standalone simulation dataset resides strictly in `data/exports/`, ensuring **zero impact or breaking changes** on the production web platform.

### A. Dataset File Matrix

Each file is 100% self-contained with its embedded W3C OWL 2 schema, BFO/UAF alignments, NATO codification namespaces, and full enterprise capability dossiers (products, NSN/FSC codes, materials, platforms, and 5 typed service categories):

| Jurisdiction / Dataset | File Path | Enterprise Suppliers | RDF Triples | File Size | Description & Key Entities |
| :--- | :--- | :---: | :---: | :---: | :--- |
| 🌐 **Master Global KG** | `data/exports/Aero_Defence_Global_Supply_Chain_Ontology.ttl` | **1,740** | **156,768** | **10.74 MB** | Unified global supply chain graph covering all 6 jurisdictions with cross-border linkages |
| 🇨🇦 **Canada** | `data/exports/canada.ttl` | **1,000** | **94,362** | **6.14 MB** | Complete Canadian defence base (Bombardier, CAE, MDA, GDLS, Magellan, Héroux-Devtek, etc.) |
| 🇬🇧 **United Kingdom** | `data/exports/uk.ttl` | **160** | **14,148** | **1.03 MB** | UK MOD supply chain (BAE Systems, Rolls-Royce, Babcock, QinetiQ, Ultra, Chemring) with NATO NCAGEs |
| 🇪🇺 **European Union** | `data/exports/eu.ttl` | **220** | **19,134** | **1.39 MB** | EU defence champions across 9 nations (Airbus, Thales, Leonardo, Rheinmetall, Saab, Dassault, Kongsberg) |
| 🇮🇳 **India** | `data/exports/india.ttl` | **180** | **15,906** | **1.20 MB** | Major DPSUs & private aerospace (HAL, BEL, BDL, TASL, L&T Defence, Bharat Forge, Tonbo Imaging) |
| 🇦🇺 **Australia** | `data/exports/australia.ttl` | **120** | **10,756** | **0.77 MB** | Sovereign industrial capabilities & DISP accredited firms (Austal, CEA Technologies, Electro Optic Systems) |
| 🇳🇿 **New Zealand** | `data/exports/new_zealand.ttl` | **60** | **5,013** | **0.36 MB** | Advanced space, propulsion & niche aerospace (Rocket Lab, Dawn Aerospace, Tait Communications, Zenith) |

---

### B. Simulation SPARQL Query Suite

Pre-tested, production-ready SPARQL 1.1 queries located in `data/exports/queries/` designed for simulation UI buttons:

1. **`01_match_alternatives_by_competence.rq`**:
   - Matches a selected supplier node with alternative qualified suppliers in a target jurisdiction (e.g., swapping a Canadian supplier with an Australian or UK counterpart sharing matching core competencies).
2. **`02_match_alternatives_by_platform.rq`**:
   - Discovers certified suppliers across jurisdictions that build components or deliver MRO services for the exact same defence platform (e.g., F-35 Lightning II, C-130J, P-8 Poseidon).
3. **`03_inspect_selected_supplier_dossier.rq`**:
   - Pulls the complete technical dossier of any clicked node: all products, part numbers, NATO NSN codes, services, accreditations, materials, and direct Tier-1 customers.
4. **`04_filter_by_country_and_services.rq`**:
   - Filters candidate suppliers in a jurisdiction by specific defence service category (`MROService`, `SystemIntegrationService`, `PrecisionMachiningService`, `RDService`, `TestingAndCertificationService`).
5. **`05_multi_tier_supply_chain_trace.rq`**:
   - Performs multi-tier recursive supply chain traversals from Tier-0 primes down to Tier-2 specialists and strategic material dependencies.

---

### C. Fast Standalone Querying via CLI (`query_ttl.py`)

A zero-overhead query CLI powered by the Rust-based `pyoxigraph` engine:

```bash
# Query any .ttl file with a SPARQL query file:
python3 scripts/query_ttl.py data/exports/canada.ttl data/exports/queries/01_match_alternatives_by_competence.rq

# Filter by platform across the entire global dataset:
python3 scripts/query_ttl.py data/exports/Aero_Defence_Global_Supply_Chain_Ontology.ttl data/exports/queries/02_match_alternatives_by_platform.rq --limit 20

# Query directly with inline SPARQL text:
python3 scripts/query_ttl.py data/exports/Aero_Defence_Global_Supply_Chain_Ontology.ttl "
  PREFIX aero: <https://w3id.org/aerospace-defence#>
  SELECT ?country (COUNT(DISTINCT ?c) AS ?suppliers) WHERE {
    ?c a aero:Company ; aero:headquartersCountry ?country .
  } GROUP BY ?country ORDER BY DESC(?suppliers)
"
```

---

### D. Direct Python / Simulation Integration

To embed these queries directly into simulation engines (e.g., NetworkX, SimPy, AnyLogic, Mesa):

```python
import pyoxigraph as oxi

# Load standalone jurisdiction file (loads in ~0.15s)
store = oxi.Store()
with open("data/exports/Aero_Defence_Global_Supply_Chain_Ontology.ttl", "rb") as f:
    store.load(f, mime_type="text/turtle")

# Run SPARQL query
query = """
PREFIX aero: <https://w3id.org/aerospace-defence#>
SELECT ?companyName ?serviceName WHERE {
    ?c a aero:Company ;
       aero:legalName ?companyName ;
       aero:deliversService ?s .
    ?s a aero:MROService ;
       aero:serviceName ?serviceName .
} LIMIT 10
"""

for solution in store.query(query):
    print(solution["companyName"].value, "->", solution["serviceName"].value)
```

For the complete technical guide on connecting UI buttons, passing dynamic parameters, and node-swapping algorithms, see:
👉 [docs/WILLIAM_SIMULATION_INTEGRATION_GUIDE.md](docs/WILLIAM_SIMULATION_INTEGRATION_GUIDE.md)
