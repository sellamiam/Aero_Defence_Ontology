# US Aerospace & Defence Supplier Dataset Schema Specification

Every worker agent must write a valid JSON array (`List[Dict[str, Any]]`) to its assigned path in `data/raw/us_sectors/<sector>.json`.

## Strict Rules
1. **REAL US COMPANIES ONLY**: Every single entry MUST be a real, existing US Aerospace & Defence enterprise (Prime, Tier-1, Tier-2, SME, Foundry, MRO, Defense-Tech, Space, Maritime, Munitions, etc.) verified via `search_web`. Do NOT invent placeholder or template names.
2. **US Headquarters / Operations**: `country` MUST be `"USA"`. `city` MUST be the real HQ city (e.g., `"Bethesda"`). `province` MUST be the 2-letter US State abbreviation (e.g., `"MD"`, `"VA"`, `"CA"`, `"TX"`, `"AL"`, `"WA"`, `"AZ"`, `"FL"`, `"CT"`, `"OH"`, `"KS"`, `"MA"`, `"CO"`, `"PA"`, `"NJ"`, `"NY"`, `"NC"`, `"GA"`, `"MO"`, `"UT"`, `"MI"`, `"IN"`, `"TN"`, `"MN"`, `"NH"`).
3. **Valid JSON Object Schema** (every record MUST include all of these keys):
```json
{
  "legal_name": "Official Legal Name Inc.",
  "trade_name": "Common Trade Name",
  "cage_code": "64677 or null if unverified (Orchestrator assigns USxxxx ID)",
  "country": "USA",
  "city": "City Name",
  "province": "ST",
  "website": "https://www.example.com",
  "tier": "Prime | Tier1Supplier | Tier2Supplier | SMESupplier",
  "controlled_goods": false,
  "itar_compliant": true,
  "facility_security_clearance": "Top Secret / SCI | Secret | Confidential | Unclassified / ITAR",
  "certifications": ["AS9100D", "ISO9001", "ITAR_Compliant"],
  "domains": ["AirPlatform", "DomainDefence", "DomainAeronautics"],
  "platforms": ["Platform_F35_Lightning_II"],
  "kics": ["KIC_AerospaceSystems", "KIC_DefenceSystemsIntegration"],
  "capabilities": [
    {
      "title": "Specific verified industrial or technical capability",
      "description": "Concrete technical description of products/processes/systems built by this company.",
      "trl": 9,
      "mrl": 9,
      "kic": "KIC_AerospaceSystems"
    }
  ],
  "products": [
    {
      "name": "Verified product/system/component line",
      "description": "Technical description of the product.",
      "part_number": "PN-USA-... or real model designation",
      "fsc_code": "1560",
      "nsn_code": null,
      "platforms": ["Platform_F35_Lightning_II"],
      "materials": ["Material_Titanium_Ti6Al4V"]
    }
  ],
  "services": [
    {
      "name": "Verified service offering",
      "description": "Technical description of engineering, MRO, testing, logistics, or cyber service.",
      "type": "MROService | EngineeringService | TestingQualificationService | SimulationTrainingService | LogisticsSupportService | CyberSecurityService",
      "accreditation": "FAA Part 145 | NADCAP | AS9100D | ISO/IEC 17025 | DCMA"
    }
  ],
  "parent_company": null,
  "supplies_to": ["Lockheed Martin Corporation", "The Boeing Company"],
  "source_note": "Brief source/verification note from search_web (e.g. AIA member / Defense News Top 100 / company website)"
}
```

## Allowed Taxonomy Values (MUST match ontology exactly)

### `tier` (exact strings)
- `"Prime"`
- `"Tier1Supplier"`
- `"Tier2Supplier"`
- `"SMESupplier"`

### `domains` (valid subset)
- `"AirPlatform"`, `"UASPlatform"`, `"SpacePlatform"`, `"LandPlatform"`, `"MaritimePlatform"`
- `"DomainDefence"`, `"DomainAeronautics"`, `"DomainSpace"`, `"DomainC4ISR"`

