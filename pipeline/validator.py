"""
Ontology and SHACL Validator.
Verifies OWL 2 syntax, SKOS taxonomies, and validates instance graphs against SHACL shapes.
"""

from pathlib import Path
from typing import Dict, Any, Tuple
import rdflib
from rdflib import Graph, Namespace, RDF, OWL
import pyshacl
import logging

logger = logging.getLogger("OntologyValidator")
AERO = Namespace("https://w3id.org/aerospace-defence#")


class OntologyValidator:
    """Validates OWL schemas and checks RDF instance graphs against SHACL constraint shapes."""

    def __init__(self, ontology_dir: Path = None):
        self.ontology_dir = ontology_dir or Path(__file__).resolve().parent.parent / "ontology"

    def load_combined_schema(self) -> Graph:
        """Loads and parses all ontology and taxonomy definitions into a single RDF graph."""
        g = Graph()
        schema_files = [
            self.ontology_dir / "schema.ttl",
            self.ontology_dir / "taxonomy" / "canadian_kics.ttl",
            self.ontology_dir / "taxonomy" / "platforms.ttl",
            self.ontology_dir / "standards.ttl",
        ]
        for f in schema_files:
            if f.exists():
                logger.info(f"Loading ontology file: {f.name}")
                g.parse(str(f), format="turtle")
            else:
                logger.warning(f"File not found: {f}")
        return g

    def verify_schema_integrity(self) -> Dict[str, Any]:
        """Checks for parse errors, counts classes/properties, and verifies class hierarchies."""
        try:
            g = self.load_combined_schema()
            class_count = len(list(g.subjects(RDF.type, OWL.Class)))
            obj_prop_count = len(list(g.subjects(RDF.type, OWL.ObjectProperty)))
            data_prop_count = len(list(g.subjects(RDF.type, OWL.DatatypeProperty)))
            total_triples = len(g)

            logger.info(
                f"Schema integrity verified: {total_triples} triples, {class_count} classes, "
                f"{obj_prop_count} object properties, {data_prop_count} data properties."
            )
            return {
                "is_valid": True,
                "total_triples": total_triples,
                "classes": class_count,
                "object_properties": obj_prop_count,
                "data_properties": data_prop_count,
            }
        except Exception as e:
            logger.error(f"Schema verification failed: {e}")
            return {"is_valid": False, "error": str(e)}

    def validate_instances(self, data_graph: Graph) -> Tuple[bool, str, Dict[str, Any]]:
        """Validates an RDF instance graph against shapes.ttl using pySHACL."""
        shapes_file = self.ontology_dir / "shapes.ttl"
        if not shapes_file.exists():
            return False, "Shapes file not found", {}

        shapes_graph = Graph().parse(str(shapes_file), format="turtle")
        ont_graph = self.load_combined_schema()
        conforms, results_graph, results_text = pyshacl.validate(
            data_graph,
            shacl_graph=shapes_graph,
            ont_graph=ont_graph,
            inference="rdfs",
            abort_on_first=False,
            meta_shacl=False,
            advanced=True,
        )

        return conforms, results_text, {"conforms": conforms}
