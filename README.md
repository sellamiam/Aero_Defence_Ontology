# Aerospace & Defence Global Supply Chain Knowledge Graph & Ontology
### Multi-Jurisdiction Sovereign Capability Datasets (W3C OWL 2 / RDF 1.1 / SPARQL 1.1)

A multi-jurisdiction sovereign capability Knowledge Graph and formal ontology spanning 7 allied industrial ecosystems: the **United States** (1,371 contractors), **Canada** (1,000 contractors), the **European Union** (220 contractors across 9 nations), **India** (180 contractors), the **United Kingdom** (160 contractors), **Australia** (120 contractors), and **New Zealand** (60 contractors) — comprising **3,111 verified defence suppliers** and **235,525 formal RDF knowledge triples**.

Engineered for sovereign resilience modeling, multi-tier supply chain traceability (`Tier-0 Prime -> Tier-1 Subsystem -> Tier-2 Specialist -> Raw Material`), neural-symbolic procurement matching, and agent-based discrete-event supply chain simulations.

---

## 1. Multi-Jurisdiction Knowledge Graph Distribution Files

The repository provides standalone, self-contained RDF Turtle (`.ttl`) knowledge graphs. Each distribution file is fully autonomous, embedding its complete W3C OWL 2 schema, taxonomy classes, object properties, and enterprise instance assertions:

| Distribution Artifact | File Path | Enterprise Suppliers | RDF Triples | File Size | Jurisdictional Scope & Industrial Base |
| :--- | :--- | :---: | :---: | :---: | :--- |
| 🌐 **Master Global KG** | `data/exports/Aero_Defence_Global_Supply_Chain_Ontology.ttl` | **3,111** | **235,525** | **15.14 MB** | Unified global supply chain graph covering all 7 jurisdictions with cross-border prime-subcontractor linkages |
| 🇺🇸 **United States** | `data/exports/usa.ttl` | **1,371** | **79,180** | **4.42 MB** | Verified US defence & aerospace industrial base across all 50 states/DC (Lockheed Martin, RTX, Northrop Grumman, Boeing, GD, L3Harris, HII, SpaceX, etc.) |
| 🇨🇦 **Canada** | `data/exports/canada.ttl` | **1,000** | **94,475** | **6.14 MB** | Complete Canadian defence base (Bombardier, CAE, MDA, GDLS, Magellan, Héroux-Devtek, IMP, etc.) |
| 🇬🇧 **United Kingdom** | `data/exports/uk.ttl` | **160** | **14,261** | **1.04 MB** | UK MOD tier-1 & tier-2 supply network (BAE Systems, Rolls-Royce, Babcock, QinetiQ, Ultra, Chemring) |
| 🇪🇺 **European Union** | `data/exports/eu.ttl` | **220** | **19,247** | **1.40 MB** | EU defence industrial base across 9 nations (Airbus, Thales, Leonardo, Rheinmetall, Saab, Dassault, Kongsberg) |
| 🇮🇳 **India** | `data/exports/india.ttl` | **180** | **16,019** | **1.21 MB** | Major DPSUs & private aerospace (HAL, BEL, BDL, TASL, L&T Defence, Bharat Forge, Tonbo Imaging) |
| 🇦🇺 **Australia** | `data/exports/australia.ttl` | **120** | **10,869** | **0.78 MB** | Sovereign industrial capabilities & DISP accredited firms (Austal, CEA Technologies, Electro Optic Systems) |
| 🇳🇿 **New Zealand** | `data/exports/new_zealand.ttl` | **60** | **5,276** | **0.36 MB** | Advanced space, propulsion & niche aerospace (Rocket Lab, Dawn Aerospace, Tait Communications, Zenith) |

*All datasets conform strictly to W3C Turtle 1.1 syntax and load into native triplestores (Oxigraph, GraphDB, Stardog, Virtuoso, Apache Jena) in < 0.25 seconds with 0 syntax errors.*

