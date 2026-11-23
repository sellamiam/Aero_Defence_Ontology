"""
Generates a 6-Page Executive Technical Brief for William Langley and Phill Reece.
Includes live application screenshots of:
- Module 1: 360-Degree Company Profile (Products, Services & Capabilities) - Answers William's Core Need
- Module 2: Leak-Proof Neural Procurement Matcher (RFP Evaluation)
- Module 3: Strategic Consortium Teaming & Canadian ITB Offsets
- Module 4: C-Suite Intelligence Due Diligence Dossier (Magellan Aerospace L2391)
- Module 5: W3C SPARQL 1.1 Multi-Hop Supply Chain Audit
- Module 6: REST API Contracts & GCP Sovereign Deployment Blueprint
"""

from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    HRFlowable,
    Image as RLImage,
    PageBreak,
)
from reportlab.pdfgen import canvas


class NumberedCanvas(canvas.Canvas):
    """Adds running headers and footers with dynamic page numbering."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_header_footer(num_pages)
            super().showPage()
        super().save()

    def draw_header_footer(self, page_count):
        self.saveState()

        # Bottom Footer
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748b"))
        self.drawString(36, 20, "Prepared by Mohamed Sellamia | For William Langley & Phill Reece")
        self.drawRightString(8.5 * inch - 36, 20, f"Page {self._pageNumber} of {page_count}")
        self.setStrokeColor(colors.HexColor("#e2e8f0"))
        self.setLineWidth(0.5)
        self.line(36, 28, 8.5 * inch - 36, 28)

        self.restoreState()


def make_figure_box(img_path: Path, caption: str, width: float = 520, height: float = 245):
    """Encapsulates an image and its caption in an executive styled border."""
    caption_style = ParagraphStyle(
        "FigCaption",
        fontName="Helvetica-Bold",
        fontSize=8,
        leading=10,
        textColor=colors.HexColor("#0284c7"),
        alignment=1, # Center
    )
    img = RLImage(str(img_path), width=width, height=height)
    data = [
        [img],
        [Paragraph(caption, caption_style)],
    ]
    t = Table(data, colWidths=[width])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#070a10")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#1e293b")),
        ('PADDING', (0,0), (-1,0), 0),
        ('PADDING', (0,1), (-1,1), 4),
        ('BOTTOMPADDING', (0,1), (-1,1), 5),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    return t


def generate_pdf(output_path: Path):
    doc = SimpleDocTemplate(
        str(output_path),
        pagesize=letter,
        leftMargin=36,
        rightMargin=36,
        topMargin=36,
        bottomMargin=36,
    )

    styles = getSampleStyleSheet()

    # Custom Palettes
    navy = colors.HexColor("#0f172a")
    blue = colors.HexColor("#0284c7")
    slate = colors.HexColor("#334155")
    light_bg = colors.HexColor("#f8fafc")
    border_color = colors.HexColor("#cbd5e1")

    # Typography Styles
    title_style = ParagraphStyle(
        "DocTitle",
        fontName="Helvetica-Bold",
        fontSize=18,
        leading=22,
        textColor=navy,
        spaceAfter=3,
    )
    subtitle_style = ParagraphStyle(
        "DocSubtitle",
        fontName="Helvetica",
        fontSize=9.5,
        leading=13,
        textColor=blue,
        spaceAfter=8,
    )
    h1_style = ParagraphStyle(
        "SectionH1",
        fontName="Helvetica-Bold",
        fontSize=11,
        leading=14,
        textColor=navy,
        spaceBefore=6,
        spaceAfter=4,
    )
    body_style = ParagraphStyle(
        "BodyTextCustom",
        fontName="Helvetica",
        fontSize=8.5,
        leading=12,
        textColor=slate,
        spaceAfter=4,
    )
    callout_text = ParagraphStyle(
        "CalloutText",
        fontName="Helvetica",
        fontSize=8,
        leading=11,
        textColor=navy,
    )
    step_style = ParagraphStyle(
        "StepStyle",
        fontName="Helvetica",
        fontSize=8.5,
        leading=12,
        textColor=navy,
        spaceAfter=3,
    )
    table_header = ParagraphStyle(
        "TableHeader",
        fontName="Helvetica-Bold",
        fontSize=8,
        leading=10,
        textColor=colors.white,
    )
    table_cell = ParagraphStyle(
        "TableCell",
        fontName="Helvetica",
        fontSize=7.5,
        leading=10,
        textColor=slate,
    )
    table_cell_bold = ParagraphStyle(
        "TableCellBold",
        fontName="Helvetica-Bold",
        fontSize=7.5,
        leading=10,
        textColor=navy,
    )

    docs_dir = output_path.parent
    img_profile = docs_dir / "screenshot_1_profile.png"
    img_match = docs_dir / "screenshot_2_match.png"
    img_consortium = docs_dir / "screenshot_3_consortium.png"
    img_dossier = docs_dir / "screenshot_4_dossier.png"
    img_sparql = docs_dir / "screenshot_5_sparql.png"
    img_swagger = docs_dir / "screenshot_4_swagger.png"

    story = []

    # ================= PAGE 1 =================
    story.append(Paragraph("AEROSPACE & DEFENCE ONTOLOGY & MATCHING ENGINE", title_style))
    story.append(Paragraph("Enterprise Knowledge Graph, Open-Source Neural Retrieval & Live Platform Blueprint", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=blue, spaceBefore=0, spaceAfter=6))

    summary_data = [
        [
            Paragraph("<b>Target Audience:</b> William Langley & Phill Reece<br/><b>Prepared By:</b> Mohamed Sellamia", callout_text),
            Paragraph("<b>Status:</b> Functional Prototype / MVP Completed<br/><b>Scope:</b> Canada (1,000+), UK, EU Industrial Bases", callout_text),
        ]
    ]
    t_summary = Table(summary_data, colWidths=[270, 270])
    t_summary.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), light_bg),
        ('BOX', (0,0), (-1,-1), 0.5, border_color),
        ('PADDING', (0,0), (-1,-1), 5),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t_summary)
    story.append(Spacer(1, 4))

    story.append(Paragraph("1. EXECUTIVE OVERVIEW & PROBLEM SOLVED", h1_style))
    story.append(Paragraph(
        "Defence procurement and strategic teaming have historically been bottlenecked by fragmented supplier registries, manual spreadsheets, and brittle keyword searches. "
        "A procurement officer querying <i>'tactical drone motors'</i> routinely misses qualified suppliers whose registries list formal technical terms such as <i>'Electric Brushless Propulsion & Motor Modules'</i>. "
        "Furthermore, commercial cloud LLMs (OpenAI/Anthropic) cannot be used with unclassified-controlled or export-controlled technical data under Canadian Controlled Goods (CGP) and US ITAR regulations. "
        "This platform solves this by pairing a <b>W3C OWL 2 Knowledge Graph</b> (32,700+ triples across 1,000+ Canadian, UK, and EU firms) with <b>local open-source neural embeddings</b> (<code>all-MiniLM-L6-v2</code>), providing sub-millisecond procurement matching with zero data leakage.",
        body_style
    ))
    story.append(Spacer(1, 4))

    story.append(Paragraph("2. PLATFORM CAPABILITY MATRIX", h1_style))
    modules_data = [
        [Paragraph("Module", table_header), Paragraph("Functional Purpose", table_header), Paragraph("Procurement Deliverable", table_header)],
        [
            Paragraph("<b>1. Profile</b>", table_cell_bold),
            Paragraph("360-degree company profile explorer linking Products, Services, Capabilities, TRL levels, and CGP/ITAR compliance.", table_cell),
            Paragraph("Complete 360-degree visibility into manufactured products, operational services, and capabilities.", table_cell),
        ],
        [
            Paragraph("<b>2. Match RFP</b>", table_cell_bold),
            Paragraph("Open-source neural embedding matcher (384-d latent vectors) + hard geographic & regulatory gates.", table_cell),
            Paragraph("Zero false-positives; eliminates keyword brittleness; handles typos and acronyms.", table_cell),
        ],
        [
            Paragraph("<b>3. Consortium</b>", table_cell_bold),
            Paragraph("Strategic Prime + Tier-1 + SME bidding consortium generator with Canadian ITB offset calculations.", table_cell),
            Paragraph("Maximizes Canadian Content Value (CCV) and calculates statutory 2x–5x ITB multipliers.", table_cell),
        ],
        [
            Paragraph("<b>4. Dossier</b>", table_cell_bold),
            Paragraph("Instant C-Suite due diligence intelligence briefing compiled by NATO CAGE code.", table_cell),
            Paragraph("Corporate ownership, facility locations, Class-A compliance ratings, and risk assessment.", table_cell),
        ],
        [
            Paragraph("<b>5. SPARQL</b>", table_cell_bold),
            Paragraph("Open-standard W3C SPARQL 1.1 analytical console powered by high-performance Oxigraph triplestore.", table_cell),
            Paragraph("Allows external software, web portals, and ERPs to execute multi-hop graph queries via REST.", table_cell),
        ],
    ]
    t_modules = Table(modules_data, colWidths=[90, 240, 210])
    t_modules.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), navy),
        ('GRID', (0,0), (-1,-1), 0.5, border_color),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, light_bg]),
        ('PADDING', (0,0), (-1,-1), 4.5),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t_modules)
    story.append(Spacer(1, 6))

    story.append(Paragraph("3. ONTOLOGY TAXONOMY & INTERACTIVE GRAPH ARCHITECTURE", h1_style))
    story.append(Paragraph(
        "The right-hand canvas of every platform module displays the <b>Live Interactive Knowledge Graph</b> (powered by Oxigraph & Vis.js). "
        "Unlike flat databases, the graph models the real-world topological dependencies of the aerospace & defence industrial base:",
        body_style
    ))
    story.append(Spacer(1, 2))

    graph_legend_data = [
        [Paragraph("Ontology Entity / Edge", table_header), Paragraph("Visual Encoding", table_header), Paragraph("Procurement & Strategic Significance", table_header)],
        [
            Paragraph("<b>Prime Contractor</b>", table_cell_bold),
            Paragraph("<font color='#0284c7'><b>Cyan Circle</b></font>", table_cell),
            Paragraph("Tier-0 Systems Integrator (e.g. Bombardier, CAE, MDA Space) holding prime contract delivery accountability.", table_cell),
        ],
        [
            Paragraph("<b>Tier-1 Supplier</b>", table_cell_bold),
            Paragraph("<font color='#059669'><b>Green Circle</b></font>", table_cell),
            Paragraph("Major subsystem and aerostructure manufacturers (e.g. Magellan Aerospace, Flying Colours, Volatus).", table_cell),
        ],
        [
            Paragraph("<b>SME Specialist</b>", table_cell_bold),
            Paragraph("<font color='#d97706'><b>Orange Circle</b></font>", table_cell),
            Paragraph("Agile Canadian SME innovators (SkyX, Draganfly, MicroPilot) qualifying for 2x–5x ITB multiplier incentives.", table_cell),
        ],
        [
            Paragraph("<b>Technical Capability</b>", table_cell_bold),
            Paragraph("<font color='#db2777'><b>Pink Diamond</b></font>", table_cell),
            Paragraph("Standardized competency classified under Canada's 16 official KICs and evaluated at TRL 1–9.", table_cell),
        ],
        [
            Paragraph("<b>Platform / System</b>", table_cell_bold),
            Paragraph("<font color='#7c3aed'><b>Purple Hexagon</b></font>", table_cell),
            Paragraph("Operational mission domain (Air Platform, Space Platform, Tactical UAS) where subsystems are integrated.", table_cell),
        ],
        [
            Paragraph("<b>Relationship Edges</b>", table_cell_bold),
            Paragraph("<code>suppliesTo</code><br/><code>possesses</code><br/><code>deployedOn</code>", table_cell),
            Paragraph("Directed semantic links: multi-tier supply chain delivery, validated capability possession, and mission platform deployment.", table_cell),
        ],
    ]
    t_graph = Table(graph_legend_data, colWidths=[105, 95, 340])
    t_graph.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), navy),
        ('GRID', (0,0), (-1,-1), 0.5, border_color),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, light_bg]),
        ('PADDING', (0,0), (-1,-1), 3),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t_graph)

    story.append(PageBreak())

    # ================= PAGE 2 =================
    story.append(Paragraph("5. MODULE 1: 360-DEGREE COMPANY PROFILE (PRODUCTS, SERVICES & CAPABILITIES)", h1_style))
    story.append(Paragraph(
        "A defence intelligence platform must provide complete visibility into a contractor's products, services, and capabilities. "
        "<b>Module 1 (Profile)</b> is positioned at the front of the platform as the primary intelligence console. "
        "When an executive or procurement officer selects any company (e.g. <b>Flying Colours Corp.</b>, CAGE: <code>L2108</code>), it aggregates everything a defence professional requires on the left, "
        "while dynamically mapping its supply chain position on the interactive knowledge graph canvas on the right:",
        body_style
    ))
    story.append(Spacer(1, 4))

    # Screenshot 1: Profile
    if img_profile.exists():
        story.append(make_figure_box(
            img_profile,
            "FIGURE 1: Module 1 in Action — Profile for Flying Colours Corp. (Left) & Live Supply Chain Graph (Right: Green Tier-1 Node suppliesTo Cyan Prime Bombardier Inc.)",
            width=520,
            height=260
        ))
    story.append(Spacer(1, 6))

    story.append(Paragraph("6. HOW TO USE MODULE 1 & AUDIT THE GRAPH", h1_style))
    profile_steps = [
        "<b>Step 1: Lookup Any Contractor:</b> Type a company name or NATO CAGE code (e.g. <i>MDA Space</i>, <i>Magellan Aerospace</i>, <i>Bombardier</i>, <i>CAE</i>, <i>L2108</i>), or click any quick-pill.",
        "<b>Step 2: Inspect Manufactured Products & Services:</b> Audit physical product lines (e.g. <i>Special Mission Jet Modification Packages</i>) and depot-level MRO services.",
        "<b>Step 3: Verify Security & Regulatory Clearance:</b> Instantly audit Canadian Controlled Goods Program (CGP) clearance, ITAR readiness, and aerospace quality standards (AS9100 Rev D, ISO 9001:2015, NATO AQAP-2110).",
        "<b>Step 4: Trace Visual Graph Dependencies:</b> In the right-hand canvas, observe how Flying Colours (green circle) is connected via <code>suppliesTo</code> to Bombardier Inc. (cyan prime) and <code>possesses</code> Business Jet MRO (pink diamond) deployed on Air Platforms (purple hexagon).",
    ]
    for s in profile_steps:
        story.append(Paragraph(f"• {s}", step_style))

    story.append(PageBreak())

    # ================= PAGE 3 =================
    story.append(Paragraph("7. MODULE 2: LEAK-PROOF NEURAL PROCUREMENT MATCHER", h1_style))
    story.append(Paragraph(
        "<b>Module 2 (Match RFP)</b> takes natural language procurement requirements and projects them into a 384-dimensional continuous latent space using open-source SentenceTransformers (<code>all-MiniLM-L6-v2</code>). "
        "When an RFP queries <i>'Tactical uncrewed aerial systems (UAS) composite aerostructures and long-endurance electric propulsion in Ontario'</i>, "
        "the engine identifies qualified Canadian suppliers (Pegasus Imagery, Draganfly Innovations, Volatus Aerospace) with a <b>0.83–0.92 match score</b> while strictly isolating regional and regulatory gates so foreign or non-CGP contractors never leak into results. "
        "The right-hand graph canvas visually organizes the surrounding subsystem clusters, linking drone motor and autopilot SMEs directly to the Tactical UAS mission platform:",
        body_style
    ))
    story.append(Spacer(1, 4))

    # Screenshot 2: Match
    if img_match.exists():
        story.append(make_figure_box(
            img_match,
            "FIGURE 2: Module 2 in Action — Semantic UAS Match (Left) & Topology Graph (Right: Orange SME Specialists clustering around Tactical UAS Platform)",
            width=520,
            height=260
        ))
    story.append(Spacer(1, 6))

    story.append(Paragraph("8. HOW TO USE MODULE 2 & CROSS-NAVIGATE", h1_style))
    match_steps = [
        "<b>Step 1: Input Natural Language Tender:</b> Enter raw requirements without worrying about exact keyword phrasing or acronym mismatches.",
        "<b>Step 2: Apply Mandatory Compliance Gates:</b> Set Minimum Technology Readiness Level (e.g. TRL 8 Flight Qualified) and toggle Mandatory Controlled Goods (CGP) registration.",
        "<b>Step 3: Analyze Matching Graph Ecosystem:</b> Visually explore the right-hand graph to see how SME specialists (orange circles: Draganfly, SkyX) and Tier-1 integrators (green circles: Volatus, MicroPilot) connect to the Tactical UAS mission node (purple hexagon).",
        "<b>Step 4: Cross-Navigate to Company Profile:</b> Click any result card to immediately load that contractor's full 360-degree profile in Module 1, or click 'Add to Consortium' to initiate a bidding proposal.",
    ]
    for s in match_steps:
        story.append(Paragraph(f"• {s}", step_style))

    story.append(PageBreak())

    # ================= PAGE 4 =================
    story.append(Paragraph("9. MODULE 3: STRATEGIC CONSORTIUM TEAMING & CANADIAN ITB OFFSETS", h1_style))
    story.append(Paragraph(
        "In major defence bids (e.g. Canadian Multi-Mission Aircraft / CMMA, Future Aircrew Training / FAcT), prime contractors cannot bid alone; they must assemble balanced multi-tier consortia. "
        "Under Canada's <b>Industrial and Technological Benefits (ITB)</b> policy, prime contractors must invest 100% of contract value into Canadian suppliers. "
        "<b>Module 3 (Consortium)</b> automatically pairs Prime Contractors (e.g. Bombardier, CAE) with Tier-1 integrators and Canadian SMEs, computing statutory investment multipliers (2x to 5x for Canadian SME and green aviation content). "
        "The interactive graph visually maps the teaming architecture, proving multi-tier contract compliance:",
        body_style
    ))
    story.append(Spacer(1, 4))

    # Screenshot 3: Consortium
    if img_consortium.exists():
        story.append(make_figure_box(
            img_consortium,
            "FIGURE 3: Module 3 in Action — CMMA Strategic Teaming Proposal (Left: 90% Canadian Content, 2.67x ITB Multiplier) & Teaming Graph (Right)",
            width=520,
            height=260
        ))
    story.append(Spacer(1, 6))

    story.append(Paragraph("10. HOW TO USE MODULE 3: STRATEGIC TEAMING", h1_style))
    consortium_steps = [
        "<b>Step 1: Define Procurement Tender:</b> Enter program title (e.g. <i>'Canadian Multi-Mission Aircraft (CMMA) / Strategic UAS Patrol Teaming'</i>).",
        "<b>Step 2: Input Required Work Packages:</b> Specify operational subsystems (<i>'Tactical UAS Airframe Integration'</i>, <i>'Secure NATO Tactical Datalink'</i>, <i>'Autonomous Flight Control'</i>).",
        "<b>Step 3: Generate Optimized Teaming Consortium:</b> The engine runs a constrained optimization algorithm across the triplestore, appointing a certified Prime Integrator (Bombardier Inc.), assigning specialized Tier-1/SME teammates (IMP Aerospace, Polaris Longueuil), and calculating Canadian Content Value (90% CCV) and ITB offset multipliers (2.67x).",
        "<b>Step 4: Audit Graph Alliance:</b> The graph visually highlights how the prime integrator anchors the subsystem and SME network, verifying there are no single-source failure points.",
    ]
    for s in consortium_steps:
        story.append(Paragraph(f"• {s}", step_style))

    story.append(PageBreak())

    # ================= PAGE 5 =================
    story.append(Paragraph("11. MODULE 4: EXECUTIVE DUE DILIGENCE DOSSIERS", h1_style))
    story.append(Paragraph(
        "<b>Module 4 (Dossier)</b> compiles a comprehensive C-Suite intelligence briefing on any contractor in milliseconds by NATO CAGE code (e.g. <b>L2391</b> for Magellan Aerospace). "
        "It provides compliance audits, facility footprint, ownership structure, and strategic teaming recommendations, while the graph isolates its upstream supply chain links:",
        body_style
    ))
    story.append(Spacer(1, 2))

    # Screenshot 4: Dossier
    if img_dossier.exists():
        story.append(make_figure_box(
            img_dossier,
            "FIGURE 4: Module 4 in Action — Magellan Aerospace Due Diligence Dossier (Left: Class-A Clearance, TRL 9, F-35 Assemblies) & Network (Right)",
            width=520,
            height=180
        ))
    story.append(Spacer(1, 4))

    story.append(Paragraph("12. MODULE 5: W3C SPARQL 1.1 ANALYTICAL TERMINAL", h1_style))
    story.append(Paragraph(
        "<b>Module 5 (SPARQL)</b> provides an open W3C SPARQL 1.1 query console running directly against Oxigraph. "
        "Below, a multi-hop query retrieves Canadian defence suppliers holding CGP registration and certified capabilities at TRL >= 8, returning tabular verification on the left alongside the visual ontology map on the right:",
        body_style
    ))
    story.append(Spacer(1, 2))

    # Screenshot 5: SPARQL
    if img_sparql.exists():
        story.append(make_figure_box(
            img_sparql,
            "FIGURE 5: Module 5 in Action — Multi-Hop Supply Chain Query: Canadian Contractors with CGP & TRL >= 8 against Oxigraph Triplestore",
            width=520,
            height=180
        ))

    story.append(PageBreak())

    # ================= PAGE 6 =================
    story.append(Paragraph("13. APPLICATION ACCESS & DEVELOPER INTEGRATION", h1_style))
    story.append(Paragraph(
        "Enterprise software integration requires an ontology that can be queried seamlessly from downstream applications and procurement systems. "
        "The platform exposes an enterprise-grade REST API and standard W3C SPARQL 1.1 query interface:",
        body_style
    ))
    story.append(Spacer(1, 2))

    # Screenshot 6: Swagger Docs
    if img_swagger.exists():
        story.append(make_figure_box(
            img_swagger,
            "FIGURE 6: Interactive OpenAPI / Swagger 3.0 Documentation Suite (http://localhost:8000/docs) for Enterprise App Integration",
            width=520,
            height=200
        ))
    story.append(Spacer(1, 6))

    access_data = [
        [Paragraph("Channel", table_header), Paragraph("Interface / Endpoint", table_header), Paragraph("Target Use Case", table_header)],
        [
            Paragraph("<b>Interactive Web UI</b>", table_cell_bold),
            Paragraph("<code>http://localhost:8000/</code>", table_cell),
            Paragraph("Executive command center, visual graph exploration, procurement matching.", table_cell),
        ],
        [
            Paragraph("<b>REST API (JSON)</b>", table_cell_bold),
            Paragraph("<code>GET /api/v1/companies/{cage}</code><br/><code>POST /api/v1/match</code><br/><code>POST /api/v1/consortium</code>", table_cell),
            Paragraph("Downstream web applications, procurement portals, and ERP pipelines.", table_cell),
        ],
        [
            Paragraph("<b>SPARQL 1.1 Terminal</b>", table_cell_bold),
            Paragraph("<code>POST /api/v1/sparql</code>", table_cell),
            Paragraph("Semantic data science queries and automated graph traversals.", table_cell),
        ],
    ]
    t_access = Table(access_data, colWidths=[100, 210, 230])
    t_access.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), navy),
        ('GRID', (0,0), (-1,-1), 0.5, border_color),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, light_bg]),
        ('PADDING', (0,0), (-1,-1), 3.5),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t_access)
    story.append(Spacer(1, 8))

    story.append(Paragraph("14. CLOUD & SOVEREIGN DEPLOYMENT BLUEPRINT", h1_style))
    story.append(Paragraph(
        "• <b>Option A: Google Cloud Run (Canada Region — Recommended):</b> Serverless container in GCP Montreal (<code>northamerica-northeast1</code>) or Toronto (<code>northamerica-northeast2</code>). Scales to zero when not in use (costs pennies/month), provides instant HTTPS URL, and connects with Google Identity-Aware Proxy (IAP) OAuth.<br/>"
        "• <b>Option B: Dedicated GCP Compute VM (e2-standard-4):</b> Persistent Linux VM inside corporate VPC with in-memory triplestore caching for sub-10ms query latency.<br/>"
        "• <b>Option C: On-Premise Air-Gapped Docker:</b> 100% sovereign, offline container deployment with zero external internet dependencies—strictly compliant with Canadian Controlled Goods Program (CGP) and US ITAR data security rules.",
        body_style
    ))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Executive PDF generated successfully at: {output_path}")


if __name__ == "__main__":
    out = Path(__file__).resolve().parent.parent / "docs" / "Aero_Defence_Ontology_Executive_Brief.pdf"
    generate_pdf(out)
