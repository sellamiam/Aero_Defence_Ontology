"""
RDF Triple Extraction & Knowledge Graph Generation.
Transforms normalized company JSON records into a formal W3C RDF graph using the aero: ontology.
Supports pure ABox instance graph extraction, deterministic entity URIs, and TBox schema separation.
"""

from typing import List, Dict, Any, Optional
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
    "ISR": "ISR", "ISRAEL": "ISR",
    "SGP": "SGP", "SINGAPORE": "SGP",
    "KOR": "KOR", "SOUTH KOREA": "KOR",
    "JPN": "JPN", "JAPAN": "JPN",
}

PARENT_COUNTRY_MAP = {
    "General Dynamics Corporation": "USA",
    "L3Harris Technologies, Inc.": "USA",
    "Rheinmetall AG": "DEU",
    "RTX Corporation": "USA",
    "Textron Inc.": "USA",
    "MBDA": "FRA",
    "BAE Systems plc": "GBR",
    "Airbus SE": "FRA",
    "Leonardo S.p.A.": "ITA",
    "Safran SA": "FRA",
    "Thales SA": "FRA",
    "Rolls-Royce plc": "GBR",
    "Rolls-Royce Holdings plc": "GBR",
    "QinetiQ Group plc": "GBR",
    "Chemring Group plc": "GBR",
    "Ultra Electronics Holdings Limited": "GBR",
    "Cobham Limited": "GBR",
    "Senior plc": "GBR",
    "Meggitt PLC": "GBR",
    "Saab AB": "SWE",
    "Kongsberg Gruppen ASA": "NOR",
    "Elbit Systems Ltd.": "ISR",
    "Israel Aerospace Industries Ltd.": "ISR",
    "Rafael Advanced Defense Systems Ltd.": "ISR",
    "CAE Inc.": "CAN",
    "Magellan Aerospace Corporation": "CAN",
    "Héroux-Devtek Inc.": "CAN",
    "LISI Group": "FRA",
    "SKF Group": "SWE",
    "Trelleborg AB": "SWE",
    "ST Engineering Ltd": "SGP",
    "Hanwha Aerospace Co., Ltd.": "KOR",
    "The Boeing Company": "USA",
    "Lockheed Martin Corporation": "USA",
    "Honeywell International Inc.": "USA",
    "Northrop Grumman Corporation": "USA",
    "Moog Inc.": "USA",
    "AAR Corp.": "USA",
    "Curtiss-Wright Corporation": "USA",
    "Howmet Aerospace Inc.": "USA",
    "Teledyne Technologies Incorporated": "USA",
    "TransDigm Group Incorporated": "USA",
    "Parker-Hannifin Corporation": "USA",
    "Huntington Ingalls Industries, Inc.": "USA",
    "Hensoldt AG": "DEU",
    "Diehl Defence GmbH & Co. KG": "DEU",
    "Dassault Aviation SA": "FRA",
    "Fincantieri S.p.A.": "ITA",
    "Navantia S.A., S.M.E.": "ESP",
}


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
        Uses Company_{slug} so multinational parents, primes, and suppliers resolve identically.
        """
        if isinstance(comp_or_name, dict):
            name = comp_or_name.get("legal_name") or comp_or_or_name.get("name") or "Company"
        else:
            name = str(comp_or_name)
        slug = self._slugify(name)
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

        logger.info(f"Extracting triples for {len(companies)} companies (include_schema={include_schema})...")

        # Global deterministic company mapping: Name -> canonical URI, CAGE -> canonical URI
        comp_uri_map: Dict[str, URIRef] = {}
        for comp in companies:
            comp_uri = self.get_company_uri(comp)
            legal_name = comp.get("legal_name")
            if legal_name:
                comp_uri_map[legal_name] = comp_uri
                comp_uri_map[legal_name.strip().lower()] = comp_uri
            cage = comp.get("cage_code")
            if cage and str(cage).strip().lower() not in ["none", "n/a", "null", ""]:
                comp_uri_map[cage] = comp_uri

        # Build entities and cross-references
        for comp in companies:
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

            if cage and str(cage).strip().lower() not in ["none", "n/a", "null", ""]:
                g.add((comp_uri, AERO.cageCode, Literal(str(cage), datatype=XSD.string)))

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

            # Parent / Subsidiary Links (Deterministic cross-border resolving)
            parent_name = comp.get("parent_company")
            if parent_name and str(parent_name).strip().lower() not in ["none", "n/a", "null", ""]:
                parent_uri = self.get_company_uri(parent_name)
                g.add((comp_uri, AERO.subsidiaryOf, parent_uri))
                g.add((parent_uri, AERO.hasSubsidiary, comp_uri))

                # Ensure target is typed as aero:Company in this graph
                g.add((parent_uri, RDF.type, AERO.Company))
                g.add((parent_uri, AERO.legalName, Literal(str(parent_name), datatype=XSD.string)))
                parent_cntry = PARENT_COUNTRY_MAP.get(parent_name, "USA")
                g.add((parent_uri, AERO.headquartersCountry, Literal(parent_cntry, datatype=XSD.string)))

            # Supply Chain Relationships (Deterministic cross-border resolving)
            for prime_ref in comp.get("supplies_to", []):
                if prime_ref and str(prime_ref).strip().lower() not in ["none", "n/a", "null", ""]:
                    prime_uri = comp_uri_map.get(prime_ref) or comp_uri_map.get(prime_ref.strip().lower()) or self.get_company_uri(prime_ref)
                    g.add((comp_uri, AERO.suppliesTo, prime_uri))
                    g.add((prime_uri, AERO.hasDirectSupplier, comp_uri))

                    # Ensure target is typed as aero:Company in this graph
                    g.add((prime_uri, RDF.type, AERO.Company))
                    g.add((prime_uri, AERO.legalName, Literal(str(prime_ref), datatype=XSD.string)))
                    prime_cntry = PARENT_COUNTRY_MAP.get(prime_ref, "USA")
                    g.add((prime_uri, AERO.headquartersCountry, Literal(prime_cntry, datatype=XSD.string)))

            # Certifications
            for cert_name in comp.get("certifications", []):
                if cert_name and str(cert_name).strip().lower() not in ["none", "n/a", "null", ""]:
                    cert_slug = cert_name if cert_name.startswith("Cert_") else f"Cert_{cert_name}"
                    cert_uri = URIRef(f"https://w3id.org/aerospace-defence#{cert_slug}")
                    g.add((comp_uri, AERO.holdsCertification, cert_uri))

            # Capabilities
            comp_slug = self._slugify(legal_name)
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

            # Products
            for i, prod in enumerate(comp.get("products", [])):
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

            # Services
            for i, serv in enumerate(comp.get("services", [])):
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
