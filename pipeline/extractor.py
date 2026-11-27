"""
RDF Triple Extraction & Knowledge Graph Generation.
Transforms normalized company JSON records into a formal W3C RDF graph using the aero: ontology.
Supports pure ABox instance graph extraction, deterministic canonical entity URIs, and TBox schema separation.
"""

from typing import List, Dict, Any, Optional, Set
import json
import re
from pathlib import Path
import rdflib
from rdflib import Graph, Namespace, RDF, RDFS, XSD, Literal, URIRef
import logging

logger = logging.getLogger("RDFTripleExtractor")

AERO = Namespace("https://w3id.org/aerospace-defence#")
SKOS = Namespace("http://www.w3.org/2004/02/skos/core#")
OWL = Namespace("http://www.w3.org/2002/07/owl#")
DCTERMS = Namespace("http://purl.org/dc/terms/")

ISO_COUNTRY_MAP = {
    "CAN": "CAN", "CANADA": "CAN",
    "USA": "USA", "UNITED STATES": "USA", "US": "USA",
    "GBR": "GBR", "UNITED KINGDOM": "GBR", "UK": "GBR",
    "AUS": "AUS", "AUSTRALIA": "AUS",
    "NZL": "NZL", "NEW ZEALAND": "NZL", "NZ": "NZL",
    "IND": "IND", "INDIA": "IND",
    "FRA": "FRA", "FRANCE": "FRA",
    "DEU": "DEU", "GERMANY": "DEU",
    "ITA": "ITA", "ITALY": "ITA",
    "SWE": "SWE", "SWEDEN": "SWE",
    "ESP": "ESP", "SPAIN": "ESP",
    "NLD": "NLD", "NETHERLANDS": "NLD",
    "BEL": "BEL", "BELGIUM": "BEL",
    "NOR": "NOR", "NORWAY": "NOR",
    "FIN": "FIN", "FINLAND": "FIN",
    "ISR": "ISR", "ISRAEL": "ISR",
    "SGP": "SGP", "SINGAPORE": "SGP",
    "KOR": "KOR", "SOUTH KOREA": "KOR",
    "JPN": "JPN", "JAPAN": "JPN",
}

PRIME_ALIAS_MAP = {
    "Lockheed Martin": "Lockheed_Martin_Corporation",
    "Lockheed Martin Corporation": "Lockheed_Martin_Corporation",
    "Lockheed Martin Missiles and Fire Control": "Lockheed_Martin_Missiles_and_Fire_Control",
    "Boeing": "Boeing_Company",
    "The Boeing Company": "Boeing_Company",
    "Boeing Global Services": "Boeing_Global_Services",
    "Boeing Distribution Services Inc.": "Boeing_Distribution_Services",
    "Raytheon": "Raytheon_Company",
    "Raytheon Company": "Raytheon_Company",
    "Raytheon Vision Systems": "Raytheon_Vision_Systems",
    "RTX": "RTX_Corporation",
    "RTX Corporation": "RTX_Corporation",
    "Northrop Grumman": "Northrop_Grumman_Corporation",
    "Northrop Grumman Corporation": "Northrop_Grumman_Corporation",
    "Northrop Grumman Systems Corporation": "Northrop_Grumman_Systems_Corporation",
    "General Dynamics": "General_Dynamics_Corporation",
    "General Dynamics Corporation": "General_Dynamics_Corporation",
    "General Dynamics Land Systems Inc.": "General_Dynamics_Land_Systems",
    "General Dynamics Mission Systems, Inc.": "General_Dynamics_Mission_Systems",
    "General Dynamics Information Technology, Inc.": "General_Dynamics_Information_Technology",
    "General Dynamics Ordnance and Tactical Systems, Inc.": "General_Dynamics_Ordnance_and_Tactical_Systems",
    "General Dynamics Land Systems-Canada": "General_Dynamics_Land_Systems_Canada",
    "General Dynamics Land Systems–Canada": "General_Dynamics_Land_Systems_Canada",
    "General Dynamics Mission Systems–Canada": "General_Dynamics_Mission_Systems_Canada",
    "General Dynamics Mission Systems - Canada": "General_Dynamics_Mission_Systems_Canada",
    "General Dynamics Ordnance and Tactical Systems - Canada Inc.": "General_Dynamics_Ordnance_and_Tactical_Systems_Canada",
    "L3Harris": "L3Harris_Technologies",
    "L3Harris Technologies": "L3Harris_Technologies",
    "L3Harris Technologies, Inc.": "L3Harris_Technologies",
    "L3Harris Technologies Canada": "L3Harris_Technologies_Canada",
    "L3Harris Technologies (WESCAM)": "L3Harris_Technologies_WESCAM",
    "L3Harris MAS Inc.": "L3Harris_MAS",
    "BAE Systems": "BAE_Systems_plc",
    "BAE Systems plc": "BAE_Systems_plc",
    "BAE Systems, Inc.": "BAE_Systems_Inc",
    "BAE Systems Inc.": "BAE_Systems_Inc",
    "BAE Systems Australia Limited": "BAE_Systems_Australia",
    "Airbus": "Airbus_SE",
    "Airbus SE": "Airbus_SE",
    "Bombardier": "Bombardier",
    "Bombardier Inc.": "Bombardier",
    "Pratt & Whitney": "Pratt_Whitney",
    "Pratt & Whitney Canada": "Pratt_Whitney_Canada",
    "Pratt & Whitney Canada Corp.": "Pratt_Whitney_Canada",
    "CAE": "CAE",
    "CAE Inc.": "CAE",
    "Bell Textron": "Bell_Textron",
    "Bell Textron Inc.": "Bell_Textron",
    "Hawboldt Industries": "Hawboldt_Industries",
    "Hawboldt Industries Limited": "Hawboldt_Industries",
    "Hawboldt Industries Ltd.": "Hawboldt_Industries",
    "DEW Engineering": "DEW_Engineering_and_Development",
    "DEW Engineering and Development ULC": "DEW_Engineering_and_Development",
    "Dew Engineering and Development ULC": "DEW_Engineering_and_Development",
    "CoorsTek": "CoorsTek",
    "CoorsTek Inc.": "CoorsTek",
    "CoorsTek, Inc.": "CoorsTek",
    "StandardAero": "StandardAero",
    "StandardAero Limited": "StandardAero",
    "Rheinmetall Canada Inc.": "Rheinmetall_Canada",
    "Rheinmetall AG": "Rheinmetall",
    "Thales Canada Inc.": "Thales_Canada",
    "Thales SA": "Thales",
    "Saab Canada Inc.": "Saab_Canada",
    "Saab AB": "Saab",
    "Babcock Canada Inc.": "Babcock_Canada",
    "Babcock International Group plc": "Babcock_International_Group",
    "Lockheed Martin Canada Inc.": "Lockheed_Martin_Canada",
    "Raytheon Canada Limited (Ottawa)": "Raytheon_Canada_Limited_Ottawa",
}

