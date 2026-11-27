import json
import re
from pathlib import Path
from urllib.parse import urlparse

EXISTING_PATH = Path("/Users/mohamedsellamia/projects/Ontology/harvesters/data/usa_verified_suppliers.json")
OUT_PATH = Path("/Users/mohamedsellamia/projects/Ontology/data/raw/us_sectors/14_exp_northeast_sbir.json")

def norm_name(s):
    s = s.lower().strip()
    for suf in [", inc.", " inc.", ", llc", " llc", ", corp.", " corp.", " corporation", " co.", " company", " ltd.", " ltd", " lp", " llp"]:
        if s.endswith(suf):
            s = s[:-len(suf)]
    return re.sub(r"[^a-z0-9]", "", s)

def norm_domain(url):
    if not url:
        return ""
    if not url.startswith("http"):
        url = "https://" + url
    netloc = urlparse(url).netloc.lower()
    if netloc.startswith("www."):
        netloc = netloc[4:]
    return netloc

existing = json.loads(EXISTING_PATH.read_text())
existing_names = set()
existing_domains = set()
for item in existing:
    if item.get("legal_name"):
        existing_names.add(norm_name(item["legal_name"]))
    if item.get("trade_name"):
        existing_names.add(norm_name(item["trade_name"]))
    if item.get("website"):
        existing_domains.add(norm_domain(item["website"]))

def make_rec(legal_name, trade_name, city, state, website, tier, certs, domains, platforms, kics, cap_title, cap_desc, cap_kic, prod_name, prod_desc, fsc, mats, svc_name, svc_desc, svc_type, svc_acc, supplies_to, source_note, fsc_clear="Unclassified / ITAR", itar=True, ctrl=False):
    return {
        "legal_name": legal_name,
        "trade_name": trade_name,
        "cage_code": None,
        "country": "USA",
        "city": city,
        "province": state,
        "website": website,
        "tier": tier,
        "controlled_goods": ctrl,
        "itar_compliant": itar,
        "facility_security_clearance": fsc_clear,
        "certifications": certs,
        "domains": domains,
        "platforms": platforms,
        "kics": kics,
        "capabilities": [
            {
                "title": cap_title,
                "description": cap_desc,
                "trl": 9,
                "mrl": 9 if tier in ("Tier1Supplier", "Tier2Supplier") else 8,
                "kic": cap_kic
            }
        ],
        "products": [
            {
                "name": prod_name,
                "description": prod_desc,
                "part_number": None,
                "fsc_code": fsc,
                "nsn_code": None,
                "platforms": platforms[:2],
                "materials": mats
            }
        ],
        "services": [
            {
                "name": svc_name,
                "description": svc_desc,
                "type": svc_type,
                "accreditation": svc_acc
            }
        ],
        "parent_company": None,
        "supplies_to": supplies_to,
        "source_note": source_note
    }

