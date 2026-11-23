"""
RDF Triple Extraction & Knowledge Graph Generation.
Transforms normalized company JSON records into a formal W3C RDF graph using the aero: ontology.
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


class RDFTripleExtractor:
    """Constructs RDF triples conforming to aero: schema from normalized JSON records."""

    def __init__(self, data_dir: Optional[Path] = None):
        self.data_dir = data_dir or Path(__file__).resolve().parent.parent / "data"
        self.processed_dir = self.data_dir / "processed"

    def _slugify(self, text: str) -> str:
        """Creates a safe URI fragment from a string."""
        cleaned = re.sub(r"[^\w\s-]", "", text)
        return re.sub(r"[\s_-]+", "_", cleaned).strip("_")

    def build_rdf_graph(self, companies: Optional[List[Dict[str, Any]]] = None) -> Graph:
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

        logger.info(f"Extracting triples for {len(companies)} companies...")

        for comp in companies:
            cage = comp.get("cage_code", "UNKNOWN")
            comp_slug = self._slugify(comp.get("legal_name", cage))
            comp_uri = URIRef(f"https://w3id.org/aerospace-defence#Company_{comp_slug}_{cage}")

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
            g.add((comp_uri, AERO.legalName, Literal(comp["legal_name"], datatype=XSD.string)))
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

            # Parent / Subsidiary Link
            if comp.get("parent_company"):
                parent_slug = self._slugify(comp["parent_company"])
                parent_uri = URIRef(f"https://w3id.org/aerospace-defence#Company_{parent_slug}")
                parent_country = {
                    "General Dynamics Corporation": "USA",
                    "L3Harris Technologies, Inc.": "USA",
                    "Rheinmetall AG": "DEU",
                    "RTX Corporation": "USA",
                    "Textron Inc.": "USA",
                    "MBDA": "FRA",
                }.get(comp["parent_company"], "USA")

                g.add((comp_uri, AERO.subsidiaryOf, parent_uri))
                g.add((parent_uri, AERO.hasSubsidiary, comp_uri))
                g.add((parent_uri, RDF.type, AERO.Company))
                g.add((parent_uri, AERO.legalName, Literal(comp["parent_company"], datatype=XSD.string)))
                g.add((parent_uri, AERO.headquartersCountry, Literal(parent_country, datatype=XSD.string)))

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
                g.add((cap_uri, AERO.capabilityDescription, Literal(cap.get("description", ""), datatype=XSD.string)))
                if "trl" in cap:
                    g.add((cap_uri, AERO.trlValue, Literal(int(cap["trl"]), datatype=XSD.integer)))
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
                g.add((comp_uri, AERO.manufacturesProduct, prod_uri))

                # Platform links
                for plat in comp.get("platforms", []):
                    plat_uri = URIRef(f"https://w3id.org/aerospace-defence#{plat}")
                    g.add((prod_uri, AERO.deployedOnPlatform, plat_uri))

            # Services
            for i, serv in enumerate(comp.get("services", [])):
                serv_slug = self._slugify(serv.get("name", f"serv_{i+1}"))
                serv_uri = URIRef(f"https://w3id.org/aerospace-defence#Service_{serv_slug}_{cage}")
                serv_type = getattr(AERO, serv.get("type", "Service"), AERO.Service)
                g.add((serv_uri, RDF.type, serv_type))
                g.add((serv_uri, RDFS.label, Literal(serv["name"], datatype=XSD.string)))
                g.add((comp_uri, AERO.providesService, serv_uri))

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