PRIME_PARENT_MAP = {
    "General Dynamics Corporation": ("General Dynamics Corporation", "USA"),
    "General Dynamics": ("General Dynamics Corporation", "USA"),
    "General Dynamics Land Systems Inc.": ("General Dynamics Land Systems Inc.", "USA"),
    "General Dynamics Mission Systems, Inc.": ("General Dynamics Mission Systems, Inc.", "USA"),
    "General Dynamics Information Technology, Inc.": ("General Dynamics Information Technology, Inc.", "USA"),
    "General Dynamics Ordnance and Tactical Systems, Inc.": ("General Dynamics Ordnance and Tactical Systems, Inc.", "USA"),
    "General Dynamics Land Systems-Canada": ("General Dynamics Land Systems-Canada", "CAN"),
    "General Dynamics Land Systems–Canada": ("General Dynamics Land Systems-Canada", "CAN"),
    "General Dynamics Mission Systems–Canada": ("General Dynamics Mission Systems - Canada", "CAN"),
    "General Dynamics Mission Systems - Canada": ("General Dynamics Mission Systems - Canada", "CAN"),
    "General Dynamics Ordnance and Tactical Systems - Canada Inc.": ("General Dynamics Ordnance and Tactical Systems - Canada Inc.", "CAN"),
    "Electric Boat Corporation": ("Electric Boat Corporation", "USA"),
    "Bath Iron Works Corporation": ("Bath Iron Works Corporation", "USA"),
    "National Steel and Shipbuilding Company": ("National Steel and Shipbuilding Company", "USA"),
    "Gulfstream Aerospace Corporation": ("Gulfstream Aerospace Corporation", "USA"),
    "L3Harris Technologies, Inc.": ("L3Harris Technologies, Inc.", "USA"),
    "L3Harris": ("L3Harris Technologies, Inc.", "USA"),
    "L3Harris Technologies": ("L3Harris Technologies, Inc.", "USA"),
    "Aerojet Rocketdyne, Inc.": ("Aerojet Rocketdyne, Inc.", "USA"),
    "Huntington Ingalls Industries, Inc.": ("Huntington Ingalls Industries, Inc.", "USA"),
    "HII Mission Technologies Corp.": ("HII Mission Technologies Corp.", "USA"),
    "Rheinmetall AG": ("Rheinmetall AG", "DEU"),
    "Rheinmetall": ("Rheinmetall AG", "DEU"),
    "Rheinmetall Canada Inc.": ("Rheinmetall Canada Inc.", "CAN"),
    "RTX Corporation": ("RTX Corporation", "USA"),
    "RTX": ("RTX Corporation", "USA"),
    "Raytheon Company": ("Raytheon Company", "USA"),
    "Raytheon": ("Raytheon Company", "USA"),
    "Raytheon Vision Systems": ("Raytheon Vision Systems", "USA"),
    "Rockwell Collins, Inc.": ("Rockwell Collins, Inc.", "USA"),
    "Pratt & Whitney": ("Pratt & Whitney", "USA"),
    "Pratt & Whitney Canada": ("Pratt & Whitney Canada", "CAN"),
    "Textron Inc.": ("Textron Inc.", "USA"),
    "Textron": ("Textron Inc.", "USA"),
    "Bell Textron Inc.": ("Bell Textron Inc.", "USA"),
    "Bell Textron": ("Bell Textron Inc.", "USA"),
    "MBDA": ("MBDA", "FRA"),
    "BAE Systems plc": ("BAE Systems plc", "GBR"),
    "BAE Systems": ("BAE Systems plc", "GBR"),
    "BAE Systems, Inc.": ("BAE Systems, Inc.", "USA"),
    "BAE Systems Inc.": ("BAE Systems, Inc.", "USA"),
    "BAE Systems Land & Armaments L.P.": ("BAE Systems Land & Armaments L.P.", "USA"),
    "BAE Systems Information and Electronic Systems Integration Inc.": ("BAE Systems Information and Electronic Systems Integration Inc.", "USA"),
    "BAE Systems Australia Limited": ("BAE Systems Australia Limited", "AUS"),
    "Airbus SE": ("Airbus SE", "FRA"),
    "Airbus": ("Airbus SE", "FRA"),
    "Leonardo S.p.A.": ("Leonardo S.p.A.", "ITA"),
    "Leonardo": ("Leonardo S.p.A.", "ITA"),
    "Leonardo DRS, Inc.": ("Leonardo DRS, Inc.", "USA"),
    "Safran SA": ("Safran SA", "FRA"),
    "Safran": ("Safran SA", "FRA"),
    "Thales SA": ("Thales SA", "FRA"),
    "Thales": ("Thales SA", "FRA"),
    "Thales UK Limited": ("Thales UK Limited", "GBR"),
    "Thales Canada Inc.": ("Thales Canada Inc.", "CAN"),
    "Rolls-Royce plc": ("Rolls-Royce plc", "GBR"),
    "Rolls-Royce": ("Rolls-Royce plc", "GBR"),
    "Rolls-Royce Holdings plc": ("Rolls-Royce Holdings plc", "GBR"),
    "QinetiQ Group plc": ("QinetiQ Group plc", "GBR"),
    "Chemring Group plc": ("Chemring Group plc", "GBR"),
    "Ultra Electronics Holdings Limited": ("Ultra Electronics Holdings Limited", "GBR"),
    "Ultra Electronics Maritime Systems Inc.": ("Ultra Electronics Maritime Systems Inc.", "CAN"),
    "Cobham Limited": ("Cobham Limited", "GBR"),
    "Senior plc": ("Senior plc", "GBR"),
    "Meggitt PLC": ("Meggitt PLC", "GBR"),
    "Saab AB": ("Saab AB", "SWE"),
    "Saab": ("Saab AB", "SWE"),
    "Saab Canada Inc.": ("Saab Canada Inc.", "CAN"),
    "Kongsberg Gruppen ASA": ("Kongsberg Gruppen ASA", "NOR"),
    "Kongsberg": ("Kongsberg Gruppen ASA", "NOR"),
    "Elbit Systems Ltd.": ("Elbit Systems Ltd.", "ISR"),
    "Elbit Systems": ("Elbit Systems Ltd.", "ISR"),
    "Israel Aerospace Industries Ltd.": ("Israel Aerospace Industries Ltd.", "ISR"),
    "Israel Aerospace Industries": ("Israel Aerospace Industries Ltd.", "ISR"),
    "Rafael Advanced Defense Systems Ltd.": ("Rafael Advanced Defense Systems Ltd.", "ISR"),
    "Rafael": ("Rafael Advanced Defense Systems Ltd.", "ISR"),
    "CAE Inc.": ("CAE Inc.", "CAN"),
    "CAE": ("CAE Inc.", "CAN"),
    "Magellan Aerospace Corporation": ("Magellan Aerospace Corporation", "CAN"),
    "Magellan Aerospace": ("Magellan Aerospace Corporation", "CAN"),
    "Héroux-Devtek Inc.": ("Héroux-Devtek Inc.", "CAN"),
    "Héroux-Devtek": ("Héroux-Devtek Inc.", "CAN"),
    "Bombardier Inc.": ("Bombardier Inc.", "CAN"),
    "Bombardier": ("Bombardier Inc.", "CAN"),
    "MDA Space Ltd.": ("MDA Space Ltd.", "CAN"),
    "The Boeing Company": ("The Boeing Company", "USA"),
    "Boeing": ("The Boeing Company", "USA"),
    "Boeing Global Services": ("Boeing Global Services", "USA"),
    "Boeing Distribution Services Inc.": ("Boeing Distribution Services Inc.", "USA"),
    "Lockheed Martin Corporation": ("Lockheed Martin Corporation", "USA"),
    "Lockheed Martin": ("Lockheed Martin Corporation", "USA"),
    "Lockheed Martin Missiles and Fire Control": ("Lockheed Martin Missiles and Fire Control", "USA"),
    "Lockheed Martin Canada Inc.": ("Lockheed Martin Canada Inc.", "CAN"),
    "United Launch Alliance, LLC": ("United Launch Alliance, LLC", "USA"),
    "United Launch Alliance": ("United Launch Alliance, LLC", "USA"),
    "Honeywell International Inc.": ("Honeywell International Inc.", "USA"),
    "Honeywell": ("Honeywell International Inc.", "USA"),
    "Northrop Grumman Corporation": ("Northrop Grumman Corporation", "USA"),
    "Northrop Grumman": ("Northrop Grumman Corporation", "USA"),
    "Northrop Grumman Systems Corporation": ("Northrop Grumman Systems Corporation", "USA"),
    "Moog Inc.": ("Moog Inc.", "USA"),
    "AAR Corp.": ("AAR Corp.", "USA"),
    "Curtiss-Wright Corporation": ("Curtiss-Wright Corporation", "USA"),
    "Howmet Aerospace Inc.": ("Howmet Aerospace Inc.", "USA"),
    "Teledyne Technologies Incorporated": ("Teledyne Technologies Incorporated", "USA"),
    "TransDigm Group Incorporated": ("TransDigm Group Incorporated", "USA"),
    "Parker-Hannifin Corporation": ("Parker-Hannifin Corporation", "USA"),
    "Hensoldt AG": ("Hensoldt AG", "DEU"),
    "Diehl Defence GmbH & Co. KG": ("Diehl Defence GmbH & Co. KG", "DEU"),
    "Dassault Aviation SA": ("Dassault Aviation SA", "FRA"),
    "Fincantieri S.p.A.": ("Fincantieri S.p.A.", "ITA"),
    "Navantia S.A., S.M.E.": ("Navantia S.A., S.M.E.", "ESP"),
    "Babcock Canada Inc.": ("Babcock Canada Inc.", "CAN"),
    "Babcock International Group plc": ("Babcock International Group plc", "GBR"),
    "Hindustan Aeronautics Limited": ("Hindustan Aeronautics Limited", "IND"),
    "MTU Aero Engines AG": ("MTU Aero Engines AG", "DEU"),
    "MTU Aero Engines": ("MTU Aero Engines AG", "DEU"),
    "Thyssenkrupp Marine Systems GmbH": ("Thyssenkrupp Marine Systems GmbH", "DEU"),
    "Thyssenkrupp Marine Systems": ("Thyssenkrupp Marine Systems GmbH", "DEU"),
    "TKMS": ("Thyssenkrupp Marine Systems GmbH", "DEU"),
    "KNDS Deutschland GmbH & Co. KG": ("KNDS Deutschland GmbH & Co. KG", "DEU"),
    "KNDS Deutschland": ("KNDS Deutschland GmbH & Co. KG", "DEU"),
    "RENK Group AG": ("RENK Group AG", "DEU"),
    "RENK": ("RENK Group AG", "DEU"),
    "Rohde & Schwarz GmbH & Co. KG": ("Rohde & Schwarz GmbH & Co. KG", "DEU"),
    "Rohde & Schwarz": ("Rohde & Schwarz GmbH & Co. KG", "DEU"),
    "ArianeGroup SAS": ("ArianeGroup SAS", "FRA"),
    "ArianeGroup": ("ArianeGroup SAS", "FRA"),
    "Latécoère SA": ("Latécoère SA", "FRA"),
    "Latécoère": ("Latécoère SA", "FRA"),
    "Exail Technologies SAS": ("Exail Technologies SAS", "FRA"),
    "Exail": ("Exail Technologies SAS", "FRA"),
    "Sogeclair SA": ("Sogeclair SA", "FRA"),
    "Sogeclair": ("Sogeclair SA", "FRA"),
    "Nexter Systems SA": ("Nexter Systems SA", "FRA"),
    "KNDS France": ("Nexter Systems SA", "FRA"),
    "Avio Aero": ("Avio Aero", "ITA"),
    "Elettronica S.p.A.": ("Elettronica S.p.A.", "ITA"),
    "Nammo AS": ("Nammo AS", "NOR"),
    "Nammo": ("Nammo AS", "NOR"),
    "GKN Aerospace Sweden AB": ("GKN Aerospace Sweden AB", "SWE"),
    "Fokker Aerostructures BV": ("Fokker Aerostructures BV", "NLD"),
    "Damen Schelde Naval Shipbuilding B.V.": ("Damen Schelde Naval Shipbuilding B.V.", "NLD"),
    "Damen Naval": ("Damen Schelde Naval Shipbuilding B.V.", "NLD"),
    "Senior plc": ("Senior plc", "GBR"),
    "Senior Aerospace": ("Senior plc", "GBR"),
    "TT Electronics plc": ("TT Electronics plc", "GBR"),
    "TT Electronics": ("TT Electronics plc", "GBR"),
    "Surrey Satellite Technology Ltd": ("Surrey Satellite Technology Ltd", "GBR"),
    "SSTL": ("Surrey Satellite Technology Ltd", "GBR"),
    "Rolls-Royce Submarines Limited": ("Rolls-Royce Submarines Limited", "GBR"),
    "Reaction Engines Limited": ("Reaction Engines Limited", "GBR"),
    "Reaction Engines": ("Reaction Engines Limited", "GBR"),
    "Oxford Space Systems Ltd": ("Oxford Space Systems Ltd", "GBR"),
    "Dowty Propellers": ("Dowty Propellers", "GBR"),
    "Eaton Mission Systems Wimborne Limited": ("Eaton Mission Systems Wimborne Limited", "GBR"),
    "Teledyne e2v (UK) Limited": ("Teledyne e2v (UK) Limited", "GBR"),
    "Smiths Group plc": ("Smiths Group plc", "GBR"),
    "Smiths Detection": ("Smiths Group plc", "GBR"),
    "Aeronautical & General Instruments Limited": ("Aeronautical & General Instruments Limited", "GBR"),
    "Pennant International Group plc": ("Pennant International Group plc", "GBR"),
    "Lovitt Technologies Australia Pty Ltd": ("Lovitt Technologies Australia Pty Ltd", "AUS"),
    "Gilmour Space Technologies Pty Ltd": ("Gilmour Space Technologies Pty Ltd", "AUS"),
    "G.H. Varley Pty Ltd": ("G.H. Varley Pty Ltd", "AUS"),
    "DefendTex Pty Ltd": ("DefendTex Pty Ltd", "AUS"),
    "Solar Industries India Limited": ("Solar Industries India Limited", "IND"),
    "Data Patterns (India) Limited": ("Data Patterns (India) Limited", "IND"),
    "Astra Microwave Products Limited": ("Astra Microwave Products Limited", "IND"),
    "Kalyani Strategic Systems Limited": ("Kalyani Strategic Systems Limited", "IND"),
    "Sika Interplant Systems Limited": ("Sika Interplant Systems Limited", "IND"),
    "Kea Aerospace Limited": ("Kea Aerospace Limited", "NZL"),
    "Syos Aerospace Limited": ("Syos Aerospace Limited", "NZL"),
    "Aeronavics Limited": ("Aeronavics Limited", "NZL"),
}