> [!TIP]
> **Data Distribution & Release Archives**: For local inspection and offline simulation development, pre-compiled standalone `.ttl` distribution files are tracked directly under `data/exports/`. Snapshot packages and release checksums are maintained under [GitHub Releases (v2.1.0)](https://github.com/sellamiam/Aero_Defence_Ontology/releases/tag/v2.1.0).

---

## 2. Simulation & Analytical SPARQL 1.1 Suite

Standardized, pre-compiled SPARQL queries located in `data/exports/queries/` engineered for supply chain resilience simulations, node-swapping algorithms, and sovereign capability matching:

| Query File | Simulation Objective | Analytical Mechanics |
| :--- | :--- | :--- |
| **`01_match_alternatives_by_competence.rq`** | Sovereign Alternative Matching | Matches and swaps a disrupted supplier node with qualified alternatives in a target allied jurisdiction sharing core competencies. |
| **`02_match_alternatives_by_platform.rq`** | Platform-Specific Commonality | Discovers qualified suppliers across jurisdictions certified on the exact same defence platform (e.g., F-35 Lightning II, C-130J, P-8). |
| **`03_inspect_selected_supplier_dossier.rq`** | Node Inspection & Dossier Extraction | Returns full technical dossier: CAGE/NCAGE, NATO NSN/FSC parts, accredited service classes, materials, and prime buyers. |
| **`04_filter_by_country_and_services.rq`** | Service Specialization Filter | Queries candidate firms by typed defence service class (`MROService`, `SystemIntegrationService`, `PrecisionMachiningService`, `RDService`). |
| **`05_multi_tier_supply_chain_trace.rq`** | Multi-Tier Upstream Traceability | Traverses dependency graph from Tier-0 primes down to Tier-2 component specialists and strategic material feeds. |

### Fast Standalone Querying via CLI (`query_ttl.py`)
A zero-dependency CLI powered by the Rust-based `pyoxigraph` engine:

```bash
# Query any standalone jurisdiction file with a SPARQL query file:
python3 scripts/query_ttl.py data/exports/canada.ttl data/exports/queries/01_match_alternatives_by_competence.rq

# Cross-jurisdiction platform search across the global graph:
python3 scripts/query_ttl.py data/exports/Aero_Defence_Global_Supply_Chain_Ontology.ttl data/exports/queries/02_match_alternatives_by_platform.rq --limit 20

# Query directly with inline SPARQL:
python3 scripts/query_ttl.py data/exports/Aero_Defence_Global_Supply_Chain_Ontology.ttl "
  PREFIX aero: <https://w3id.org/aerospace-defence#>
  SELECT ?country (COUNT(DISTINCT ?c) AS ?suppliers) WHERE {
    ?c a aero:Company ; aero:headquartersCountry ?country .
  } GROUP BY ?country ORDER BY DESC(?suppliers)
"
```

### Direct Programmatic Integration (Python / Simulation Engines)
To embed queries directly into simulation runtimes (NetworkX, SimPy, AnyLogic, Mesa):

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

For the complete technical guide on connecting simulation UI buttons, passing dynamic parameters, and node-swapping algorithms, see:
👉 [docs/SIMULATION_INTEGRATION_GUIDE.md](docs/SIMULATION_INTEGRATION_GUIDE.md)

---

## 3. Formal Ontology Architecture & Standards Alignment

The ontology enforces rigorous semantic grounding and domain formalisms:
- **Upper Ontology Grounding**: Formally aligned with **Basic Formal Ontology (BFO 2020 / ISO/IEC 21838-2)** (`bfo:MaterialEntity`, `bfo:Disposition`, `bfo:Process`) and **DoD / NATO Unified Architecture Framework (UAF 1.2)**.
- **NATO Codification System (NCS STANAG 3151)**: Enterprise modeling of Commercial and Government Entity codes (**NCAGE / CAGE**), Federal Supply Classification (**FSC**), and National Stock Numbers (**NSN**).
- **Multi-Tier Industrial Topology**: Explicit modeling of contractual and physical supply relationships (`aero:suppliesTo`, `aero:hasDirectSupplier`, `aero:subcontractorOf`).
- **Strategic Material Dependencies**: Tracks high-risk feedstocks including Titanium aerospace grade (Ti-6Al-4V), Carbon Fiber intermediate modulus, Gallium Nitride (GaN) semiconductors, and Rare Earth Elements.
- **Defence Procurement Policies**: Formulates **Canadian Key Industrial Capabilities (KICs)**, **Industrial and Technological Benefits (ITB)** offset multipliers (up to 5x for Canadian SMEs), UK Cyber Essentials Plus, and Australian Defence Industry Security Program (DISP) levels.

```
                                  +-------------------------------------------------------+
                                  |         Basic Formal Ontology (BFO 2020 Upper)        |
                                  +-------------------------------------------------------+
                                                              |
                                  +-------------------------------------------------------+
                                  |         Unified Architecture Framework (UAF 1.2)      |
                                  +-------------------------------------------------------+
                                                              |
                                  +-------------------------------------------------------+
                                  |     Aerospace & Defence Domain Ontology (OWL 2 DL)    |
                                  |      (aero:Company, aero:Product, aero:Service)       |
                                  +---------------------------+---------------------------+
                                                              |
                                  +---------------------------+---------------------------+
                                  |                                                       |
                 +------------------------------------+               +------------------------------------+
                 |   NATO Codification Standards      |               |     Policy & Capability Models     |
                 |  (STANAG 3151 / NCAGE / NSN / FSC) |               |     (KICs, ITB Offsets, DISP)      |
                 +-----------------+------------------+               +-----------------+------------------+
                                   |                                                       |
                                   +--------------------------+----------------------------+
                                                              |
                                         +--------------------+--------------------+
                                         |    Multi-Jurisdiction Knowledge Graphs  |
                                         |     (235,525 Triples | 3,111 Entities)  |
                                         +-----------------------------------------+
```

---

## 4. Neural-Symbolic Procurement Matching & Strategic Consortium Engine

The platform implements a hybrid neural-symbolic architecture combining deep semantic vector representations with deterministic Knowledge Graph constraints:

- **Neural Semantic Vector Retrieval**: Employs sentence-transformer dense embeddings (`all-MiniLM-L6-v2`) to project unstructured defence procurement tenders and requirement statements into a 384-dimensional vector space, executing cosine similarity ranking against contractor capability profiles.
- **Deterministic SPARQL & Policy Filtering**: Applies formal W3C SPARQL graph constraints to enforce zero-leak sovereign geographic boundaries (Canadian provinces, UK clusters, EU member states), Controlled Goods Program (CGP) compliance, ITAR postures, security clearances, and Technology Readiness Levels (TRL $\ge$ threshold).
- **Strategic Teaming & Consortium Assembler**: A constraint-satisfaction heuristic solver that automatically composes compliant **Lead Prime + Tier-1 Subsystem Integrator + SME Specialist** joint-venture bidding teams, maximizing Canadian Content Value (CCV) and official Industrial and Technological Benefits (ITB) offset multipliers (up to 5x for Canadian SMEs).

### Command-Line Interface
```bash
# Match sovereign suppliers for patrol aircraft life extension:
python3 main.py match "Maritime patrol aircraft depot-level overhaul and structural life extension" \
  --country CAN --cgp --certs AS9100D,CGP_Canada --min-trl 8

# Assemble an optimal bidding consortium for a major defence program:
python3 main.py consortium "Canadian Future Aircrew Training Program" \
  --caps "Flight simulation Level D,Turboprop engine MRO,Special mission avionics"

# Generate strategic intelligence dossier for a contractor by CAGE:
python3 main.py dossier L0815  # General Dynamics Land Systems-Canada
```

---

## 5. Automated Verification & Test Suite

The test suite validates SHACL constraints, OWL DL consistency, geographic leak-proofing, and SPARQL 1.1 determinism:

```bash
PYTHONPATH=. pytest -v tests/
```
*All 16 automated tests verify formal ontology contracts, SPARQL endpoint determinism, and mathematical score normalization.*

---

## 6. Reference Inspection Dashboard (Optional Web Visualizer)

A lightweight analytical visualizer and SPARQL terminal is included for interactive graph exploration:

```bash
python3 main.py serve --host 127.0.0.1 --port 8000
```
- Interactive Visual Graph Inspector: `http://127.0.0.1:8000/`
- OpenAPI Specification: `http://127.0.0.1:8000/docs`