### `kics` & `capability.kic` (exact keys — map US capabilities cleanly to these ontology KICs)
- `"KIC_AdvancedMaterials"` (Composites, Ti/Al/Inconel/superalloys, forgings, castings, ceramics, metals)
- `"KIC_AerospaceSystems"` (Airframes, aerostructures, propulsion, landing gear, actuation, ECS, fuel systems)
- `"KIC_AIAutonomousSystems"` (Autonomy software, swarming, edge AI, mission autonomy, UGV/USV/UAS AI)
- `"KIC_ArmouredVehicles"` (Combat/tactical vehicles, hulls, armor, drivetrains, suspensions)
- `"KIC_CBRNDefence"` (CBRN detection, filtration, decon, protective gear)
- `"KIC_CyberResilience"` (Zero-trust, cryptography, CMMC/RMF, TEMPEST, electronic cyber warfare)
- `"KIC_DefenceSystemsIntegration"` (Prime system integration, C2, missile defense integration, weapons systems)
- `"KIC_EOIRSystems"` (Electro-optical, FLIR, IRST, laser designators, space optics, NVGs)
- `"KIC_InServiceSupport"` (Depot MRO, sustainment, PBL, aircraft/ship/vehicle overhaul & upgrades)
- `"KIC_Munitions"` (Missiles, hypersonics, energetics, propellants, fuzing, warheads, ammunition)
- `"KIC_NavalShipbuilding"` (Warships, submarines, naval reactors, marine propulsion, sonar/undersea)
- `"KIC_RemotelyPilotedSystems"` (Drones, UAVs, loitering munitions, ground control stations, counter-UAS)
- `"KIC_SensorsSonar"` (AESA radar, sonar, EW, SIGINT, avionics, GaN RF, inertial navigation, timing)
- `"KIC_SoftwareDefinedRadio"` (Tactical radios, Link 16, SATCOM terminals, datalinks, mesh networking)
- `"KIC_SpaceSystems"` (Launch vehicles, satellites, orbital buses, rocket engines, star trackers, ground segment)
- `"KIC_TrainingSimulation"` (Simulators, LVC training, digital twins, combat mission simulators)

### `certifications` (omit `"Cert_"` prefix! Extractor prepends `"Cert_"` automatically)
Allowed values (use exact tokens):
- `"AS9100D"`, `"ISO9001"`, `"ISO14001"`, `"ISO27001"`
- `"NADCAP_Composites"`, `"NADCAP_NDT"`, `"NADCAP_Chemical"`, `"NADCAP_HeatTreating"`, `"NADCAP_Welding"`
- `"ITAR_Compliant"`, `"NATO_AQAP2110"`, `"CMMC_Level2"`
- `"FacilitySecurity_Secret"`, `"FacilitySecurity_TopSecret"`
- New US standards to be added to `standards.ttl` by Orchestrator: `"AS9110C"`, `"AS9120B"`, `"CMMC_Level3"`, `"FAA_Part145"`, `"DFARS_NIST800171"`

### `platforms` (existing + US platforms to be added to `platforms.ttl` by Orchestrator)
Existing:
- `"Platform_FixedWingCombat"`, `"Platform_FixedWingTransport"`, `"Platform_RotaryWing"`, `"Platform_TacticalUAS"`, `"Platform_LEOSatellite"`, `"Platform_ArmouredCombatVehicle"`, `"Platform_SurfaceCombatant"`, `"Platform_Submarine"`, `"Platform_F35_Lightning_II"`, `"Platform_Type26_GlobalCombatShip"`, `"Platform_P8_Poseidon"`, `"Platform_MQ9B_SkyGuardian"`, `"Platform_C130J_SuperHercules"`, `"Platform_SpaceLaunchVehicle"`
New US platforms (to add to `platforms.ttl`):
- `"Platform_B21_Raider"`, `"Platform_F22_Raptor"`, `"Platform_F15EX_EagleII"`, `"Platform_FA18_SuperHornet"`, `"Platform_KC46_Pegasus"`, `"Platform_CH53K_KingStallion"`, `"Platform_UH60_BlackHawk"`, `"Platform_AH64_Apache"`, `"Platform_V22_Osprey"`, `"Platform_DDG51_ArleighBurke"`, `"Platform_ColumbiaClass_Submarine"`, `"Platform_VirginiaClass_Submarine"`, `"Platform_FordClass_Carrier"`, `"Platform_M1A2_Abrams"`, `"Platform_M2_Bradley"`, `"Platform_Stryker_ICV"`, `"Platform_JLTV"`, `"Platform_Patriot_PAC3"`, `"Platform_THAAD"`, `"Platform_Falcon9_Heavy"`

### `materials` (omit `"Material_"` prefix? NO! `materials` MUST KEEP `"Material_"` prefix in JSON because `extractor.py` does `https://w3id.org/aerospace-defence#{mat}`)
Allowed values:
- `"Material_Titanium_Ti6Al4V"`, `"Material_Inconel_718"`, `"Material_CarbonFiber_Composite"`, `"Material_GalliumNitride_GaN"`, `"Material_SiliconCarbide_SiC"`, `"Material_SingleCrystal_Superalloy"`, `"Material_Kevlar_Aramid"`
New materials (Orchestrator will add to `standards.ttl`):
- `"Material_AluminiumLithium_2055"`, `"Material_Beryllium_Optical"`, `"Material_Rhenium_Refractory"`, `"Material_Tungsten_HeavyAlloy"`, `"Material_RareEarth_Neodymium"`

### `service.type` (exact strings)
- `"MROService"`, `"EngineeringService"`, `"TestingQualificationService"`, `"SimulationTrainingService"`, `"LogisticsSupportService"`, `"CyberSecurityService"`