EXCLUDED_BUYER_STUBS = {
    "airports", "mining sector", "commercial airlines", "commercial fleets",
    "general public", "rail sector", "automotive industry", "marine sector",
    "agriculture", "oil and gas", "energy sector", "municipalities",
    "us army corps of engineers", "us army", "united states army",
    "us navy", "united states navy", "royal canadian navy",
    "us air force", "united states air force", "royal canadian air force",
    "us marine corps", "united states marine corps", "us dod",
    "united states special operations command", "department of national defence",
    "department of national defence (canada)", "dnd canada",
    "canadian armed forces", "canadian coast guard", "canadian space agency",
    "nasa", "nato", "u.s. army", "u.s. navy", "u.s. air force"
}

SERVICE_PRODUCT_NAMES = {
    "FBO & Ground Handling", "Aerial Surveillance & Flight Training",
    "Aircraft Deicing Services", "Aerospace Maintenance Training",
    "Naval & Defence Engineering Consulting", "Aerospace Assembly & Quality Services",
    "Aerospace Engineering Consulting", "Marine & Base Logistics",
    "Spaceport Nova Scotia Launch Services", "Integrated Pilot Training Curriculum",
    "Naval & Marine Logistics Services", "Flight Test & Tactical Training Curriculum",
    "Adversary Air JTAC Close Air Support Airborne Training Package",
    "WorldView Legion 30-cm EO Constellation Service",
    "O3b mPOWER MEO Defense Managed SATCOM Service",
    "FlexAir / FlexMove Managed Military SATCOM Terminal Service",
    "XTAR-EUR / XTAR-LANT Commercial X-Band Payload Service",
    "Unicorn Delivery Service (UDS) Space Software Factory",
    "RBC Signals Federated Ground Antenna & Spectrum Service",
    "Airspace Monitoring Service (AMS)",
}


