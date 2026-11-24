"""
RDF Triple Extraction & Knowledge Graph Generation.
Transforms normalized company JSON records into a formal W3C RDF graph using the aero: ontology.
Supports complete standalone graph serialization with embedded OWL 2 ontology headers.
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


class RDFTripleExtractor:
    """Constructs RDF triples conforming to aero: schema from normalized JSON records."""

    def __init__(self, data_dir: Optional[Path] = None):
        self.data_dir = data_dir or Path(__file__).resolve().parent.parent / "data"
        self.processed_dir = self.data_dir / "processed"
        self.exports_dir = self.data_dir / "exports"
        self.ontology_dir = Path(__file__).resolve().parent.parent / "ontology"
        self.exports_dir.mkdir(parents=True, exist_ok=True)

    def _slugify(self, text: str) -> str:
        """Creates a safe URI fragment from a string."""
        cleaned = re.sub(r"[^\w\s-]", "", str(text))
        return re.sub(r"[\s_-]+", "_", cleaned).strip("_")

    def load_base_ontology(self, g: Graph) -> None:
        """Loads formal OWL 2 schema and taxonomy definitions into the graph."""
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

    def build_rdf_graph(
        self,
        companies: Optional[List[Dict[str, Any]]] = None,
        include_schema: bool = True
    ) -> Graph:
        """Iterates through company records and builds the full RDF Graph."""
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

        logger.info(f"Extracting triples for {len(companies)} companies...")

        # Mapping for supply chain inter-linking (CAGE -> URI, Name -> URI)
        comp_uri_map: Dict[str, URIRef] = {}

        # First pass: Register company URIs
        for comp in companies:
            cage = comp.get("cage_code", "UNKNOWN")
            legal_name = comp.get("legal_name", cage)
            comp_slug = self._slugify(legal_name)
            comp_uri = URIRef(f"https://w3id.org/aerospace-defence#Company_{comp_slug}_{cage}")
            comp_uri_map[cage] = comp_uri
            comp_uri_map[legal_name] = comp_uri

        # Second pass: Build entities and cross-references
        for comp in companies:
            cage = comp.get("cage_code", "UNKNOWN")
            legal_name = comp.get("legal_name", cage)
            comp_slug = self._slugify(legal_name)
            comp_uri = comp_uri_map.get(cage) or URIRef(f"https://w3id.org/aerospace-defence#Company_{comp_slug}_{cage}")

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
            g.add((comp_uri, AERO.legalName, Literal(legal_name, datatype=XSD.string)))
            if comp.get("trade_name"):
                g.add((comp_uri, AERO.tradeName, Literal(comp["trade_name"], datatype=XSD.string)))
            g.add((comp_uri, AERO.cageCode, Literal(cage, datatype=XSD.string)))
            if comp.get("duns_number"):
                g.add((comp_uri, AERO.dunsNumber, Literal(comp["duns_number"], datatype=XSD.string)))
            if comp.get("business_number"):
                g.add((comp_uri, AERO.businessNumber, Literal(comp["business_number"], datatype=XSD.string)))
            g.add((comp_uri, AERO.headquartersCountry, Literal(comp["country"], datatype=XSD.string)))
            if comp.get("province"):
                g.add((comp_uri, AERO.headquartersProvince, Literal(comp["province"], datatype=XSD.string)))
            g.add((comp_uri, AERO.headquartersCity, Literal(comp["city"], datatype=XSD.string)))
            if comp.get("website"):
                clean_url = str(comp["website"]).replace(" ", "")
                g.add((comp_uri, AERO.website, Literal(clean_url, datatype=XSD.anyURI)))
            g.add((comp_uri, AERO.controlledGoodsRegistered, Literal(comp.get("controlled_goods", False), datatype=XSD.boolean)))
            g.add((comp_uri, AERO.itarCompliant, Literal(comp.get("itar_compliant", False), datatype=XSD.boolean)))

            if comp.get("facility_security_clearance"):
                g.add((comp_uri, AERO.facilitySecurityClearance, Literal(comp["facility_security_clearance"], datatype=XSD.string)))
            if comp.get("canadian_content_percentage"):
                g.add((comp_uri, AERO.canadianContentPercentage, Literal(float(comp["canadian_content_percentage"]), datatype=XSD.decimal)))

            # Domains
            for dom in comp.get("domains", []):
                dom_uri = getattr(AERO, dom, URIRef(f"https://w3id.org/aerospace-defence#{dom}"))
                g.add((comp_uri, AERO.operatesInDomain, dom_uri))

            # Parent / Subsidiary Link
            if comp.get("parent_company"):
                parent_name = comp["parent_company"]
                parent_slug = self._slugify(parent_name)
                parent_uri = comp_uri_map.get(parent_name) or URIRef(f"https://w3id.org/aerospace-defence#Company_{parent_slug}")

                parent_country = {
                    "General Dynamics Corporation": "USA",
                    "L3Harris Technologies, Inc.": "USA",
                    "Rheinmetall AG": "DEU",
                    "RTX Corporation": "USA",
                    "Textron Inc.": "USA",
                    "MBDA": "FRA",
                    "BAE Systems plc": "GBR",
                    "Airbus SE": "FRA",
                }.get(parent_name, "USA")

                g.add((comp_uri, AERO.subsidiaryOf, parent_uri))
                g.add((parent_uri, AERO.hasSubsidiary, comp_uri))
                g.add((parent_uri, RDF.type, AERO.Company))
                g.add((parent_uri, AERO.legalName, Literal(parent_name, datatype=XSD.string)))
                g.add((parent_uri, AERO.headquartersCountry, Literal(parent_country, datatype=XSD.string)))

            # Supply Chain Relationships
            for prime_ref in comp.get("supplies_to", []):
                prime_uri = comp_uri_map.get(prime_ref)
                if prime_uri:
                    g.add((comp_uri, AERO.suppliesTo, prime_uri))
                    g.add((prime_uri, AERO.hasDirectSupplier, comp_uri))

            # Certifications
            for cert_name in comp.get("certifications", []):
                cert_uri = URIRef(f"https://w3id.org/aerospace-defence#Cert_{cert_name}")
                g.add((comp_uri, AERO.holdsCertification, cert_uri))

            # Capabilities
            for i, cap in enumerate(comp.get("capabilities", [])):
                cap_id = f"Cap_{cage}_{i+1}"
                cap_uri = URIRef(f"https://w3id.org/aerospace-defence#{cap_id}")
                g.add((cap_uri, RDF.type, AERO.Capability))
                g.add((cap_uri, RDFS.label, Literal(cap.get("title", f"Capability {i+1}"), datatype=XSD.string)))
                if cap.get("description"):
                    g.add((cap_uri, AERO.capabilityDescription, Literal(cap["description"], datatype=XSD.string)))
                if "trl" in cap:
                    g.add((cap_uri, AERO.trlValue, Literal(int(cap["trl"]), datatype=XSD.integer)))
                if "mrl" in cap:
                    g.add((cap_uri, AERO.mrlValue, Literal(int(cap["mrl"]), datatype=XSD.integer)))
                if "kic" in cap:
                    kic_uri = URIRef(f"https://w3id.org/aerospace-defence#{cap['kic']}")
                    g.add((cap_uri, AERO.alignedWithKIC, kic_uri))

                g.add((comp_uri, AERO.hasCapability, cap_uri))

            # Products
            for i, prod in enumerate(comp.get("products", [])):
                prod_slug = self._slugify(prod.get("name", f"prod_{i+1}"))
                prod_uri = URIRef(f"https://w3id.org/aerospace-defence#Product_{prod_slug}_{cage}")
                g.add((prod_uri, RDF.type, AERO.Product))
                g.add((prod_uri, RDFS.label, Literal(prod["name"], datatype=XSD.string)))
                if prod.get("description"):
                    g.add((prod_uri, AERO.productDescription, Literal(prod["description"], datatype=XSD.string)))
                if prod.get("part_number"):
                    g.add((prod_uri, AERO.partNumber, Literal(prod["part_number"], datatype=XSD.string)))
                if prod.get("fsc_code"):
                    g.add((prod_uri, AERO.fscCode, Literal(prod["fsc_code"], datatype=XSD.string)))
                if prod.get("nsn_code"):
                    g.add((prod_uri, AERO.nsnCode, Literal(prod["nsn_code"], datatype=XSD.string)))

                g.add((comp_uri, AERO.manufacturesProduct, prod_uri))

                # Platform links
                prod_platforms = prod.get("platforms") or comp.get("platforms", [])
                for plat in prod_platforms:
                    plat_uri = URIRef(f"https://w3id.org/aerospace-defence#{plat}")
                    g.add((prod_uri, AERO.deployedOnPlatform, plat_uri))

                # Critical Materials
                for mat in prod.get("materials", []):
                    mat_uri = URIRef(f"https://w3id.org/aerospace-defence#{mat}")
                    g.add((prod_uri, AERO.dependsOnMaterial, mat_uri))

            # Services
            for i, serv in enumerate(comp.get("services", [])):
                serv_slug = self._slugify(serv.get("name", f"serv_{i+1}"))
                serv_uri = URIRef(f"https://w3id.org/aerospace-defence#Service_{serv_slug}_{cage}")
                serv_type = getattr(AERO, serv.get("type", "Service"), AERO.Service)
                g.add((serv_uri, RDF.type, serv_type))
                g.add((serv_uri, RDF.type, AERO.Service))
                g.add((serv_uri, RDFS.label, Literal(serv["name"], datatype=XSD.string)))
                if serv.get("description"):
                    g.add((serv_uri, AERO.serviceDescription, Literal(serv["description"], datatype=XSD.string)))
                if serv.get("accreditation"):
                    g.add((serv_uri, AERO.serviceAccreditation, Literal(serv["accreditation"], datatype=XSD.string)))

                g.add((comp_uri, AERO.providesService, serv_uri))

                # Platforms supported by service
                for plat in comp.get("platforms", []):
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
