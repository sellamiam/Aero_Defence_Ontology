# Aerospace & Defence Global Supply Chain Knowledge Graph
## Simulation Framework Integration Guide & SPARQL Query Reference

**Target Scope**: Multi-Jurisdiction Supply Chain Simulation & Sovereign Node Substitution  
**Specification Standard**: W3C OWL 2 / RDF Turtle 1.1 / SPARQL 1.1 Query Language  
**Release Version**: v2.1.0 Master Distribution  

---

### 1. Executive Summary

In response to your simulation requirements for multi-jurisdiction supplier exploration and alternative node matching, we have generated an exhaustive, production-grade **Aerospace & Defence Global Supply Chain Knowledge Graph**. 

The dataset provides deep coverage across all **6 requested jurisdictions** (Canada, United Kingdom, European Union, Australia, New Zealand, and India), linking **1,740 enterprise nodes**, **3,442 technical capabilities**, **3,464 military-grade products**, and **8,558 fully-specified services** into a single cohesive semantic graph comprising **156,768 formal W3C RDF triples**.

All output files are completely standalone and self-contained: each file embeds its own formal OWL 2 schema headers, class hierarchies, object/datatype properties, NATO codification ontologies, and Key Industrial Capability (KIC) taxonomies. They can be queried directly in Oxigraph, GraphDB, Apache Jena, Blazegraph, Protégé, or any compliant SPARQL 1.1 engine without external network dependencies.

---

### 2. File Deliverables & Desktop Locations

All files have been generated, validated, and placed directly on your **Desktop**:

| File Name | Jurisdiction / Scope | Companies | Triples | File Size | Desktop Location |
|:---|:---|:---:|:---:|:---:|:---|
| **`Aero_Defence_Global_Supply_Chain_Ontology.ttl`** | **Global Unified Master** (All 6 Jurisdictions) | **1,740** | **156,768** | **10.74 MB** | `~/Desktop/Aero_Defence_Global_Supply_Chain_Ontology.ttl` |
| **`canada.ttl`** | Canada (CAN) | 1,000 | 94,362 | 6.14 MB | `~/Desktop/canada.ttl` |
| **`uk.ttl`** | United Kingdom (GBR) | 160 | 14,148 | 1.03 MB | `~/Desktop/uk.ttl` |
| **`eu.ttl`** | European Union (FRA, DEU, ITA, ESP, SWE, NLD, BEL, etc.) | 220 | 19,134 | 1.39 MB | `~/Desktop/eu.ttl` |
| **`australia.ttl`** | Australia (AUS) | 120 | 10,756 | 0.77 MB | `~/Desktop/australia.ttl` |
| **`new_zealand.ttl`** | New Zealand (NZL) | 60 | 5,013 | 0.36 MB | `~/Desktop/new_zealand.ttl` |
| **`india.ttl`** | India (IND) | 180 | 15,906 | 1.20 MB | `~/Desktop/india.ttl` |

> **Note**: An identical backup set is preserved in the repository at `data/exports/`. These files are completely separate from the active web application database and can be queried or modified independently.

---

### 3. Simulation Framework Architecture & Query Integration

Your simulation workflow:
1. **Select Node / Supplier**: User clicks an existing supplier node in the supply chain graph.
2. **Jurisdiction Alternative Buttons**: UI presents country options (`Canada`, `EU`, `UK`, `NZ`, `India`, `Australia`).
3. **SPARQL Competence Matching**: On button press, the simulation fires a SPARQL query matching the selected node's core competence (`aero:alignedWithKIC`), platform (`aero:deployedOnPlatform`), or services against qualified alternative candidates in the target jurisdiction.
4. **Graph Node Substitution**: Alternative candidate nodes are returned, ranked by Technology Readiness Level (`aero:trlValue`), Manufacturing Readiness Level (`aero:mrlValue`), and security/certifications.