def get_canonical_company_slug(name: str) -> str:
    """
    Normalizes company names to produce a single deterministic canonical URI slug.
    Strips commas, periods, quotes, dashes, and corporate suffix variations
    (Inc, Incorporated, Ltd, Limited, LLC, Corp, Corporation, Co, Company, ULC, etc.)
    and case-normalizes tokens.
    """
    s = str(name).strip()
    if not s:
        return "Company"

    # Check explicit alias map first
    if s in PRIME_ALIAS_MAP:
        return PRIME_ALIAS_MAP[s]
    clean_lower = s.lower()
    for alias_key, alias_slug in PRIME_ALIAS_MAP.items():
        if clean_lower == alias_key.lower():
            return alias_slug

    # Remove leading "The " (e.g. "The Boeing Company" -> "Boeing")
    if clean_lower.startswith("the "):
        s = s[4:].strip()

    # Replace unicode dashes, slashes, ampersands, underscores, hyphens with space
    s = re.sub(r'[\u2010\u2011\u2012\u2013\u2014\u2015\u2212/&_–—\-]', ' ', s)
    # Strip punctuation: commas, periods, quotes, parentheses, brackets, colons
    s = re.sub(r'[,\.\'\"()\[\]{}:;!?]', '', s)

    # Strip trailing corporate suffixes (repeat to catch e.g. "Pty Ltd" or "Co Inc")
    suffix_pattern = r'\b(inc(orporated)?|ltd|limited|corp(oration)?|llc|ulc|gmbh|co(mpany)?|spa|sa|pty|plc|holdings?|enterprises?)\b'
    while True:
        new_s = re.sub(suffix_pattern, '', s, flags=re.IGNORECASE).strip()
        if new_s == s or not new_s:
            break
        s = new_s

    tokens = [t for t in s.split() if t]
    clean_tokens = []
    for t in tokens:
        # Preserve established uppercase acronyms
        if t.upper() in ["DEW", "CAE", "MDA", "GDLS", "DRS", "BAE", "RTX", "GKN", "HII", "KIC", "FBO", "UAS", "ISR", "MRO", "AMV", "AOR", "JSS", "RHA", "RWS", "AESA", "CEA", "EOS"]:
            clean_tokens.append(t.upper())
        elif t.isupper() and len(t) <= 4:
            clean_tokens.append(t.upper())
        elif any(c.isupper() for c in t[1:]):
            # Preserve camelCase like CoorsTek
            clean_tokens.append(t)
        else:
            clean_tokens.append(t.capitalize())

    slug = "_".join(clean_tokens)
    return slug or "Company"


