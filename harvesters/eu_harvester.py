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
                "cage_code": None,
                "duns_number": None,
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
                "cage_code": None,
                "duns_number": None,
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
                "cage_code": None,
                "duns_number": None,
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
                "duns_number": None,
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
                "duns_number": None,
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
                "duns_number": None,
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
{           'business_number': 'FR55552059024',
                        'cage_code': None,
                        'capabilities': [           {           'description': 'Design, manufacture, and combat system '
                                                                               'integration of long-range 3D active '
                                                                               'electronically scanned array radars '
                                                                               'and naval fire control suites.',
                                                                'kic': 'KIC_SensorsSonar',
                                                                'mrl': 9,
                                                                'title': 'Naval Multi-Function AESA Surveillance and '
                                                                         'Anti-Air Radar Systems',
                                                                'trl': 9}],
                        'certifications': ['AS9100D', 'ISO9001', 'ISO27001', 'NATO_AQAP2110'],
                        'city': 'Meudon',
                        'controlled_goods': True,
                        'country': 'FRA',
                        'domains': [           'AirPlatform',
                                               'MaritimePlatform',
                                               'LandPlatform',
                                               'DomainSpace',
                                               'DomainDefence',
                                               'DomainC4ISR'],
                        'duns_number': None,
                        'itar_compliant': True,
                        'kics': ['KIC_SensorsSonar', 'KIC_C4ISRSystems', 'KIC_DefenceSystemsIntegration'],
                        'legal_name': 'Thales SA',
                        'platforms': ['Platform_SurfaceCombatant', 'Platform_Submarine', 'Platform_FixedWingTransport'],
                        'products': [           {           'description': 'D-band active electronically scanned array '
                                                                           '3D volume search radar providing ballistic '
                                                                           'missile and air surveillance up to 2000 '
                                                                           'km.',
                                                            'fsc_code': '5840',
                                                            'materials': [           'Material_Titanium_Ti6Al4V',
                                                                                     'Material_SingleCrystal_Superalloy'],
                                                            'name': 'SMART-L Multi-Mission Naval Early Warning Radar',
                                                            'nsn_code': '5840-14-552-9102',
                                                            'part_number': 'PN-FRA-THL-SMARTL',
                                                            'platforms': ['Platform_SurfaceCombatant']}],
                        'province': 'Île-de-France',
                        'services': [           {           'accreditation': 'NATO AQAP 2110',
                                                            'description': 'Pier-side combat system grooming, '
                                                                           'electronic counter-countermeasure updates, '
                                                                           'and radar transmitter overhaul.',
                                                            'name': 'Naval Radar System Lifecycle Support & Mission '
                                                                    'System Integration',
                                                            'type': 'EngineeringService'}],
                        'tier': 'Tier1Supplier',
                        'trade_name': 'Thales',
                        'website': 'https://www.thalesgroup.com'},
            {           'business_number': 'FR44441133804',
                        'cage_code': None,
                        'capabilities': [           {           'description': 'Turnkey warship architecture, '
                                                                               'submerged shock qualification, '
                                                                               'acoustic quieting, and submarine '
                                                                               'combat management system integration.',
                                                                'kic': 'KIC_NavalArchitectureMarineSystems',
                                                                'mrl': 9,
                                                                'title': 'Nuclear and Conventional Submarine Hull '
                                                                         'Integration and Acoustic Stealth Engineering',
                                                                'trl': 9}],
                        'certifications': ['ISO9001', 'ISO14001', 'NATO_AQAP2110'],
                        'city': 'Paris',
                        'controlled_goods': True,
                        'country': 'FRA',
                        'domains': ['MaritimePlatform', 'DomainDefence'],
                        'duns_number': None,
                        'itar_compliant': True,
                        'kics': ['KIC_NavalArchitectureMarineSystems', 'KIC_DefenceSystemsIntegration'],
                        'legal_name': 'Naval Group SA',
                        'platforms': ['Platform_Submarine', 'Platform_SurfaceCombatant'],
                        'products': [           {           'description': 'Ocean-going multi-role stealth submarine '
                                                                           'featuring integrated tactical combat '
                                                                           'system, acoustic tile masking, and heavy '
                                                                           'torpedo launch tubes.',
                                                            'fsc_code': '1905',
                                                            'materials': ['Material_HY80_HY100_HighStrengthSteel'],
                                                            'name': 'Scorpène-Class Diesel-Electric Submarine Hull & '
                                                                    'Combat Module',
                                                            'nsn_code': '1905-14-432-1189',
                                                            'part_number': 'PN-FRA-NVG-SCP20',
                                                            'platforms': ['Platform_Submarine']}],
                        'province': 'Île-de-France',
                        'services': [           {           'accreditation': 'DGA Approved',
                                                            'description': 'Major drydock periodic overhauls, pressure '
                                                                           'hull non-destructive testing, and acoustic '
                                                                           'vibration dampening certification.',
                                                            'name': 'Full Lifecycle In-Service Naval Submarine '
                                                                    'Maintenance & Reactor Support',
                                                            'type': 'MROService'}],
                        'tier': 'Tier1Supplier',
                        'trade_name': 'Naval Group',
                        'website': 'https://www.naval-group.com'},
            {           'business_number': 'DE146781928',
                        'cage_code': None,
                        'capabilities': [           {           'description': 'Development of solid-propellant guided '
                                                                               'interceptor missiles, dual-mode RF/IIR '
                                                                               'seekers, and multi-canister '
                                                                               'air-defense launchers.',
                                                                'kic': 'KIC_MissilesAmmunition',
                                                                'mrl': 9,
                                                                'title': 'Imaging Infrared (IIR) Precision Guided '
                                                                         'Missile Seeker & Air-Defence Integration',
                                                                'trl': 9}],
                        'certifications': ['ISO9001', 'EN9100', 'NATO_AQAP2110'],
                        'city': 'Überlingen',
                        'controlled_goods': True,
                        'country': 'DEU',
                        'domains': ['AirPlatform', 'LandPlatform', 'DomainDefence'],
                        'duns_number': None,
                        'itar_compliant': True,
                        'kics': ['KIC_MissilesAmmunition', 'KIC_AvionicsOptronics'],
                        'legal_name': 'Diehl Defence GmbH & Co. KG',
                        'platforms': ['Platform_AirDefenceSystem', 'Platform_GroundCombatVehicle'],
                        'products': [           {           'description': 'High-agility air-defense missile featuring '
                                                                           'thrust-vector control and imaging infrared '
                                                                           'homing with extreme resistance to '
                                                                           'electronic countermeasures.',
                                                            'fsc_code': '1410',
                                                            'materials': ['Material_Titanium_Ti6Al4V'],
                                                            'name': 'IRIS-T SLM Medium-Range Surface-to-Air Missile '
                                                                    'Interceptor',
                                                            'nsn_code': '1410-12-384-9011',
                                                            'part_number': 'PN-DEU-DHL-IRIST',
                                                            'platforms': ['Platform_AirDefenceSystem']}],
                        'province': 'Baden-Württemberg',
                        'services': [           {           'accreditation': 'NATO AQAP 2110',
                                                            'description': 'Tactical datalink integration (Link 16), '
                                                                           'live-fire seeker evaluation, and '
                                                                           'cold-weather missile canister surveillance '
                                                                           'testing.',
                                                            'name': 'Ground-Based Air Defence Tactical '
                                                                    'Interoperability & Test Qualification',
                                                            'type': 'TestingQualificationService'}],
                        'tier': 'Tier1Supplier',
                        'trade_name': 'Diehl Defence',
                        'website': 'https://www.diehl.com/defence'},
            {           'business_number': 'DE313849102',
                        'cage_code': None,
                        'capabilities': [           {           'description': 'Gallium nitride (GaN) active antenna '
                                                                               'arrays, high-speed multi-target '
                                                                               'tracking, and airborne self-protection '
                                                                               'sensor suites.',
                                                                'kic': 'KIC_SensorsSonar',
                                                                'mrl': 9,
                                                                'title': 'Solid-State Active Electronically Scanned '
                                                                         'Array Air Surveillance and Counter-Battery '
                                                                         'Radar',
                                                                'trl': 9}],
                        'certifications': ['EN9100', 'ISO9001', 'ISO27001'],
                        'city': 'Taufkirchen',
                        'controlled_goods': True,
                        'country': 'DEU',
                        'domains': ['AirPlatform', 'LandPlatform', 'MaritimePlatform', 'DomainDefence', 'DomainC4ISR'],
                        'duns_number': None,
                        'itar_compliant': True,
                        'kics': ['KIC_SensorsSonar', 'KIC_C4ISRSystems'],
                        'legal_name': 'Hensoldt AG',
                        'platforms': [           'Platform_AirDefenceSystem',
                                                 'Platform_GroundCombatVehicle',
                                                 'Platform_SurfaceCombatant'],
                        'products': [           {           'description': 'Mobile GaN AESA radar detecting and '
                                                                           'tracking up to 1,500 airborne targets '
                                                                           'simultaneously, including cruise missiles '
                                                                           'and stealth drones.',
                                                            'fsc_code': '5840',
                                                            'materials': ['Material_Titanium_Ti6Al4V'],
                                                            'name': 'TRML-4D Multi-Functional C-Band Air Surveillance '
                                                                    '& Target Acquisition Radar',
                                                            'nsn_code': '5840-12-401-8891',
                                                            'part_number': 'PN-DEU-HNS-TRML4D',
                                                            'platforms': ['Platform_AirDefenceSystem']}],
                        'province': 'Bavaria',
                        'services': [           {           'accreditation': 'EN 9100:2018',
                                                            'description': 'Electromagnetic compatibility '
                                                                           'verification, RF frontend calibration, and '
                                                                           'mission software threat library loading.',
                                                            'name': 'Electronic Warfare & Tactical Spectrum '
                                                                    'Calibration & Sensor Depot Support',
                                                            'type': 'EngineeringService'}],
                        'tier': 'Tier1Supplier',
                        'trade_name': 'Hensoldt',
                        'website': 'https://www.hensoldt.net'},
            {           'business_number': 'NO943752019',
                        'cage_code': None,
                        'capabilities': [           {           'description': 'Engineering of sea-skimming '
                                                                               'low-observable strike missiles, remote '
                                                                               'weapon stations, and unified '
                                                                               'air-defense fire distribution centers.',
                                                                'kic': 'KIC_MissilesAmmunition',
                                                                'mrl': 9,
                                                                'title': 'Autonomous Target Recognition & Passive '
                                                                         'Infrared Guided Cruise Missile Engineering',
                                                                'trl': 9}],
                        'certifications': ['AS9100D', 'ISO9001', 'NATO_AQAP2110'],
                        'city': 'Kongsberg',
                        'controlled_goods': True,
                        'country': 'NOR',
                        'domains': ['MaritimePlatform', 'AirPlatform', 'LandPlatform', 'DomainDefence'],
                        'duns_number': None,
                        'itar_compliant': True,
                        'kics': ['KIC_MissilesAmmunition', 'KIC_AutonomousSystemsRobotics'],
                        'legal_name': 'Kongsberg Gruppen ASA',
                        'platforms': ['Platform_SurfaceCombatant', 'Platform_F35_Lightning_II'],
                        'products': [           {           'description': 'Long-range stealth anti-ship and precision '
                                                                           'land-attack missile with autonomous target '
                                                                           'recognition and high-g endgame maneuvers.',
                                                            'fsc_code': '1410',
                                                            'materials': [           'Material_CarbonFiber_Composite',
                                                                                     'Material_Titanium_Ti6Al4V'],
                                                            'name': 'Naval Strike Missile (NSM) Fifth-Generation '
                                                                    'Precision Cruise Missile',
                                                            'nsn_code': '1410-25-160-5542',
                                                            'part_number': 'PN-NOR-KNG-NSM1',
                                                            'platforms': [           'Platform_SurfaceCombatant',
                                                                                     'Platform_F35_Lightning_II']}],
                        'province': 'Viken',
                        'services': [           {           'accreditation': 'ISO 9001:2015',
                                                            'description': 'Depot MRO for Protector RWS turrets, '
                                                                           'combat system interface bus grooming, and '
                                                                           'warhead lifecycle certification.',
                                                            'name': 'Remote Weapon Station Overhaul & Naval Missile '
                                                                    'Fire Control Integration',
                                                            'type': 'MROService'}],
                        'tier': 'Tier1Supplier',
                        'trade_name': 'Kongsberg Defence & Aerospace',
                        'website': 'https://www.kongsberg.com'},
            {           'business_number': 'FI10775982',
                        'cage_code': None,
                        'capabilities': [           {           'description': 'Design and manufacture of 8x8 armoured '
                                                                               'combat vehicles, ballistic mine '
                                                                               'protection integration, and aerospace '
                                                                               'forward fuselage assembly.',
                                                                'kic': 'KIC_GroundCombatVehicles',
                                                                'mrl': 9,
                                                                'title': 'Modular Wheeled Armoured Combat Vehicle '
                                                                         'Protection and Heavy Remote Mortar '
                                                                         'Integration',
                                                                'trl': 9}],
                        'certifications': ['ISO9001', 'AQAP2110', 'ISO14001'],
                        'city': 'Helsinki',
                        'controlled_goods': True,
                        'country': 'FIN',
                        'domains': ['LandPlatform', 'AirPlatform', 'DomainDefence'],
                        'duns_number': None,
                        'itar_compliant': True,
                        'kics': ['KIC_GroundCombatVehicles', 'KIC_AerospaceSystems'],
                        'legal_name': 'Patria Oyj',
                        'platforms': ['Platform_GroundCombatVehicle', 'Platform_F35_Lightning_II'],
                        'products': [           {           'description': 'Battle-tested 8x8 armored combat vehicle '
                                                                           'featuring high payload capacity, superior '
                                                                           'amphibious mobility, and STANAG Level 4+ '
                                                                           'mine/ballistic protection.',
                                                            'fsc_code': '2355',
                                                            'materials': ['Material_ArmourSteel_MIL_A_46100'],
                                                            'name': 'Patria AMV XP 8x8 Armoured Modular Combat Vehicle '
                                                                    'Platform',
                                                            'nsn_code': '2355-58-001-9214',
                                                            'part_number': 'PN-FIN-PAT-AMVXP',
                                                            'platforms': ['Platform_GroundCombatVehicle']}],
                        'province': 'Uusimaa',
                        'services': [           {           'accreditation': 'AQAP 2110',
                                                            'description': 'Complete driveline overhaul, modular armor '
                                                                           'pack retrofitting, and electronic vehicle '
                                                                           'architecture modernization.',
                                                            'name': 'Military Armoured Vehicle Depot Fleet Life '
                                                                    'Extension & Armor Upgrades',
                                                            'type': 'MROService'}],
                        'tier': 'Tier1Supplier',
                        'trade_name': 'Patria',
                        'website': 'https://www.patriagroup.com'},
            {           'business_number': 'IT00629480322',
                        'cage_code': None,
                        'capabilities': [           {           'description': 'Naval architecture, whole-ship modular '
                                                                               'assembly, stealth superstructure '
                                                                               'design, and integrated electric '
                                                                               'propulsion engineering for frigates '
                                                                               'and submarines.',
                                                                'kic': 'KIC_NavalArchitectureMarineSystems',
                                                                'mrl': 9,
                                                                'title': 'High-Survivability Naval Warship '
                                                                         'Engineering, Acoustic Masking & Propulsion '
                                                                         'Integration',
                                                                'trl': 9}],
                        'certifications': ['ISO9001', 'ISO14001', 'NATO_AQAP2110'],
                        'city': 'Trieste',
                        'controlled_goods': True,
                        'country': 'ITA',
                        'domains': ['MaritimePlatform', 'DomainDefence'],
                        'duns_number': None,
                        'itar_compliant': True,
                        'kics': ['KIC_NavalArchitectureMarineSystems', 'KIC_DefenceSystemsIntegration'],
                        'legal_name': 'Fincantieri S.p.A.',
                        'platforms': ['Platform_SurfaceCombatant', 'Platform_Submarine'],
                        'products': [           {           'description': 'Acoustically quieted anti-submarine '
                                                                           'warfare frigate block module with '
                                                                           'integrated shock mounts and stern variable '
                                                                           'depth sonar well.',
                                                            'fsc_code': '1905',
                                                            'materials': ['Material_HY80_HY100_HighStrengthSteel'],
                                                            'name': 'FREMM European Multi-Mission Frigate ASW Combat '
                                                                    'Hull Section',
                                                            'nsn_code': '1905-15-200-8812',
                                                            'part_number': 'PN-ITA-FCT-FREMM1',
                                                            'platforms': ['Platform_SurfaceCombatant']}],
                        'province': 'Friuli-Venezia Giulia',
                        'services': [           {           'accreditation': 'NATO AQAP 2110',
                                                            'description': 'Drydock hull maintenance, shaft alignment, '
                                                                           'combat sensor mast integration, and '
                                                                           'acoustic sea acceptance trials.',
                                                            'name': 'Drydock Warship Modernization, Combat System '
                                                                    'Installation & Sea Trials',
                                                            'type': 'EngineeringService'}],
                        'tier': 'Tier1Supplier',
                        'trade_name': 'Fincantieri',
                        'website': 'https://www.fincantieri.com'},
            {           'business_number': 'ESB84076397',
                        'cage_code': None,
                        'capabilities': [           {           'description': 'Engineering of high-endurance '
                                                                               'submarine air-independent propulsion '
                                                                               'systems, Aegis combat system shipboard '
                                                                               'integration, and naval hull '
                                                                               'fabrication.',
                                                                'kic': 'KIC_NavalArchitectureMarineSystems',
                                                                'mrl': 9,
                                                                'title': 'Bio-Ethanol Stealth Air-Independent '
                                                                         'Propulsion & Warship Combat System '
                                                                         'Integration',
                                                                'trl': 9}],
                        'certifications': ['ISO9001', 'ISO14001', 'PECAL2110'],
                        'city': 'Madrid',
                        'controlled_goods': True,
                        'country': 'ESP',
                        'domains': ['MaritimePlatform', 'DomainDefence'],
                        'duns_number': None,
                        'itar_compliant': True,
                        'kics': ['KIC_NavalArchitectureMarineSystems', 'KIC_DefenceSystemsIntegration'],
                        'legal_name': 'Navantia S.A., S.M.E.',
                        'platforms': ['Platform_Submarine', 'Platform_SurfaceCombatant'],
                        'products': [           {           'description': 'Acoustically decoupled submarine pressure '
                                                                           'section incorporating bio-ethanol fuel '
                                                                           'cell AIP for extended underwater submerged '
                                                                           'endurance.',
                                                            'fsc_code': '1905',
                                                            'materials': ['Material_HY80_HY100_HighStrengthSteel'],
                                                            'name': 'S-80 Plus Class AIP Submarine Module and '
                                                                    'Structural Bulkhead',
                                                            'nsn_code': '1905-09-112-9904',
                                                            'part_number': 'PN-ESP-NAV-S80P',
                                                            'platforms': ['Platform_Submarine']}],
                        'province': 'Madrid',
                        'services': [           {           'accreditation': 'PECAL 2110',
                                                            'description': 'Shipboard cybersecurity auditing, '
                                                                           'automated platform management software '
                                                                           'upgrades, and mid-life combatant refits.',
                                                            'name': 'Integrated Naval Platform Management System '
                                                                    '(IPMS) Software Assurance & Fleet MRO',
                                                            'type': 'EngineeringService'}],
                        'tier': 'Tier1Supplier',
                        'trade_name': 'Navantia',
                        'website': 'https://www.navantia.es'}
        ,
{
                "legal_name": "MTU Aero Engines AG",
                "trade_name": "MTU Aero Engines",
                "cage_code": None,
                "duns_number": None,
                "business_number": "DE129273398",
                "country": "DEU",
                "city": "Munich",
                "province": "Bavaria",
                "website": "https://www.mtu.de",
                "tier": "Tier1Supplier",
                "controlled_goods": True,
                "itar_compliant": True,
                "certifications": [
                                "AS9100D",
                                "ISO9001",
                                "NATO_AQAP2110",
                                "FacilitySecurity_TopSecret"
                ],
                "domains": [
                                "AirPlatform",
                                "DomainDefence"
                ],
                "platforms": [
                                "Platform_Eurofighter_Typhoon",
                                "Platform_A400M_Atlas"
                ],
                "kics": [
                                "KIC_AerospaceSystems",
                                "KIC_AdvancedMaterials"
                ],
                "supplies_to": [
                                "Airbus SE",
                                "Rolls-Royce plc"
                ],
                "capabilities": [
                                {
                                                "title": "Military Gas Turbine Low-Pressure Turbines & Intermediate Casings",
                                                "description": "Design and manufacture of single-crystal turbine blades, blisks (bladed disks), and low-pressure turbine modules for Eurofighter EJ200 and TP400-D6 turboprop engines.",
                                                "trl": 9,
                                                "mrl": 9,
                                                "kic": "KIC_AerospaceSystems"
                                }
                ],
                "products": [
                                {
                                                "name": "EJ200 Low-Pressure Turbine Module",
                                                "description": "High-efficiency uncooled low-pressure turbine module engineered with advanced nickel superalloys for the Eurofighter Typhoon powerplant.",
                                                "part_number": "PN-DEU-MTU-EJLPT",
                                                "fsc_code": "2840",
                                                "nsn_code": "2840-12-381-9012",
                                                "platforms": [
                                                                "Platform_Eurofighter_Typhoon"
                                                ],
                                                "materials": [
                                                                "Material_SingleCrystal_Superalloy",
                                                                "Material_Inconel_718"
                                                ]
                                }
                ],
                "services": [
                                {
                                                "name": "Military Aeroengine Depot-Level MRO & Turbine Blisk Re-profiling",
                                                "description": "Electrochemical machining, laser powder bed additive blade tip repair, and high-speed dynamic balancing.",
                                                "type": "MROService",
                                                "accreditation": "EASA Part 145"
                                }
                ]
},
{
                "legal_name": "Thyssenkrupp Marine Systems GmbH",
                "trade_name": "TKMS",
                "cage_code": None,
                "duns_number": None,
                "business_number": "DE242691901",
                "country": "DEU",
                "city": "Kiel",
                "province": "Schleswig-Holstein",
                "website": "https://www.thyssenkrupp-marinesystems.com",
                "tier": "Prime",
                "controlled_goods": True,
                "itar_compliant": True,
                "certifications": [
                                "AS9100D",
                                "ISO9001",
                                "NATO_AQAP2110",
                                "FacilitySecurity_TopSecret"
                ],
                "domains": [
                                "MaritimePlatform",
                                "DomainDefence"
                ],
                "platforms": [
                                "Platform_Submarine",
                                "Platform_SurfaceCombatant"
                ],
                "kics": [
                                "KIC_NavalShipbuilding",
                                "KIC_NavalArchitectureMarineSystems"
                ],
                "supplies_to": [
                                "Kongsberg Gruppen ASA",
                                "Naval Group SA"
                ],
                "capabilities": [
                                {
                                                "title": "Air-Independent Propulsion (AIP) Non-Nuclear Submarines & Naval Combatants",
                                                "description": "World-leading design and construction of fuel-cell AIP conventional submarines (Type 212A / Type 212CD) and stealth surface frigates (MEKO / F125).",
                                                "trl": 9,
                                                "mrl": 9,
                                                "kic": "KIC_NavalShipbuilding"
                                }
                ],
                "products": [
                                {
                                                "name": "HDW Fuel Cell Air-Independent Propulsion (AIP) Plant",
                                                "description": "PEM fuel cell system utilizing metal hydride hydrogen storage and liquid oxygen for weeks of silent submerged patrol.",
                                                "part_number": "PN-DEU-TKM-AIP01",
                                                "fsc_code": "2010",
                                                "nsn_code": "2010-12-884-1192",
                                                "platforms": [
                                                                "Platform_Submarine"
                                                ],
                                                "materials": [
                                                                "Material_HY80_HY100_HighStrengthSteel",
                                                                "Material_Titanium_Ti6Al4V"
                                                ]
                                }
                ],
                "services": [
                                {
                                                "name": "Submarine Non-Magnetic Steel Pressure Hull Overhaul & Battery Recertification",
                                                "description": "Depot full-cycle docking, austenitic stainless steel acoustic hull repair, and AIP fuel cell stack renewal.",
                                                "type": "ShipyardMROService",
                                                "accreditation": "NATO AQAP 2110"
                                }
                ]
},
{
                "legal_name": "KNDS Deutschland GmbH & Co. KG",
                "trade_name": "KNDS Deutschland",
                "cage_code": None,
                "duns_number": None,
                "business_number": "DE129391081",
                "country": "DEU",
                "city": "Munich",
                "province": "Bavaria",
                "website": "https://www.knds.de",
                "tier": "Prime",
                "controlled_goods": True,
                "itar_compliant": True,
                "certifications": [
                                "AS9100D",
                                "ISO9001",
                                "NATO_AQAP2110",
                                "FacilitySecurity_TopSecret"
                ],
                "domains": [
                                "LandPlatform",
                                "DomainDefence"
                ],
                "platforms": [
                                "Platform_Leopard2_MainBattleTank",
                                "Platform_ArmouredCombatVehicle"
                ],
                "kics": [
                                "KIC_GroundCombatVehicles",
                                "KIC_ArmouredVehicles"
                ],
                "supplies_to": [
                                "Rheinmetall AG"
                ],
                "capabilities": [
                                {
                                                "title": "Heavy Armoured Combat Vehicle Systems & Main Battle Tanks",
                                                "description": "Prime integration of Leopard 2A7/2A8 main battle tanks, Boxer modular armoured personnel carriers, and automated remote weapon turrets.",
                                                "trl": 9,
                                                "mrl": 9,
                                                "kic": "KIC_GroundCombatVehicles"
                                }
                ],
                "products": [
                                {
                                                "name": "Leopard 2A8 Main Battle Tank Armoured Turret Assembly",
                                                "description": "Multi-layer composite and high-hardness armour turret module integrated with EuroTrophy active protection system and 120mm smoothbore gun mount.",
                                                "part_number": "PN-DEU-KND-L2A8",
                                                "fsc_code": "2350",
                                                "nsn_code": "2350-12-401-2891",
                                                "platforms": [
                                                                "Platform_Leopard2_MainBattleTank"
                                                ],
                                                "materials": [
                                                                "Material_ArmourSteel_MIL_A_46100",
                                                                "Material_Titanium_Ti6Al4V"
                                                ]
                                }
                ],
                "services": [
                                {
                                                "name": "Armoured Vehicle Hull Ballistic Upgrade & Trophy APS Integration",
                                                "description": "In-theater survivability kit integration, reactive armor recertification, and digital hull vetronics network upgrade.",
                                                "type": "CombatVehicleMROService",
                                                "accreditation": "ISO 9001"
                                }
                ]
},
{
                "legal_name": "RENK Group AG",
                "trade_name": "RENK",
                "cage_code": None,
                "duns_number": None,
                "business_number": "DE127491029",
                "country": "DEU",
                "city": "Augsburg",
                "province": "Bavaria",
                "website": "https://www.renk.com",
                "tier": "Tier1Supplier",
                "controlled_goods": True,
                "itar_compliant": True,
                "certifications": [
                                "AS9100D",
                                "ISO9001",
                                "NATO_AQAP2110"
                ],
                "domains": [
                                "LandPlatform",
                                "MaritimePlatform",
                                "DomainDefence"
                ],
                "platforms": [
                                "Platform_Leopard2_MainBattleTank",
                                "Platform_SurfaceCombatant"
                ],
                "kics": [
                                "KIC_GroundCombatVehicles",
                                "KIC_NavalArchitectureMarineSystems"
                ],
                "supplies_to": [
                                "KNDS Deutschland GmbH & Co. KG",
                                "Rheinmetall AG",
                                "Thyssenkrupp Marine Systems GmbH"
                ],
                "capabilities": [
                                {
                                                "title": "Heavy-Duty Tracked Vehicle Transmissions & Naval Gear Systems",
                                                "description": "Design and manufacture of powershift transmissions with integrated steering and braking systems (HSWL 354) for 70-tonne battle tanks and low-noise naval reduction gearboxes.",
                                                "trl": 9,
                                                "mrl": 9,
                                                "kic": "KIC_GroundCombatVehicles"
                                }
                ],
                "products": [
                                {
                                                "name": "HSWL 354 Powershift Transmission System",
                                                "description": "Full-automatic powershift transmission with hydrodynamic retarder and electro-hydraulic brake system for Leopard 2 chassis.",
                                                "part_number": "PN-DEU-RNK-354",
                                                "fsc_code": "2520",
                                                "nsn_code": "2520-12-192-3811",
                                                "platforms": [
                                                                "Platform_Leopard2_MainBattleTank"
                                                ],
                                                "materials": [
                                                                "Material_ArmourSteel_MIL_A_46100",
                                                                "Material_Aluminium_7075_T6"
                                                ]
                                }
                ],
                "services": [
                                {
                                                "name": "Military Drivetrain Dynamometer Testing & Full Depot Rebuild",
                                                "description": "High-torque automated dynamometer load-profiling, hydraulic valve block overhaul, and planetary gear set rejuvenation.",
                                                "type": "TransmissionOverhaulService",
                                                "accreditation": "NATO AQAP 2110"
                                }
                ]
},
{
                "legal_name": "Rohde & Schwarz GmbH & Co. KG",
                "trade_name": "Rohde & Schwarz",
                "cage_code": None,
                "duns_number": None,
                "business_number": "DE129721448",
                "country": "DEU",
                "city": "Munich",
                "province": "Bavaria",
                "website": "https://www.rohde-schwarz.com",
                "tier": "Tier1Supplier",
                "controlled_goods": True,
                "itar_compliant": True,
                "certifications": [
                                "AS9100D",
                                "ISO9001",
                                "NATO_AQAP2110",
                                "FacilitySecurity_TopSecret"
                ],
                "domains": [
                                "AirPlatform",
                                "MaritimePlatform",
                                "LandPlatform",
                                "DomainDefence"
                ],
                "platforms": [
                                "Platform_Eurofighter_Typhoon",
                                "Platform_SurfaceCombatant"
                ],
                "kics": [
                                "KIC_C4ISRSystems",
                                "KIC_CyberResilience"
                ],
                "supplies_to": [
                                "Airbus SE",
                                "Hensoldt AG",
                                "Thyssenkrupp Marine Systems GmbH"
                ],
                "capabilities": [
                                {
                                                "title": "Software-Defined Radios (SDR) & Secure Military Tactical Communications",
                                                "description": "Development of SOVERON digital tactical communications architectures, cryptographic key management, and naval integrated communications systems (NAVICS).",
                                                "trl": 9,
                                                "mrl": 9,
                                                "kic": "KIC_C4ISRSystems"
                                }
                ],
                "products": [
                                {
                                                "name": "SOVERON AR5000 Airborne Software-Defined Radio",
                                                "description": "VHF/UHF wideband secure airborne transceiver with ECCM frequency hopping and SATURN / Have Quick waveform support.",
                                                "part_number": "PN-DEU-RS-AR5000",
                                                "fsc_code": "5821",
                                                "nsn_code": "5821-12-384-9182",
                                                "platforms": [
                                                                "Platform_Eurofighter_Typhoon",
                                                                "Platform_A400M_Atlas"
                                                ],
                                                "materials": [
                                                                "Material_Aluminium_7075_T6"
                                                ]
                                }
                ],
                "services": [
                                {
                                                "name": "Tactical Radio Waveform Cryptographic Hardening & Cyber Vulnerability Audit",
                                                "description": "Cryptographic algorithm evaluation, frequency-hopping jammer resistance verification, and tactical communications penetration testing.",
                                                "type": "CyberSecurityService",
                                                "accreditation": "BSI Certified"
                                }
                ]
},
{
                "legal_name": "ArianeGroup SAS",
                "trade_name": "ArianeGroup",
                "cage_code": None,
                "duns_number": None,
                "business_number": "FR89808389102",
                "country": "FRA",
                "city": "Issy-les-Moulineaux",
                "province": "\u00cele-de-France",
                "website": "https://www.ariane.group",
                "tier": "Prime",
                "controlled_goods": True,
                "itar_compliant": True,
                "certifications": [
                                "AS9100D",
                                "ISO9001",
                                "NATO_AQAP2110",
                                "FacilitySecurity_TopSecret"
                ],
                "domains": [
                                "SpacePlatform",
                                "DomainSpace",
                                "DomainDefence"
                ],
                "platforms": [
                                "Platform_SpaceLaunchVehicle"
                ],
                "kics": [
                                "KIC_SpaceSystems",
                                "KIC_Munitions",
                                "KIC_AdvancedMaterials"
                ],
                "supplies_to": [
                                "Airbus SE",
                                "Safran SA"
                ],
                "capabilities": [
                                {
                                                "title": "Cryogenic & Solid Rocket Propulsion Systems (Ariane 6 / M51)",
                                                "description": "Prime industrial integration of Ariane 6 orbital launch vehicles, Vulcain 2.1 / Vinci cryogenic liquid engines, and solid rocket motors for strategic deterrence.",
                                                "trl": 9,
                                                "mrl": 9,
                                                "kic": "KIC_SpaceSystems"
                                }
                ],
                "products": [
                                {
                                                "name": "Vinci Re-ignitable Cryogenic Rocket Engine Upper Stage",
                                                "description": "Expandable nozzle cryo-engine generating 180 kN of thrust with multiple re-ignition capability for complex orbital satellite deployment.",
                                                "part_number": "PN-FRA-ARG-VNC01",
                                                "fsc_code": "1336",
                                                "nsn_code": "1336-14-551-9012",
                                                "platforms": [
                                                                "Platform_SpaceLaunchVehicle"
                                                ],
                                                "materials": [
                                                                "Material_Inconel_718",
                                                                "Material_CarbonFiber_Composite"
                                                ]
                                }
                ],
                "services": [
                                {
                                                "name": "Space Launch Vehicle Pyrotechnic Stage Separation & Hot-Fire Testing",
                                                "description": "Vacuum altitude simulation hot-fire propulsion testing, acoustic vibration resonance assessment, and pyrotechnic separation bolt testing.",
                                                "type": "PropulsionTestingService",
                                                "accreditation": "ESA / CNES Certified"
                                }
                ]
},
{
                "legal_name": "Lat\u00e9co\u00e8re SA",
                "trade_name": "Lat\u00e9co\u00e8re",
                "cage_code": None,
                "duns_number": None,
                "business_number": "FR34572049182",
                "country": "FRA",
                "city": "Toulouse",
                "province": "Occitanie",
                "website": "https://www.latecoere.aero",
                "tier": "Tier1Supplier",
                "controlled_goods": True,
                "itar_compliant": True,
                "certifications": [
                                "AS9100D",
                                "ISO9001",
                                "FacilitySecurity_Secret"
                ],
                "domains": [
                                "AirPlatform",
                                "DomainDefence"
                ],
                "platforms": [
                                "Platform_Dassault_Rafale",
                                "Platform_A400M_Atlas",
                                "Platform_F35_Lightning_II"
                ],
                "kics": [
                                "KIC_AerospaceSystems",
                                "KIC_AdvancedMaterials"
                ],
                "supplies_to": [
                                "Dassault Aviation SA",
                                "Airbus SE",
                                "Boeing Company"
                ],
                "capabilities": [
                                {
                                                "title": "Aerostructures Aircraft Doors & Electrical Wiring Interconnection Systems (EWIS)",
                                                "description": "Design and manufacture of complex metallic/composite aircraft doors and military harness interconnection packages for tactical airlifters and fighters.",
                                                "trl": 9,
                                                "mrl": 9,
                                                "kic": "KIC_AerospaceSystems"
                                }
                ],
                "products": [
                                {
                                                "name": "Rafale Combat Aircraft Main Landing Gear Door Assembly",
                                                "description": "High-stiffness carbon-fiber composite landing gear door assembly engineered to withstand Mach 1.8 aerodynamic buffet pressures.",
                                                "part_number": "PN-FRA-LAT-RF01",
                                                "fsc_code": "1560",
                                                "nsn_code": "1560-14-412-8821",
                                                "platforms": [
                                                                "Platform_Dassault_Rafale"
                                                ],
                                                "materials": [
                                                                "Material_CarbonFiber_Composite",
                                                                "Material_Titanium_Ti6Al4V"
                                                ]
                                }
                ],
                "services": [
                                {
                                                "name": "Composite Aerostructure Ultrasonic C-Scan NDT & Structural Door Rig Testing",
                                                "description": "Automated multi-axis phased array ultrasonic testing, moisture ingress evaluation, and cycle fatigue door hinge testing.",
                                                "type": "NDTService",
                                                "accreditation": "NADCAP Composites"
                                }
                ]
},
{
                "legal_name": "Exail Technologies SAS",
                "trade_name": "Exail",
                "cage_code": None,
                "duns_number": None,
                "business_number": "FR55552084192",
                "country": "FRA",
                "city": "Saint-Germain-en-Laye",
                "province": "\u00cele-de-France",
                "website": "https://www.exail.com",
                "tier": "Tier1Supplier",
                "controlled_goods": True,
                "itar_compliant": True,
                "certifications": [
                                "AS9100D",
                                "ISO9001",
                                "NATO_AQAP2110",
                                "FacilitySecurity_TopSecret"
                ],
                "domains": [
                                "MaritimePlatform",
                                "LandPlatform",
                                "DomainDefence"
                ],
                "platforms": [
                                "Platform_Submarine",
                                "Platform_SurfaceCombatant"
                ],
                "kics": [
                                "KIC_SensorsSonar",
                                "KIC_AIAutonomousSystems",
                                "KIC_NavalArchitectureMarineSystems"
                ],
                "supplies_to": [
                                "Naval Group SA",
                                "Thales SA"
                ],
                "capabilities": [
                                {
                                                "title": "Fiber-Optic Gyroscope (FOG) Inertial Navigation & Autonomous Mine Countermeasure Robotics",
                                                "description": "World-leading sub-nautical-mile/month drift fiber-optic gyro inertial navigation systems (Phins / Marins) and unmanned surface/underwater robotic vehicles (A18-M / UMIS).",
                                                "trl": 9,
                                                "mrl": 9,
                                                "kic": "KIC_SensorsSonar"
                                }
                ],
                "products": [
                                {
                                                "name": "Marins M7 High-Accuracy Submarine Inertial Navigation System",
                                                "description": "Military-grade optical fiber gyro INS delivering GPS-denied navigation precision for nuclear and conventional attack submarines.",
                                                "part_number": "PN-FRA-EXL-M701",
                                                "fsc_code": "6605",
                                                "nsn_code": "6605-14-592-3109",
                                                "platforms": [
                                                                "Platform_Submarine",
                                                                "Platform_SurfaceCombatant"
                                                ],
                                                "materials": [
                                                                "Material_Titanium_Ti6Al4V",
                                                                "Material_Beryllium_Optical"
                                                ]
                                }
                ],
                "services": [
                                {
                                                "name": "Subsea Acoustic Positioning Calibration & Autonomous Vehicle Navigation Tuning",
                                                "description": "High-depth pressure tank sensor qualification, long-baseline (LBL) transponder calibration, and autonomous obstacle-avoidance firmware validation.",
                                                "type": "HydrographicService",
                                                "accreditation": "ISO 9001"
                                }
                ]
},
{
                "legal_name": "Sogeclair SA",
                "trade_name": "Sogeclair",
                "cage_code": None,
                "duns_number": None,
                "business_number": "FR48384210981",
                "country": "FRA",
                "city": "Blagnac",
                "province": "Occitanie",
                "website": "https://www.sogeclair.com",
                "tier": "Tier2Supplier",
                "controlled_goods": True,
                "itar_compliant": True,
                "certifications": [
                                "AS9100D",
                                "ISO9001"
                ],
                "domains": [
                                "AirPlatform",
                                "LandPlatform",
                                "DomainDefence"
                ],
                "platforms": [
                                "Platform_Dassault_Rafale",
                                "Platform_ArmouredCombatVehicle"
                ],
                "kics": [
                                "KIC_AerospaceSystems",
                                "KIC_TrainingSimulation"
                ],
                "supplies_to": [
                                "Airbus SE",
                                "Dassault Aviation SA",
                                "Thales SA"
                ],
                "capabilities": [
                                {
                                                "title": "High-Fidelity Virtual Simulation & Tactical Vehicle Cabin Engineering",
                                                "description": "Specialized simulation software architectures, structural finite element modeling (FEM), and blast-attenuating military vehicle cab systems.",
                                                "trl": 8,
                                                "mrl": 8,
                                                "kic": "KIC_TrainingSimulation"
                                }
                ],
                "products": [
                                {
                                                "name": "Tactical Vehicle Driver Interactive Simulation Cabin",
                                                "description": "Full-motion multi-axis physical vehicle driver training simulator cab with realistic synthetic terrain visual projection.",
                                                "part_number": "PN-FRA-SOG-SIM01",
                                                "fsc_code": "6930",
                                                "nsn_code": "6930-14-338-9128",
                                                "platforms": [
                                                                "Platform_ArmouredCombatVehicle"
                                                ],
                                                "materials": [
                                                                "Material_Aluminium_7075_T6"
                                                ]
                                }
                ],
                "services": [
                                {
                                                "name": "Aerospace Finite Element Stress Analysis & Crashworthiness Modeling",
                                                "description": "Non-linear dynamic crash simulation, cockpit bird strike analysis, and fatigue life assessment of airframe bulkheads.",
                                                "type": "EngineeringSimulationService",
                                                "accreditation": "ISO 9001"
                                }
                ]
},
{
                "legal_name": "Nexter Systems SA",
                "trade_name": "KNDS France",
                "cage_code": None,
                "duns_number": None,
                "business_number": "FR70444901928",
                "country": "FRA",
                "city": "Versailles",
                "province": "\u00cele-de-France",
                "website": "https://www.knds.fr",
                "tier": "Prime",
                "controlled_goods": True,
                "itar_compliant": True,
                "certifications": [
                                "AS9100D",
                                "ISO9001",
                                "NATO_AQAP2110",
                                "FacilitySecurity_TopSecret"
                ],
                "domains": [
                                "LandPlatform",
                                "DomainDefence"
                ],
                "platforms": [
                                "Platform_GroundCombatVehicle",
                                "Platform_ArmouredCombatVehicle"
                ],
                "kics": [
                                "KIC_GroundCombatVehicles",
                                "KIC_Munitions",
                                "KIC_ArmouredVehicles"
                ],
                "supplies_to": [
                                "KNDS Deutschland GmbH & Co. KG",
                                "Thales SA"
                ],
                "capabilities": [
                                {
                                                "title": "Truck-Mounted Artillery Systems (CAESAR) & Medium Armoured Combat Vehicles",
                                                "description": "Prime development of 155mm 52-caliber CAESAR self-propelled artillery systems, VBCI 8x8 infantry fighting vehicles, and high-precision extended-range munitions (KATANA).",
                                                "trl": 9,
                                                "mrl": 9,
                                                "kic": "KIC_GroundCombatVehicles"
                                }
                ],
                "products": [
                                {
                                                "name": "CAESAR 155mm 52-Caliber Artillery Gun System",
                                                "description": "Highly mobile truck-mounted artillery system firing 6 rounds per minute at ranges exceeding 40km with autonomous navigation.",
                                                "part_number": "PN-FRA-NXT-CSR52",
                                                "fsc_code": "1025",
                                                "nsn_code": "1025-14-558-4019",
                                                "platforms": [
                                                                "Platform_GroundCombatVehicle"
                                                ],
                                                "materials": [
                                                                "Material_ArmourSteel_MIL_A_46100",
                                                                "Material_Titanium_Ti6Al4V"
                                                ]
                                }
                ],
                "services": [
                                {
                                                "name": "Artillery Barrel Autofrettage & Gun Tube Erosion Inspection",
                                                "description": "Hydraulic high-pressure autofrettage processing, laser bore profilometry, and erosion life modeling for tank and artillery tubes.",
                                                "type": "ArtilleryOverhaulService",
                                                "accreditation": "NATO AQAP 2110"
                                }
                ]
},
{
                "legal_name": "Avio Aero",
                "trade_name": "GE Avio S.r.l.",
                "cage_code": None,
                "duns_number": None,
                "business_number": "IT02598120014",
                "country": "ITA",
                "city": "Rivalta di Torino",
                "province": "Piedmont",
                "website": "https://www.avioaero.com",
                "tier": "Tier1Supplier",
                "controlled_goods": True,
                "itar_compliant": True,
                "certifications": [
                                "AS9100D",
                                "ISO9001",
                                "NATO_AQAP2110",
                                "FacilitySecurity_TopSecret"
                ],
                "domains": [
                                "AirPlatform",
                                "DomainDefence"
                ],
                "platforms": [
                                "Platform_Eurofighter_Typhoon",
                                "Platform_RotaryWing"
                ],
                "kics": [
                                "KIC_AerospaceSystems",
                                "KIC_AdvancedMaterials"
                ],
                "supplies_to": [
                                "Leonardo S.p.A.",
                                "MTU Aero Engines AG",
                                "Safran SA"
                ],
                "capabilities": [
                                {
                                                "title": "Aeroengine Power Transmissions, Accessory Gearboxes & Electron Beam Melting (EBM) Additive",
                                                "description": "High-speed transmission systems for military turbofans and turboshafts, additive manufacturing of titanium aluminide (TiAl) low-pressure turbine blades.",
                                                "trl": 9,
                                                "mrl": 9,
                                                "kic": "KIC_AerospaceSystems"
                                }
                ],
                "products": [
                                {
                                                "name": "EJ200 Accessory Drive Gearbox (ADGB)",
                                                "description": "Cast magnesium alloy high-power accessory gearbox transmitting auxiliary drive to hydraulic pumps and generators for Eurofighter Typhoon.",
                                                "part_number": "PN-ITA-AVI-ADGB",
                                                "fsc_code": "2840",
                                                "nsn_code": "2840-15-441-9011",
                                                "platforms": [
                                                                "Platform_Eurofighter_Typhoon"
                                                ],
                                                "materials": [
                                                                "Material_Titanium_Ti6Al4V",
                                                                "Material_Aluminium_7075_T6"
                                                ]
                                }
                ],
                "services": [
                                {
                                                "name": "Additive Titanium Aluminide EBM Melting & Metallurgical Fatigue Testing",
                                                "description": "Electron beam powder bed additive manufacturing, hot isostatic pressing (HIP) density validation, and high-cycle blade fatigue testing.",
                                                "type": "AdditiveManufacturingService",
                                                "accreditation": "NADCAP Additive"
                                }
                ]
},
{
                "legal_name": "Elettronica S.p.A.",
                "trade_name": "ELT Group",
                "cage_code": None,
                "duns_number": None,
                "business_number": "IT00428910582",
                "country": "ITA",
                "city": "Rome",
                "province": "Lazio",
                "website": "https://www.elt-roma.com",
                "tier": "Tier1Supplier",
                "controlled_goods": True,
                "itar_compliant": True,
                "certifications": [
                                "AS9100D",
                                "ISO9001",
                                "NATO_AQAP2110",
                                "FacilitySecurity_TopSecret"
                ],
                "domains": [
                                "AirPlatform",
                                "MaritimePlatform",
                                "DomainDefence"
                ],
                "platforms": [
                                "Platform_Eurofighter_Typhoon",
                                "Platform_SurfaceCombatant"
                ],
                "kics": [
                                "KIC_SensorsSonar",
                                "KIC_CyberResilience",
                                "KIC_DefenceSystemsIntegration"
                ],
                "supplies_to": [
                                "Leonardo S.p.A.",
                                "Airbus SE"
                ],
                "capabilities": [
                                {
                                                "title": "Airborne & Naval Electronic Warfare (EW) Suites and Directional Infrared Countermeasures (DIRCM)",
                                                "description": "Self-protection suites (Praetorian DASS for Typhoon), wideband digital radar warning receivers, and multi-band electronic attack jammers.",
                                                "trl": 9,
                                                "mrl": 9,
                                                "kic": "KIC_SensorsSonar"
                                }
                ],
                "products": [
                                {
                                                "name": "Praetorian Defensive Aids Sub-System (DASS) Wingtip EW Pod",
                                                "description": "Wingtip-mounted wideband digital radar warner and cross-eye electronic countermeasure pod for Eurofighter air dominance.",
                                                "part_number": "PN-ITA-ELT-PRT01",
                                                "fsc_code": "5865",
                                                "nsn_code": "5865-15-881-3092",
                                                "platforms": [
                                                                "Platform_Eurofighter_Typhoon"
                                                ],
                                                "materials": [
                                                                "Material_CarbonFiber_Composite",
                                                                "Material_GalliumNitride_GaN"
                                                ]
                                }
                ],
                "services": [
                                {
                                                "name": "Electronic Warfare Threat Library Generation & Anechoic Chamber Testing",
                                                "description": "Radar emitter pulse train simulation, automated jammer response latency verification, and full-scale anechoic RF chamber characterization.",
                                                "type": "EWTestingService",
                                                "accreditation": "NATO Secret"
                                }
                ]
},
{
                "legal_name": "Nammo AS",
                "trade_name": "Nammo",
                "cage_code": None,
                "duns_number": None,
                "business_number": "NO980192841",
                "country": "NOR",
                "city": "Raufoss",
                "province": "Innlandet",
                "website": "https://www.nammo.com",
                "tier": "Tier1Supplier",
                "controlled_goods": True,
                "itar_compliant": True,
                "certifications": [
                                "AS9100D",
                                "ISO9001",
                                "NATO_AQAP2110",
                                "FacilitySecurity_TopSecret"
                ],
                "domains": [
                                "LandPlatform",
                                "AirPlatform",
                                "DomainDefence"
                ],
                "platforms": [
                                "Platform_F35_Lightning_II",
                                "Platform_GroundCombatVehicle"
                ],
                "kics": [
                                "KIC_Munitions",
                                "KIC_AdvancedMaterials"
                ],
                "supplies_to": [
                                "Diehl Defence GmbH & Co. KG",
                                "Kongsberg Gruppen ASA",
                                "Raytheon Company"
                ],
                "capabilities": [
                                {
                                                "title": "Specialized Military Energetics, Missile Rocket Motors & Insensitive Munitions",
                                                "description": "Design and manufacture of 25mm APEX ammunition for F-35, solid rocket booster motors for AMRAAM / IRIS-T, and ramjet missile propulsion.",
                                                "trl": 9,
                                                "mrl": 9,
                                                "kic": "KIC_Munitions"
                                }
                ],
                "products": [
                                {
                                                "name": "25mm APEX Multi-Purpose Armor-Piercing High-Explosive Round",
                                                "description": "Semi-armor-piercing high-explosive round engineered for F-35 GAU-22/A cannon to defeat armored targets and bunker structures.",
                                                "part_number": "PN-NOR-NAM-APX25",
                                                "fsc_code": "1305",
                                                "nsn_code": "1305-25-112-9981",
                                                "platforms": [
                                                                "Platform_F35_Lightning_II"
                                                ],
                                                "materials": [
                                                                "Material_Tungsten_HeavyAlloy",
                                                                "Material_ArmourSteel_MIL_A_46100"
                                                ]
                                }
                ],
                "services": [
                                {
                                                "name": "Insensitive Munitions Fast-Cookoff & Bullet Impact Proof Testing",
                                                "description": "STANAG 4439 thermal cookoff testing, sympathetic detonation range verification, and ballistic gelatin penetration evaluation.",
                                                "type": "BallisticsTestingService",
                                                "accreditation": "NATO AQAP 2110"
                                }
                ]
},
{
                "legal_name": "GKN Aerospace Sweden AB",
                "trade_name": "GKN Aerospace Sweden",
                "cage_code": None,
                "duns_number": None,
                "business_number": "SE556024982101",
                "country": "SWE",
                "city": "Trollh\u00e4ttan",
                "province": "V\u00e4stra G\u00f6taland",
                "website": "https://www.gknaerospace.com",
                "tier": "Tier1Supplier",
                "controlled_goods": True,
                "itar_compliant": True,
                "certifications": [
                                "AS9100D",
                                "ISO9001",
                                "NATO_AQAP2110",
                                "FacilitySecurity_TopSecret"
                ],
                "domains": [
                                "AirPlatform",
                                "DomainDefence"
                ],
                "platforms": [
                                "Platform_Saab_Gripen_E"
                ],
                "kics": [
                                "KIC_AerospaceSystems",
                                "KIC_AdvancedMaterials"
                ],
                "supplies_to": [
                                "Saab AB",
                                "Rolls-Royce plc"
                ],
                "capabilities": [
                                {
                                                "title": "Gripen RM12 / RM16 Military Aeroengine Prime Manufacturing & Nozzle Integration",
                                                "description": "Design and manufacture of convergent-divergent supersonic exhaust nozzles, turbine exhaust casings, and combustor structures for JAS 39 Gripen fighters.",
                                                "trl": 9,
                                                "mrl": 9,
                                                "kic": "KIC_AerospaceSystems"
                                }
                ],
                "products": [
                                {
                                                "name": "RM12 / RM16 Supersonic Variable-Area Exhaust Nozzle",
                                                "description": "Multi-flap titanium and superalloy afterburning exhaust nozzle with hydraulic actuator synchronization for Gripen combat aircraft.",
                                                "part_number": "PN-SWE-GKN-RMNOZ",
                                                "fsc_code": "2840",
                                                "nsn_code": "2840-25-881-2091",
                                                "platforms": [
                                                                "Platform_Saab_Gripen_E"
                                                ],
                                                "materials": [
                                                                "Material_Titanium_Ti6Al4V",
                                                                "Material_Inconel_718"
                                                ]
                                }
                ],
                "services": [
                                {
                                                "name": "Fighter Engine Sea-Level Test Cell Operation & Hot Gas Overhaul",
                                                "description": "Full-afterburner thrust calibration, laser holographic blade vibration inspection, and thermal barrier coating restoration.",
                                                "type": "EngineMROService",
                                                "accreditation": "SWEDAC / EASA"
                                }
                ]
},
{
                "legal_name": "Fokker Aerostructures BV",
                "trade_name": "GKN Aerospace Netherlands",
                "cage_code": None,
                "duns_number": None,
                "business_number": "NL803921841B01",
                "country": "NLD",
                "city": "Papendrecht",
                "province": "South Holland",
                "website": "https://www.gknaerospace.com",
                "tier": "Tier1Supplier",
                "controlled_goods": True,
                "itar_compliant": True,
                "certifications": [
                                "AS9100D",
                                "ISO9001",
                                "FacilitySecurity_TopSecret"
                ],
                "domains": [
                                "AirPlatform",
                                "DomainDefence"
                ],
                "platforms": [
                                "Platform_F35_Lightning_II"
                ],
                "kics": [
                                "KIC_AerospaceSystems",
                                "KIC_AdvancedMaterials"
                ],
                "supplies_to": [
                                "Lockheed Martin Corporation",
                                "Airbus SE"
                ],
                "capabilities": [
                                {
                                                "title": "Thermoplastic Composite Aerostructures & F-35 Flaperon Manufacturing",
                                                "description": "Pioneering high-rate thermoplastic composite induction welding and automated tape laying for F-35 flaperons, in-flight refuelling doors, and engine arrestor hooks.",
                                                "trl": 9,
                                                "mrl": 9,
                                                "kic": "KIC_AerospaceSystems"
                                }
                ],
                "products": [
                                {
                                                "name": "F-35 Lightning II Carbon Composite Flaperon Control Surface",
                                                "description": "Molded thermoplastic carbon-fiber flight control surface engineered to sustain extreme supersonic acoustic flutter.",
                                                "part_number": "PN-NLD-FOK-F35FLP",
                                                "fsc_code": "1560",
                                                "nsn_code": "1560-17-119-4821",
                                                "platforms": [
                                                                "Platform_F35_Lightning_II"
                                                ],
                                                "materials": [
                                                                "Material_CarbonFiber_Composite",
                                                                "Material_Titanium_Ti6Al4V"
                                                ]
                                }
                ],
                "services": [
                                {
                                                "name": "Thermoplastic In-Situ Consolidation NDT & Bond Line Ultrasonic Inspection",
                                                "description": "Laser shearography delamination detection, robotic water-coupled ultrasonic inspection, and high-energy impact damage repair.",
                                                "type": "AdvancedCompositeNDTService",
                                                "accreditation": "NADCAP Composites"
                                }
                ]
},
{
                "legal_name": "Damen Schelde Naval Shipbuilding B.V.",
                "trade_name": "Damen Naval",
                "cage_code": None,
                "duns_number": None,
                "business_number": "NL001092841B01",
                "country": "NLD",
                "city": "Vlissingen",
                "province": "Zeeland",
                "website": "https://www.damen.com/naval",
                "tier": "Prime",
                "controlled_goods": True,
                "itar_compliant": True,
                "certifications": [
                                "AS9100D",
                                "ISO9001",
                                "NATO_AQAP2110",
                                "FacilitySecurity_TopSecret"
                ],
                "domains": [
                                "MaritimePlatform",
                                "DomainDefence"
                ],
                "platforms": [
                                "Platform_SurfaceCombatant"
                ],
                "kics": [
                                "KIC_NavalShipbuilding",
                                "KIC_NavalArchitectureMarineSystems"
                ],
                "supplies_to": [
                                "Thyssenkrupp Marine Systems GmbH",
                                "Thales SA"
                ],
                "capabilities": [
                                {
                                                "title": "Multi-Purpose Frigate (F126) & Combatant Modular Naval Shipbuilding",
                                                "description": "Design and construction of advanced modular anti-submarine warfare frigates, SIGMA-class corvettes, and Enforcer-class joint support ships.",
                                                "trl": 9,
                                                "mrl": 9,
                                                "kic": "KIC_NavalShipbuilding"
                                }
                ],
                "products": [
                                {
                                                "name": "F126 Frigate Pre-Outfitted Modular Hull Block Assembly",
                                                "description": "Shock-hardened, low-radar-cross-section steel hull section pre-fitted with acoustic vibration damping mounts for frigate integration.",
                                                "part_number": "PN-NLD-DMN-F126B",
                                                "fsc_code": "1905",
                                                "nsn_code": "1905-17-901-4412",
                                                "platforms": [
                                                                "Platform_SurfaceCombatant"
                                                ],
                                                "materials": [
                                                                "Material_HY80_HY100_HighStrengthSteel",
                                                                "Material_ArmourSteel_MIL_A_46100"
                                                ]
                                }
                ],
                "services": [
                                {
                                                "name": "Warship Underwater Acoustic Radiated Noise (URN) Measurement & Signature Quieting",
                                                "description": "Full-scale sea-range hydrophone acoustic signature logging, cavitation baseline tracking, and structural resonant vibration suppression.",
                                                "type": "AcousticRangeService",
                                                "accreditation": "NATO AQAP 2110"
                                }
                ]
}
        ]

    def harvest(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        records = self._get_flagship_eu_companies()
        if limit is not None:
            records = records[:limit]
        self.save_raw(records, "eu_aero_defence_catalog.json")
        return records