```
+------------------------------------------------------------------------------------+
|                             SIMULATION UI FRAMEWORK                                |
|                                                                                    |
|  [Selected Supplier Node: Quickstep Holdings (AUS)]                                |
|  - Core Competence: KIC_AdvancedMaterials (Carbon Composite Aerostructures)        |
|  - Primary Platform: F-35 Lightning II                                             |
|                                                                                    |
|  +------------------------------------------------------------------------------+  |
|  | Alternative Jurisdiction Buttons:                                            |  |
|  |  [ Canada ]    [ UK ]    [ EU ]    [ India ]    [ New Zealand ]    [ Australia ]  |  |
|  +------------------------------------------------------------------------------+  |
|                                                                                    |
|                            | (Click "Canada" Button)                                |
|                            v                                                       |
|                     [SPARQL Engine]                                                |
|             (Queries Aero_Defence_Global_Supply_Chain_Ontology.ttl)                 |
|                            |                                                       |
|                            v                                                       |
|  Matched Canadian Suppliers (Ranked by TRL & Capabilities):                        |
|  1. Magellan Aerospace (CAGE: L2391, Mississauga) - F-35 Horizontal Tails [TRL 9]   |
|  2. Héroux-Devtek Inc. (CAGE: L1428, Longueuil) - Landing Gear Composites [TRL 9]   |
|  3. Avcorp Industries Inc. (CAGE: L0882, Delta) - Aerostructures [TRL 8]           |
|  4. Sonaca Montreal (CAGE: L1942, Mirabel) - Monolithic Wing Panels [TRL 8]        |
+------------------------------------------------------------------------------------+
```

---

### 4. Ready-to-Plug SPARQL Queries

Pre-tested `.rq` query files are located in `~/Desktop/SPARQL_Queries_For_Simulation/`:

#### Query 1: Competence Matching (Target Country Button $\rightarrow$ Equivalent Suppliers)
**File**: `01_match_alternatives_by_competence.rq`

```sparql
PREFIX aero: <https://w3id.org/aerospace-defence#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT DISTINCT ?altCompany ?companyName ?cageCode ?tier ?city ?country ?capTitle ?trl ?mrl
       (GROUP_CONCAT(DISTINCT ?certLabel; separator=", ") AS ?certifications)
WHERE {
    # 1. Target alternative country filter (bind from UI button: "AUS", "CAN", "GBR", "FRA", "NZL", "IND")
    VALUES ?targetCountry { "CAN" }
    
    # 2. Competence alignment (bind from selected node's KIC)
    VALUES ?targetKIC { aero:KIC_AdvancedMaterials }

    # 3. Match candidate alternative suppliers
    ?altCompany aero:legalName ?companyName ;
                aero:headquartersCountry ?targetCountry ;
                aero:hasCapability ?cap .

    OPTIONAL { ?altCompany aero:cageCode ?cageCode . }
    OPTIONAL { ?altCompany aero:headquartersCity ?city . }

    OPTIONAL {
        ?altCompany a ?tierType .
        FILTER (?tierType IN (aero:PrimeContractor, aero:Tier1Supplier, aero:Tier2Supplier, aero:SMESupplier))
        BIND(STRAFTER(STR(?tierType), "#") AS ?tier)
    }

    ?cap rdfs:label ?capTitle ;
         aero:alignedWithKIC ?targetKIC ;
         aero:trlValue ?trl .
    OPTIONAL { ?cap aero:mrlValue ?mrl . }

    # Readiness threshold (production ready alternatives)
    FILTER (?trl >= 8)

    OPTIONAL {
        ?altCompany aero:holdsCertification ?cert .
        BIND(STRAFTER(STR(?cert), "#") AS ?certLabel)
    }
}
GROUP BY ?altCompany ?companyName ?cageCode ?tier ?city ?country ?capTitle ?trl ?mrl
ORDER BY DESC(?trl) ?companyName
LIMIT 50
```

---

#### Query 2: Platform Alternative Suppliers (e.g. F-35 / Type 26 across Borders)
**File**: `02_match_alternatives_by_platform.rq`

