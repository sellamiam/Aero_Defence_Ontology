"""
Aerospace & Defence NLP Query & Intent Parser.
Extracts geographic entities (Country, Province, City), technical domain concepts,
and regulatory constraints from natural language procurement queries.
Expands colloquial terms into formal A&D ontology taxonomies and military acronyms.
"""

from typing import Dict, Any, List, Tuple, Optional
import re
import logging

logger = logging.getLogger("QueryParser")

# Canadian City -> Province mapping
CANADIAN_CITY_PROVINCE = {
    # Ontario
    "toronto": "ON",
    "mississauga": "ON",
    "ottawa": "ON",
    "markham": "ON",
    "london": "ON",
    "cambridge": "ON",
    "kitchener": "ON",
    "waterloo": "ON",
    "peterborough": "ON",
    "barrie": "ON",
    "brampton": "ON",
    "oakville": "ON",
    "ajax": "ON",
    "kanata": "ON",
    # Quebec
    "montreal": "QC",
    "saint-laurent": "QC",
    "longueuil": "QC",
    "mirabel": "QC",
    "dorval": "QC",
    "laval": "QC",
    "quebec city": "QC",
    "levis": "QC",
    "saint-jean-sur-richelieu": "QC",
    # Western Canada
    "winnipeg": "MB",
    "calgary": "AB",
    "edmonton": "AB",
    "vancouver": "BC",
    "richmond": "BC",
    "victoria": "BC",
    "delta": "BC",
    "abbotsford": "BC",
    # Atlantic Canada
    "halifax": "NS",
    "dartmouth": "NS",
    "enfield": "NS",
    "st. john's": "NL",
}

# US City -> State mapping (excludes cities already in CANADIAN_CITY_PROVINCE like London/Cambridge/Victoria/Richmond)
US_CITY_STATE = {
    "los angeles": "CA",
    "el segundo": "CA",
    "palmdale": "CA",
    "san diego": "CA",
    "sunnyvale": "CA",
    "santa clara": "CA",
    "hawthorne": "CA",
    "costa mesa": "CA",
    "irvine": "CA",
    "torrance": "CA",
    "san jose": "CA",
    "seattle": "WA",
    "everett": "WA",
    "kent": "WA",
    "tukwila": "WA",
    "huntsville": "AL",
    "tucson": "AZ",
    "mesa": "AZ",
    "phoenix": "AZ",
    "tempe": "AZ",
    "scottsdale": "AZ",
    "fort worth": "TX",
    "dallas": "TX",
    "grand prairie": "TX",
    "austin": "TX",
    "houston": "TX",
    "san antonio": "TX",
    "wichita": "KS",
    "st. louis": "MO",
    "hartford": "CT",
    "east hartford": "CT",
    "stratford": "CT",
    "windsor locks": "CT",
    "groton": "CT",
    "bethesda": "MD",
    "linthicum": "MD",
    "arlington": "VA",
    "reston": "VA",
    "falls church": "VA",
    "mclean": "VA",
    "chantilly": "VA",
    "newport news": "VA",
    "herndon": "VA",
    "orlando": "FL",
    "melbourne": "FL",
    "palm bay": "FL",
    "clearwater": "FL",
    "colorado springs": "CO",
    "littleton": "CO",
    "denver": "CO",
    "boulder": "CO",
    "cincinnati": "OH",
    "evendale": "OH",
    "dayton": "OH",
    "cleveland": "OH",
    "boston": "MA",
    "lexington": "MA",
    "andover": "MA",
    "waltham": "MA",
    "bedford": "MA",
    "pascagoula": "MS",
    "bath": "ME",
    "charlotte": "NC",
    "indianapolis": "IN",
    "nashua": "NH",
    "salt lake city": "UT",
    "magna": "UT",
    "cedar rapids": "IA",
    "sterling heights": "MI",
    "troy": "MI",
    "savannah": "GA",
    "marietta": "GA",
}

