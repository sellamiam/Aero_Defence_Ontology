# Aerospace & Defence Global Supply Chain Knowledge Graph & Ontology
### Enterprise Multi-Jurisdiction Sovereign Capability Datasets (W3C OWL 2 / RDF 1.1 / SPARQL 1.1)

A formal, enterprise-grade **Knowledge Graph Ontology** and **Sovereign Capability Dataset** engineered for the Aerospace & Defence (A&D) industrial ecosystems across 6 allied and global jurisdictions: **Canada** (1,000 enterprises), the **United Kingdom** (160 enterprises), the **European Union** (220 enterprises across 9 nations), **India** (180 enterprises), **Australia** (120 enterprises), and **New Zealand** (60 enterprises) — totaling **1,740 verified defence contractors** and **156,768 formal RDF knowledge triples**.

Engineered for sovereign resilience modeling, multi-tier supply chain traceability (`Tier-0 Prime -> Tier-1 Subsystem -> Tier-2 Specialist -> Raw Material`), strategic procurement matching, and agent-based discrete-event supply chain simulations.

---

## 1. Multi-Jurisdiction Knowledge Graph Distribution Files

The repository provides standalone, self-contained RDF Turtle (`.ttl`) knowledge graphs. Each distribution file is fully autonomous, embedding its complete W3C OWL 2 schema, taxonomy classes, object properties, and enterprise instance assertions:

| Distribution Artifact | File Path | Enterprise Suppliers | RDF Triples | File Size | Jurisdictional Scope & Industrial Base |
| :--- | :--- | :---: | :---: | :---: | :--- |
| 🌐 **Master Global KG** | `data/exports/Aero_Defence_Global_Supply_Chain_Ontology.ttl` | **1,740** | **156,768** | **10.74 MB** | Unified global supply chain graph covering all 6 jurisdictions with cross-border prime-subcontractor linkages |
| 🇨🇦 **Canada** | `data/exports/canada.ttl` | **1,000** | **94,362** | **6.14 MB** | Complete Canadian defence base (Bombardier, CAE, MDA, GDLS, Magellan, Héroux-Devtek, IMP, etc.) |
| 🇬🇧 **United Kingdom** | `data/exports/uk.ttl` | **160** | **14,148** | **1.03 MB** | UK MOD tier-1 & tier-2 supply network (BAE Systems, Rolls-Royce, Babcock, QinetiQ, Ultra, Chemring) |
| 🇪🇺 **European Union** | `data/exports/eu.ttl` | **220** | **19,134** | **1.39 MB** | EU defence industrial base across 9 nations (Airbus, Thales, Leonardo, Rheinmetall, Saab, Dassault, Kongsberg) |
| 🇮🇳 **India** | `data/exports/india.ttl` | **180** | **15,906** | **1.20 MB** | Major DPSUs & private aerospace (HAL, BEL, BDL, TASL, L&T Defence, Bharat Forge, Tonbo Imaging) |
| 🇦🇺 **Australia** | `data/exports/australia.ttl` | **120** | **10,756** | **0.77 MB** | Sovereign industrial capabilities & DISP accredited firms (Austal, CEA Technologies, Electro Optic Systems) |
| 🇳🇿 **New Zealand** | `data/exports/new_zealand.ttl` | **60** | **5,013** | **0.36 MB** | Advanced space, propulsion & niche aerospace (Rocket Lab, Dawn Aerospace, Tait Communications, Zenith) |

*All datasets conform strictly to W3C Turtle 1.1 syntax and load into native triplestores (Oxigraph, GraphDB, Stardog, Virtuoso, Apache Jena) in < 0.25 seconds with 0 syntax errors.*

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

*For complete implementation documentation on connecting simulation UI buttons, passing dynamic parameters, and node-swapping algorithms, see [docs/WILLIAM_SIMULATION_INTEGRATION_GUIDE.md](docs/WILLIAM_SIMULATION_INTEGRATION_GUIDE.md).*

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
                                         |     (156,768 Triples | 1,740 Entities)  |
                                         +-----------------------------------------+
```

---

## 4. Multi-Criteria Procurement Matching & Consortium Engine

In addition to static graph exports, the platform includes a multi-criteria procurement matching engine:
- **Zero-Leak Geographic Scoping**: Strict boundary enforcement eliminating foreign entity leakage when querying sovereign-restricted tenders.
- **Dynamic Weight Normalization**: Multi-criteria utility scoring across Technology Readiness Level (TRL 1–9), security clearance status, facility accreditations (AS9100D, NADCAP, ISO 9001), and NATO qualification.
- **Strategic Teaming & Consortium Assembler**: Heuristic solver that automatically composes compliant **Lead Prime + Tier-1 Integrator + SME Specialist** joint-venture bidding teams maximizing Canadian Content Value (CCV) and offset credits.

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
*All 14 automated tests verify formal ontology contracts, SPARQL endpoint determinism, and mathematical score normalization.*

---

## 6. Reference Inspection Dashboard (Optional Web Visualizer)

A lightweight analytical visualizer and SPARQL terminal is included for interactive graph exploration:

```bash
python3 main.py serve --host 127.0.0.1 --port 8000
```
- Interactive Visual Graph Inspector: `http://127.0.0.1:8000/`
- OpenAPI Specification: `http://127.0.0.1:8000/docs`