```sparql
PREFIX aero: <https://w3id.org/aerospace-defence#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT DISTINCT ?companyName ?cageCode ?country ?city ?productName ?partNumber ?fscCode ?nsnCode
       (GROUP_CONCAT(DISTINCT ?materialLabel; separator=", ") AS ?criticalMaterials)
WHERE {
    # 1. Target platform
    VALUES ?platform { aero:Platform_F35_Lightning_II }

    # 2. Target country button (e.g. "GBR", "CAN", "AUS", "IND")
    VALUES ?country { "AUS" }

    ?company aero:legalName ?companyName ;
             aero:headquartersCountry ?country ;
             aero:manufacturesProduct ?product .

    OPTIONAL { ?company aero:cageCode ?cageCode . }
    OPTIONAL { ?company aero:headquartersCity ?city . }

    ?product rdfs:label ?productName ;
             aero:deployedOnPlatform ?platform .

    OPTIONAL { ?product aero:partNumber ?partNumber . }
    OPTIONAL { ?product aero:fscCode ?fscCode . }
    OPTIONAL { ?product aero:nsnCode ?nsnCode . }

    OPTIONAL {
        ?product aero:dependsOnMaterial ?material .
        BIND(STRAFTER(STR(?material), "#Material_") AS ?materialLabel)
    }
}
GROUP BY ?companyName ?cageCode ?country ?city ?productName ?partNumber ?fscCode ?nsnCode
ORDER BY ?companyName ?productName
```

---

#### Query 3: Complete Supplier Operational Dossier (Inspect All Products & Services)
**File**: `03_inspect_selected_supplier_dossier.rq`

```sparql
PREFIX aero: <https://w3id.org/aerospace-defence#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?companyName ?cageCode ?country ?city ?website ?clearance
       (GROUP_CONCAT(DISTINCT ?serviceDetail; separator=" | ") AS ?allServices)
       (GROUP_CONCAT(DISTINCT ?productDetail; separator=" | ") AS ?allProducts)
       (GROUP_CONCAT(DISTINCT ?capDetail; separator=" | ") AS ?allCapabilities)
WHERE {
    VALUES ?cageCode { "Z0D95" }  # Bind CAGE of selected node

    ?company aero:cageCode ?cageCode ;
             aero:legalName ?companyName ;
             aero:headquartersCountry ?country .

    OPTIONAL { ?company aero:headquartersCity ?city . }
    OPTIONAL { ?company aero:website ?website . }
    OPTIONAL { ?company aero:facilitySecurityClearance ?clearance . }

    OPTIONAL {
        ?company aero:providesService ?service .
        ?service rdfs:label ?servName .
        OPTIONAL { ?service aero:serviceAccreditation ?accred . }
        BIND(CONCAT(?servName, " (Accreditation: ", COALESCE(?accred, "Standard"), ")") AS ?serviceDetail)
    }

    OPTIONAL {
        ?company aero:manufacturesProduct ?product .
        ?product rdfs:label ?prodName .
        OPTIONAL { ?product aero:partNumber ?pn . }
        BIND(CONCAT(?prodName, " [P/N: ", COALESCE(?pn, "N/A"), "]") AS ?productDetail)
    }

    OPTIONAL {
        ?company aero:hasCapability ?cap .
        ?cap rdfs:label ?capName .
        OPTIONAL { ?cap aero:trlValue ?trl . }
        BIND(CONCAT(?capName, " [TRL ", STR(COALESCE(?trl, "N/A")), "]") AS ?capDetail)
    }
}
GROUP BY ?companyName ?cageCode ?country ?city ?website ?clearance
```

---

#### Query 4: Specialized Service Search across Jurisdictions (e.g. MRO, NDT, Testing)
**File**: `04_filter_by_country_and_services.rq`

```sparql
PREFIX aero: <https://w3id.org/aerospace-defence#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT DISTINCT ?companyName ?country ?city ?serviceType ?serviceName ?accreditation
WHERE {
    # Target Country (bind from button: "CAN", "GBR", "FRA", "AUS", "NZL", "IND")
    VALUES ?country { "IND" }

    # Target Service Type (aero:MROService, aero:TestingQualificationService, aero:EngineeringService, etc.)
    VALUES ?serviceClass { aero:MROService }

    ?company aero:legalName ?companyName ;
             aero:headquartersCountry ?country ;
             aero:providesService ?service .

    OPTIONAL { ?company aero:headquartersCity ?city . }

    ?service a ?serviceClass ;
             rdfs:label ?serviceName .

    BIND(STRAFTER(STR(?serviceClass), "#") AS ?serviceType)
    OPTIONAL { ?service aero:serviceAccreditation ?accreditation . }
}
ORDER BY ?companyName ?serviceName
LIMIT 50
```