# Province / State normalization
PROVINCES = {
    "ontario": ("CAN", "ON"),
    "on": ("CAN", "ON"),
    "quebec": ("CAN", "QC"),
    "qc": ("CAN", "QC"),
    "british columbia": ("CAN", "BC"),
    "bc": ("CAN", "BC"),
    "alberta": ("CAN", "AB"),
    "ab": ("CAN", "AB"),
    "manitoba": ("CAN", "MB"),
    "mb": ("CAN", "MB"),
    "nova scotia": ("CAN", "NS"),
    "ns": ("CAN", "NS"),
    # US States (full unambiguous names only; 2-letter codes handled case-sensitively in geo phrases)
    "california": ("USA", "CA"),
    "virginia": ("USA", "VA"),
    "maryland": ("USA", "MD"),
    "texas": ("USA", "TX"),
    "alabama": ("USA", "AL"),
    "arizona": ("USA", "AZ"),
    "washington": ("USA", "WA"),
    "florida": ("USA", "FL"),
    "connecticut": ("USA", "CT"),
    "massachusetts": ("USA", "MA"),
    "ohio": ("USA", "OH"),
    "kansas": ("USA", "KS"),
    "missouri": ("USA", "MO"),
    "utah": ("USA", "UT"),
    "michigan": ("USA", "MI"),
    "pennsylvania": ("USA", "PA"),
    "georgia": ("USA", "GA"),
    "colorado": ("USA", "CO"),
    "north carolina": ("USA", "NC"),
    "south carolina": ("USA", "SC"),
    "new jersey": ("USA", "NJ"),
    "new york": ("USA", "NY"),
    "minnesota": ("USA", "MN"),
    "new hampshire": ("USA", "NH"),
    "indiana": ("USA", "IN"),
    "tennessee": ("USA", "TN"),
    "nevada": ("USA", "NV"),
    "oregon": ("USA", "OR"),
    "illinois": ("USA", "IL"),
    "wisconsin": ("USA", "WI"),
    "oklahoma": ("USA", "OK"),
    "new mexico": ("USA", "NM"),
    "iowa": ("USA", "IA"),
    "kentucky": ("USA", "KY"),
    "louisiana": ("USA", "LA"),
    "mississippi": ("USA", "MS"),
    "maine": ("USA", "ME"),
}

US_STATE_CODES = {
    "CA", "VA", "MD", "TX", "AL", "AZ", "WA", "FL", "CT", "MA",
    "OH", "KS", "MO", "UT", "MI", "PA", "GA", "CO", "NC", "SC",
    "NJ", "NY", "MN", "NH", "IN", "TN", "NV", "OR", "IL", "WI",
    "OK", "NM", "IA", "KY", "LA", "MS", "ME", "DC",
}

# Country aliases
COUNTRIES = {
    "canada": "CAN",
    "canadian": "CAN",
    "can": "CAN",
    "uk": "GBR",
    "united kingdom": "GBR",
    "britain": "GBR",
    "british": "GBR",
    "gbr": "GBR",
    "france": "FRA",
    "french": "FRA",
    "fra": "FRA",
    "germany": "DEU",
    "german": "DEU",
    "deu": "DEU",
    "italy": "ITA",
    "italian": "ITA",
    "ita": "ITA",
    "spain": "ESP",
    "spanish": "ESP",
    "esp": "ESP",
    "sweden": "SWE",
    "swedish": "SWE",
    "swe": "SWE",
    "netherlands": "NLD",
    "dutch": "NLD",
    "nld": "NLD",
    "usa": "USA",
    "us": "USA",
    "united states": "USA",
    "american": "USA",
    "australia": "AUS",
    "australian": "AUS",
    "aus": "AUS",
    "new zealand": "NZL",
    "nzl": "NZL",
    "india": "IND",
    "indian": "IND",
    "ind": "IND",
}

# Common Aerospace & Defence Typo Normalization
TYPO_CORRECTIONS = {
    "maintenace": "maintenance",
    "maintanance": "maintenance",
    "maintanence": "maintenance",
    "maintenence": "maintenance",
    "engeneering": "engineering",
    "enginering": "engineering",
    "propultion": "propulsion",
    "propuslion": "propulsion",
    "aerospase": "aerospace",
    "aerospce": "aerospace",
    "avionic": "avionics",
    "surveilance": "surveillance",
    "survelance": "surveillance",
    "satelite": "satellite",
    "satallite": "satellite",
    "simulater": "simulator",
    "simualtion": "simulation",
}

