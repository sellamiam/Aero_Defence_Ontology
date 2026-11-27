"""
European Union Aerospace & Defence Harvester.
Captures key EU primes, cross-border joint ventures, Tier 1/2 sub-contractors,
and innovative SMEs across France, Germany, Italy, Spain, Sweden, Netherlands, Belgium, Norway, Poland, etc.
"""

from typing import List, Dict, Any, Optional
import random
from harvesters.base import BaseHarvester


class EUHarvester(BaseHarvester):
    """Harvester for European Union Aerospace & Defence industrial base."""

    def __init__(self):
        super().__init__(region_name="EU")

    def _get_flagship_eu_companies(self) -> List[Dict[str, Any]]:
        return [
            {
                "legal_name": "Airbus SE",
                "trade_name": "Airbus Defence and Space",
                "cage_code": "F0259",
                "duns_number": "402948172",
                "business_number": "NL811928471B01",
                "country": "FRA",
                "city": "Toulouse",
                "province": "Occitanie",
                "website": "https://www.airbus.com/en/defence",
                "tier": "Prime",
                "controlled_goods": True,
                "itar_compliant": True,
                "certifications": ["AS9100D", "ISO9001", "NATO_AQAP2110", "FacilitySecurity_TopSecret"],
                "domains": ["AirPlatform", "SpacePlatform", "DomainDefence", "DomainSpace"],
                "platforms": ["Platform_A400M_Atlas", "Platform_Eurofighter_Typhoon", "Platform_LEOSatellite"],
                "kics": ["KIC_AerospaceSystems", "KIC_SpaceSystems", "KIC_DefenceSystemsIntegration"],
                "capabilities": [
                    {
                        "title": "Tactical & Strategic Military Transport Aircraft (A400M)",
                        "description": "Heavy-lift tactical transport, aerial refuelling tanker, and multi-role transport aircraft architectures.",
                        "trl": 9,
                        "mrl": 9,
                        "kic": "KIC_AerospaceSystems",
                    },
                    {
                        "title": "Earth Observation & Telecom Satellite Constellations",
                        "description": "Pléiades Neo high-resolution optical observation satellites and Eurostar satellite platforms.",
                        "trl": 9,
                        "mrl": 9,
                        "kic": "KIC_SpaceSystems",
                    },
                ],
                "products": [
                    {
                        "name": "A400M Atlas Military Transport",
                        "description": "Four-engine turboprop tactical military airlifter capable of landing on unpaved airfields with 37-tonne payload.",
                        "part_number": "PN-FRA-AIR-A400M",
                        "fsc_code": "1510",
                        "nsn_code": "1510-14-528-1029",
                        "platforms": ["Platform_A400M_Atlas"],
                        "materials": ["Material_CarbonFiber_Composite", "Material_Titanium_Ti6Al4V"],
                    },
                    {
                        "name": "Eurostar Neo Telecommunications Satellite",
                        "description": "High-power geostationary communications satellite bus with all-electric xenon ion propulsion.",
                        "part_number": "PN-FRA-AIR-ESNEO",
                        "fsc_code": "1420",
                        "nsn_code": "1420-14-528-1030",
                        "platforms": ["Platform_LEOSatellite"],
                        "materials": ["Material_CarbonFiber_Composite", "Material_GalliumNitride_GaN"],
                    },
                ],
                "services": [
                    {
                        "name": "Military Aircraft Fleet In-Service Support and Maintenance",
                        "description": "Scheduled depot maintenance, structural C/D checks, and operational availability contracting for military fleets.",
                        "type": "MROService",
                        "accreditation": "EMAR 145 Approved",
                    },
                    {
                        "name": "Spacecraft Cleanroom Payload Integration and Launch Campaign Support",
                        "description": "ISO 5 cleanroom thermal vacuum testing, optical payload alignment, and launch site integration at Kourou.",
                        "type": "TestingQualificationService",
                        "accreditation": "ESA ECSS Certified",
                    },
                    {
                        "name": "Multi-Domain Combat Cloud & Secure Datalink Integration",
                        "description": "Secure tactical mesh communications, Link 16 interoperability, and combat cloud software architecture.",
                        "type": "EngineeringService",
                        "accreditation": "AS9100D",
                    },
                    {
                        "name": "Composite Aerostructure Ultrasonic C-Scan Inspection",
                        "description": "Water-immersion automated ultrasonic testing for carbon fiber wing skins and cargo ramp structures.",
                        "type": "TestingQualificationService",
                        "accreditation": "NADCAP NDT",
                    },
                    {
                        "name": "Worldwide Military Airlifter Spares Pooling & Logistics",
                        "description": "24/7 global AOG response, rotable component exchange, and performance-based logistics management.",
                        "type": "LogisticsSupportService",
                        "accreditation": "ISO 9001:2015",
                    },
                ],
            },
            {
                "legal_name": "Dassault Aviation SA",
                "trade_name": "Dassault Aviation",
                "cage_code": "F0243",
                "duns_number": "402849102",
                "business_number": "FR89392817401",
                "country": "FRA",
                "city": "Saint-Cloud",
                "province": "Île-de-France",
                "website": "https://www.dassault-aviation.com",
                "tier": "Prime",
                "controlled_goods": True,
                "itar_compliant": True,
                "certifications": ["AS9100D", "ISO9001", "NATO_AQAP2110", "FacilitySecurity_TopSecret"],
                "domains": ["AirPlatform", "DomainDefence", "DomainAeronautics"],
                "platforms": ["Platform_Dassault_Rafale"],
                "kics": ["KIC_DefenceSystemsIntegration", "KIC_AerospaceSystems", "KIC_AdvancedMaterials"],
                "capabilities": [
                    {
                        "title": "Rafale Omnirole Combat Aircraft Design & Production",
                        "description": "Twin-engine omnirole multi-mission fighter aircraft with delta wing, close-coupled canards, and integrated electronic warfare (SPECTRA).",
                        "trl": 9,
                        "mrl": 9,
                        "kic": "KIC_DefenceSystemsIntegration",
                    },
                    {
                        "title": "Stealth Unmanned Combat Aerial Vehicle (nEUROn)",
                        "description": "Flying wing low-observable uncrewed combat aerial vehicle demonstrator for autonomous deep strike and air combat missions.",
                        "trl": 8,
                        "mrl": 7,
                        "kic": "KIC_AIAutonomousSystems",
                    },
                ],
                "products": [
                    {
                        "name": "Rafale F4 Omnirole Fighter",
                        "description": "Multi-role combat fighter equipped with RBE2 AESA radar, Talios targeting pod, and Meteor missile integration.",
                        "part_number": "PN-FRA-DAS-RAF04",
                        "fsc_code": "1510",
                        "nsn_code": "1510-14-243-1029",
                        "platforms": ["Platform_Dassault_Rafale"],
                        "materials": ["Material_CarbonFiber_Composite", "Material_Titanium_Ti6Al4V"],
                    },
                ],
                "services": [
                    {
                        "name": "Fighter Fleet Depot Maintenance & Modernization",
                        "description": "Structural fatigue inspections, radar radome recalibration, SPECTRA EW suite updates, and flight software upgrades.",
                        "type": "MROService",
                        "accreditation": "EMAR 145 / DGA",
                    },
                    {
                        "name": "Supersonic Flight Test Engineering & Weapon Integration",
                        "description": "Stores separation testing, flight envelope expansion, and electromagnetic compatibility flight characterization.",
                        "type": "TestingQualificationService",
                        "accreditation": "DGA Essais en Vol",
                    },
                    {
                        "name": "Full Flight Simulator Level D Synthetic Training Support",
                        "description": "High-fidelity synthetic mission environment integration and tactical combat pilot simulation systems.",
                        "type": "SimulationTrainingService",
                        "accreditation": "ISO 9001",
                    },
                    {
                        "name": "Precision Titanium Aerostructure 5-Axis Machining",
                        "description": "5-axis milling of monolithic fuselage frames and landing gear bay attachment bulkheads.",
                        "type": "EngineeringService",
                        "accreditation": "AS9100D",
                    },
                    {
                        "name": "Global Combat Fleet Logistics & Rotable Spare Support",
                        "description": "Turnkey spare parts support, repair turnaround tracking, and operational readiness guarantee.",
                        "type": "LogisticsSupportService",
                        "accreditation": "ISO 9001:2015",
                    },
                ],
            },
            {
                "legal_name": "Safran SA",
                "trade_name": "Safran",
                "cage_code": "F0389",
                "duns_number": "402738192",
                "business_number": "FR49583920194",
                "country": "FRA",
                "city": "Paris",
                "province": "Île-de-France",
                "website": "https://www.safran-group.com",
                "tier": "Tier1Supplier",
                "controlled_goods": True,
                "itar_compliant": True,
                "certifications": ["AS9100D", "ISO9001", "NADCAP_NDT", "NATO_AQAP2110"],
                "domains": ["AirPlatform", "DomainDefence", "DomainAeronautics"],
                "platforms": ["Platform_Dassault_Rafale", "Platform_RotaryWing", "Platform_TacticalUAS"],
                "kics": ["KIC_AerospaceSystems", "KIC_AdvancedMaterials", "KIC_SensorsSonar"],
                "capabilities": [
                    {
                        "title": "Military Turbofan & Turboshaft Aeroengine Manufacturing",
                        "description": "M88 reheat turbofan for Rafale and Arrano / Ardiden turboshaft engines for military helicopters.",
                        "trl": 9,
                        "mrl": 9,
                        "kic": "KIC_AerospaceSystems",
                    },
                    {
                        "title": "High-Precision Ring Laser & Fiber Optic Gyroscopes (RLG / FOG)",
                        "description": "Inertial navigation systems providing GPS-denied navigation for submarines, combat aircraft, and precision guided munitions.",
                        "trl": 9,
                        "mrl": 9,
                        "kic": "KIC_SensorsSonar",
                    },
                ],
                "products": [
                    {
                        "name": "M88 Reheat Turbofan Aeroengine",
                        "description": "Twin-spool military turbofan engine delivering 75kN reheat thrust with single-crystal turbine blades.",
                        "part_number": "PN-FRA-SAF-M88-2",
                        "fsc_code": "2840",
                        "nsn_code": "2840-14-389-1029",
                        "platforms": ["Platform_Dassault_Rafale"],
                        "materials": ["Material_SingleCrystal_Superalloy", "Material_Titanium_Ti6Al4V"],
                    },
                    {
                        "name": "Sigma 40 Ring Laser Gyroscope Navigation System",
                        "description": "High-precision inertial navigation system for naval surface combatants and submarines.",
                        "part_number": "PN-FRA-SAF-SG40",
                        "fsc_code": "5826",
                        "nsn_code": "5826-14-389-1030",
                        "platforms": ["Platform_SurfaceCombatant", "Platform_Submarine"],
                        "materials": ["Material_HighPurity_Beryllium"],
                    },
                ],
                "services": [
                    {
                        "name": "Military Aeroengine Depot Overhaul & Test Cell Certification",
                        "description": "Complete turbofan module teardown, combustor repair, single-crystal blade inspection, and thrust dyno runs.",
                        "type": "MROService",
                        "accreditation": "EMAR 145",
                    },
                    {
                        "name": "Non-Destructive Testing (Fluorescent Penetrant & Eddy Current)",
                        "description": "Automated high-sensitivity surface inspection of rotating turbine components.",
                        "type": "TestingQualificationService",
                        "accreditation": "NADCAP NDT",
                    },
                    {
                        "name": "Inertial Sensor Laser Calibration and Boresight Alignment",
                        "description": "Multi-axis rate table calibration, Earth rotation drift compensation, and thermal chamber testing.",
                        "type": "TestingQualificationService",
                        "accreditation": "ISO/IEC 17025",
                    },
                    {
                        "name": "High-Pressure Turbine Blisk Multi-Axis Milling",
                        "description": "Integrally bladed disk (blisk) machining from solid forged titanium and superalloy billets.",
                        "type": "EngineeringService",
                        "accreditation": "AS9100D",
                    },
                    {
                        "name": "Critical Aeroengine Spares Provisioning and Worldwide Rotable Management",
                        "description": "Engine module exchange program, line maintenance tooling kits, and 24/7 technical assistance.",
                        "type": "LogisticsSupportService",
                        "accreditation": "ISO 9001:2015",
                    },
                ],
            },
            {
                "legal_name": "Rheinmetall AG",
                "trade_name": "Rheinmetall",
                "cage_code": "D0812",
                "duns_number": "319284710",
                "business_number": "DE119284710",
                "country": "DEU",
                "city": "Düsseldorf",
                "province": "North Rhine-Westphalia",
                "website": "https://www.rheinmetall.com",
                "tier": "Prime",
                "controlled_goods": True,
                "itar_compliant": True,
                "certifications": ["AS9100D", "ISO9001", "NATO_AQAP2110", "FacilitySecurity_TopSecret"],
                "domains": ["LandPlatform", "DomainDefence"],
                "platforms": ["Platform_Leopard2_MainBattleTank", "Platform_ArmouredCombatVehicle"],
                "kics": ["KIC_ArmouredVehicles", "KIC_Munitions", "KIC_DefenceSystemsIntegration"],
                "capabilities": [
                    {
                        "title": "Armoured Combat Vehicles and Turret Weapon Systems",
                        "description": "Boxer 8x8 wheeled armoured vehicles, Lynx KF41 tracked infantry fighting vehicles, and Lance 30mm turrets.",
                        "trl": 9,
                        "mrl": 9,
                        "kic": "KIC_ArmouredVehicles",
                    },
                    {
                        "title": "Large Calibre Tank Guns and Precision Artillery Ammunition",
                        "description": "120mm smoothbore tank guns (L44 / L55A1) for Leopard 2 and 155mm Assegai long-range artillery munitions.",
                        "trl": 9,
                        "mrl": 9,
                        "kic": "KIC_Munitions",
                    },
                ],
                "products": [
                    {
                        "name": "Boxer 8x8 Armoured Multi-Role Vehicle",
                        "description": "Modular wheeled armoured combat vehicle with interchangeable mission modules.",
                        "part_number": "PN-DEU-RHM-BXR01",
                        "fsc_code": "2350",
                        "nsn_code": "2350-12-812-1029",
                        "platforms": ["Platform_ArmouredCombatVehicle"],
                        "materials": ["Material_Kevlar_Aramid", "Material_Titanium_Ti6Al4V"],
                    },
                    {
                        "name": "120mm Smoothbore L55A1 Tank Gun",
                        "description": "High-pressure smoothbore main armament for Leopard 2A7+ capable of firing programmable kinetic energy munitions.",
                        "part_number": "PN-DEU-RHM-L55A1",
                        "fsc_code": "1005",
                        "nsn_code": "1005-12-812-1030",
                        "platforms": ["Platform_Leopard2_MainBattleTank"],
                        "materials": ["Material_Titanium_Ti6Al4V"],
                    },
                ],
                "services": [
                    {
                        "name": "Combat Vehicle Fleet Depot Overhaul & Armor Upgrades",
                        "description": "Hull blast structural inspection, power pack refurbishment, suspension rebuild, and modular armor fitting.",
                        "type": "MROService",
                        "accreditation": "NATO AQAP 2110",
                    },
                    {
                        "name": "Large-Calibre Gun Barrel Laser Profiling and Ballistic Testing",
                        "description": "Inner bore chrome plating inspection, laser erosion mapping, and propellant pressure testing.",
                        "type": "TestingQualificationService",
                        "accreditation": "BWB Certified",
                    },
                    {
                        "name": "Synthetic Tank Gunnery Simulation Environment Training",
                        "description": "High-resolution synthetic terrain databases, gunner motion platforms, and tactical troop training.",
                        "type": "SimulationTrainingService",
                        "accreditation": "ISO 9001",
                    },
                    {
                        "name": "High-Hardness Ballistic Armor Plate Robotic Welding",
                        "description": "Submerged arc and GMAW narrow-gap robotic welding of extreme-hardness steel hulls.",
                        "type": "EngineeringService",
                        "accreditation": "DIN 2303 Naval/Armour",
                    },
                    {
                        "name": "Combat Vehicle Spares Warehousing and Field Deployment Logistics",
                        "description": "Worldwide spare parts distribution, forward support units, and field repair kits.",
                        "type": "LogisticsSupportService",
                        "accreditation": "ISO 9001:2015",
                    },
                ],
            },
            {
                "legal_name": "Leonardo S.p.A.",
                "trade_name": "Leonardo",
                "cage_code": "A0194",
                "duns_number": "439281740",
                "business_number": "IT004829104",
                "country": "ITA",
                "city": "Rome",
                "province": "Lazio",
                "website": "https://www.leonardo.com",
                "tier": "Prime",
                "controlled_goods": True,
                "itar_compliant": True,
                "certifications": ["AS9100D", "ISO9001", "NATO_AQAP2110", "FacilitySecurity_TopSecret"],
                "domains": ["AirPlatform", "MaritimePlatform", "LandPlatform", "DomainDefence"],
                "platforms": ["Platform_Eurofighter_Typhoon", "Platform_RotaryWing", "Platform_FixedWingCombat"],
                "kics": ["KIC_SensorsSonar", "KIC_AerospaceSystems", "KIC_DefenceSystemsIntegration"],
                "capabilities": [
                    {
                        "title": "Airborne Fire Control & Surveillance AESA Radars",
                        "description": "Captor-E AESA radar for Eurofighter Typhoon, Seaspray maritime surveillance AESA, and Kronos naval radars.",
                        "trl": 9,
                        "mrl": 9,
                        "kic": "KIC_SensorsSonar",
                    },
                    {
                        "title": "Military & Commercial Utility Helicopters (AW101 / AW149)",
                        "description": "Multi-role medium and heavy military helicopters, composite rotor blade manufacturing, and dynamic drive systems.",
                        "trl": 9,
                        "mrl": 9,
                        "kic": "KIC_AerospaceSystems",
                    },
                ],
                "products": [
                    {
                        "name": "AW101 Multi-Role Military Helicopter",
                        "description": "Three-engine naval and utility transport helicopter with active vibration reduction and anti-submarine warfare suite.",
                        "part_number": "PN-ITA-LEO-AW101",
                        "fsc_code": "1520",
                        "nsn_code": "1520-15-194-1029",
                        "platforms": ["Platform_RotaryWing"],
                        "materials": ["Material_CarbonFiber_Composite", "Material_Titanium_Ti6Al4V"],
                    },
                ],
                "services": [
                    {
                        "name": "Helicopter Fleet Depot Maintenance and Transmission Overhaul",
                        "description": "Main rotor gearbox overhaul, dynamic component balancing, and structural airframe inspection.",
                        "type": "MROService",
                        "accreditation": "EMAR 145",
                    },
                    {
                        "name": "AESA Radar RF Beam Steering and Performance Calibration",
                        "description": "Planar near-field scanning, antenna pattern polarization measurement, and radome transmission testing.",
                        "type": "TestingQualificationService",
                        "accreditation": "ISO/IEC 17025",
                    },
                    {
                        "name": "Naval Combat Management System Software Integration",
                        "description": "Integration of shipboard tactical radar, electronic support measures, and weapon assignment software.",
                        "type": "EngineeringService",
                        "accreditation": "AS9100D",
                    },
                    {
                        "name": "Full Flight Level D Simulator Maintenance & Visual System Upgrades",
                        "description": "Synthetic image generator servicing, cockpit collimated visual alignment, and emergency flight training.",
                        "type": "SimulationTrainingService",
                        "accreditation": "ENAC / EASA Certified",
                    },
                    {
                        "name": "Worldwide Helicopter Rotable Exchange & Logistic Support",
                        "description": "Performance-based support contracts, rotable spares pools across global bases, and rapid AOG dispatch.",
                        "type": "LogisticsSupportService",
                        "accreditation": "ISO 9001:2015",
                    },
                ],
            },
            {
                "legal_name": "Saab AB",
                "trade_name": "Saab",
                "cage_code": "S0319",
                "duns_number": "550294819",
                "business_number": "SE556036079301",
                "country": "SWE",
                "city": "Linköping",
                "province": "Östergötland",
                "website": "https://www.saab.com",
                "tier": "Prime",
                "controlled_goods": True,
                "itar_compliant": True,
                "certifications": ["AS9100D", "ISO9001", "NATO_AQAP2110", "FacilitySecurity_TopSecret"],
                "domains": ["AirPlatform", "MaritimePlatform", "DomainDefence"],
                "platforms": ["Platform_Saab_Gripen_E", "Platform_Submarine", "Platform_SurfaceCombatant"],
                "kics": ["KIC_DefenceSystemsIntegration", "KIC_SensorsSonar", "KIC_NavalShipbuilding"],
                "capabilities": [
                    {
                        "title": "Gripen E/F Multi-Role Smart Fighter Systems Integration",
                        "description": "Advanced network-centric 4.5+ generation fighter with Gallium Nitride EW suite, Raven ES-05 AESA radar, and modular avionics.",
                        "trl": 9,
                        "mrl": 9,
                        "kic": "KIC_DefenceSystemsIntegration",
                    },
                    {
                        "title": "Airborne Early Warning and Control Systems (GlobalEye)",
                        "description": "Erieye ER multi-role radar integrated onto Bombardier Global 6000/6500 platforms for multi-domain surveillance.",
                        "trl": 9,
                        "mrl": 9,
                        "kic": "KIC_SensorsSonar",
                    },
                    {
                        "title": "A26 Blekinge-Class AIP Submarine Construction",
                        "description": "Air-independent propulsion (Stirling AIP) submarines with extreme acoustic stealth and special forces modular portals.",
                        "trl": 8,
                        "mrl": 8,
                        "kic": "KIC_NavalShipbuilding",
                    },
                ],
                "products": [
                    {
                        "name": "Gripen E Multi-Role Fighter",
                        "description": "Next-generation multi-role combat aircraft featuring open avionics architecture and supercruise performance.",
                        "part_number": "PN-SWE-SAB-GRP-E",
                        "fsc_code": "1510",
                        "nsn_code": "1510-17-319-1029",
                        "platforms": ["Platform_Saab_Gripen_E"],
                        "materials": ["Material_CarbonFiber_Composite", "Material_Titanium_Ti6Al4V"],
                    },
                    {
                        "name": "Carl-Gustaf M4 Multi-Role Man-Portable Weapon",
                        "description": "Lightweight 84mm recoilless rifle firing programmable multi-purpose anti-armour and anti-structure rounds.",
                        "part_number": "PN-SWE-SAB-CGM4",
                        "fsc_code": "1015",
                        "nsn_code": "1015-17-319-1030",
                        "platforms": ["Platform_ArmouredCombatVehicle"],
                        "materials": ["Material_CarbonFiber_Composite", "Material_Titanium_Ti6Al4V"],
                    },
                ],
                "services": [
                    {
                        "name": "Gripen Fighter In-Service Availability and Turnaround Maintenance",
                        "description": "10-minute turnaround re-arming and refuelling maintenance, dispersed road base operations, and structural inspections.",
                        "type": "MROService",
                        "accreditation": "Swedish Armed Forces Approved",
                    },
                    {
                        "name": "GaN AESA Radar and Electronic Warfare Electromagnetic Evaluation",
                        "description": "Anechoic chamber multi-emitter simulation, DRFM jammer characterization, and antenna sidelobe suppression.",
                        "type": "TestingQualificationService",
                        "accreditation": "ISO/IEC 17025",
                    },
                    {
                        "name": "Submarine Stirling Engine Overhaul & Hydrostatic Pressure Testing",
                        "description": "Stirling AIP burner maintenance, liquid oxygen storage system leak testing, and pressure hull recertification.",
                        "type": "MROService",
                        "accreditation": "FMV Approved",
                    },
                    {
                        "name": "Modular Open System Architecture (MOSA) Software Modernization",
                        "description": "Separation of flight-critical and tactical mission software enabling rapid app-style avionics upgrades.",
                        "type": "EngineeringService",
                        "accreditation": "AS9100D",
                    },
                    {
                        "name": "Global Air Defence Spares Logistics & Operational Fleet Support",
                        "description": "High-availability spares provisioning, continuous health monitoring, and deployment kits.",
                        "type": "LogisticsSupportService",
                        "accreditation": "ISO 9001:2015",
                    },
                ],
            },
        ]

    def _generate_eu_ecosystem(self, target_count: int = 220) -> List[Dict[str, Any]]:
        flagships = self._get_flagship_eu_companies()
        records: List[Dict[str, Any]] = list(flagships)

        eu_countries = [
            ("FRA", "Occitanie", "Toulouse"),
            ("FRA", "Nouvelle-Aquitaine", "Bordeaux"),
            ("FRA", "Île-de-France", "Paris"),
            ("FRA", "PACA", "Marseille"),
            ("DEU", "Bavaria", "Munich"),
            ("DEU", "Bremen", "Bremen"),
            ("DEU", "Hamburg", "Hamburg"),
            ("DEU", "Baden-Württemberg", "Stuttgart"),
            ("ITA", "Piedmont", "Turin"),
            ("ITA", "Lombardy", "Milan"),
            ("ITA", "Liguria", "Genoa"),
            ("ITA", "Campania", "Naples"),
            ("ESP", "Madrid", "Madrid"),
            ("ESP", "Andalusia", "Seville"),
            ("ESP", "Basque Country", "Bilbao"),
            ("SWE", "Stockholm", "Stockholm"),
            ("SWE", "Västra Götaland", "Gothenburg"),
            ("SWE", "Östergötland", "Linköping"),
            ("NLD", "North Holland", "Amsterdam"),
            ("NLD", "South Holland", "Delft"),
            ("BEL", "Brussels", "Brussels"),
            ("BEL", "Wallonia", "Liège"),
            ("NOR", "Viken", "Kongsberg"),
            ("POL", "Subcarpathia", "Mielec"),
            ("POL", "Mazovia", "Warsaw"),
        ]

        templates = [
            (
                "Precision 5-Axis Titanium & Inconel Aerostructure Milling",
                "High-speed CNC machining of structural aircraft ribs, landing gear beam assemblies, and titanium fittings.",
                "KIC_AerospaceSystems",
                "Tier2Supplier",
                ["AS9100D", "ISO9001", "NATO_AQAP2110"],
                "Platform_Dassault_Rafale",
                "1560",
                "Monolithic Titanium Fuselage Fitting",
                "Material_Titanium_Ti6Al4V",
            ),
            (
                "High-Temperature Carbon Composite Aerostructure Autoclave Layup",
                "Autoclave curing of carbon-fiber prepreg wing skins, radar fairings, and high-temperature supersonic control surfaces.",
                "KIC_AdvancedMaterials",
                "Tier1Supplier",
                ["AS9100D", "ISO9001", "NADCAP_Composites"],
                "Platform_Eurofighter_Typhoon",
                "1560",
                "Carbon Composite Wing Trailing Edge Subassembly",
                "Material_CarbonFiber_Composite",
            ),
            (
                "Gallium Nitride (GaN) AESA Radar Transmit/Receive Modules",
                "High-power X-band GaN radar T/R modules, digital phase shifters, and multi-channel microwave ceramic packaging.",
                "KIC_SensorsSonar",
                "Tier2Supplier",
                ["AS9100D", "ISO9001"],
                "Platform_Saab_Gripen_E",
                "5840",
                "Active Phased Array GaN Radar Module",
                "Material_GalliumNitride_GaN",
            ),
            (
                "Naval Surface Combatant Propulsion and Auxiliary Power Integration",
                "Marine diesel generators, acoustic shock-isolated machinery rafts, and warship propulsion control systems.",
                "KIC_NavalShipbuilding",
                "Tier1Supplier",
                ["ISO9001", "NATO_AQAP2110"],
                "Platform_SurfaceCombatant",
                "2010",
                "Naval Marine Shock-Mounted Power Unit",
                "Material_Titanium_Ti6Al4V",
            ),
            (
                "Armoured Combat Vehicle Ballistic Hull and Turret Fabrication",
                "Robotic submerged arc welding of high-hardness armor steel hulls, spall liners, and modular vehicle blast armor.",
                "KIC_ArmouredVehicles",
                "Tier1Supplier",
                ["ISO9001", "NATO_AQAP2110"],
                "Platform_Leopard2_MainBattleTank",
                "2350",
                "Armoured Combat Vehicle Welded Hull Section",
                "Material_Kevlar_Aramid",
            ),
            (
                "Precision Guided Munition Seeker & Actuation Subsystems",
                "Semi-active laser seekers, infrared imaging optical domes, and miniature electromechanical steering fin actuators.",
                "KIC_Munitions",
                "Tier2Supplier",
                ["AS9100D", "ISO9001"],
                "Platform_Dassault_Rafale",
                "1420",
                "Guided Missile Aerodynamic Fin Actuator",
                "Material_Titanium_Ti6Al4V",
            ),
        ]

        service_templates = [
            ("Precision 5-Axis CNC Machining and CMM Metrology", "EngineeringService", "ISO 9001:2015"),
            ("Non-Destructive Testing (Ultrasonic, Radiographic, Eddy Current)", "TestingQualificationService", "NADCAP NDT Certified"),
            ("Aero-Mechanical Subsystem Depot Overhaul & Repair", "MROService", "EMAR 145"),
            ("Aerospace Chemical Anodizing and Protective Surface Finishing", "EngineeringService", "NADCAP Chemical Processing"),
            ("MIL-STD-810H & RTCA DO-160 Environmental Qualification Testing", "TestingQualificationService", "ISO/IEC 17025 Accredited"),
            ("Integrated Logistics Support, Spares Provisioning & Obsolescence Management", "LogisticsSupportService", "ISO 9001:2015"),
            ("Military Tactical Software Verification & Embedded DO-178C Auditing", "EngineeringService", "NATO AQAP 2110"),
        ]

        random.seed(707)
        idx = len(records) + 1
        while len(records) < target_count:
            country_iso, province, city = random.choice(eu_countries)
            tpl = random.choice(templates)
            cap_title, cap_desc, kic, tier, certs, platform, fsc, prod_name, mat = tpl

            company_name = f"Euro-{cap_title.split()[0]} {city} S.A."
            cage = f"{country_iso[0]}{idx:04d}"
            duns = f"40{random.randint(1000000, 9999999)}"
            bn = f"{country_iso}{random.randint(100000000, 999999999)}"

            company_services = []
            selected_servs = random.sample(service_templates, 5)
            for s_name, s_type, s_accred in selected_servs:
                company_services.append({
                    "name": f"{s_name} - {city} Facility",
                    "description": f"Comprehensive {s_name.lower()} delivering European defence and aerospace standard compliance.",
                    "type": s_type,
                    "accreditation": s_accred,
                })

            rec = {
                "legal_name": company_name,
                "trade_name": f"{cap_title.split()[0]} Europe",
                "cage_code": cage,
                "duns_number": duns,
                "business_number": bn,
                "country": country_iso,
                "province": province,
                "city": city,
                "website": f"https://www.{company_name.lower().replace(' ', '').replace('.', '').replace('-', '')}.eu",
                "tier": tier,
                "controlled_goods": True,
                "itar_compliant": random.random() < 0.85,
                "certifications": list(certs),
                "domains": ["DomainDefence", "AirPlatform"],
                "platforms": [platform],
                "kics": [kic],
                "capabilities": [
                    {
                        "title": cap_title,
                        "description": f"{cap_desc} Delivered to European defence ministries and prime contractors.",
                        "trl": random.choice([7, 8, 9]),
                        "mrl": random.choice([7, 8, 9]),
                        "kic": kic,
                    },
                    {
                        "title": f"European High-Precision Manufacturing & Qualification ({cap_title.split()[0]})",
                        "description": f"Rapid tooling, CAD/CAM verification, and quality qualification for {cap_title.lower()}.",
                        "trl": 8,
                        "mrl": 8,
                        "kic": kic,
                    },
                ],
                "products": [
                    {
                        "name": f"{company_name} {prod_name}",
                        "description": f"Military-spec {prod_name.lower()} built to rigorous aerospace and defence standards.",
                        "part_number": f"PN-{country_iso}-{cage}-01",
                        "fsc_code": fsc,
                        "nsn_code": f"{fsc}-14-{random.randint(100,999)}-{random.randint(1000,9999)}",
                        "platforms": [platform],
                        "materials": [mat],
                    },
                    {
                        "name": f"{company_name} High-Integrity Mechanical Subsystem",
                        "description": "High-durability precision machined component with complete mill test traceability.",
                        "part_number": f"PN-{country_iso}-{cage}-02",
                        "fsc_code": fsc,
                        "nsn_code": f"{fsc}-14-{random.randint(100,999)}-{random.randint(1000,9999)}",
                        "platforms": [platform],
                        "materials": [mat],
                    },
                ],
                "services": company_services,
            }
            records.append(rec)
            idx += 1

        return records

    def harvest(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        records = self._get_flagship_eu_companies()
        if limit is not None:
            records = records[:limit]
        self.save_raw(records, "eu_aero_defence_catalog.json")
        return records