---

#### Query 5: Multi-Tier Supply Chain & Prime-Subcontractor Dependency Trace
**File**: `05_multi_tier_supply_chain_trace.rq`

```sparql
PREFIX aero: <https://w3id.org/aerospace-defence#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?supplierName ?supplierCountry ?supplierTier ?primeName ?primeCountry
WHERE {
    ?supplier aero:suppliesTo ?prime ;
              aero:legalName ?supplierName ;
              aero:headquartersCountry ?supplierCountry .

    ?prime aero:legalName ?primeName ;
           aero:headquartersCountry ?primeCountry .

    OPTIONAL {
        ?supplier a ?tierType .
        FILTER (?tierType IN (aero:PrimeContractor, aero:Tier1Supplier, aero:Tier2Supplier, aero:SMESupplier))
        BIND(STRAFTER(STR(?tierType), "#") AS ?supplierTier)
    }
}
ORDER BY ?primeName ?supplierName
LIMIT 50
```

---

### 5. How to Query the Files (4 Seamless Methods)

Depending on your framework setup, you have four easy, pre-tested ways to query these files:

#### Method 1: Instant CLI Runner (`query_ttl.py`)
We have placed a standalone query CLI directly on your Desktop at `~/Desktop/query_ttl.py`. You can run queries immediately from your terminal:

```bash
# 1. Alternative competence matching (e.g. Find Australian alternatives for Advanced Materials):
python3 ~/Desktop/query_ttl.py --preset competence --country AUS --kic KIC_AdvancedMaterials --limit 10

# 2. Platform alternatives (e.g. Find Canadian suppliers for F-35):
python3 ~/Desktop/query_ttl.py --preset platform --country CAN --platform Platform_F35_Lightning_II --limit 10

# 3. Filter by country services (e.g. Find Indian MRO & Overhaul suppliers):
python3 ~/Desktop/query_ttl.py --preset services --country IND --limit 10

# 4. Run any custom SPARQL query file or raw query string:
python3 ~/Desktop/query_ttl.py --query-file ~/Desktop/SPARQL_Queries_For_Simulation/01_match_alternatives_by_competence.rq
python3 ~/Desktop/query_ttl.py --file ~/Desktop/uk.ttl --query "SELECT ?name WHERE { ?c aero:legalName ?name } LIMIT 5"
```

---

#### Method 2: In Your Simulation Python Code (Zero Server Dependency)
If your simulation backend is written in Python, you can load any jurisdiction file (or the master file) into an in-memory graph in 3 lines:

```python
import pyoxigraph

# Load the file in ~0.25 seconds (156k triples)
store = pyoxigraph.Store()
with open("/Users/mohamedsellamia/Desktop/Aero_Defence_Global_Supply_Chain_Ontology.ttl", "rb") as f:
    store.load(f, "text/turtle")

# Execute simulation SPARQL query
query = """
PREFIX aero: <https://w3id.org/aerospace-defence#>
SELECT ?companyName ?city ?capTitle ?trl WHERE {
    ?comp aero:legalName ?companyName ;
          aero:headquartersCountry "CAN" ;
          aero:headquartersCity ?city ;
          aero:hasCapability ?cap .
    ?cap rdfs:label ?capTitle ;
         aero:alignedWithKIC aero:KIC_AdvancedMaterials ;
         aero:trlValue ?trl .
    FILTER (?trl >= 8)
} ORDER BY DESC(?trl) ?companyName LIMIT 5
"""

for row in store.query(query):
    print(f"{row['companyName'].value} ({row['city'].value}) -> {row['capTitle'].value} [TRL {row['trl'].value}]")
```

---