# Domain & Military Acronym Synonyms
DOMAIN_SYNONYMS = {
    r"\b(jet|jets|business jet|aircraft|airplane)\b": [
        "business jet",
        "fixed-wing aircraft",
        "turbofan",
        "Challenger",
        "airframe",
        "aeronautics",
    ],
    r"\b(maintenance|mro|repair|overhaul|servicing|inspection)\b": [
        "MRO",
        "depot-level maintenance",
        "in-service support",
        "aircraft structural inspection",
        "fleet overhaul",
        "life extension",
    ],
    r"\b(drone|drones)\b": [
        "UAS",
        "UAV",
        "RPAS",
        "Unmanned Aerial System",
        "Remotely Piloted Aircraft",
        "Uncrewed Aerial Vehicle",
    ],
    r"\b(motor|motors)\b": [
        "propulsion",
        "electric motor",
        "brushless motor",
        "BLDC",
        "powertrain",
        "actuator",
        "electric drive",
    ],
    r"\b(mid[\s-]size|medium[\s-]size|tactical)\b": [
        "tactical UAS",
        "MALE",
        "Group 2",
        "Group 3",
        "medium altitude",
    ],
    r"\b(radar|radars)\b": [
        "AESA",
        "Active Electronically Scanned Array",
        "SAR",
        "Synthetic Aperture Radar",
        "RF sensor",
    ],
    r"\b(night vision|thermal|infrared)\b": [
        "EO/IR",
        "Electro-Optical",
        "FLIR",
        "Infrared sensor",
        "hyperspectral",
    ],
    r"\b(armor|armour|armored vehicle|armoured vehicle)\b": [
        "LAV",
        "Combat Vehicle",
        "AFV",
        "tactical armoured",
        "survivability hull",
    ],
    r"\b(satellite|satellites|spacecraft)\b": [
        "SmallSat",
        "CubeSat",
        "LEO satellite",
        "orbital payload",
        "space platform",
    ],
    r"\b(missile|missiles|rocket|rockets)\b": [
        "guided weapon",
        "munition",
        "hypersonic",
        "energetics",
        "interceptor",
    ],
}


class ParsedQuery:
    """Represents a structured query with extracted intents, geo filters, and technical terms."""

    def __init__(
        self,
        raw_query: str,
        cleaned_query: str,
        expanded_query: str,
        target_country: Optional[str] = None,
        target_region: Optional[str] = None,
        target_city: Optional[str] = None,
        extracted_certs: List[str] = None,
        require_cgp: Optional[bool] = None,
        min_trl: Optional[int] = None,
    ):
        self.raw_query = raw_query
        self.cleaned_query = cleaned_query
        self.expanded_query = expanded_query
        self.target_country = target_country
        self.target_region = target_region
        self.target_city = target_city
        self.extracted_certs = extracted_certs or []
        self.require_cgp = require_cgp
        self.min_trl = min_trl

    def __repr__(self):
        return (
            f"ParsedQuery(cleaned='{self.cleaned_query}', "
            f"country={self.target_country}, region={self.target_region}, city={self.target_city})"
        )


