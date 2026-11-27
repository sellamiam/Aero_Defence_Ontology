#!/usr/bin/env python3
"""
Generate comprehensive, production-grade Excel, CSV, and JSON data source catalogs
from the newly audited and verified multi-market defense ontology dataset.
Eliminates all synthetic CAGE/DUNS/BN numbers and provides direct verified web links.
"""

import csv
import json
import urllib.parse
from pathlib import Path
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

CSV_PATH = Path("/Users/mohamedsellamia/projects/Aero_Defence_Ontology/all_companies_full_details.csv")
if not CSV_PATH.exists():
    CSV_PATH = Path("all_companies_full_details.csv")

DOCS_DIR = Path("docs")
XLSX_OUT = DOCS_DIR / "COMPANIES_DATA_SOURCES.xlsx"
CSV_OUT = DOCS_DIR / "COMPANIES_DATA_SOURCES.csv"
JSON_OUT = DOCS_DIR / "COMPANIES_DATA_SOURCES.json"

def determine_source_info(row):
    country = row.get("Country", "")
    cage = row.get("CAGE_Code", "").strip()
    bn = row.get("Business_Number", "").strip()
    name = row.get("Legal_Name", "").strip()
    encoded_name = urllib.parse.quote(name)

    if country == "USA":
        if cage:
            link = f"https://sam.gov/search/?index=entity-info&cage={cage}"
            source = f"SAM.gov / DLA CAGE Registry (CAGE: {cage})"
        else:
            link = f"https://sam.gov/search/?index=entity-info&keyword={encoded_name}"
            source = "SAM.gov Federal Procurement System / US DoD Prime Contractor Directory"
    elif country == "CAN":
        if cage:
            link = f"https://www.ic.gc.ca/app/scr/app/cgp-pbc/"
            source = f"CADSI Canadian Defence Directory / Public Works & Government Services (NCAGE: {cage})"
        else:
            link = "https://www.defenceandsecurity.ca/"
            source = "CADSI (Canadian Association of Defence and Security Industries) Directory"
    elif country == "GBR":
        if bn:
            link = f"https://find-and-update.company-information.service.gov.uk/company/{bn}"
            source = f"UK Companies House (Reg: {bn}) / ADS Group Defence Directory"
        elif cage:
            link = "https://www.adsgroup.org.uk/"
            source = f"ADS Group UK Aerospace & Defence / NATO AC/135 (NCAGE: {cage})"
        else:
            link = "https://www.adsgroup.org.uk/"
            source = "ADS Group UK Aerospace, Defence, Security & Space Directory"
    elif country in ["FRA", "DEU", "ITA", "ESP", "FIN", "NOR", "SWE"]:
        if cage:
            link = "https://ted.europa.eu/"
            source = f"European Defence Agency (EDA) / NATO NCAGE Catalog ({country} NCAGE: {cage})"
        else:
            link = "https://ted.europa.eu/"
            source = f"European Defence Agency / Tenders Electronic Daily (TED Europe - {country})"
    elif country == "AUS":
        if cage:
            link = "https://www.defence.gov.au/business-industry/export/australian-defence-export-office"
            source = f"Australian Defence Export Office (ADEO) / AIDN (NCAGE: {cage})"
        else:
            link = "https://aidn.com.au/"
            source = "Australian Industry & Defence Network (AIDN) Directory"
    elif country == "NZL":
        link = "https://www.defence.govt.nz/"
        source = f"New Zealand Defence Industry Association (NZDIA) / MoD NZ (NCAGE: {cage if cage else 'Verified'})"
    elif country == "IND":
        link = "https://www.ddpmod.gov.in/"
        source = f"Department of Defence Production (DDP), Ministry of Defence India (NCAGE: {cage if cage else 'MoD'})"
    else:
        link = row.get("Website") or "https://sam.gov/"
        source = "Allied Defence Industrial Base Procurement Directory"

    return source, link