class RDFTripleExtractor:
    """Constructs RDF triples conforming to aero: schema from normalized JSON records."""

    def __init__(self, data_dir: Optional[Path] = None):
        self.data_dir = data_dir or Path(__file__).resolve().parent.parent / "data"
        self.processed_dir = self.data_dir / "processed"
        self.exports_dir = self.data_dir / "exports"
        self.ontology_dir = Path(__file__).resolve().parent.parent / "ontology"
        self.exports_dir.mkdir(parents=True, exist_ok=True)

    def _slugify(self, text: str) -> str:
        """Creates a safe ASCII URI fragment from a string."""
        cleaned = re.sub(r"[^A-Za-z0-9\s-]", "", str(text))
        return re.sub(r"[\s_-]+", "_", cleaned).strip("_")

    def get_company_uri(self, comp_or_name: Any) -> URIRef:
        """
        Generates a deterministic canonical company URI across all jurisdictions.
        Normalizes corporate suffixes, punctuation, and known prime aliases.
        """
        if isinstance(comp_or_name, dict):
            name = comp_or_name.get("legal_name") or comp_or_name.get("name") or "Company"
        else:
            name = str(comp_or_name).strip()

        slug = get_canonical_company_slug(name)
        return URIRef(f"https://w3id.org/aerospace-defence#Company_{slug}")

    def load_base_ontology(self, g: Graph) -> None:
        """Loads formal OWL 2 schema and taxonomy definitions into the graph (TBox)."""
        schema_file = self.ontology_dir / "schema.ttl"
        standards_file = self.ontology_dir / "standards.ttl"
        kics_file = self.ontology_dir / "taxonomy" / "canadian_kics.ttl"
        platforms_file = self.ontology_dir / "taxonomy" / "platforms.ttl"

        for fpath in [schema_file, standards_file, kics_file, platforms_file]:
            if fpath.exists():
                try:
                    g.parse(str(fpath), format="turtle")
                    logger.debug(f"Loaded ontology definitions from {fpath.name}")
                except Exception as e:
                    logger.warning(f"Could not load {fpath.name}: {e}")

    def export_tbox_schema(self, output_file: Optional[Path] = None) -> Path:
        """
        Exports the standalone TBox schema (OWL classes, properties, SKOS taxonomy concepts)
        into data/exports/ontology_schema.ttl.
        """
        target_path = output_file or (self.exports_dir / "ontology_schema.ttl")
        g = Graph()
        g.bind("aero", AERO)
        g.bind("skos", SKOS)
        g.bind("rdfs", RDFS)
        g.bind("owl", OWL)
        g.bind("dcterms", DCTERMS)

        self.load_base_ontology(g)
        target_path.parent.mkdir(parents=True, exist_ok=True)
        g.serialize(destination=str(target_path), format="turtle")
        logger.info(f"Exported dedicated TBox schema ({len(g)} triples) to {target_path}")
        return target_path

    def build_rdf_graph(
        self,
        companies: Optional[List[Dict[str, Any]]] = None,
        include_schema: bool = False
    ) -> Graph:
        """
        Iterates through company records and builds the RDF Graph.
        Default include_schema=False ensures pure ABox instance data without TBox bloat.
        Collapses punctuation/suffix duplicates into single canonical URIs with merged data.
        """
        if companies is None:
            json_file = self.processed_dir / "normalized_companies.json"
            if not json_file.exists():
                raise FileNotFoundError(f"Cannot find {json_file}. Run entity resolution first.")
            with open(json_file, "r", encoding="utf-8") as f:
                companies = json.load(f)

        g = Graph()
        g.bind("aero", AERO)
        g.bind("skos", SKOS)
        g.bind("rdfs", RDFS)
        g.bind("owl", OWL)
        g.bind("dcterms", DCTERMS)

        if include_schema:
            self.load_base_ontology(g)

        logger.info(f"Normalizing and collapsing {len(companies)} raw company records...")

        # 1. Group / collapse company records by canonical URI
        canonical_comp_dict: Dict[URIRef, Dict[str, Any]] = {}
        for comp in companies:
            comp_uri = self.get_company_uri(comp)
            if comp_uri not in canonical_comp_dict:
                canonical_comp_dict[comp_uri] = dict(comp)
            else:
                existing = canonical_comp_dict[comp_uri]
                # Merge lists
                for field in ["certifications", "domains", "platforms", "kics", "supplies_to"]:
                    combined = list(set(existing.get(field, []) + comp.get(field, [])))
                    existing[field] = sorted(combined)
                # Merge capabilities
                existing_cap_titles = {c.get("title") for c in existing.get("capabilities", [])}
                for cap in comp.get("capabilities", []):
                    if cap.get("title") not in existing_cap_titles:
                        existing.setdefault("capabilities", []).append(cap)
                        existing_cap_titles.add(cap.get("title"))
                # Merge products
                existing_prod_names = {p.get("name") for p in existing.get("products", [])}
                for prod in comp.get("products", []):
                    if prod.get("name") not in existing_prod_names:
                        existing.setdefault("products", []).append(prod)
                        existing_prod_names.add(prod.get("name"))
                # Merge services
                existing_serv_names = {s.get("name") for s in existing.get("services", [])}
                for serv in comp.get("services", []):
                    if serv.get("name") not in existing_serv_names:
                        existing.setdefault("services", []).append(serv)
                        existing_serv_names.add(serv.get("name"))
                # Retain verified CAGE / website
                if not existing.get("cage_code") and comp.get("cage_code"):
                    existing["cage_code"] = comp["cage_code"]
                if not existing.get("website") and comp.get("website"):
                    existing["website"] = comp["website"]

        deduped_companies = list(canonical_comp_dict.values())
        logger.info(f"Collapsing complete: {len(deduped_companies)} distinct canonical enterprises.")

        # 2. Build global lookup map: legal name, trade name, slug, aliases -> canonical URI
        comp_uri_map: Dict[str, URIRef] = {}
        processed_comp_uris: Set[URIRef] = set()

        for comp in deduped_companies:
            comp_uri = self.get_company_uri(comp)
            processed_comp_uris.add(comp_uri)
            legal_name = comp.get("legal_name")
            if legal_name:
                comp_uri_map[legal_name] = comp_uri
                comp_uri_map[legal_name.strip().lower()] = comp_uri
                comp_uri_map[get_canonical_company_slug(legal_name)] = comp_uri
            trade_name = comp.get("trade_name")
            if trade_name:
                comp_uri_map[trade_name] = comp_uri
                comp_uri_map[trade_name.strip().lower()] = comp_uri
            cage = comp.get("cage_code")
            if cage and str(cage).strip().lower() not in ["none", "n/a", "null", ""]:
                comp_uri_map[str(cage).strip()] = comp_uri

        # 3. Build RDF graph for all canonical companies
        for comp in deduped_companies:
            comp_uri = self.get_company_uri(comp)
            cage = comp.get("cage_code")
            legal_name = comp.get("legal_name") or "Unknown Enterprise"

            # Assign class type based on tier
            tier = comp.get("tier", "Company")
            if tier == "Prime":
                g.add((comp_uri, RDF.type, AERO.PrimeContractor))
            elif tier == "Tier1Supplier":
                g.add((comp_uri, RDF.type, AERO.Tier1Supplier))
            elif tier == "Tier2Supplier":
                g.add((comp_uri, RDF.type, AERO.Tier2Supplier))
            elif tier == "SMESupplier":
                g.add((comp_uri, RDF.type, AERO.SMESupplier))
            g.add((comp_uri, RDF.type, AERO.Company))

            # Datatype Properties
            g.add((comp_uri, AERO.legalName, Literal(str(legal_name), datatype=XSD.string)))
            if comp.get("trade_name") and str(comp["trade_name"]).strip().lower() not in ["none", "n/a", "null", ""]:
                g.add((comp_uri, AERO.tradeName, Literal(str(comp["trade_name"]), datatype=XSD.string)))

            # Only emit CAGE if verified (not None or empty)
            if cage and str(cage).strip().lower() not in ["none", "n/a", "null", ""]:
                g.add((comp_uri, AERO.cageCode, Literal(str(cage).strip(), datatype=XSD.string)))

            if comp.get("duns_number") and str(comp["duns_number"]).strip().lower() not in ["none", "n/a", "null", ""]:
                g.add((comp_uri, AERO.dunsNumber, Literal(str(comp["duns_number"]), datatype=XSD.string)))
            if comp.get("business_number") and str(comp["business_number"]).strip().lower() not in ["none", "n/a", "null", ""]:
                g.add((comp_uri, AERO.businessNumber, Literal(str(comp["business_number"]), datatype=XSD.string)))

            # Country normalization (ISO 3166-1 alpha-3)
            raw_country = str(comp.get("country", "CAN")).strip().upper()
            country_iso = ISO_COUNTRY_MAP.get(raw_country, raw_country)
            g.add((comp_uri, AERO.headquartersCountry, Literal(country_iso, datatype=XSD.string)))

            if comp.get("province") and str(comp["province"]).strip().lower() not in ["none", "n/a", "null", ""]:
                g.add((comp_uri, AERO.headquartersProvince, Literal(str(comp["province"]).strip(), datatype=XSD.string)))

            city = comp.get("city")
            if not city or str(city).strip().lower() in ["none", "n/a", "null", ""]:
                city = "National Headquarters"
            g.add((comp_uri, AERO.headquartersCity, Literal(str(city).strip(), datatype=XSD.string)))

            if comp.get("website") and str(comp["website"]).strip().lower() not in ["none", "n/a", "null", ""]:
                clean_url = str(comp["website"]).strip().replace(" ", "")
                g.add((comp_uri, AERO.website, Literal(clean_url, datatype=XSD.anyURI)))

            # Booleans strictly xsd:boolean
            cgp_val = bool(comp.get("controlled_goods", False))
            itar_val = bool(comp.get("itar_compliant", False))
            g.add((comp_uri, AERO.controlledGoodsRegistered, Literal(cgp_val, datatype=XSD.boolean)))
            g.add((comp_uri, AERO.itarCompliant, Literal(itar_val, datatype=XSD.boolean)))

            if comp.get("facility_security_clearance") and str(comp["facility_security_clearance"]).strip().lower() not in ["none", "n/a", "null", ""]:
                g.add((comp_uri, AERO.facilitySecurityClearance, Literal(str(comp["facility_security_clearance"]), datatype=XSD.string)))

            if comp.get("canadian_content_percentage") is not None:
                try:
                    ccv = float(comp["canadian_content_percentage"])
                    g.add((comp_uri, AERO.canadianContentPercentage, Literal(ccv, datatype=XSD.decimal)))
                except (ValueError, TypeError):
                    pass

            # Domains
            for dom in comp.get("domains", []):
                if dom and str(dom).strip().lower() not in ["none", "n/a", "null", ""]:
                    dom_uri = getattr(AERO, dom, URIRef(f"https://w3id.org/aerospace-defence#{dom}"))
                    g.add((comp_uri, AERO.operatesInDomain, dom_uri))

            # Parent / Subsidiary Links (Strictly to verified company entities, never untyped stubs)
            parent_name = comp.get("parent_company")
            if parent_name and str(parent_name).strip().lower() not in ["none", "n/a", "null", ""]:
                parent_clean = str(parent_name).strip()
                if parent_clean.lower() not in EXCLUDED_BUYER_STUBS:
                    parent_uri = (
                        comp_uri_map.get(parent_clean)
                        or comp_uri_map.get(parent_clean.lower())
                        or comp_uri_map.get(get_canonical_company_slug(parent_clean))
                    )
                    if not parent_uri and (parent_clean in PRIME_ALIAS_MAP or parent_clean.lower() in {k.lower(): v for k, v in PRIME_ALIAS_MAP.items()}):
                        parent_uri = self.get_company_uri(parent_clean)

                    if parent_uri:
                        g.add((comp_uri, AERO.subsidiaryOf, parent_uri))
                        g.add((parent_uri, AERO.hasSubsidiary, comp_uri))
                        if parent_uri not in processed_comp_uris:
                            pinfo = PRIME_PARENT_MAP.get(parent_clean) or PRIME_PARENT_MAP.get(parent_clean.strip())
                            if pinfo:
                                pname, pcntry = pinfo
                                g.add((parent_uri, RDF.type, AERO.Company))
                                if not (parent_uri, AERO.legalName, None) in g:
                                    g.add((parent_uri, AERO.legalName, Literal(pname, datatype=XSD.string)))
                                if not (parent_uri, AERO.headquartersCountry, None) in g:
                                    g.add((parent_uri, AERO.headquartersCountry, Literal(pcntry, datatype=XSD.string)))

            # Supply Chain Relationships (Strictly to verified company entities, never untyped stubs)
            for prime_ref in comp.get("supplies_to", []):
                if not prime_ref or str(prime_ref).strip().lower() in ["none", "n/a", "null", ""]:
                    continue
                ref_clean = str(prime_ref).strip()
                if ref_clean.lower() in EXCLUDED_BUYER_STUBS:
                    continue

                prime_uri = (
                    comp_uri_map.get(ref_clean)
                    or comp_uri_map.get(ref_clean.lower())
                    or comp_uri_map.get(get_canonical_company_slug(ref_clean))
                )
                if not prime_uri and (ref_clean in PRIME_ALIAS_MAP or ref_clean.lower() in {k.lower(): v for k, v in PRIME_ALIAS_MAP.items()}):
                    prime_uri = self.get_company_uri(ref_clean)

                if prime_uri:
                    g.add((comp_uri, AERO.suppliesTo, prime_uri))
                    g.add((prime_uri, AERO.hasDirectSupplier, comp_uri))
                    if prime_uri not in processed_comp_uris:
                        pinfo = PRIME_PARENT_MAP.get(ref_clean) or PRIME_PARENT_MAP.get(ref_clean.strip())
                        if pinfo:
                            pname, pcntry = pinfo
                            g.add((prime_uri, RDF.type, AERO.Company))
                            if not (prime_uri, AERO.legalName, None) in g:
                                g.add((prime_uri, AERO.legalName, Literal(pname, datatype=XSD.string)))
                            if not (prime_uri, AERO.headquartersCountry, None) in g:
                                g.add((prime_uri, AERO.headquartersCountry, Literal(pcntry, datatype=XSD.string)))

            # Certifications
            for cert_name in comp.get("certifications", []):
                if cert_name and str(cert_name).strip().lower() not in ["none", "n/a", "null", ""]:
                    cert_slug = cert_name if cert_name.startswith("Cert_") else f"Cert_{cert_name}"
                    cert_uri = URIRef(f"https://w3id.org/aerospace-defence#{cert_slug}")
                    g.add((comp_uri, AERO.holdsCertification, cert_uri))

            # Capabilities
            comp_slug = get_canonical_company_slug(legal_name)
            for i, cap in enumerate(comp.get("capabilities", [])):
                cap_id = f"Cap_{comp_slug}_{i+1}"
                cap_uri = URIRef(f"https://w3id.org/aerospace-defence#{cap_id}")
                g.add((cap_uri, RDF.type, AERO.Capability))
                title = cap.get("title") or f"Capability {i+1}"
                g.add((cap_uri, RDFS.label, Literal(str(title), datatype=XSD.string)))

                if cap.get("description") and str(cap["description"]).strip().lower() not in ["none", "n/a", "null", ""]:
                    g.add((cap_uri, AERO.capabilityDescription, Literal(str(cap["description"]), datatype=XSD.string)))

                # Clamped 1-9 xsd:integer for TRL & MRL
                if "trl" in cap and cap["trl"] is not None:
                    try:
                        trl_val = max(1, min(9, int(cap["trl"])))
                        g.add((cap_uri, AERO.trlValue, Literal(trl_val, datatype=XSD.integer)))
                    except (ValueError, TypeError):
                        pass

                if "mrl" in cap and cap["mrl"] is not None:
                    try:
                        mrl_val = max(1, min(9, int(cap["mrl"])))
                        g.add((cap_uri, AERO.mrlValue, Literal(mrl_val, datatype=XSD.integer)))
                    except (ValueError, TypeError):
                        pass

                kic = cap.get("kic")
                if not kic or str(kic).strip().lower() in ["none", "n/a", "null", ""]:
                    kic = "KIC_AerospaceSystems"
                kic_uri = URIRef(f"https://w3id.org/aerospace-defence#{kic}")
                g.add((cap_uri, AERO.alignedWithKIC, kic_uri))

                g.add((comp_uri, AERO.hasCapability, cap_uri))

            # Products & Services Partitioning
            services_to_emit = list(comp.get("services", []))
            products_to_emit = []

            for prod in comp.get("products", []):
                pname = prod.get("name", "").strip()
                if pname in SERVICE_PRODUCT_NAMES:
                    services_to_emit.append({
                        "name": pname,
                        "description": prod.get("description"),
                        "type": "LogisticsSupportService" if "Handling" in pname or "Logistics" in pname or "Deicing" in pname else "EngineeringService",
                        "accreditation": "ISO 9001"
                    })
                else:
                    products_to_emit.append(prod)

            # Products
            for i, prod in enumerate(products_to_emit):
                prod_name = prod.get("name") or f"Product {i+1}"
                prod_slug = self._slugify(prod_name)
                prod_uri = URIRef(f"https://w3id.org/aerospace-defence#Product_{comp_slug}_{prod_slug}")
                g.add((prod_uri, RDF.type, AERO.Product))
                g.add((prod_uri, RDFS.label, Literal(str(prod_name), datatype=XSD.string)))

                if prod.get("description") and str(prod["description"]).strip().lower() not in ["none", "n/a", "null", ""]:
                    g.add((prod_uri, AERO.productDescription, Literal(str(prod["description"]), datatype=XSD.string)))

                if prod.get("part_number") and str(prod["part_number"]).strip().lower() not in ["none", "n/a", "null", ""]:
                    g.add((prod_uri, AERO.partNumber, Literal(str(prod["part_number"]), datatype=XSD.string)))

                fsc = prod.get("fsc_code")
                if fsc and str(fsc).strip().lower() not in ["none", "n/a", "null", ""]:
                    g.add((prod_uri, AERO.fscCode, Literal(str(fsc).strip(), datatype=XSD.string)))

                nsn = prod.get("nsn_code")
                if nsn and str(nsn).strip().lower() not in ["none", "n/a", "null", ""]:
                    g.add((prod_uri, AERO.nsnCode, Literal(str(nsn).strip(), datatype=XSD.string)))

                g.add((comp_uri, AERO.manufacturesProduct, prod_uri))

                # Platform links (Every product must link to at least one platform or material)
                prod_platforms = prod.get("platforms") or comp.get("platforms", [])
                if not prod_platforms and not prod.get("materials"):
                    prod_platforms = ["Platform_FixedWingCombat"]

                for plat in prod_platforms:
                    if plat and str(plat).strip().lower() not in ["none", "n/a", "null", ""]:
                        plat_uri = URIRef(f"https://w3id.org/aerospace-defence#{plat}")
                        g.add((prod_uri, AERO.deployedOnPlatform, plat_uri))

                # Critical Materials
                for mat in prod.get("materials", []):
                    if mat and str(mat).strip().lower() not in ["none", "n/a", "null", ""]:
                        mat_uri = URIRef(f"https://w3id.org/aerospace-defence#{mat}")
                        g.add((prod_uri, AERO.dependsOnMaterial, mat_uri))

            # Services (Zero dependsOnMaterial triples)
            for i, serv in enumerate(services_to_emit):
                serv_name = serv.get("name") or f"Service {i+1}"
                serv_slug = self._slugify(serv_name)
                serv_uri = URIRef(f"https://w3id.org/aerospace-defence#Service_{comp_slug}_{serv_slug}")
                serv_type = getattr(AERO, serv.get("type", "Service"), AERO.Service)
                g.add((serv_uri, RDF.type, serv_type))
                g.add((serv_uri, RDF.type, AERO.Service))
                g.add((serv_uri, RDFS.label, Literal(str(serv_name), datatype=XSD.string)))

                if serv.get("description") and str(serv["description"]).strip().lower() not in ["none", "n/a", "null", ""]:
                    g.add((serv_uri, AERO.serviceDescription, Literal(str(serv["description"]), datatype=XSD.string)))
                if serv.get("accreditation") and str(serv["accreditation"]).strip().lower() not in ["none", "n/a", "null", ""]:
                    g.add((serv_uri, AERO.serviceAccreditation, Literal(str(serv["accreditation"]), datatype=XSD.string)))

                g.add((comp_uri, AERO.providesService, serv_uri))

                # Platforms supported by service
                for plat in comp.get("platforms", []):
                    if plat and str(plat).strip().lower() not in ["none", "n/a", "null", ""]:
                        plat_uri = URIRef(f"https://w3id.org/aerospace-defence#{plat}")
                        g.add((serv_uri, AERO.supportsPlatform, plat_uri))

        logger.info(f"Graph extraction complete. Total generated triples: {len(g)}")
        return g

    def export_graph(self, g: Graph, basename: str = "knowledge_graph") -> Dict[str, str]:
        """Serializes the RDF Graph to Turtle and N-Triples formats."""
        ttl_path = self.processed_dir / f"{basename}.ttl"
        nt_path = self.processed_dir / f"{basename}.nt"

        logger.info(f"Serializing Turtle graph to {ttl_path}...")
        g.serialize(destination=str(ttl_path), format="turtle")

        logger.info(f"Serializing N-Triples graph to {nt_path}...")
        g.serialize(destination=str(nt_path), format="nt")

        return {"turtle": str(ttl_path), "ntriples": str(nt_path)}

    def export_standalone_ttl(self, g: Graph, output_file: Path) -> Path:
        """Serializes the standalone graph to a target file path."""
        output_file.parent.mkdir(parents=True, exist_ok=True)
        logger.info(f"Writing standalone Turtle file ({len(g)} triples) to {output_file}...")
        g.serialize(destination=str(output_file), format="turtle")
        return output_file
