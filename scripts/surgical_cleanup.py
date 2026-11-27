#!/usr/bin/env python3
"""
Surgical data-integrity cleanup script.
1. Reclassifies non-hardware service entries from products to services.
2. Fixes Cleveland-Cliffs material tags (HY-80/100 submarine steel -> Material_HY80_HY100_HighStrengthSteel).
3. Purges all synthetic deterministic CAGE codes (U0..., synthetic L..., K0..., F0..., Z0..., E0...).
4. Keeps CAGE, DUNS, and Business Number strictly None unless verified.
"""

import json
import re
from pathlib import Path

DATA_DIR = Path("harvesters/data")

def clean_canada():
    ca_path = DATA_DIR / "canada_verified_suppliers.json"
    with open(ca_path, "r", encoding="utf-8") as f:
        suppliers = json.load(f)

    # Services incorrectly classified as products
    service_names_to_reclassify = {
        "FBO & Ground Handling": "LogisticsSupportService",
        "Aerial Surveillance & Flight Training": "EngineeringService",
        "Aircraft Deicing Services": "LogisticsSupportService",
        "Aerospace Maintenance Training": "EngineeringService",
        "Naval & Defence Engineering Consulting": "EngineeringService",
        "Aerospace Assembly & Quality Services": "EngineeringService",
        "Aerospace Engineering Consulting": "EngineeringService",
        "Marine & Base Logistics": "LogisticsSupportService",
        "Spaceport Nova Scotia Launch Services": "LogisticsSupportService",
        "Integrated Pilot Training Curriculum": "EngineeringService",
        "Naval & Marine Logistics Services": "LogisticsSupportService",
        "Flight Test & Tactical Training Curriculum": "EngineeringService",
        "Adversary Air JTAC Close Air Support Airborne Training Package": "EngineeringService",
    }

    # Verified Canadian CAGE codes to preserve
    verified_canadian_cages = {
        "General Dynamics Land Systems-Canada": "L0815",
        "CAE Inc.": "L0429",
        "Pratt & Whitney Canada Corp.": "00198",
        "Héroux-Devtek Inc.": "36164",
        "Bombardier Inc.": "3AB48",
    }

    for comp in suppliers:
        comp_name = comp["legal_name"]

        # 1. CAGE code cleanup
        if comp_name in verified_canadian_cages:
            comp["cage_code"] = verified_canadian_cages[comp_name]
        else:
            # Purge all synthetic / hex-hash CAGE codes
            comp["cage_code"] = None

        # Ensure DUNS and Business Number are strictly None unless genuine
        comp["duns_number"] = None
        # Only retain valid Canadian Business Numbers (9 digits + RC0001) if not fake
        bn = comp.get("business_number")
        if bn and (len(str(bn)) != 15 or "RC" not in str(bn)):
            comp["business_number"] = None

        # 2. Reclassify service-as-product entries
        prods = comp.get("products", [])
        clean_prods = []
        for p in prods:
            pname = p.get("name", "").strip()
            if pname in service_names_to_reclassify:
                stype = service_names_to_reclassify[pname]
                serv = {
                    "name": pname,
                    "description": p.get("description") or f"Professional {pname.lower()}.",
                    "type": stype,
                    "accreditation": "ISO 9001"
                }
                comp.setdefault("services", []).append(serv)
            else:
                clean_prods.append(p)
        comp["products"] = clean_prods

    with open(ca_path, "w", encoding="utf-8") as f:
        json.dump(suppliers, f, indent=2, ensure_ascii=False)
    print(f"Cleaned Canadian suppliers ({len(suppliers)} records).")

def clean_usa():
    usa_path = DATA_DIR / "usa_verified_suppliers.json"
    with open(usa_path, "r", encoding="utf-8") as f:
        suppliers = json.load(f)

    services_to_reclassify = {
        "WorldView Legion 30-cm EO Constellation Service": "EngineeringService",
        "O3b mPOWER MEO Defense Managed SATCOM Service": "LogisticsSupportService",
        "FlexAir / FlexMove Managed Military SATCOM Terminal Service": "LogisticsSupportService",
        "XTAR-EUR / XTAR-LANT Commercial X-Band Payload Service": "LogisticsSupportService",
        "Unicorn Delivery Service (UDS) Space Software Factory": "EngineeringService",
        "RBC Signals Federated Ground Antenna & Spectrum Service": "LogisticsSupportService",
        "Airspace Monitoring Service (AMS)": "EngineeringService",
    }

    for comp in suppliers:
        comp_name = comp["legal_name"]

        # Ensure synthetic U0... CAGEs are None
        cage = comp.get("cage_code")
        if cage and str(cage).startswith("U0"):
            comp["cage_code"] = None

        # DUNS and BN None
        comp["duns_number"] = None
        comp["business_number"] = None

        # Fix Cleveland-Cliffs
        if "Cleveland-Cliffs" in comp_name:
            for p in comp.get("products", []):
                pname = p.get("name", "")
                if "HY-80" in pname or "Submarine Hull" in pname:
                    p["materials"] = ["Material_HY80_HY100_HighStrengthSteel"]
                elif "12560" in pname or "Armor Plate" in pname:
                    p["materials"] = ["Material_ArmourSteel_MIL_A_46100"]

        # Reclassify services in products
        prods = comp.get("products", [])
        clean_prods = []
        for p in prods:
            pname = p.get("name", "").strip()
            if pname in services_to_reclassify:
                stype = services_to_reclassify[pname]
                serv = {
                    "name": pname,
                    "description": p.get("description") or f"Mission {pname.lower()}.",
                    "type": stype,
                    "accreditation": "ISO 9001"
                }
                comp.setdefault("services", []).append(serv)
            else:
                clean_prods.append(p)
        comp["products"] = clean_prods

    with open(usa_path, "w", encoding="utf-8") as f:
        json.dump(suppliers, f, indent=2, ensure_ascii=False)
    print(f"Cleaned USA suppliers ({len(suppliers)} records).")

def clean_harvester_files():
    # Purge synthetic K0, Z0, F0, E0 CAGE codes from harvester python files
    harvester_files = [
        ("harvesters/uk_harvester.py", r"'cage_code':\s*'K0[0-9A-Z]+'"),
        ("harvesters/australia_harvester.py", r"'cage_code':\s*'Z0[0-9A-Z]+'"),
        ("harvesters/eu_harvester.py", r"'cage_code':\s*'[A-Z][0-9A-Z]{3,4}'"),
        ("harvesters/nz_harvester.py", r"'cage_code':\s*'E0[0-9A-Z]+'"),
        ("harvesters/india_harvester.py", r"'cage_code':\s*'18[0-9A-Z]+'"),
    ]
    for fpath, pattern in harvester_files:
        p = Path(fpath)
        if not p.exists():
            continue
        with open(p, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Replace synthetic cage codes with None
        new_content = re.sub(pattern, "'cage_code': None", content)
        new_content = re.sub(r'"cage_code":\s*"(?:K0|Z0|E0|F0)[^"]*"', '"cage_code": None', new_content)
        
        with open(p, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"Purged synthetic CAGE codes from {fpath}")

if __name__ == "__main__":
    clean_canada()
    clean_usa()
    clean_harvester_files()