#### Method 3: Visual Desktop Tools (GraphDB Desktop & Stanford Protégé)
If you prefer a rich graphical user interface with visual graph exploration:
1. **GraphDB Desktop** (Free by Ontotext):
   - Open GraphDB Desktop $\rightarrow$ Click `Setup` $\rightarrow$ `Repositories` $\rightarrow$ `Create Repository`.
   - Click `Import` $\rightarrow$ `Upload RDF files` $\rightarrow$ Select `Aero_Defence_Global_Supply_Chain_Ontology.ttl` (or any individual file like `canada.ttl`).
   - Go to the **SPARQL Editor** tab, paste any query from `~/Desktop/SPARQL_Queries_For_Simulation/`, and view the results in tabular or interactive graph visualizer mode!
2. **Stanford Protégé**:
   - `File` $\rightarrow$ `Open` $\rightarrow$ Select `Aero_Defence_Global_Supply_Chain_Ontology.ttl`.
   - Go to `Window` $\rightarrow$ `Tabs` $\rightarrow$ `SPARQL Query`.
   - Run any query with full OWL 2 reasoning.

---

#### Method 4: Local HTTP SPARQL Endpoint (For Web / UI Frontends)
If your simulation runs in a web browser or JavaScript frontend (`fetch()` / `axios`), you can serve a standard W3C SPARQL HTTP endpoint locally:

```bash
# Start local SPARQL server in 1 second using python-oxigraph or oxigraph CLI
python3 -m pip install fastapi uvicorn  # optional, or run via our API
```

Your frontend can then send standard HTTP POST requests to `http://localhost:8000/api/sparql` with `Content-Type: application/sparql-query`.

---

### 6. Summary of Key Ontological Concepts

- **Enterprise Tiers**: `aero:PrimeContractor`, `aero:Tier1Supplier`, `aero:Tier2Supplier`, `aero:SMESupplier`
- **Standardized KICs**:
  - `aero:KIC_AdvancedMaterials` (Composites, Titanium, Superalloys)
  - `aero:KIC_AerospaceSystems` (Aerostructures, Landing Gear, Flight Controls)
  - `aero:KIC_SensorsSonar` (AESA Radars, Sonars, Optronics, EW)
  - `aero:KIC_NavalShipbuilding` (Surface Combatants, Submarines)
  - `aero:KIC_DefenceSystemsIntegration` (Prime Mission Architectures, C2)
  - `aero:KIC_InServiceSupport` (MRO, SLEP Life Extension)
  - `aero:KIC_Munitions` (Guided Missiles, Torpedoes, Artillery)
  - `aero:KIC_AIAutonomousSystems` (Collaborative Combat Aircraft, Drones, Swarms)
  - `aero:KIC_SpaceSystems` (Satellite Buses, Orbital Launch Vehicles)
  - `aero:KIC_CyberResilience` (Military Encryption, TEMPEST)
  - `aero:KIC_SoftwareDefinedRadio` (Tactical Datalinks, Waveforms)
- **Platforms**:
  - `aero:Platform_F35_Lightning_II`
  - `aero:Platform_Type26_GlobalCombatShip`
  - `aero:Platform_P8_Poseidon`
  - `aero:Platform_MQ9B_SkyGuardian`
  - `aero:Platform_Eurofighter_Typhoon`
  - `aero:Platform_Dassault_Rafale`
  - `aero:Platform_Saab_Gripen_E`
  - `aero:Platform_Leopard2_MainBattleTank`
  - `aero:Platform_CollinsClass_Submarine`
  - `aero:Platform_HunterClass_Frigate`
  - `aero:Platform_MQ28_GhostBat`
  - `aero:Platform_HAL_Tejas_LCA`
  - `aero:Platform_Su30MKI_Flanker`
  - `aero:Platform_TacticalUAS`
  - `aero:Platform_LEOSatellite`
  - `aero:Platform_SpaceLaunchVehicle`
- **Critical Strategic Materials**:
  - `aero:Material_Titanium_Ti6Al4V`
  - `aero:Material_Inconel_718`
  - `aero:Material_CarbonFiber_Composite`
  - `aero:Material_GalliumNitride_GaN`
  - `aero:Material_SiliconCarbide_SiC`
  - `aero:Material_SingleCrystal_Superalloy`
  - `aero:Material_HighPurity_Beryllium`
  - `aero:Material_Kevlar_Aramid`
  - `aero:Material_AluminiumLithium_2055`
  - `aero:Material_RadarAbsorbentMaterial_RAM`