class QueryParser:
    """Extracts geographic entities, compliance requests, and expands technical synonyms."""

    @classmethod
    def parse(cls, query: str) -> ParsedQuery:
        text = query.strip()
        # 0. Typo normalization
        words = text.split()
        normalized_words = [TYPO_CORRECTIONS.get(w.lower(), w) for w in words]
        text = " ".join(normalized_words)

        target_country = None
        target_region = None
        target_city = None
        extracted_certs = []
        require_cgp = None
        min_trl = None

        # 1. Extract TRL mentions (e.g. "TRL 8", "TRL >= 7")
        trl_match = re.search(r"\bTRL\s*(?:>=|>)?\s*([1-9])\b", text, re.IGNORECASE)
        if trl_match:
            min_trl = int(trl_match.group(1))
            text = re.sub(r"\bTRL\s*(?:>=|>)?\s*[1-9]\b", "", text, flags=re.IGNORECASE)

        # 2. Extract Certification mentions (e.g. "AS9100", "CGP", "ITAR")
        if re.search(r"\b(CGP|Controlled Goods)\b", text, re.IGNORECASE):
            require_cgp = True
            extracted_certs.append("CGP_Canada")
            text = re.sub(r"\b(CGP|Controlled Goods(?:\s*Program)?)\b", "", text, flags=re.IGNORECASE)

        if re.search(r"\bAS9100[D]?\b", text, re.IGNORECASE):
            extracted_certs.append("AS9100D")
            text = re.sub(r"\bAS9100[D]?\b", "", text, flags=re.IGNORECASE)

        if re.search(r"\bISO\s*9001\b", text, re.IGNORECASE):
            extracted_certs.append("ISO9001")
            text = re.sub(r"\bISO\s*9001(?::2015)?\b", "", text, flags=re.IGNORECASE)

        if re.search(r"\bCyber\s*Essentials\b", text, re.IGNORECASE):
            extracted_certs.append("CyberEssentialsPlus")
            text = re.sub(r"\bCyber\s*Essentials(?:\s*Plus)?\b", "", text, flags=re.IGNORECASE)

        # 3. Extract Geographic Entities (Province, City, Country)
        # Check patterns like "in Ontario", "in Quebec", "in Canada", "in the UK", "near Toronto"
        geo_pattern = r"\b(?:in|near|around|from|based\s+in)\s+(?:the\s+)?([A-Za-z.\s]+?)(?:$|\b(?=with|for|having|who|that))"
        geo_match = re.search(geo_pattern, text, re.IGNORECASE)

        extracted_geo_phrase = None
        if geo_match:
            raw_candidate = geo_match.group(1).strip()
            candidate = raw_candidate.lower()
            # Test candidate against known provinces/states (longest match first, word-boundary safe)
            for prov_name, (cntry, prov_code) in sorted(PROVINCES.items(), key=lambda x: len(x[0]), reverse=True):
                if re.search(rf"\b{re.escape(prov_name)}\b", candidate):
                    target_country = cntry
                    target_region = prov_code
                    extracted_geo_phrase = geo_match.group(0)
                    break

            # Case-sensitive check for 2-letter US state abbreviations inside geo phrase (e.g. "in TX", "in CA")
            if not target_region:
                for st_code in US_STATE_CODES:
                    if re.search(rf"\b{st_code}\b", raw_candidate):
                        target_country = "USA"
                        target_region = st_code
                        extracted_geo_phrase = geo_match.group(0)
                        break

            if not target_region:
                for city_name, prov_code in sorted(CANADIAN_CITY_PROVINCE.items(), key=lambda x: len(x[0]), reverse=True):
                    if re.search(rf"\b{re.escape(city_name)}\b", candidate):
                        target_country = "CAN"
                        target_region = prov_code
                        target_city = city_name.title()
                        extracted_geo_phrase = geo_match.group(0)
                        break

            if not target_region:
                for city_name, state_code in sorted(US_CITY_STATE.items(), key=lambda x: len(x[0]), reverse=True):
                    if re.search(rf"\b{re.escape(city_name)}\b", candidate):
                        target_country = "USA"
                        target_region = state_code
                        target_city = city_name.title()
                        extracted_geo_phrase = geo_match.group(0)
                        break

            if not target_country:
                for c_name, c_code in sorted(COUNTRIES.items(), key=lambda x: len(x[0]), reverse=True):
                    if re.search(rf"\b{re.escape(c_name)}\b", candidate):
                        target_country = c_code
                        extracted_geo_phrase = geo_match.group(0)
                        break

        # Also direct standalone checks if "in X" wasn't used but words like "Ontario" or "California" appear
        if not target_region:
            for prov_name, (cntry, prov_code) in sorted(PROVINCES.items(), key=lambda x: len(x[0]), reverse=True):
                if len(prov_name) <= 2:
                    # Require exact uppercase for 2-letter codes to avoid matching English words like "on"
                    if re.search(rf"\b{re.escape(prov_name.upper())}\b", text):
                        target_country = cntry
                        target_region = prov_code
                        text = re.sub(rf"\b{re.escape(prov_name.upper())}\b", "", text)
                        break
                elif re.search(rf"\b{re.escape(prov_name)}\b", text, re.IGNORECASE):
                    target_country = cntry
                    target_region = prov_code
                    text = re.sub(rf"\b{re.escape(prov_name)}\b", "", text, flags=re.IGNORECASE)
                    break

        if not target_country:
            for c_name, c_code in sorted(COUNTRIES.items(), key=lambda x: len(x[0]), reverse=True):
                if re.search(rf"\b{re.escape(c_name)}\b", text, re.IGNORECASE):
                    target_country = c_code
                    text = re.sub(rf"\b{re.escape(c_name)}\b", "", text, flags=re.IGNORECASE)
                    break

        # Remove the extracted geo phrase from text so it does not contaminate technical matching
        if extracted_geo_phrase:
            text = text.replace(extracted_geo_phrase, " ")

        cleaned_query = " ".join(text.split()).strip()

        # 4. Synonym & Domain Taxonomy Expansion
        expanded_terms = []
        for pat, synonyms in DOMAIN_SYNONYMS.items():
            if re.search(pat, cleaned_query, re.IGNORECASE):
                expanded_terms.extend(synonyms)

        if expanded_terms:
            expanded_query = f"{cleaned_query} " + " ".join(expanded_terms[:6])
        else:
            expanded_query = cleaned_query

        return ParsedQuery(
            raw_query=query,
            cleaned_query=cleaned_query,
            expanded_query=expanded_query,
            target_country=target_country,
            target_region=target_region,
            target_city=target_city,
            extracted_certs=extracted_certs,
            require_cgp=require_cgp,
            min_trl=min_trl,
        )