RAW = [
    # --- CT (Connecticut) ---
    ("CBS Manufacturing Company, Inc.", "CBS Manufacturing", "East Hartford", "CT", "https://www.cbsmfg.com", "Tier2Supplier",
     ["AS9100D", "ISO9001", "ITAR_Compliant"], ["AirPlatform", "DomainAeronautics", "DomainDefence"],
     ["Platform_F35_Lightning_II", "Platform_UH60_BlackHawk"], ["KIC_AerospaceSystems", "KIC_AdvancedMaterials"],
     "Precision Aero-Engine & Housing Machining", "5-axis CNC machining of complex housings, castings, and turbine engine components.", "KIC_AerospaceSystems",
     "Machined Aero-Engine Housings", "Precision-machined complex castings and housings for gas turbine engines.", "2840", ["Material_Inconel_718", "Material_Titanium_Ti6Al4V"],
     "Build-to-Print Aerospace CNC Machining", "Multi-axis CNC milling and turning of flight-critical engine hardware.", "EngineeringService", "AS9100D",
     ["Pratt & Whitney", "Collins Aerospace"], "ACM Aerospace Alley member directory"),

    ("Aero Gear, Inc.", "Aero Gear", "Windsor", "CT", "https://www.aerogear.com", "Tier2Supplier",
     ["AS9100D", "NADCAP_NDT", "NADCAP_HeatTreating", "ITAR_Compliant"], ["AirPlatform", "DomainAeronautics", "DomainDefence"],
     ["Platform_UH60_BlackHawk", "Platform_CH53K_KingStallion", "Platform_V22_Osprey"], ["KIC_AerospaceSystems"],
     "Aerospace Precision Gear & Gearbox Manufacturing", "Design and manufacture of precision spur, helical, and bevel gears and helicopter transmission assemblies.", "KIC_AerospaceSystems",
     "Helicopter Transmission Gears", "High-precision carburized and ground aerospace power drive gears.", "3020", ["Material_Titanium_Ti6Al4V"],
     "Aerospace Gear Engineering & Testing", "Gearbox design, metallurgical testing, and NDT inspection.", "TestingQualificationService", "NADCAP",
     ["Sikorsky Aircraft", "Bell Textron", "GE Aerospace"], "ACM Aerospace Alley member directory"),

    ("Joining Technologies, Inc.", "Joining Technologies", "East Windsor", "CT", "https://www.joiningtech.com", "Tier2Supplier",
     ["AS9100D", "NADCAP_Welding", "ITAR_Compliant"], ["AirPlatform", "SpacePlatform", "DomainAeronautics"],
     ["Platform_F35_Lightning_II", "Platform_SpaceLaunchVehicle"], ["KIC_AerospaceSystems", "KIC_AdvancedMaterials"],
     "Laser & Electron Beam Welding & Additive Cladding", "Precision laser welding, electron beam welding, and laser cladding for jet engine and space propulsion components.", "KIC_AdvancedMaterials",
     "Laser-Welded Aero-Engine Assemblies", "Hermetically sealed and precision-welded superalloy turbine and sensor assemblies.", "2840", ["Material_Inconel_718", "Material_Titanium_Ti6Al4V"],
     "NADCAP Laser & EB Welding", "Contract laser welding, EBW, and metallurgical process development.", "EngineeringService", "NADCAP",
     ["Pratt & Whitney", "Collins Aerospace"], "ACM Aerospace Alley member directory"),

    ("Acuren Inspection, Inc. (East Hartford)", "Acuren East Hartford", "East Hartford", "CT", "https://www.acuren.com", "Tier2Supplier",
     ["AS9100D", "NADCAP_NDT", "ITAR_Compliant"], ["AirPlatform", "DomainAeronautics", "DomainDefence"],
     ["Platform_F35_Lightning_II", "Platform_F22_Raptor"], ["KIC_AerospaceSystems", "KIC_AdvancedMaterials"],
     "Aerospace Non-Destructive Testing & Metallurgy", "Ultrasonic, radiographic, magnetic particle, and penetrant NDT inspection for turbine and structural hardware.", "KIC_AdvancedMaterials",
     "NDT-Certified Aerospace Component Inspection", "Qualified non-destructive testing and failure analysis for flight-critical hardware.", "1560", ["Material_Titanium_Ti6Al4V", "Material_Inconel_718"],
     "NADCAP Non-Destructive Testing", "Accredited NDT and metallurgical laboratory testing services.", "TestingQualificationService", "NADCAP",
     ["Pratt & Whitney", "Sikorsky Aircraft"], "ACM Aerospace Alley member directory"),

    ("C&M Corporation", "C&M", "Wauregan", "CT", "https://www.cmcorporation.com", "Tier2Supplier",
     ["AS9100D", "ISO9001", "ITAR_Compliant"], ["AirPlatform", "LandPlatform", "DomainC4ISR"],
     ["Platform_UH60_BlackHawk", "Platform_JLTV"], ["KIC_AerospaceSystems", "KIC_SensorsSonar"],
     "Military & Aerospace Cable Assemblies", "Design and manufacture of ruggedized bulk cable, coil cords, and overmolded mil-spec wire harnesses.", "KIC_AerospaceSystems",
     "Mil-Spec Interconnect Cable Harnesses", "Ruggedized shielded cable assemblies for tactical vehicles and avionics.", "6150", ["Material_CarbonFiber_Composite"],
     "Custom Cable & Harness Engineering", "Build-to-print and custom mil-spec interconnect manufacturing.", "EngineeringService", "AS9100D",
     ["Sikorsky Aircraft", "General Dynamics"], "Company website"),

    ("Edro Engineering, Inc.", "Edro Engineering", "Plainville", "CT", "https://www.edroeng.com", "SMESupplier",
     ["AS9100D", "ITAR_Compliant"], ["AirPlatform", "DomainAeronautics"],
     ["Platform_F35_Lightning_II", "Platform_KC46_Pegasus"], ["KIC_AerospaceSystems"],
     "Precision Aerospace Turned & Milled Parts", "CNC turning and milling of aerospace engine and airframe fittings, bushings, and sleeves.", "KIC_AerospaceSystems",
     "Aerospace Bushings & Precision Fittings", "Tight-tolerance turned and milled structural and engine hardware.", "5365", ["Material_Titanium_Ti6Al4V", "Material_Inconel_718"],
     "AS9100D Contract Machining", "Production CNC turning and milling for aerospace OEMs.", "EngineeringService", "AS9100D",
     ["Pratt & Whitney", "Collins Aerospace"], "ACM Aerospace Alley member"),

    ("Apex Tool & Manufacturing, Inc.", "Apex Tool", "Windsor", "CT", "https://www.apextoolmfg.com", "SMESupplier",
     ["AS9100D", "ITAR_Compliant"], ["AirPlatform", "DomainAeronautics"],
     ["Platform_F35_Lightning_II", "Platform_UH60_BlackHawk"], ["KIC_AerospaceSystems"],
     "Aerospace Sheet Metal & Precision Machining", "Precision sheet metal fabrication, hydroforming, and CNC machining for aircraft structures.", "KIC_AerospaceSystems",
     "Formed Aerospace Sheet Metal Brackets", "Precision-formed and machined aluminum and titanium airframe brackets.", "1560", ["Material_Titanium_Ti6Al4V"],
     "Aerospace Sheet Metal Fabrication", "Hydroforming, stamping, and CNC machining.", "EngineeringService", "AS9100D",
     ["Sikorsky Aircraft", "Collins Aerospace"], "ACM Aerospace Alley member"),

    ("Connecticut Tool & Manufacturing Co.", "CTM", "Bristol", "CT", "https://www.ctm-co.com", "SMESupplier",
     ["AS9100D", "ITAR_Compliant"], ["AirPlatform", "DomainAeronautics"],
     ["Platform_F35_Lightning_II", "Platform_CH53K_KingStallion"], ["KIC_AerospaceSystems"],
     "Precision Aerospace Tooling & Components", "CNC machining of flight-critical aerospace brackets, housings, and precision tooling.", "KIC_AerospaceSystems",
     "Precision Machined Aero Housings", "Multi-axis machined aluminum and titanium aerospace housings.", "1560", ["Material_Titanium_Ti6Al4V"],
     "AS9100D Precision Machining", "Build-to-print CNC milling and turning.", "EngineeringService", "AS9100D",
     ["Pratt & Whitney", "Sikorsky Aircraft"], "ACM member"),

    ("D&N Machining, Inc.", "D&N Machining", "Manchester", "CT", "https://www.dnmachining.com", "SMESupplier",
     ["AS9100D", "ITAR_Compliant"], ["AirPlatform", "DomainAeronautics"],
     ["Platform_F35_Lightning_II", "Platform_UH60_BlackHawk"], ["KIC_AerospaceSystems"],
     "5-Axis CNC Machining of Superalloys", "Precision CNC milling and turning of Inconel, titanium, and stainless steel aerospace parts.", "KIC_AerospaceSystems",
     "Superalloy Engine Brackets & Mounts", "Precision-machined high-temp alloy engine mounts.", "2840", ["Material_Inconel_718", "Material_Titanium_Ti6Al4V"],
     "Superalloy CNC Machining", "Contract 5-axis machining for aerospace propulsion.", "EngineeringService", "AS9100D",
     ["Pratt & Whitney", "Collins Aerospace"], "ACM member"),

    ("Flanagan Industries, Inc.", "Flanagan Industries", "Glastonbury", "CT", "https://www.flanaganind.com", "Tier2Supplier",
     ["AS9100D", "NADCAP_NDT", "NADCAP_Welding", "ITAR_Compliant"], ["AirPlatform", "DomainAeronautics"],
     ["Platform_F35_Lightning_II", "Platform_F15EX_EagleII"], ["KIC_AerospaceSystems"],
     "Jet Engine Sheet Metal & Ring Assemblies", "Precision machining, TIG/resistance welding, and sheet metal fabrication for jet engines.", "KIC_AerospaceSystems",
     "Jet Engine Shrouds & Ring Assemblies", "Welded and machined superalloy gas turbine rings and shrouds.", "2840", ["Material_Inconel_718", "Material_Titanium_Ti6Al4V"],
     "NADCAP Welding & Machining", "Aerospace engine component fabrication and NDT.", "EngineeringService", "NADCAP",
     ["Pratt & Whitney", "GE Aerospace"], "ACM member"),

    ("G&W Machine Co., Inc.", "G&W Machine", "East Windsor", "CT", "https://www.gwmachine.com", "SMESupplier",
     ["AS9100D", "ITAR_Compliant"], ["AirPlatform", "DomainAeronautics"],
     ["Platform_UH60_BlackHawk", "Platform_F35_Lightning_II"], ["KIC_AerospaceSystems"],
     "Precision Aerospace Milling & Turning", "CNC milling, turning, and grinding of aerospace structural and engine components.", "KIC_AerospaceSystems",
     "Precision Machined Aero Fittings", "Tight-tolerance machined aerospace fittings and housings.", "1560", ["Material_Titanium_Ti6Al4V"],
     "AS9100D Contract Machining", "Build-to-print CNC machining.", "EngineeringService", "AS9100D",
     ["Pratt & Whitney", "Sikorsky Aircraft"], "ACM member"),

    ("ACMT, Inc.", "ACMT", "Manchester", "CT", "https://www.acmtinc.com", "Tier2Supplier",
     ["AS9100D", "NADCAP_Welding", "NADCAP_NDT", "ITAR_Compliant"], ["AirPlatform", "DomainAeronautics"],
     ["Platform_F35_Lightning_II", "Platform_KC46_Pegasus"], ["KIC_AerospaceSystems"],
     "Aerospace Sheet Metal & Engine Ducting", "Complex sheet metal fabrication, hydroforming, and welding for jet engine nacelles and ducting.", "KIC_AerospaceSystems",
     "Jet Engine Bleed Air Ducting & Fairings", "Precision-formed and welded titanium and Inconel engine ducting.", "2840", ["Material_Inconel_718", "Material_Titanium_Ti6Al4V"],
     "NADCAP Aerospace Sheet Metal", "Hydroforming, laser cutting, and NADCAP welding.", "EngineeringService", "NADCAP",
     ["Pratt & Whitney", "Collins Aerospace"], "NHADC / ACM member"),

    ("L&I Precision Machining, Inc.", "L&I Precision", "New Britain", "CT", "https://www.liprecision.com", "SMESupplier",
     ["AS9100D", "ITAR_Compliant"], ["AirPlatform", "DomainAeronautics"],
     ["Platform_F35_Lightning_II", "Platform_UH60_BlackHawk"], ["KIC_AerospaceSystems"],
     "CNC Swiss & Multi-Axis Machining", "Precision Swiss turning and 5-axis milling for aerospace and defense hardware.", "KIC_AerospaceSystems",
     "Precision Swiss-Turned Aerospace Pins", "Tight-tolerance pins, shafts, and bushings for flight controls.", "5315", ["Material_Titanium_Ti6Al4V"],
     "AS9100D Swiss Machining", "High-volume precision Swiss turning.", "EngineeringService", "AS9100D",
     ["Collins Aerospace", "Sikorsky Aircraft"], "ACM member"),

    ("Horst Engineering & Manufacturing Co.", "Horst Engineering", "East Hartford", "CT", "https://www.horstengineering.com", "Tier2Supplier",
     ["AS9100D", "NADCAP_NDT", "ITAR_Compliant"], ["AirPlatform", "DomainAeronautics"],
     ["Platform_F35_Lightning_II", "Platform_CH53K_KingStallion"], ["KIC_AerospaceSystems"],
     "Precision Machined Aerospace Fasteners & Bushings", "CNC Swiss turning, thread rolling, and centerless grinding of flight-critical fasteners.", "KIC_AerospaceSystems",
     "Flight-Critical Precision Bolts & Pins", "High-strength titanium and Inconel aerospace fasteners.", "5306", ["Material_Titanium_Ti6Al4V", "Material_Inconel_718"],
     "AS9100D Fastener Manufacturing", "Precision turning, grinding, and thread rolling.", "EngineeringService", "AS9100D",
     ["Pratt & Whitney", "Sikorsky Aircraft"], "ACM member"),

    ("Kaman Specialty Bearings & Engineered Products", "Kaman Specialty Bearings", "Bloomfield", "CT", "https://www.kamanaerosystems.com", "Tier2Supplier",
     ["AS9100D", "NADCAP_NDT", "ITAR_Compliant"], ["AirPlatform", "DomainAeronautics"],
     ["Platform_UH60_BlackHawk", "Platform_F35_Lightning_II"], ["KIC_AerospaceSystems"],
     "Self-Lubricating Aerospace Bearings", "Design and manufacture of KAron self-lubricating bearings and mechanical flight control assemblies.", "KIC_AerospaceSystems",
     "KAron Self-Lubricating Airframe Bearings", "High-load, maintenance-free spherical and journal bearings.", "3120", ["Material_Titanium_Ti6Al4V"],
     "Bearing Qualification & Testing", "Load, wear, and environmental qualification of aerospace bearings.", "TestingQualificationService", "AS9100D",
     ["Sikorsky Aircraft", "Boeing", "Lockheed Martin"], "Company website"),

    # --- MA (Massachusetts) ---
    ("Whalley Precision, Inc.", "Whalley Precision", "Southwick", "MA", "https://www.whalleyprecision.com", "SMESupplier",
     ["AS9100D", "ISO9001", "ITAR_Compliant", "CMMC_Level2"], ["AirPlatform", "DomainDefence", "DomainAeronautics"],
     ["Platform_F35_Lightning_II", "Platform_UH60_BlackHawk"], ["KIC_AerospaceSystems"],
     "Tight-Tolerance 5-Axis CNC Machining", "Precision 5-axis milling, turning, and Swiss machining of aerospace and defense components.", "KIC_AerospaceSystems",
     "Precision Machined Flight Hardware", "Complex multi-axis machined brackets, housings, and actuators.", "1560", ["Material_Titanium_Ti6Al4V", "Material_Inconel_718"],
     "AS9100D CNC Machining", "Build-to-print precision machining for defense primes.", "EngineeringService", "AS9100D",
     ["Collins Aerospace", "Pratt & Whitney", "Raytheon"], "Company website AS9100D & ITAR verification"),

    ("Peerless Precision, Inc.", "Peerless Precision", "Westfield", "MA", "https://www.peerlessprecision.com", "SMESupplier",
     ["AS9100D", "ISO9001", "ITAR_Compliant", "CMMC_Level2"], ["AirPlatform", "DomainDefence", "DomainAeronautics"],
     ["Platform_F35_Lightning_II", "Platform_F15EX_EagleII"], ["KIC_AerospaceSystems"],
     "Ultra-Precision Grinding, Honing & CNC Machining", "Sub-micron tolerance grinding, honing, lapping, and CNC machining for aerospace fuel and hydraulic valves.", "KIC_AerospaceSystems",
     "Precision Hydraulic & Fuel Valve Spools", "Tight-tolerance lapped and honed aerospace fluid control components.", "4820", ["Material_Inconel_718", "Material_Titanium_Ti6Al4V"],
     "Precision Grinding & Lapping", "Contract ultra-precision machining and ID/OD grinding.", "EngineeringService", "AS9100D",
     ["Collins Aerospace", "Moog Inc.", "Woodward"], "Company website AS9100D & ITAR verification"),

    ("B&E Tool & Manufacturing Co., Inc.", "B&E Tool", "Southwick", "MA", "https://www.betool.com", "Tier2Supplier",
     ["AS9100D", "NADCAP_NDT", "ITAR_Compliant"], ["AirPlatform", "DomainAeronautics", "DomainDefence"],
     ["Platform_F35_Lightning_II", "Platform_F22_Raptor"], ["KIC_AerospaceSystems"],
     "5-Axis Turbine & Structural Machining", "Large-format and 5-axis CNC machining of jet engine casings, shrouds, and structural frames.", "KIC_AerospaceSystems",
     "Machined Jet Engine Casings", "Precision-machined superalloy turbine cases and structural rings.", "2840", ["Material_Inconel_718", "Material_Titanium_Ti6Al4V"],
     "5-Axis Aerospace Machining", "Complex multi-axis machining and NADCAP NDT inspection.", "EngineeringService", "AS9100D",
     ["Pratt & Whitney", "GE Aerospace"], "Company website"),

    ("Advance Manufacturing Co., Inc.", "Advance Manufacturing", "Westfield", "MA", "https://www.advancemfg.com", "Tier2Supplier",
     ["AS9100D", "NADCAP_NDT", "NADCAP_Welding", "ITAR_Compliant"], ["AirPlatform", "MaritimePlatform", "DomainDefence"],
     ["Platform_VirginiaClass_Submarine", "Platform_F35_Lightning_II"], ["KIC_AerospaceSystems", "KIC_NavalShipbuilding"],
     "Large-Scale Precision Machining & Fabrication", "Heavy 5-axis CNC machining, welding, and assembly for naval submarine and aerospace propulsion.", "KIC_NavalShipbuilding",
     "Submarine & Aero-Engine Structural Assemblies", "Large-envelope machined and welded titanium and nickel-alloy assemblies.", "2090", ["Material_Titanium_Ti6Al4V", "Material_Inconel_718"],
     "Large-Envelope CNC Machining", "Contract machining and NADCAP welding for defense primes.", "EngineeringService", "AS9100D",
     ["General Dynamics Electric Boat", "Pratt & Whitney"], "Company website"),

    ("ConductRF", "ConductRF", "Methuen", "MA", "https://www.conductrf.com", "SMESupplier",
     ["AS9100D", "ISO9001", "ITAR_Compliant"], ["AirPlatform", "SpacePlatform", "DomainC4ISR"],
     ["Platform_F35_Lightning_II", "Platform_LEOSatellite"], ["KIC_SensorsSonar", "KIC_SoftwareDefinedRadio"],
     "RF & Microwave Coaxial Cable Assemblies", "Design and manufacture of high-frequency, phase-stable RF/microwave cable assemblies for radar and EW.", "KIC_SensorsSonar",
     "High-Frequency Mil-Spec RF Cable Assemblies", "Low-loss, phase-matched microwave interconnects up to 110 GHz.", "5995", ["Material_GalliumNitride_GaN"],
     "RF Interconnect Engineering & Testing", "Custom RF cable design and VNA phase/loss qualification.", "TestingQualificationService", "AS9100D",
     ["Raytheon", "BAE Systems", "Lockheed Martin"], "Microwave Journal AS9100 verification"),

    ("Charles River Analytics, Inc.", "Charles River Analytics", "Cambridge", "MA", "https://www.cra.com", "SMESupplier",
     ["ISO9001", "DFARS_NIST800171", "ITAR_Compliant"], ["UASPlatform", "DomainC4ISR", "DomainDefence"],
     ["Platform_TacticalUAS", "Platform_MQ9B_SkyGuardian"], ["KIC_AIAutonomousSystems", "KIC_SensorsSonar"],
     "DoD SBIR/STTR AI, Autonomy & Sensor Fusion", "Prolific DoD SBIR/STTR awardee developing autonomous teaming, probabilistic reasoning, and multi-sensor fusion software.", "KIC_AIAutonomousSystems",
     "Autonomous Mission Planning & Sensor Fusion Suite", "AI-driven multi-domain autonomy and ISR data fusion software.", "7030", [],
     "AI & Autonomy R&D Engineering", "Contract R&D under DARPA, AFRL, and ONR SBIR/STTR programs.", "EngineeringService", "DCMA",
     ["DARPA", "US Air Force", "US Navy"], "DoD SBIR/STTR awardee"),

    ("Triton Systems, Inc.", "Triton Systems", "Chelmsford", "MA", "https://www.tritonsystems.com", "SMESupplier",
     ["ISO9001", "ITAR_Compliant", "DFARS_NIST800171"], ["AirPlatform", "MaritimePlatform", "DomainDefence"],
     ["Platform_F35_Lightning_II", "Platform_VirginiaClass_Submarine"], ["KIC_AdvancedMaterials", "KIC_AIAutonomousSystems"],
     "DoD SBIR Advanced Materials & Defense Hardware", "DoD SBIR/STTR awardee developing high-temp composites, energetic materials, and autonomous maritime sensors.", "KIC_AdvancedMaterials",
     "High-Temperature Aerospace Composite Structures", "Lightweight thermal-resistant composite and ceramic matrix components.", "1560", ["Material_CarbonFiber_Composite", "Material_SiliconCarbide_SiC"],
     "Defense R&D & Prototyping", "SBIR Phase II/III applied materials and hardware engineering.", "EngineeringService", "DCMA",
     ["US Navy", "US Air Force", "US Army"], "DoD SBIR/STTR awardee"),

    ("Physical Sciences Inc.", "PSI", "Andover", "MA", "https://www.psicorp.com", "Tier2Supplier",
     ["ISO9001", "ITAR_Compliant", "FacilitySecurity_Secret"], ["AirPlatform", "SpacePlatform", "DomainDefence"],
     ["Platform_THAAD", "Platform_TacticalUAS"], ["KIC_EOIRSystems", "KIC_AdvancedMaterials"],
     "Directed Energy, EO/IR Sensors & Hypersonic Materials", "DoD SBIR/STTR leader in laser systems, optical sensors, and ultra-high-temperature hypersonic materials.", "KIC_EOIRSystems",
     "Tactical Laser & EO/IR Sensor Payloads", "Compact solid-state laser and optical sensing systems for defense.", "5855", ["Material_SiliconCarbide_SiC"],
     "Applied Physics & Defense R&D", "Contract R&D and prototype delivery for DoD and NASA.", "EngineeringService", "DCMA",
     ["DARPA", "Missile Defense Agency", "US Air Force"], "DoD SBIR/STTR awardee"),

    ("Aerodyne Research, Inc.", "Aerodyne Research", "Billerica", "MA", "https://www.aerodyne.com", "SMESupplier",
     ["ISO9001", "ITAR_Compliant", "DFARS_NIST800171"], ["AirPlatform", "SpacePlatform", "DomainDefence"],
     ["Platform_F35_Lightning_II", "Platform_LEOSatellite"], ["KIC_EOIRSystems", "KIC_SensorsSonar"],
     "Optical Signatures, Plume Physics & Remote Sensing", "DoD SBIR/STTR specialist in infrared signature modeling, electro-optical sensors, and trace gas detection.", "KIC_EOIRSystems",
     "Infrared Signature & Optical Sensor Systems", "Precision optical instrumentation for missile and aircraft signature measurement.", "5855", ["Material_Beryllium_Optical"],
     "EO/IR Signature Analysis & Testing", "Custom optical sensor development and field measurement campaigns.", "TestingQualificationService", "DCMA",
     ["US Air Force", "DARPA", "Missile Defense Agency"], "DoD SBIR/STTR awardee"),

    ("Riptide Autonomous Solutions", "Riptide", "Plymouth", "MA", "https://www.baesystems.com", "Tier2Supplier",
     ["ISO9001", "ITAR_Compliant"], ["MaritimePlatform", "UASPlatform", "DomainDefence"],
     ["Platform_VirginiaClass_Submarine"], ["KIC_RemotelyPilotedSystems", "KIC_AIAutonomousSystems"],
     "Micro-UUV & Autonomous Undersea Vehicles", "Design and manufacture of modular, open-architecture micro-uncrewed undersea vehicles (UUVs).", "KIC_RemotelyPilotedSystems",
     "Riptide Micro-UUV Family", "Flexible, open-architecture autonomous undersea vehicles for ISR and mine countermeasures.", "1990", ["Material_CarbonFiber_Composite"],
     "UUV Payload Integration & Testing", "At-sea UUV autonomy and sensor payload integration.", "TestingQualificationService", "DCMA",
     ["US Navy", "ONR"], "DoD SBIR/UUV supplier"),

    ("Tebaldi Precision, Inc.", "Tebaldi Precision", "West Springfield", "MA", "https://www.tebaldiprecision.com", "SMESupplier",
     ["AS9100D", "ITAR_Compliant"], ["AirPlatform", "DomainAeronautics"],
     ["Platform_F35_Lightning_II", "Platform_UH60_BlackHawk"], ["KIC_AerospaceSystems"],
     "Precision CNC Milling & Turning", "Contract CNC machining of aerospace brackets, housings, and engine components.", "KIC_AerospaceSystems",
     "Machined Aerospace Structural Brackets", "Tight-tolerance aluminum and titanium structural brackets.", "1560", ["Material_Titanium_Ti6Al4V"],
     "AS9100D Contract Machining", "Build-to-print CNC milling and turning.", "EngineeringService", "AS9100D",
     ["Pratt & Whitney", "Collins Aerospace"], "ACM member"),

    ("Tell Tool, Inc.", "Tell Tool", "Westfield", "MA", "https://www.telltool.com", "SMESupplier",
     ["AS9100D", "ITAR_Compliant"], ["AirPlatform", "DomainAeronautics"],
     ["Platform_F35_Lightning_II", "Platform_F22_Raptor"], ["KIC_AerospaceSystems"],
     "5-Axis Aerospace & Turbine Machining", "Precision 5-axis CNC machining of jet engine components, shrouds, and housings.", "KIC_AerospaceSystems",
     "Machined Turbine Shrouds & Rings", "Precision-machined superalloy engine components.", "2840", ["Material_Inconel_718"],
     "AS9100D 5-Axis Machining", "Contract multi-axis machining for aerospace.", "EngineeringService", "AS9100D",
     ["Pratt & Whitney", "GE Aerospace"], "ACM member"),

    ("Hoppe Technologies, Inc.", "Hoppe Technologies", "Chicopee", "MA", "https://www.hoppetech.com", "Tier2Supplier",
     ["AS9100D", "NADCAP_NDT", "ITAR_Compliant"], ["AirPlatform", "DomainAeronautics"],
     ["Platform_F35_Lightning_II", "Platform_UH60_BlackHawk"], ["KIC_AerospaceSystems"],
     "Precision Aerospace Machining & Assembly", "Multi-axis CNC machining, assembly, and kitting of flight-critical aerospace hardware.", "KIC_AerospaceSystems",
     "Machined Flight Control & Engine Assemblies", "Turnkey machined and assembled aerospace sub-assemblies.", "1560", ["Material_Titanium_Ti6Al4V"],
     "AS9100D Machining & Kitting", "Build-to-print CNC machining and mechanical assembly.", "EngineeringService", "AS9100D",
     ["Collins Aerospace", "Sikorsky Aircraft"], "ACM member"),

    ("E.T. & F. Machining, Inc.", "ET&F Machining", "Agawam", "MA", "https://www.etfmachining.com", "SMESupplier",
     ["AS9100D", "ITAR_Compliant"], ["AirPlatform", "DomainAeronautics"],
     ["Platform_F35_Lightning_II", "Platform_KC46_Pegasus"], ["KIC_AerospaceSystems"],
     "Aerospace CNC Turning & Milling", "Precision CNC turning and milling of aerospace fluid fittings and structural parts.", "KIC_AerospaceSystems",
     "Machined Aerospace Fluid Fittings", "Tight-tolerance turned and milled aerospace hardware.", "4730", ["Material_Titanium_Ti6Al4V"],
     "AS9100D Contract Machining", "Precision CNC turning and milling.", "EngineeringService", "AS9100D",
     ["Collins Aerospace", "Pratt & Whitney"], "ACM member"),

    ("Aptima, Inc.", "Aptima", "Woburn", "MA", "https://www.aptima.com", "SMESupplier",
     ["ISO9001", "DFARS_NIST800171", "FacilitySecurity_Secret"], ["AirPlatform", "DomainC4ISR", "DomainDefence"],
     ["Platform_F35_Lightning_II", "Platform_TacticalUAS"], ["KIC_TrainingSimulation", "KIC_AIAutonomousSystems"],
     "DoD SBIR Human-Centered AI & LVC Training", "DoD SBIR/STTR leader in Live-Virtual-Constructive (LVC) training assessment and human-machine teaming.", "KIC_TrainingSimulation",
     "SPOTLITE LVC Training Assessment System", "AI-enabled performance measurement for military flight and C2 simulators.", "6910", [],
     "Human-Systems Integration R&D", "SBIR/STTR R&D for AFRL, ONR, and DARPA.", "SimulationTrainingService", "DCMA",
     ["US Air Force", "US Navy", "DARPA"], "DoD SBIR/STTR awardee"),

    # --- NH (New Hampshire) ---
    ("Creare LLC", "Creare", "Hanover", "NH", "https://www.creare.com", "SMESupplier",
     ["ISO9001", "ITAR_Compliant", "DFARS_NIST800171"], ["AirPlatform", "SpacePlatform", "MaritimePlatform"],
     ["Platform_LEOSatellite", "Platform_VirginiaClass_Submarine"], ["KIC_AerospaceSystems", "KIC_SpaceSystems"],
     "DoD SBIR Cryocoolers, Turbomachinery & Acoustics", "Premier DoD SBIR/STTR engineering firm developing miniature cryocoolers, micro-turbomachinery, and acoustic sensors.", "KIC_SpaceSystems",
     "Space-Qualified Miniature Cryocoolers", "Long-life, low-vibration cryocoolers for space EO/IR focal plane arrays.", "1810", ["Material_Titanium_Ti6Al4V"],
     "Advanced Thermomechanical R&D", "SBIR/STTR prototype engineering and qualification.", "EngineeringService", "DCMA",
     ["NASA", "US Air Force", "US Navy"], "DoD SBIR/STTR awardee"),

    ("New Hampshire Ball Bearings, Inc.", "NHBB", "Peterborough", "NH", "https://www.nhbb.com", "Tier2Supplier",
     ["AS9100D", "NADCAP_NDT", "ITAR_Compliant"], ["AirPlatform", "SpacePlatform", "DomainAeronautics"],
     ["Platform_F35_Lightning_II", "Platform_UH60_BlackHawk"], ["KIC_AerospaceSystems"],
     "Precision Aerospace Bearings & Rod Ends", "Manufacture of miniature, instrument, and spherical plain bearings for flight controls and turbine engines.", "KIC_AerospaceSystems",
     "Aerospace Main-Shaft & Airframe Bearings", "High-precision ceramic-hybrid and steel bearings for aerospace.", "3110", ["Material_SiliconCarbide_SiC"],
     "Bearing Tribology & Qualification Testing", "Life testing and qualification of flight-critical bearings.", "TestingQualificationService", "AS9100D",
     ["Pratt & Whitney", "Sikorsky Aircraft", "Boeing"], "Company website"),

    ("Cirtronics Corporation", "Cirtronics", "Milford", "NH", "https://www.cirtronics.com", "Tier2Supplier",
     ["AS9100D", "ISO9001", "ITAR_Compliant"], ["AirPlatform", "DomainC4ISR", "DomainDefence"],
     ["Platform_TacticalUAS", "Platform_DDG51_ArleighBurke"], ["KIC_SensorsSonar", "KIC_CyberResilience"],
     "High-Reliability Defense Electronics Manufacturing", "Contract electronics manufacturing (PCBA, box build, electromechanical assembly) for defense and aerospace.", "KIC_SensorsSonar",
     "Ruggedized Defense PCBA & Box Builds", "IPC Class 3 printed circuit board assemblies and tactical enclosures.", "5998", [],
     "Defense EMS & Box Build", "Turnkey PCB assembly, conformal coating, and functional test.", "EngineeringService", "AS9100D",
     ["BAE Systems", "Raytheon", "L3Harris"], "Company website"),

    ("Mikros Systems Corporation", "Mikros Systems", "Princeton", "NJ", "https://www.mikrossystems.com", "SMESupplier",
     ["ISO9001", "ITAR_Compliant", "FacilitySecurity_Secret"], ["MaritimePlatform", "DomainC4ISR", "DomainDefence"],
     ["Platform_DDG51_ArleighBurke", "Platform_FordClass_Carrier"], ["KIC_SensorsSonar", "KIC_InServiceSupport"],
     "Naval Radar Prognostics & Condition-Based Maintenance", "DoD SBIR/STTR graduate providing automated radar calibration, prognostics, and electronic warfare test systems.", "KIC_SensorsSonar",
     "ADAPT Naval Radar Prognostic System", "Automated diagnostic and prognostic instrumentation for Aegis radar systems.", "6625", [],
     "Naval Combat System Sustainment", "Condition-based maintenance and radar test engineering.", "TestingQualificationService", "DCMA",
     ["US Navy", "Lockheed Martin"], "DoD SBIR/STTR awardee"),

    # --- NJ (New Jersey) ---
    ("New Jersey Precision Technologies, Inc.", "NJPT", "Mountainside", "NJ", "https://www.njpt.com", "SMESupplier",
     ["AS9100D", "ISO9001", "ITAR_Compliant"], ["AirPlatform", "SpacePlatform", "DomainDefence"],
     ["Platform_F35_Lightning_II", "Platform_THAAD"], ["KIC_AerospaceSystems", "KIC_Munitions"],
     "Precision Wire, Sinker & Hole-Drilling EDM", "High-precision electrical discharge machining (EDM) for avionics, missile guidance, and spaceflight hardware.", "KIC_AerospaceSystems",
     "EDM-Machined Avionics & Missile Components", "Micro-tolerance EDM components in exotic and hardened alloys.", "1560", ["Material_Inconel_718", "Material_Titanium_Ti6Al4V"],
     "AS9100D Contract EDM Machining", "Wire, sinker, and small-hole EDM for defense primes.", "EngineeringService", "AS9100D",
     ["Lockheed Martin", "Northrop Grumman"], "Company website AS9100 verification"),

    ("TIS Aerospace", "TIS Aerospace", "Cinnaminson", "NJ", "https://www.tisaerospace.com", "SMESupplier",
     ["AS9100D", "ITAR_Compliant"], ["AirPlatform", "DomainAeronautics", "DomainDefence"],
     ["Platform_F35_Lightning_II", "Platform_FA18_SuperHornet"], ["KIC_AerospaceSystems"],
     "Tight-Tolerance Aerospace CNC Milling & Turning", "Build-to-print CNC milling, live-tooling turning, and assembly for military aviation.", "KIC_AerospaceSystems",
     "Machined Airframe & Landing Gear Fittings", "Precision-machined aluminum, titanium, and steel flight hardware.", "1560", ["Material_Titanium_Ti6Al4V"],
     "AS9100D Build-to-Print Machining", "CNC milling, turning, and kitting for defense.", "EngineeringService", "AS9100D",
     ["Boeing", "Lockheed Martin"], "Company website AS9100 & ITAR verification"),

    ("GPR Company", "GPR Company", "Fairfield", "NJ", "https://www.gprco.com", "SMESupplier",
     ["ISO9001", "ITAR_Compliant"], ["AirPlatform", "LandPlatform", "DomainDefence"],
     ["Platform_F35_Lightning_II", "Platform_M1A2_Abrams"], ["KIC_AerospaceSystems", "KIC_ArmouredVehicles"],
     "Precision Defense & Aerospace CNC Machining", "ITAR-registered contract machining of complex military, aerospace, and optical housings.", "KIC_AerospaceSystems",
     "Machined Optical & Defense Housings", "Tight-tolerance CNC-machined housings and mechanical assemblies.", "1560", ["Material_Titanium_Ti6Al4V"],
     "ITAR Contract CNC Machining", "Multi-axis CNC milling and turning for defense.", "EngineeringService", "ISO9001",
     ["L3Harris", "BAE Systems"], "Company website ITAR verification"),

    ("Schrader & Co., Inc.", "Schrader & Co.", "Newton", "NJ", "https://www.schradermachining.com", "SMESupplier",
     ["ISO9001", "ITAR_Compliant"], ["AirPlatform", "DomainAeronautics"],
     ["Platform_KC46_Pegasus", "Platform_C130J_SuperHercules"], ["KIC_AerospaceSystems"],
     "Aerospace CNC Machining & Sheet Metal", "Precision vertical milling, turning, and sheet metal fabrication for aerospace tier contractors.", "KIC_AerospaceSystems",
     "Machined Aircraft Brackets & Enclosures", "Precision-machined aluminum and steel aircraft components.", "1560", [],
     "Precision CNC & Sheet Metal", "Contract machining and sheet metal fabrication.", "EngineeringService", "ISO9001",
     ["Collins Aerospace", "Honeywell"], "Thomasnet aerospace directory"),

    ("Rosenberger North America", "Rosenberger NA", "Pennsauken", "NJ", "https://www.rosenberger.com", "Tier2Supplier",
     ["AS9100D", "ISO9001", "ITAR_Compliant"], ["AirPlatform", "SpacePlatform", "DomainC4ISR"],
     ["Platform_F35_Lightning_II", "Platform_LEOSatellite"], ["KIC_SensorsSonar", "KIC_SpaceSystems"],
     "Hermetic Glass-to-Metal Seals & RF Connectors", "Swiss CNC machining and hermetic glass-to-metal sealing for military radar, microwave, and space electronics.", "KIC_SensorsSonar",
     "Hermetic RF & Microwave Connectors", "High-reliability hermetically sealed RF feedthroughs and connectors.", "5935", ["Material_Inconel_718"],
     "Hermetic Sealing & Swiss Machining", "Custom hermetic packaging and RF interconnect engineering.", "EngineeringService", "AS9100D",
     ["Lockheed Martin", "Raytheon", "Northrop Grumman"], "Company website"),

    # --- PA (Pennsylvania) ---
    ("Astro Machine Works, Inc.", "Astro Machine Works", "Ephrata", "PA", "https://www.astromachineworks.com", "Tier2Supplier",
     ["AS9100D", "ISO9001", "ITAR_Compliant"], ["AirPlatform", "MaritimePlatform", "DomainDefence"],
     ["Platform_VirginiaClass_Submarine", "Platform_F35_Lightning_II"], ["KIC_AerospaceSystems", "KIC_NavalShipbuilding"],
     "Precision CNC Machining & Custom Machinery", "AS9100D CNC machining, welding, and mechanical assembly for aerospace, defense, and naval systems.", "KIC_AerospaceSystems",
     "Machined Defense & Naval Sub-Assemblies", "Large-part CNC-machined structural and propulsion components.", "2090", ["Material_Titanium_Ti6Al4V", "Material_Inconel_718"],
     "AS9100D Contract Manufacturing", "CNC machining, welding, and turnkey mechanical assembly.", "EngineeringService", "AS9100D",
     ["General Dynamics", "Lockheed Martin"], "Company website"),

    ("Modern Industries, Inc.", "Modern Industries", "Erie", "PA", "https://www.modernind.com", "Tier2Supplier",
     ["AS9100D", "ISO9001", "NADCAP_HeatTreating", "ITAR_Compliant"], ["AirPlatform", "LandPlatform", "DomainDefence"],
     ["Platform_M1A2_Abrams", "Platform_F35_Lightning_II"], ["KIC_AerospaceSystems", "KIC_AdvancedMaterials"],
     "Precision Machining, Grinding & Thermal Heat Treating", "Integrated CNC machining, precision grinding, welding, and commercial heat treating for defense.", "KIC_AdvancedMaterials",
     "Heat-Treated & Ground Defense Components", "Precision-ground hydraulic and powertrain components.", "2520", ["Material_Inconel_718"],
     "NADCAP Heat Treating & Machining", "In-house thermal processing, NDT, and CNC machining.", "EngineeringService", "NADCAP",
     ["General Dynamics", "GE Aerospace"], "Company website"),

    ("PMF Industries, Inc.", "PMF Industries", "Williamsport", "PA", "https://www.pmfind.com", "Tier2Supplier",
     ["AS9100D", "NADCAP_Welding", "NADCAP_HeatTreating", "ITAR_Compliant"], ["AirPlatform", "SpacePlatform", "DomainAeronautics"],
     ["Platform_F35_Lightning_II", "Platform_SpaceLaunchVehicle"], ["KIC_AerospaceSystems", "KIC_AdvancedMaterials"],
     "Flow Forming, Spin Forming & Laser Cutting", "Precision metal forming (flow turning/spin forming) of thin-wall cylindrical aerospace and missile casings.", "KIC_AdvancedMaterials",
     "Flow-Formed Rocket & Turbine Casings", "Seamless, high-strength flow-formed superalloy and titanium cylinders.", "1420", ["Material_Inconel_718", "Material_Titanium_Ti6Al4V"],
     "Aerospace Flow Forming & Heat Treat", "Precision metal forming, laser cutting, and NADCAP welding.", "EngineeringService", "AS9100D",
     ["Pratt & Whitney", "Aerojet Rocketdyne"], "Company website"),

    ("King Precision Solutions", "King Precision", "Erie", "PA", "https://www.kingprecisionsolutions.com", "SMESupplier",
     ["ISO9001", "ITAR_Compliant"], ["AirPlatform", "LandPlatform", "DomainDefence"],
     ["Platform_M2_Bradley", "Platform_JLTV"], ["KIC_ArmouredVehicles", "KIC_AerospaceSystems"],
     "Turnkey Defense Prototyping & CNC Machining", "ITAR-registered precision machining, prototyping, and production for defense supply chains.", "KIC_ArmouredVehicles",
     "Machined Tactical Vehicle & Defense Parts", "Precision-machined aluminum, steel, and alloy defense components.", "2590", [],
     "ITAR Precision Machining", "CNC milling, turning, and turnkey assembly.", "EngineeringService", "ISO9001",
     ["General Dynamics", "BAE Systems"], "Company website"),

    ("Precision Wire Products, Inc.", "Precision Wire Products", "Blairsville", "PA", "https://www.precisionwireproducts.com", "SMESupplier",
     ["ISO9001", "ITAR_Compliant"], ["AirPlatform", "DomainAeronautics"],
     ["Platform_F35_Lightning_II", "Platform_C130J_SuperHercules"], ["KIC_AerospaceSystems", "KIC_AdvancedMaterials"],
     "High-Temp Alloy CNC Machining & Wire Forming", "CNC machining of Inconel, Hastelloy, and stainless steel for aerospace and aircraft assemblies.", "KIC_AdvancedMaterials",
     "Superalloy Aerospace Fasteners & Wire Forms", "Precision-machined and formed high-temperature alloy components.", "5305", ["Material_Inconel_718"],
     "Superalloy Machining & Forming", "Contract CNC machining of exotic alloys.", "EngineeringService", "ISO9001",
     ["GE Aerospace", "Pratt & Whitney"], "Thomasnet directory"),

    ("Sanbor Manufacturing", "Sanbor Manufacturing", "Allentown", "PA", "https://www.sanbor.com", "Tier2Supplier",
     ["AS9100D", "ISO9001", "ITAR_Compliant"], ["AirPlatform", "DomainDefence"],
     ["Platform_UH60_BlackHawk", "Platform_JLTV"], ["KIC_SensorsSonar"],
     "Defense & Aerospace Electromechanical Assembly", "Contract manufacturing of ruggedized cable harnesses, PCB assemblies, and defense sub-assemblies.", "KIC_SensorsSonar",
     "Mil-Spec Electronic Sub-Assemblies", "Tested electronic control modules and cable harnesses.", "5998", [],
     "Contract Electronics Manufacturing", "PCBA, box build, and environmental stress screening.", "EngineeringService", "AS9100D",
     ["Lockheed Martin", "General Dynamics"], "Company website"),

    # --- NY (New York) ---
    ("CPI Aerostructures, Inc.", "CPI Aero", "Edgewood", "NY", "https://www.cpiaero.com", "Tier2Supplier",
     ["AS9100D", "NADCAP_NDT", "ITAR_Compliant"], ["AirPlatform", "DomainAeronautics", "DomainDefence"],
     ["Platform_F35_Lightning_II", "Platform_FA18_SuperHornet", "Platform_UH60_BlackHawk"], ["KIC_AerospaceSystems"],
     "Military Aerostructures & Pod Assemblies", "Manufacture of complex structural aircraft assemblies, pods, and aerosystems for US defense primes.", "KIC_AerospaceSystems",
     "Military Aircraft Pods & Structural Assemblies", "Electronic warfare pods, wingtip fairings, and fuselage assemblies.", "1560", ["Material_Titanium_Ti6Al4V", "Material_CarbonFiber_Composite"],
     "Aerostructure Assembly & Kitting", "Complex structural assembly, bonding, and supply chain management.", "EngineeringService", "AS9100D",
     ["Lockheed Martin", "Northrop Grumman", "Sikorsky Aircraft"], "Company website"),

    ("Arkwin Industries, Inc.", "Arkwin Industries", "Westbury", "NY", "https://www.arkwin.com", "Tier2Supplier",
     ["AS9100D", "NADCAP_NDT", "ITAR_Compliant"], ["AirPlatform", "SpacePlatform", "DomainAeronautics"],
     ["Platform_F35_Lightning_II", "Platform_F22_Raptor", "Platform_AH64_Apache"], ["KIC_AerospaceSystems"],
     "Aerospace Hydraulic & Fuel Actuation Systems", "Design and manufacture of precision hydraulic actuators, valves, and fluid control systems for military aircraft.", "KIC_AerospaceSystems",
     "Flight Control Hydraulic Actuators & Valves", "High-pressure aerospace hydraulic cylinders, manifolds, and reservoirs.", "1650", ["Material_Titanium_Ti6Al4V"],
     "Hydraulic System Design & Qualification", "Environmental and endurance qualification of aerospace fluid power.", "TestingQualificationService", "AS9100D",
     ["Lockheed Martin", "Boeing", "Pratt & Whitney"], "Company website"),

    ("Dayton T. Brown, Inc.", "Dayton T. Brown", "Bohemia", "NY", "https://www.dtbrown.com", "Tier2Supplier",
     ["AS9100D", "ISO9001", "ITAR_Compliant"], ["AirPlatform", "MaritimePlatform", "DomainDefence"],
     ["Platform_F35_Lightning_II", "Platform_P8_Poseidon"], ["KIC_AerospaceSystems", "KIC_InServiceSupport"],
     "Defense Environmental Testing & Engineering", "Independent MIL-STD-810/461 environmental, EMI/EMC, shock, vibration, and hydraulic testing.", "KIC_AerospaceSystems",
     "MIL-STD Qualification & Test Fixtures", "Custom aerospace ground support and automated test equipment.", "4920", [],
     "MIL-STD Environmental & EMI/EMC Testing", "Accredited aerospace and defense qualification testing.", "TestingQualificationService", "ISO/IEC 17025",
     ["Northrop Grumman", "Lockheed Martin", "US Navy"], "Company website"),

    ("East/West Industries, Inc.", "East/West Industries", "Ronkonkoma", "NY", "https://www.eastwestindustries.com", "Tier2Supplier",
     ["AS9100D", "ISO9001", "ITAR_Compliant"], ["AirPlatform", "DomainAeronautics", "DomainDefence"],
     ["Platform_UH60_BlackHawk", "Platform_CH53K_KingStallion", "Platform_V22_Osprey"], ["KIC_AerospaceSystems"],
     "Aircraft Crew Seats & Life Support Systems", "Design and manufacture of crashworthy helicopter crew seats, oxygen systems, and ground support equipment.", "KIC_AerospaceSystems",
     "Crashworthy Military Crew & Troop Seats", "Energy-absorbing armored crew seating for military rotorcraft.", "1680", ["Material_CarbonFiber_Composite", "Material_Kevlar_Aramid"],
     "Crew Survivability Engineering & Testing", "Dynamic crashworthiness testing and FAA/military qualification.", "TestingQualificationService", "AS9100D",
     ["Sikorsky Aircraft", "Bell Textron", "Boeing"], "Company website"),

    ("Telephonics Corporation", "Telephonics", "Farmingdale", "NY", "https://www.telephonics.com", "Tier2Supplier",
     ["AS9100D", "ISO9001", "ITAR_Compliant", "FacilitySecurity_Secret"], ["AirPlatform", "MaritimePlatform", "DomainC4ISR"],
     ["Platform_P8_Poseidon", "Platform_UH60_BlackHawk"], ["KIC_SensorsSonar", "KIC_SoftwareDefinedRadio"],
     "Maritime Surveillance Radar & Intercommunications", "Design and manufacture of airborne maritime surveillance radars, IFF, and digital intercommunication systems.", "KIC_SensorsSonar",
     "APS-143/147 Maritime Surveillance Radar", "Multi-mode airborne maritime surveillance and weather radar.", "5841", [],
     "Radar & Comms System Integration", "Engineering, testing, and depot MRO for airborne radar.", "MROService", "AS9100D",
     ["Sikorsky Aircraft", "US Navy", "Lockheed Martin"], "Company website"),

    # --- VA (Virginia) & MD (Maryland) ---
    ("Azure Summit Technology, Inc.", "Azure Summit Technology", "Fairfax", "VA", "https://www.azuresummit.com", "Tier2Supplier",
     ["ISO9001", "ITAR_Compliant", "FacilitySecurity_TopSecret"], ["AirPlatform", "MaritimePlatform", "DomainC4ISR"],
     ["Platform_P8_Poseidon", "Platform_FA18_SuperHornet"], ["KIC_SensorsSonar", "KIC_SoftwareDefinedRadio"],
     "DoD SBIR Wideband RF & Electronic Warfare", "DoD SBIR Phase III graduate developing wideband RF transceivers, EW payloads, and passive surveillance systems.", "KIC_SensorsSonar",
     "Switchblade Wideband RF EW Processor", "High-performance multi-channel RF signal acquisition and EW system.", "5865", ["Material_GalliumNitride_GaN"],
     "EW & RF Systems Engineering", "Rapid prototyping and integration of naval/airborne EW.", "EngineeringService", "DCMA",
     ["US Navy", "NAVAIR", "ONR"], "DoD SBIR Phase III awardee"),

    ("Dynamic Dimension Technologies, LLC", "Dynamic Dimension Technologies", "Westminster", "MD", "https://www.ddt-llc.com", "SMESupplier",
     ["ISO9001", "ITAR_Compliant", "DFARS_NIST800171"], ["MaritimePlatform", "DomainC4ISR", "DomainDefence"],
     ["Platform_DDG51_ArleighBurke", "Platform_FordClass_Carrier"], ["KIC_SoftwareDefinedRadio", "KIC_TrainingSimulation"],
     "DoD SBIR Shipboard Wireless & Virtual Twins", "DoD SBIR awardee developing shipboard wireless LANs, tactical simulation, and virtual twin corridors.", "KIC_SoftwareDefinedRadio",
     "Shipboard Ruggedized Wireless Network", "Secure RF-hardened wireless communications for naval vessels.", "5820", [],
     "Naval Comms & Simulation Engineering", "SBIR R&D for NAVSEA and Patuxent River.", "EngineeringService", "DCMA",
     ["US Navy", "NAVSEA", "NAWCAD"], "Navy SBIR awardee"),

    ("Metron, Inc.", "Metron", "Reston", "VA", "https://www.metsci.com", "SMESupplier",
     ["ISO9001", "ITAR_Compliant", "FacilitySecurity_TopSecret"], ["MaritimePlatform", "UASPlatform", "DomainC4ISR"],
     ["Platform_VirginiaClass_Submarine", "Platform_TacticalUAS"], ["KIC_AIAutonomousSystems", "KIC_SensorsSonar"],
     "DoD SBIR Undersea Autonomy & Bayesian Tracking", "DoD SBIR/STTR leader in autonomous underwater vehicle (UUV) mission planning and multi-target tracking.", "KIC_AIAutonomousSystems",
     "Resilient Mission Autonomy Software", "Autonomous navigation, search, and tracking algorithms for UUVs/USVs.", "7030", [],
     "Autonomy & Operations Research R&D", "Mathematical modeling and autonomy software for ONR and DARPA.", "EngineeringService", "DCMA",
     ["US Navy", "ONR", "DARPA"], "DoD SBIR/STTR awardee"),

    ("Systems Technology Forum, Ltd.", "STF", "Fredericksburg", "VA", "https://www.stf-inc.com", "SMESupplier",
     ["ISO9001", "ITAR_Compliant", "FacilitySecurity_Secret"], ["MaritimePlatform", "DomainC4ISR", "DomainDefence"],
     ["Platform_DDG51_ArleighBurke", "Platform_FordClass_Carrier"], ["KIC_CyberResilience", "KIC_InServiceSupport"],
     "Naval C4ISR Engineering & Cybersecurity", "Engineering, C4ISR integration, and RMF cybersecurity support for US Navy surface combatants.", "KIC_CyberResilience",
     "Naval C4ISR Integration & RMF Packages", "Shipboard combat system network architecture and cyber hardening.", "7010", [],
     "Naval C4ISR & Cyber Engineering", "Systems engineering and cyber accreditation for NSWCDD.", "CyberSecurityService", "DCMA",
     ["US Navy", "NSWCDD"], "Company website"),
]

records = []
skipped = []
for row in RAW:
    rec = make_rec(*row)
    n = norm_name(rec["legal_name"])
    d = norm_domain(rec["website"])
    if n in existing_names or (d and d in existing_domains):
        skipped.append(rec["legal_name"])
        continue
    existing_names.add(n)
    if d:
        existing_domains.add(d)
    records.append(rec)

OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
OUT_PATH.write_text(json.dumps(records, indent=2) + "\n")
print(f"Wrote {len(records)} new records to {OUT_PATH}")
print(f"Skipped {len(skipped)} duplicates: {skipped}")
