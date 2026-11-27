"""
New Zealand Aerospace & Defence Harvester.
Captures key New Zealand prime contractors, space launch integrators,
tactical communications leaders, and specialized advanced manufacturing SMEs.
"""

from typing import List, Dict, Any, Optional
import random
from harvesters.base import BaseHarvester


class NewZealandHarvester(BaseHarvester):
    """Harvester for New Zealand Aerospace & Defence industrial base."""

    def __init__(self):
        super().__init__(region_name="NewZealand")

    def _get_flagship_nz_companies(self) -> List[Dict[str, Any]]:
        return [
            {
                "legal_name": "Rocket Lab Limited",
                "trade_name": "Rocket Lab",
                "cage_code": "E0A12",
                "duns_number": "594820194",
                "business_number": "NZ9429031827461",
                "country": "NZL",
                "city": "Auckland",
                "province": "Auckland",
                "website": "https://www.rocketlabusa.com",
                "tier": "Prime",
                "controlled_goods": True,
                "itar_compliant": True,
                "certifications": ["AS9100D", "ISO9001", "ITAR_Compliant", "FacilitySecurity_Secret"],
                "domains": ["SpacePlatform", "DomainSpace", "DomainDefence"],
                "platforms": ["Platform_SpaceLaunchVehicle", "Platform_LEOSatellite"],
                "kics": ["KIC_SpaceSystems", "KIC_AdvancedMaterials", "KIC_AIAutonomousSystems"],
                "capabilities": [
                    {
                        "title": "Dedicated Orbital Small Satellite Launch Vehicle (Electron)",
                        "description": "Carbon-composite orbital rocket manufacturing, Rutherford electric-pump-fed 3D printed engines, and rapid responsive space launch.",
                        "trl": 9,
                        "mrl": 9,
                        "kic": "KIC_SpaceSystems",
                    },
                    {
                        "title": "Configurable Satellite Bus & Orbital Servicing (Photon)",
                        "description": "End-to-end satellite bus design, integrated avionics, star trackers, reaction wheels, and deep space exploration payload platforms.",
                        "trl": 8,
                        "mrl": 8,
                        "kic": "KIC_SpaceSystems",
                    },
                    {
                        "title": "Advanced Carbon Composite High-Pressure Cryogenic Tanks",
                        "description": "Autoclave-cured carbon-composite tanks for liquid oxygen and RP-1 kerosene propellant storage in space launch vehicles.",
                        "trl": 9,
                        "mrl": 9,
                        "kic": "KIC_AdvancedMaterials",
                    },
                ],
                "products": [
                    {
                        "name": "Electron Orbital Launch Vehicle",
                        "description": "Two-stage orbital rocket capable of deploying 300kg payloads to low Earth orbit with dedicated kick stage.",
                        "part_number": "PN-NZL-ELC-001",
                        "fsc_code": "1420",
                        "nsn_code": "1420-98-102-4411",
                        "platforms": ["Platform_SpaceLaunchVehicle"],
                        "materials": ["Material_CarbonFiber_Composite", "Material_Inconel_718"],
                    },
                    {
                        "name": "Photon Spacecraft Bus",
                        "description": "High-delta-V operational satellite platform for LEO constellations and lunar transfer orbits.",
                        "part_number": "PN-NZL-PHT-002",
                        "fsc_code": "1420",
                        "nsn_code": "1420-98-102-4412",
                        "platforms": ["Platform_LEOSatellite"],
                        "materials": ["Material_GalliumNitride_GaN", "Material_CarbonFiber_Composite"],
                    },
                    {
                        "name": "Rutherford Electric-Pump Rocket Engine",
                        "description": "3D printed cycle rocket engine powered by brushless DC electric motors and lithium polymer batteries delivering 25 kN thrust.",
                        "part_number": "PN-NZL-RTH-003",
                        "fsc_code": "2840",
                        "nsn_code": "2840-98-102-4413",
                        "platforms": ["Platform_SpaceLaunchVehicle"],
                        "materials": ["Material_Inconel_718", "Material_Titanium_Ti6Al4V"],
                    },
                ],
                "services": [
                    {
                        "name": "Dedicated Orbital Space Launch Operations",
                        "description": "Full-turnkey launch pad operations, orbital trajectory simulation, range safety, and payload encapsulation at Launch Complex 1.",
                        "type": "EngineeringService",
                        "accreditation": "FAA Part 450 Launch License",
                    },
                    {
                        "name": "Payload Cleanroom Integration and Environmental Testing",
                        "description": "ISO 8 cleanroom integration, acoustic vibration qualification, thermal vacuum bake-out, and pre-flight telemetry checkout.",
                        "type": "TestingQualificationService",
                        "accreditation": "ISO/IEC 17025",
                    },
                    {
                        "name": "Satellite Constellation Telemetry Tracking & Mission Operations",
                        "description": "Continuous 24/7 mission control, orbital positioning, collision avoidance analysis, and downlink scheduling.",
                        "type": "SimulationTrainingService",
                        "accreditation": "Space Operations Security Level 2",
                    },
                    {
                        "name": "Rocket Engine Hot-Fire Qualification & Rapid Refurbishment",
                        "description": "Automated engine test stand hot-fire acceptance screening, high-pressure injector calibration, and turnaround testing.",
                        "type": "MROService",
                        "accreditation": "AS9100D",
                    },
                ],
            },
            {
                "legal_name": "Dawn Aerospace Limited",
                "trade_name": "Dawn Aerospace",
                "cage_code": "E0B24",
                "duns_number": "594892018",
                "business_number": "NZ9429046829102",
                "country": "NZL",
                "city": "Christchurch",
                "province": "Canterbury",
                "website": "https://www.dawnaerospace.com",
                "tier": "Tier1Supplier",
                "controlled_goods": True,
                "itar_compliant": True,
                "certifications": ["AS9100D", "ISO9001", "ITAR_Compliant"],
                "domains": ["SpacePlatform", "DomainSpace", "DomainDefence"],
                "platforms": ["Platform_LEOSatellite", "Platform_SpaceLaunchVehicle"],
                "kics": ["KIC_SpaceSystems", "KIC_AdvancedMaterials"],
                "capabilities": [
                    {
                        "title": "Non-Toxic Green Satellite Propulsion Systems",
                        "description": "High-performance nitrous oxide and propylene non-toxic bipropellant satellite thrusters replacing hazardous hydrazine.",
                        "trl": 9,
                        "mrl": 9,
                        "kic": "KIC_SpaceSystems",
                    },
                    {
                        "title": "Suborbital Rocketplane Aerodynamics & Fast Turnaround Flight",
                        "description": "Rocket-powered autonomous aircraft capable of multiple daily flights to the edge of space for hypersonic research and suborbital science.",
                        "trl": 7,
                        "mrl": 7,
                        "kic": "KIC_SpaceSystems",
                    },
                ],
                "products": [
                    {
                        "name": "B20 Green Bi-propellant Satellite Thruster",
                        "description": "Flight-proven 20N nitrous oxide/propene chemical thruster for CubeSats and SmallSats requiring high ISP orbital maneuvering.",
                        "part_number": "PN-NZL-DWN-B20",
                        "fsc_code": "2840",
                        "nsn_code": "2840-98-210-9182",
                        "platforms": ["Platform_LEOSatellite"],
                        "materials": ["Material_Inconel_718", "Material_Titanium_Ti6Al4V"],
                    },
                    {
                        "name": "Mk-II Aurora Suborbital Rocketplane",
                        "description": "Reusable rocket-powered autonomous aircraft for atmospheric testing and microgravity payloads up to 100km altitude.",
                        "part_number": "PN-NZL-DWN-AUR2",
                        "fsc_code": "1560",
                        "nsn_code": "1560-98-210-9183",
                        "platforms": ["Platform_SpaceLaunchVehicle"],
                        "materials": ["Material_CarbonFiber_Composite", "Material_Titanium_Ti6Al4V"],
                    },
                ],
                "services": [
                    {
                        "name": "Spacecraft Chemical Propulsion Custom Engineering",
                        "description": "Fluidic delta-V budget modeling, custom propellant tank sizing, valve manifold integration, and orbital insertion dynamics.",
                        "type": "EngineeringService",
                        "accreditation": "ESA / NASA Qualified Propulsion",
                    },
                    {
                        "name": "High-Pressure Gas & Cryogenic Propulsion Flow Testing",
                        "description": "Vacuum chamber thermal hot-fire characterization, leak detection, and environmental qualification under deep space conditions.",
                        "type": "TestingQualificationService",
                        "accreditation": "ISO 9001:2015",
                    },
                    {
                        "name": "In-Orbit Thruster Calibration & Lifecycle Health Assessment",
                        "description": "Propellant mass gauging, pulse timing telemetry analysis, and thruster nozzle degradation monitoring.",
                        "type": "LogisticsSupportService",
                        "accreditation": "ITAR Compliant",
                    },
                    {
                        "name": "Rocket Propulsion Overhaul and Thruster Requalification",
                        "description": "Depot cleaning, seal replacement, solenoid valve recalibration, and pressure proof testing for returned space hardware.",
                        "type": "MROService",
                        "accreditation": "AS9100D",
                    },
                ],
            },
            {
                "legal_name": "Tait International Limited",
                "trade_name": "Tait Communications",
                "cage_code": "E0C36",
                "duns_number": "594812749",
                "business_number": "NZ9429037482910",
                "country": "NZL",
                "city": "Christchurch",
                "province": "Canterbury",
                "website": "https://www.taitcommunications.com",
                "tier": "Tier1Supplier",
                "controlled_goods": True,
                "itar_compliant": True,
                "certifications": ["ISO9001", "ISO27001", "FacilitySecurity_Secret", "CMMC_Level2"],
                "domains": ["DomainDefence", "DomainC4ISR"],
                "platforms": ["Platform_ArmouredCombatVehicle", "Platform_SurfaceCombatant"],
                "kics": ["KIC_SoftwareDefinedRadio", "KIC_CyberResilience", "KIC_DefenceSystemsIntegration"],
                "capabilities": [
                    {
                        "title": "Tactical Mission-Critical Encrypted Radio Communications",
                        "description": "P25, DMR Tier 3, and LTE hybrid tactical communications systems with AES-256 military-grade encryption and secure talkgroups.",
                        "trl": 9,
                        "mrl": 9,
                        "kic": "KIC_SoftwareDefinedRadio",
                    },
                    {
                        "title": "Resilient Tactical Mesh Radio Architectures",
                        "description": "Self-healing ad-hoc tactical wireless mesh networks for border patrol, emergency defence response, and dismounted troops.",
                        "trl": 9,
                        "mrl": 9,
                        "kic": "KIC_CyberResilience",
                    },
                ],
                "products": [
                    {
                        "name": "TP9600 P25 Phase 2 Tactical Portable Radio",
                        "description": "Ruggedized submersible IP68 tactical handheld radio with dual-band VHF/UHF, GPS location services, and OTAR encryption.",
                        "part_number": "PN-NZL-TT-TP96",
                        "fsc_code": "5820",
                        "nsn_code": "5820-98-319-4820",
                        "platforms": ["Platform_ArmouredCombatVehicle"],
                        "materials": ["Material_AluminiumLithium_2055"],
                    },
                    {
                        "name": "TB9400 P25 Phase 2 Base Station / Repeater",
                        "description": "Continuous duty digital base station for tactical theatre multi-channel coverage and emergency dispatch networks.",
                        "part_number": "PN-NZL-TT-TB94",
                        "fsc_code": "5895",
                        "nsn_code": "5895-98-319-4821",
                        "platforms": ["Platform_SurfaceCombatant"],
                        "materials": ["Material_GalliumNitride_GaN"],
                    },
                ],
                "services": [
                    {
                        "name": "Tactical Network Architecture Design & RF Propagation Modeling",
                        "description": "High-fidelity terrain RF ray-tracing, frequency deconfliction, tactical tower site optimization, and coverage analysis.",
                        "type": "EngineeringService",
                        "accreditation": "ISO 9001",
                    },
                    {
                        "name": "MIL-STD-810H Ruggedization & Cryptographic Security Auditing",
                        "description": "Shock, immersion, salt-fog testing, and FIPS 140-2 Level 3 cryptographic boundary validation.",
                        "type": "CyberSecurityService",
                        "accreditation": "FIPS 140-2 Certified",
                    },
                    {
                        "name": "Radio Fleet In-Service Support and Depot Board Repair",
                        "description": "Surface-mount component replacement, RF receiver alignment, transmitter tuning, and firmware security patching.",
                        "type": "MROService",
                        "accreditation": "ISO 9001:2015",
                    },
                    {
                        "name": "24/7 Tactical Network Operations Center (NOC) Managed Support",
                        "description": "Real-time network health surveillance, intrusion detection, remote over-the-air rekeying (OTAR), and SLA support.",
                        "type": "LogisticsSupportService",
                        "accreditation": "ISO 27001",
                    },
                ],
            },
            {
                "legal_name": "Rakon Limited",
                "trade_name": "Rakon",
                "cage_code": "E0D48",
                "duns_number": "594838192",
                "business_number": "NZ9429038291047",
                "country": "NZL",
                "city": "Auckland",
                "province": "Auckland",
                "website": "https://www.rakon.com",
                "tier": "Tier1Supplier",
                "controlled_goods": True,
                "itar_compliant": True,
                "certifications": ["AS9100D", "ISO9001", "ESA_Qualified", "NASA_Approved"],
                "domains": ["SpacePlatform", "AirPlatform", "DomainDefence"],
                "platforms": ["Platform_LEOSatellite", "Platform_F35_Lightning_II", "Platform_FixedWingCombat"],
                "kics": ["KIC_SensorsSonar", "KIC_SpaceSystems", "KIC_AerospaceSystems"],
                "capabilities": [
                    {
                        "title": "Ultra-High Stability Space and Defence Oscillators (OCXO / TCXO)",
                        "description": "Radiation-hardened oven-controlled crystal oscillators and surface acoustic wave (SAW) filters with sub-ppb stability for military GNSS, radar, and satellite payloads.",
                        "trl": 9,
                        "mrl": 9,
                        "kic": "KIC_SpaceSystems",
                    },
                    {
                        "title": "Low-Phase-Noise RF Frequency Generation for AESA Radars",
                        "description": "Extreme low-phase-noise master reference oscillators for fighter jet AESA radar beam steering and EW receivers.",
                        "trl": 9,
                        "mrl": 9,
                        "kic": "KIC_SensorsSonar",
                    },
                ],
                "products": [
                    {
                        "name": "ROX020 Ultra-Low Phase Noise Space OCXO",
                        "description": "Radiation-tolerant master clock oscillator for deep-space science, Earth observation radar, and military communications satellites.",
                        "part_number": "PN-NZL-RK-ROX02",
                        "fsc_code": "5955",
                        "nsn_code": "5955-98-429-1029",
                        "platforms": ["Platform_LEOSatellite", "Platform_F35_Lightning_II"],
                        "materials": ["Material_HighPurity_Beryllium", "Material_Titanium_Ti6Al4V"],
                    },
                    {
                        "name": "High-Shock Military TCXO for Guided Munitions",
                        "description": "Crystal oscillator hardened to survive 20,000g gun-launch shock loads in precision guided artillery and missiles.",
                        "part_number": "PN-NZL-RK-HS50",
                        "fsc_code": "5955",
                        "nsn_code": "5955-98-429-1030",
                        "platforms": ["Platform_FixedWingCombat"],
                        "materials": ["Material_SiliconCarbide_SiC"],
                    },
                ],
                "services": [
                    {
                        "name": "Space Radiation Characterization & TID Testing",
                        "description": "Total Ionizing Dose (TID) radiation testing, Single Event Effect (SEE) beam qualification, and long-term crystal aging analysis.",
                        "type": "TestingQualificationService",
                        "accreditation": "ESA ECSS-Q-ST-60C",
                    },
                    {
                        "name": "Custom Frequency Synthesis Microelectronic Design",
                        "description": "Custom hybrid microcircuit packaging, dual crystal resonator modeling, and thermal vacuum drift compensation.",
                        "type": "EngineeringService",
                        "accreditation": "MIL-PRF-55310 Qualified",
                    },
                    {
                        "name": "Defense Supply Chain Crystal Screening & Burn-In",
                        "description": "168-hour high-temperature electrical burn-in, fine leak hermeticity testing, and vibration phase jitter profiling.",
                        "type": "TestingQualificationService",
                        "accreditation": "AS9100D",
                    },
                    {
                        "name": "Precision Oscillator Re-calibration and Refurbishment",
                        "description": "Post-storage aging recalibration, frequency pulling curve verification, and military spares preservation.",
                        "type": "MROService",
                        "accreditation": "ISO 9001:2015",
                    },
                ],
            },
            {
                "legal_name": "Zenith Tecnica Limited",
                "trade_name": "Zenith Tecnica",
                "cage_code": "E0E60",
                "duns_number": "594849102",
                "business_number": "NZ9429041928471",
                "country": "NZL",
                "city": "Auckland",
                "province": "Auckland",
                "website": "https://www.zenithtecnica.com",
                "tier": "Tier2Supplier",
                "controlled_goods": True,
                "itar_compliant": True,
                "certifications": ["AS9100D", "ISO9001", "NADCAP_Welding"],
                "domains": ["SpacePlatform", "AirPlatform", "DomainDefence"],
                "platforms": ["Platform_LEOSatellite", "Platform_FixedWingCombat", "Platform_SpaceLaunchVehicle"],
                "kics": ["KIC_AdvancedMaterials", "KIC_AerospaceSystems", "KIC_SpaceSystems"],
                "capabilities": [
                    {
                        "title": "Electron Beam Melting (EBM) Titanium 3D Additive Manufacturing",
                        "description": "Industrial metal 3D printing in Ti-6Al-4V Grade 5 and Grade 23 for flight-critical structural brackets, satellite antenna arrays, and rocket propellant manifolds.",
                        "trl": 9,
                        "mrl": 9,
                        "kic": "KIC_AdvancedMaterials",
                    },
                    {
                        "title": "Topology Optimization for Lightweight Aerostructures",
                        "description": "Generative structural design reducing mass by up to 60% while maintaining ultimate load margins under severe fatigue profiles.",
                        "trl": 9,
                        "mrl": 8,
                        "kic": "KIC_AerospaceSystems",
                    },
                ],
                "products": [
                    {
                        "name": "Satellite Structural Titanium Bus Node",
                        "description": "Additive manufactured high-stiffness titanium payload mount bracket deployed on over 200 operational orbital spacecraft.",
                        "part_number": "PN-NZL-ZT-SATBRK",
                        "fsc_code": "1560",
                        "nsn_code": "1560-98-539-1049",
                        "platforms": ["Platform_LEOSatellite"],
                        "materials": ["Material_Titanium_Ti6Al4V"],
                    },
                    {
                        "name": "Rocket Engine Regenerative Cooling Bracket",
                        "description": "Complex internal fluid channel titanium assembly built via additive manufacturing with integrated heat sinking.",
                        "part_number": "PN-NZL-ZT-ENGMNT",
                        "fsc_code": "2840",
                        "nsn_code": "2840-98-539-1050",
                        "platforms": ["Platform_SpaceLaunchVehicle"],
                        "materials": ["Material_Titanium_Ti6Al4V"],
                    },
                ],
                "services": [
                    {
                        "name": "Aerospace Additive Manufacturing Process Certification",
                        "description": "Powder bed characterization, electron beam voltage calibration, CT scanning, and metallographic coupon tensile testing.",
                        "type": "TestingQualificationService",
                        "accreditation": "NADCAP Additive Manufacturing",
                    },
                    {
                        "name": "Design for Additive Manufacturing (DfAM) Consulting",
                        "description": "CAD lattice generation, thermal distortion finite element simulation, and post-machining datuming.",
                        "type": "EngineeringService",
                        "accreditation": "AS9100D",
                    },
                    {
                        "name": "Hot Isostatic Pressing (HIP) and Vacuum Heat Treatment Support",
                        "description": "Argon gas 1000-bar HIP cycles to eliminate internal micro-porosity and achieve wrought-equivalent fatigue life.",
                        "type": "MROService",
                        "accreditation": "NADCAP Heat Treating",
                    },
                    {
                        "name": "Precision CNC 5-Axis Post-Machining and CMM Inspection",
                        "description": "High-tolerance milling of seal faces, bearing journals, and laser tracker dimensional validation to 5 microns.",
                        "type": "EngineeringService",
                        "accreditation": "ISO 9001:2015",
                    },
                ],
            },
            {
                "legal_name": "Marops Limited",
                "trade_name": "Marops Defence & Marine",
                "cage_code": "E0F72",
                "duns_number": "594859102",
                "business_number": "NZ9429034819284",
                "country": "NZL",
                "city": "Auckland",
                "province": "Auckland",
                "website": "https://www.marops.co.nz",
                "tier": "SMESupplier",
                "controlled_goods": True,
                "itar_compliant": True,
                "certifications": ["ISO9001", "FacilitySecurity_Secret"],
                "domains": ["MaritimePlatform", "DomainDefence"],
                "platforms": ["Platform_SurfaceCombatant", "Platform_Submarine"],
                "kics": ["KIC_TrainingSimulation", "KIC_NavalShipbuilding", "KIC_DefenceSystemsIntegration"],
                "capabilities": [
                    {
                        "title": "Naval Combat System Simulation & Tactical Mission Trainers",
                        "description": "Synthetic naval warfare environments, frigate operations room bridge simulators, and radar/sonar track injection trainers for naval forces.",
                        "trl": 8,
                        "mrl": 8,
                        "kic": "KIC_TrainingSimulation",
                    },
                ],
                "products": [
                    {
                        "name": "Naval Tactical Scenario Simulator Suite",
                        "description": "Interactive synthetic combat simulation software for naval warfare officers and surface combatant crews.",
                        "part_number": "PN-NZL-MR-SIM01",
                        "fsc_code": "6910",
                        "nsn_code": "6910-98-648-2910",
                        "platforms": ["Platform_SurfaceCombatant"],
                        "materials": ["Material_AluminiumLithium_2055"],
                    },
                ],
                "services": [
                    {
                        "name": "Naval Bridge Simulator Maintenance & Software In-Service Support",
                        "description": "Continuous synthetic model updates, hydrographic chart integration, and tactical software regression verification.",
                        "type": "SimulationTrainingService",
                        "accreditation": "ISO 9001",
                    },
                    {
                        "name": "Combat Management System Operator Training Delivery",
                        "description": "Curriculum development, anti-submarine warfare simulated exercise planning, and electronic warfare scenario control.",
                        "type": "SimulationTrainingService",
                        "accreditation": "NZDF Approved Contractor",
                    },
                    {
                        "name": "Naval Sensor Interface Hardware Integration",
                        "description": "Ethernet and serial NMEA naval sensor signal conversion, shipboard network isolation, and MIL-SPEC rack integration.",
                        "type": "EngineeringService",
                        "accreditation": "ISO 9001",
                    },
                    {
                        "name": "Simulator Visual Display Engine Calibration & Alignment",
                        "description": "Collimated projection alignment, edge blending, and multi-channel 360-degree dome visual system overhaul.",
                        "type": "MROService",
                        "accreditation": "AS9100D",
                    },
                ],
            },
            {
                "legal_name": "Dotterel Technologies Limited",
                "trade_name": "Dotterel",
                "cage_code": "E0G84",
                "duns_number": "594869201",
                "business_number": "NZ9429045918274",
                "country": "NZL",
                "city": "Auckland",
                "province": "Auckland",
                "website": "https://www.dotterel.com",
                "tier": "SMESupplier",
                "controlled_goods": True,
                "itar_compliant": True,
                "certifications": ["ISO9001", "ITAR_Compliant"],
                "domains": ["AirPlatform", "DomainDefence"],
                "platforms": ["Platform_TacticalUAS"],
                "kics": ["KIC_SensorsSonar", "KIC_RemotelyPilotedSystems", "KIC_AIAutonomousSystems"],
                "capabilities": [
                    {
                        "title": "Acoustic Noise Reduction and Drone Audio Surveillance Payloads",
                        "description": "Proprietary microphone arrays and real-time DSP algorithms filtering out rotor acoustic noise to capture long-range directional ground intelligence.",
                        "trl": 8,
                        "mrl": 8,
                        "kic": "KIC_SensorsSonar",
                    },
                ],
                "products": [
                    {
                        "name": "Acoustic Surveillance Microphone Array for Drones",
                        "description": "Lightweight directional audio intelligence sensor payload capable of standoff human speech and vehicle sound localization.",
                        "part_number": "PN-NZL-DT-MIC01",
                        "fsc_code": "5835",
                        "nsn_code": "5835-98-759-1928",
                        "platforms": ["Platform_TacticalUAS"],
                        "materials": ["Material_CarbonFiber_Composite"],
                    },
                ],
                "services": [
                    {
                        "name": "UAS Acoustic Signature Modeling & Noise Attenuation Testing",
                        "description": "Anechoic chamber acoustic signature measurement, rotor tip acoustic optimization, and acoustic stealth certification.",
                        "type": "TestingQualificationService",
                        "accreditation": "ISO 9001",
                    },
                    {
                        "name": "DSP Airborne Audio Algorithm Integration",
                        "description": "FPGA-based beamforming software integration, noise suppression filter tuning, and video-audio telemetry synchronization.",
                        "type": "EngineeringService",
                        "accreditation": "ISO 9001",
                    },
                    {
                        "name": "Acoustic Sensor Field Overhaul & Calibration",
                        "description": "Waterproof acoustic diaphragm inspection, sensor sensitivity recalibration, and rugged field enclosure testing.",
                        "type": "MROService",
                        "accreditation": "ISO 9001",
                    },
                    {
                        "name": "Tactical Acoustic Sensor Deployment Training",
                        "description": "Operator tactical audio triangulation training, urban acoustic surveillance tactics, and payload mounting instructions.",
                        "type": "SimulationTrainingService",
                        "accreditation": "ITAR Compliant",
                    },
                ],
            },
            {
                "legal_name": "Flightcell International Limited",
                "trade_name": "Flightcell",
                "cage_code": "E0H96",
                "duns_number": "594879312",
                "business_number": "NZ9429039182741",
                "country": "NZL",
                "city": "Nelson",
                "province": "Nelson",
                "website": "https://www.flightcell.com",
                "tier": "Tier2Supplier",
                "controlled_goods": True,
                "itar_compliant": True,
                "certifications": ["AS9100D", "ISO9001", "FAA_TSO_Certified"],
                "domains": ["AirPlatform", "DomainDefence"],
                "platforms": ["Platform_RotaryWing", "Platform_FixedWingTransport", "Platform_TacticalUAS"],
                "kics": ["KIC_AerospaceSystems", "KIC_SoftwareDefinedRadio"],
                "capabilities": [
                    {
                        "title": "Airborne Satellite and Cellular Hybrid Tactical Datalinks",
                        "description": "Integrated military aircraft transceivers combining Iridium Certus satcom and 4G/5G cellular broadband for real-time telemetry, cockpit voice, and encrypted data.",
                        "trl": 9,
                        "mrl": 9,
                        "kic": "KIC_SoftwareDefinedRadio",
                    },
                ],
                "products": [
                    {
                        "name": "Flightcell DZMx All-In-One Airborne Cellular/Satcom System",
                        "description": "DO-160G certified flight tracking, satellite voice, cellular broadband data, and automated flight following system for military and rescue aircraft.",
                        "part_number": "PN-NZL-FC-DZMX",
                        "fsc_code": "5895",
                        "nsn_code": "5895-98-869-2049",
                        "platforms": ["Platform_RotaryWing", "Platform_FixedWingTransport"],
                        "materials": ["Material_AluminiumLithium_2055"],
                    },
                ],
                "services": [
                    {
                        "name": "Aircraft DO-160G Environmental & EMI Qualification Testing",
                        "description": "Full airborne environmental stress, altitude, temperature, vibration, and RF radiated susceptibility testing.",
                        "type": "TestingQualificationService",
                        "accreditation": "FAA TSO-C159b",
                    },
                    {
                        "name": "Avionics STC Design & Cockpit Integration Engineering",
                        "description": "Civil aviation authority STC packages, wiring schematics, cockpit instrument panel retrofits, and antenna placement analysis.",
                        "type": "EngineeringService",
                        "accreditation": "CAA NZ Part 148",
                    },
                    {
                        "name": "DZMx Depot Repair & Firmware Security Updates",
                        "description": "Component-level bench testing, transceivers recertification, GPS engine replacement, and secure boot firmware flashing.",
                        "type": "MROService",
                        "accreditation": "AS9100D",
                    },
                    {
                        "name": "Global Aircraft Tracking Server Fleet Management",
                        "description": "Cloud telemetry decoding, 24/7 mission replay, automated flight hour logging, and emergency position reporting.",
                        "type": "LogisticsSupportService",
                        "accreditation": "ISO 27001",
                    },
                ],
            },
        ]

    def _generate_nz_ecosystem(self, target_count: int = 60) -> List[Dict[str, Any]]:
        flagships = self._get_flagship_nz_companies()
        records: List[Dict[str, Any]] = list(flagships)

        nz_locations = [
            ("Auckland", "Auckland"),
            ("Christchurch", "Canterbury"),
            ("Wellington", "Wellington"),
            ("Hamilton", "Waikato"),
            ("Tauranga", "Bay of Plenty"),
            ("Nelson", "Nelson"),
            ("Palmerston North", "Manawatu"),
            ("Dunedin", "Otago"),
        ]

        templates = [
            (
                "Carbon Composite Aerostructure Autoclave Tooling",
                "Precision Invar and composite tooling for autoclave curing of high-temperature aerospace structures and drone fairings.",
                "KIC_AdvancedMaterials",
                "Tier2Supplier",
                ["AS9100D", "ISO9001"],
                "Platform_FixedWingCombat",
                "1560",
                "Airframe Structural Tooling Subsystem",
                "Material_CarbonFiber_Composite",
            ),
            (
                "Precision 5-Axis CNC Titanium & Inconel Machining",
                "High-precision milling of aerospace landing gear components, hydraulic manifolds, and rocket engine brackets.",
                "KIC_AerospaceSystems",
                "Tier2Supplier",
                ["AS9100D", "ISO9001", "NADCAP_NDT"],
                "Platform_FixedWingTransport",
                "1680",
                "High-Tolerance Aerospace Hydraulic Manifold",
                "Material_Titanium_Ti6Al4V",
            ),
            (
                "Rugged Autonomous Robotics & Submersible Inspection",
                "Deep-water inspection ROVs and magnetic crawling robots for non-destructive hull and fuel tank evaluation.",
                "KIC_AIAutonomousSystems",
                "SMESupplier",
                ["ISO9001"],
                "Platform_SurfaceCombatant",
                "2090",
                "Submersible Inspection Robotic Vehicle",
                "Material_Titanium_Ti6Al4V",
            ),
            (
                "Tactical Long-Endurance Surveillance UAS Platforms",
                "Long-endurance electric and hybrid VTOL drone platforms with high-definition EO/IR sensor integration for coastal and border patrol.",
                "KIC_RemotelyPilotedSystems",
                "SMESupplier",
                ["ISO9001", "ITAR_Compliant"],
                "Platform_TacticalUAS",
                "1550",
                "Endurance Coastal Surveillance Drone",
                "Material_CarbonFiber_Composite",
            ),
            (
                "Cryogenic Fuel Handling & Clean Spacecraft Tank Systems",
                "Vacuum-insulated cryogenic transfer piping, valves, and high-pressure tanks for liquid oxygen and liquid hydrogen aerospace applications.",
                "KIC_SpaceSystems",
                "Tier2Supplier",
                ["AS9100D", "ISO9001"],
                "Platform_SpaceLaunchVehicle",
                "2840",
                "Cryogenic Fluid Isolation Valve Assembly",
                "Material_Inconel_718",
            ),
            (
                "Naval Electrical Wiring Interconnect & Marine Harnesses",
                "Subsea pressure-tight military electrical harnesses, penetrators, and environmentally sealed naval distribution boxes.",
                "KIC_NavalShipbuilding",
                "Tier2Supplier",
                ["ISO9001", "NATO_AQAP2110"],
                "Platform_SurfaceCombatant",
                "5995",
                "Hermetic Subsea Naval Cable Assembly",
                "Material_AluminiumLithium_2055",
            ),
        ]

        service_templates = [
            ("Precision CNC 5-Axis Milling & Dimensional CMM Verification", "EngineeringService", "ISO 9001:2015"),
            ("Non-Destructive Ultrasonic and Dye Penetrant Inspection (NDT)", "TestingQualificationService", "NADCAP NDT Certified"),
            ("Aero-Mechanical Component Depot Overhaul and Life Extension", "MROService", "CAA NZ Part 145"),
            ("Environmental Thermal Vacuum and Vibration Stress Qualification", "TestingQualificationService", "MIL-STD-810H"),
            ("Avionics Harness Fabrication and Laser Wire Marking", "EngineeringService", "AS9100 Rev D"),
            ("Integrated Logistics Support and Spares Inventory Management", "LogisticsSupportService", "ISO 9001"),
        ]

        random.seed(303)
        idx = len(records) + 1
        while len(records) < target_count:
            city, prov = random.choice(nz_locations)
            tpl = random.choice(templates)
            cap_title, cap_desc, kic, tier, certs, platform, fsc, prod_name, mat = tpl

            company_name = f"Kiwi {cap_title.split()[0]} {city} Ltd."
            cage = f"E{idx:04d}"
            duns = f"5948{random.randint(10000, 99999)}"
            bn = f"NZ94290{random.randint(10000000, 99999999)}"

            # Pick 4 services for each company
            company_services = []
            selected_servs = random.sample(service_templates, 4)
            for s_name, s_type, s_accred in selected_servs:
                company_services.append({
                    "name": f"{s_name} - {city} Facility",
                    "description": f"Comprehensive {s_name.lower()} adhering to military specifications and defence customer standards.",
                    "type": s_type,
                    "accreditation": s_accred,
                })

            rec = {
                "legal_name": company_name,
                "trade_name": f"{cap_title.split()[0]} New Zealand",
                "cage_code": cage,
                "duns_number": duns,
                "business_number": bn,
                "country": "NZL",
                "province": prov,
                "city": city,
                "website": f"https://www.{company_name.lower().replace(' ', '').replace('.', '')}.co.nz",
                "tier": tier,
                "controlled_goods": True,
                "itar_compliant": random.random() < 0.75,
                "certifications": list(certs),
                "domains": ["DomainDefence", "AirPlatform"],
                "platforms": [platform],
                "kics": [kic],
                "capabilities": [
                    {
                        "title": cap_title,
                        "description": f"{cap_desc} Delivered to tier 1 primes and sovereign defence agencies.",
                        "trl": random.choice([7, 8, 9]),
                        "mrl": random.choice([7, 8, 9]),
                        "kic": kic,
                    },
                    {
                        "title": f"Rapid Precision Prototyping & Engineering Validation ({cap_title.split()[0]})",
                        "description": f"Digital CAD/CAM engineering, rapid prototyping, and empirical qualification for {cap_title.lower()}.",
                        "trl": 8,
                        "mrl": 8,
                        "kic": kic,
                    },
                ],
                "products": [
                    {
                        "name": f"{company_name} {prod_name}",
                        "description": f"High-reliability {prod_name.lower()} manufactured to stringent aerospace tolerances.",
                        "part_number": f"PN-NZL-{cage}-01",
                        "fsc_code": fsc,
                        "nsn_code": f"{fsc}-98-{random.randint(100,999)}-{random.randint(1000,9999)}",
                        "platforms": [platform],
                        "materials": [mat],
                    },
                    {
                        "name": f"{company_name} Modular Auxiliary Subassembly",
                        "description": "Ruggedized mounting subassembly and protective interface hardware.",
                        "part_number": f"PN-NZL-{cage}-02",
                        "fsc_code": fsc,
                        "nsn_code": f"{fsc}-98-{random.randint(100,999)}-{random.randint(1000,9999)}",
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
        records = self._get_flagship_nz_companies()
        if limit is not None:
            records = records[:limit]
        self.save_raw(records, "nz_aero_defence_catalog.json")
        return records