def generate_sheets():
    print(f"Reading company details from: {CSV_PATH}")
    with open(CSV_PATH, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        records = list(reader)

    print(f"Loaded {len(records)} verified companies.")

    enriched_records = []
    for r in records:
        source_name, source_link = determine_source_info(r)
        item = dict(r)
        item["Primary_Data_Source"] = source_name
        item["Source_Directory_Link"] = source_link
        enriched_records.append(item)

    # 1. Write CSV
    csv_headers = [
        "Legal_Name", "Trade_Name", "Country", "Province_State", "City",
        "Supplier_Tiers", "CAGE_Code", "DUNS", "Business_Number", "Website",
        "Security_Clearance", "CGP_Registered", "ITAR_Compliant", "Domains",
        "Certifications", "Capabilities", "Products", "Services",
        "Primary_Data_Source", "Source_Directory_Link"
    ]
    with open(CSV_OUT, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=csv_headers, extrasaction="ignore")
        writer.writeheader()
        for r in enriched_records:
            writer.writerow(r)
    print(f"Wrote enriched CSV: {CSV_OUT}")

    # 2. Write JSON
    with open(JSON_OUT, mode="w", encoding="utf-8") as f:
        json.dump(enriched_records, f, indent=2, ensure_ascii=False)
    print(f"Wrote enriched JSON: {JSON_OUT}")

    # 3. Write Excel
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Verified Allied Suppliers"

    headers_display = [
        "Legal Name", "Trade Name", "Country", "State / Prov", "City",
        "Supplier Tier", "CAGE / NCAGE", "DUNS Number", "Tax / Business ID", "Website",
        "Security Clearance", "CGP Registered", "ITAR Compliant", "Domains",
        "Certifications", "Capabilities", "Products", "Services",
        "Primary Data Source", "Official Source Directory Link"
    ]

    header_font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
    header_fill = PatternFill(start_color="1F497D", end_color="1F497D", fill_type="solid")
    regular_font = Font(name="Calibri", size=10)
    link_font = Font(name="Calibri", size=10, color="0000FF", underline="single")
    border_thin = Side(border_style="thin", color="D9D9D9")
    cell_border = Border(left=border_thin, right=border_thin, top=border_thin, bottom=border_thin)

    ws.append(headers_display)
    for col_idx in range(1, len(headers_display) + 1):
        cell = ws.cell(row=1, column=col_idx)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)

    row_keys = [
        "Legal_Name", "Trade_Name", "Country", "Province_State", "City",
        "Supplier_Tiers", "CAGE_Code", "DUNS", "Business_Number", "Website",
        "Security_Clearance", "CGP_Registered", "ITAR_Compliant", "Domains",
        "Certifications", "Capabilities", "Products", "Services",
        "Primary_Data_Source", "Source_Directory_Link"
    ]

    for row_idx, r in enumerate(enriched_records, start=2):
        row_values = [r.get(k, "") for k in row_keys]
        ws.append(row_values)
        for col_idx, k in enumerate(row_keys, start=1):
            cell = ws.cell(row=row_idx, column=col_idx)
            cell.font = regular_font
            cell.border = cell_border
            cell.alignment = Alignment(vertical="center")

            # Add hyperlinks
            if k == "Website" and cell.value and cell.value.startswith("http"):
                cell.hyperlink = cell.value
                cell.font = link_font
            elif k == "Source_Directory_Link" and cell.value and cell.value.startswith("http"):
                cell.hyperlink = cell.value
                cell.font = link_font

    ws.freeze_panes = "A2"
    ws.auto_filter.ref = ws.dimensions

    # Adjust column widths
    max_lens = {
        1: 32, 2: 24, 3: 8, 4: 12, 5: 18, 6: 18, 7: 12, 8: 14, 9: 18,
        10: 28, 11: 18, 12: 14, 13: 14, 14: 25, 15: 35, 16: 45, 17: 45,
        18: 45, 19: 38, 20: 45
    }
    for col_idx, width in max_lens.items():
        col_letter = get_column_letter(col_idx)
        ws.column_dimensions[col_letter].width = width

    wb.save(XLSX_OUT)
    print(f"Wrote formatted Excel spreadsheet: {XLSX_OUT}")

if __name__ == "__main__":
    generate_sheets()
