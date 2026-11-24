#!/usr/bin/env python3
"""
Aero Defence Ontology - Executive App Tour Video Generator (With Action Text Overlays)
Produces a high-definition 1080p MP4 video walkthrough for Phill Reece and William Langley,
featuring on-screen action text overlays that explain what is happening step-by-step.
Saved to: /Users/mohamedsellamia/Desktop/Aero_Defence_Ontology_App_Tour.mp4
"""

import os
import sys
import wave
import shutil
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

WORKSPACE = Path(__file__).resolve().parent.parent
DOCS_DIR = WORKSPACE / "docs"
DESKTOP = Path("/Users/mohamedsellamia/Desktop")
OUTPUT_VIDEO = DESKTOP / "Aero_Defence_Ontology_App_Tour.mp4"
TEMP_DIR = Path("/tmp/aero_video_build")

FFMPEG = "/opt/miniconda3/bin/ffmpeg"
FONT_BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
FONT_REG = "/System/Library/Fonts/Supplemental/Arial.ttf"

SHOTS = [
    # --- SCENE 0: INTRO ---
    {
        "id": "intro_1",
        "type": "title_card",
        "tag": "EXECUTIVE PLATFORM TOUR",
        "title": "AERO-DEFENCE INTELLIGENCE ONTOLOGY",
        "subtitle": "Interactive Web Command Center • Zero GitHub Required",
        "subsubtitle": "Walkthrough for Phill Reece & William Langley | Prepared by Mohamed Sellamia",
        "action_badge": "▶ EXECUTIVE TOUR",
        "action_title": "SOLVING DEFENCE PROCUREMENT & SUPPLY CHAIN TEAMING",
        "action_desc": "Live knowledge graph with 32,723 triples across 1,000+ Canadian, UK, and EU suppliers.",
        "lower_title": "OVERVIEW // LIVE OPERATIONAL KNOWLEDGE GRAPH",
        "lower_desc": "Zero GitHub required • 100% interactive web command center running locally.",
        "narration": "Hi Phill! Don't worry about GitHub — here is a quick look at the actual application interface. We built this as an interactive web command center, so anyone can explore suppliers and run matches without touching a single line of code.",
    },
    # --- SCENE 1: MODULE 1 (PROFILE) ---
    {
        "id": "profile_step1_search",
        "type": "app_screen",
        "screenshot": DOCS_DIR / "screenshot_1_profile.png",
        "tag": "MODULE 1: 360° COMPANY PROFILES",
        "action_badge": "▶ STEP 1: SEARCH",
        "action_title": "LOOKING UP CONTRACTOR: \"Flying Colours Corp.\" (CAGE: L2108)",
        "action_desc": "Enter company name or NATO CAGE code. Live auto-complete resolves records instantly.",
        "highlight_box": [245, 195, 730, 280],
        "lower_title": "MODULE 1 // INSTANT CONTRACTOR LOOKUP",
        "lower_desc": "Search by legal company name or NATO CAGE code (e.g. MDA Space, Magellan, Bombardier).",
        "narration": "First is the Company Profile tab. You can look up any contractor by name or NATO CAGE code, or click any quick pill.",
    },
    {
        "id": "profile_step2_audit",
        "type": "app_screen",
        "screenshot": DOCS_DIR / "screenshot_1_profile.png",
        "tag": "MODULE 1: 360° COMPANY PROFILES",
        "action_badge": "▶ STEP 2: AUDIT",
        "action_title": "AUDITING PRODUCTS, MRO SERVICES & DEFENCE CLEARANCE",
        "action_desc": "Verifying Canadian Controlled Goods (CGP), AS9100 Rev D, and Special Mission Jet Modification packages.",
        "highlight_box": [245, 280, 730, 890],
        "lower_title": "MODULE 1 // COMPLETE 360° INTELLIGENCE",
        "lower_desc": "Controlled Goods (CGP) Verified • ITAR Compliant • Class-A Defence Clearance • TRL 1-9.",
        "narration": "On the left, it instantly organizes their manufactured products, maintenance services, Canadian Controlled Goods clearance, and aerospace certifications.",
    },
    {
        "id": "profile_step3_graph",
        "type": "app_screen",
        "screenshot": DOCS_DIR / "screenshot_1_profile.png",
        "tag": "MODULE 1: 360° COMPANY PROFILES",
        "action_badge": "▶ STEP 3: GRAPH",
        "action_title": "TRACING SUPPLY CHAIN TIER & PLATFORM DEPLOYMENT",
        "action_desc": "Graph maps Flying Colours (green Tier-1) suppliesTo Bombardier Inc. (cyan Prime) on Air Platform.",
        "highlight_box": [740, 195, 1665, 890],
        "lower_title": "MODULE 1 // LIVE SUPPLY CHAIN GRAPH",
        "lower_desc": "Interactive network traces who the supplier delivers to and what mission platforms they fly on.",
        "narration": "On the right, the interactive graph visually maps their supply chain position, who they supply to, and what mission platforms they fly on.",
    },
    # --- SCENE 2: MODULE 2 (MATCH RFP) ---
    {
        "id": "match_step1_input",
        "type": "app_screen",
        "screenshot": DOCS_DIR / "screenshot_2_match.png",
        "tag": "MODULE 2: NEURAL PROCUREMENT MATCHER",
        "action_badge": "▶ STEP 1: QUERY",
        "action_title": "INPUTTING PROCUREMENT REQUIREMENT IN PLAIN ENGLISH",
        "action_desc": "Query: \"Tactical uncrewed aerial systems composite aerostructures and long-endurance electric propulsion in Ontario\".",
        "highlight_box": [245, 195, 730, 280],
        "lower_title": "MODULE 2 // SEMANTIC INTENT RETRIEVAL",
        "lower_desc": "Enter raw RFP requirements without worrying about exact keyword phrasing or acronym mismatches.",
        "narration": "Second is the Neural Matcher. You simply type your requirements in plain English, like tactical drone motors in Ontario.",
    },
    {
        "id": "match_step2_gates",
        "type": "app_screen",
        "screenshot": DOCS_DIR / "screenshot_2_match.png",
        "tag": "MODULE 2: NEURAL PROCUREMENT MATCHER",
        "action_badge": "▶ STEP 2: GATES",
        "action_title": "ENFORCING HARD REGULATORY & READINESS FILTERS",
        "action_desc": "Minimum Readiness: TRL 8 (Flight Qualified) • Controlled Goods (CGP): Mandatory.",
        "highlight_box": [245, 280, 730, 370],
        "lower_title": "MODULE 2 // LEAK-PROOF FILTRATION",
        "lower_desc": "Strict geographic and regulatory gates prevent foreign suppliers or non-cleared firms from leaking in.",
        "narration": "Our neural engine matches semantic intent, eliminating keyword friction, while strictly locking down regional and Controlled Goods boundaries with zero leaks.",
    },
    {
        "id": "match_step3_results",
        "type": "app_screen",
        "screenshot": DOCS_DIR / "screenshot_2_match.png",
        "tag": "MODULE 2: NEURAL PROCUREMENT MATCHER",
        "action_badge": "▶ STEP 3: MATCH",
        "action_title": "EVALUATING TOP CANADIAN SUPPLIERS IN < 15MS",
        "action_desc": "#1 Pegasus Imagery (91.8% match) • #2 Draganfly (83.9%) • #3 Volatus Aerospace (83.7%).",
        "highlight_box": [245, 370, 730, 890],
        "lower_title": "MODULE 2 // RANKED QUALIFIED SUPPLIERS",
        "lower_desc": "Clicking any supplier immediately cross-navigates to their full 360° Company Profile.",
        "narration": "It evaluates suppliers in milliseconds, isolating qualified Canadian SMEs like Pegasus Imagery and Draganfly Innovations.",
    },
    # --- SCENE 3: MODULE 3 (CONSORTIUM) ---
    {
        "id": "consortium_step1_tender",
        "type": "app_screen",
        "screenshot": DOCS_DIR / "screenshot_3_consortium.png",
        "tag": "MODULE 3: CONSORTIUM TEAMING & ITB OFFSETS",
        "action_badge": "▶ STEP 1: TENDER",
        "action_title": "SPECIFYING MAJOR DEFENCE BID WORK PACKAGES",
        "action_desc": "Program: Canadian Multi-Mission Aircraft (CMMA) / Strategic UAS Patrol Teaming.",
        "highlight_box": [245, 195, 730, 365],
        "lower_title": "MODULE 3 // STRATEGIC TEAMING ENGINE",
        "lower_desc": "Define subsystems: Tactical UAS Airframe Integration, NATO Tactical Datalinks, Autonomous Flight AI.",
        "narration": "Third is the Consortium builder for major defence bids like the Canadian Multi-Mission Aircraft.",
    },
    {
        "id": "consortium_step2_proposal",
        "type": "app_screen",
        "screenshot": DOCS_DIR / "screenshot_3_consortium.png",
        "tag": "MODULE 3: CONSORTIUM TEAMING & ITB OFFSETS",
        "action_badge": "▶ STEP 2: TEAMING",
        "action_title": "APPOINTING LEAD PRIME INTEGRATOR & SME TEAMMATES",
        "action_desc": "Lead Prime: Bombardier Inc. • Tier-1 Subsystem: IMP Aerospace • SME Partner: Polaris Longueuil.",
        "highlight_box": [245, 365, 730, 680],
        "lower_title": "MODULE 3 // PRIME + SME COLLABORATION",
        "lower_desc": "Optimization algorithm covers 100% of capabilities while pairing Primes with specialized Canadian SMEs.",
        "narration": "It automatically pairs lead prime contractors with Tier-1s and Canadian SMEs to achieve full capability coverage.",
    },
    {
        "id": "consortium_step3_itb",
        "type": "app_screen",
        "screenshot": DOCS_DIR / "screenshot_3_consortium.png",
        "tag": "MODULE 3: CONSORTIUM TEAMING & ITB OFFSETS",
        "action_badge": "▶ STEP 3: ITB OFFSETS",
        "action_title": "CALCULATING CANADIAN CONTENT VALUE & ITB MULTIPLIERS",
        "action_desc": "Canadian Content: 90% CCV • ITB Multiplier: 2.67x • 100% Controlled Goods Compliant.",
        "highlight_box": [245, 470, 730, 560],
        "lower_title": "MODULE 3 // STATUTORY OFFSET CREDITS",
        "lower_desc": "Calculates official 2x to 5x ITB investment multipliers under Canadian defence procurement rules.",
        "narration": "And instantly calculates statutory Canadian Content Value and up to five-times ITB investment offset multipliers.",
    },
    # --- SCENE 4: MODULE 4 (DOSSIER) ---
    {
        "id": "dossier_step1_briefing",
        "type": "app_screen",
        "screenshot": DOCS_DIR / "screenshot_4_dossier.png",
        "tag": "MODULE 4: C-SUITE DUE DILIGENCE DOSSIERS",
        "action_badge": "▶ STEP 1: DOSSIER",
        "action_title": "GENERATING STRATEGIC INTELLIGENCE BRIEFING: MAGELLAN AEROSPACE",
        "action_desc": "NATO CAGE Code: L2391 • Class-A Defence Cleared • CGP Verified • ITAR Compliant.",
        "highlight_box": [245, 195, 730, 890],
        "lower_title": "MODULE 4 // C-SUITE DUE DILIGENCE",
        "lower_desc": "Audits corporate ownership, facility footprint, and quality certifications (AS9100D, NADCAP).",
        "narration": "Fourth gives you instant C-Suite due diligence dossiers with corporate ownership and facility security clearances.",
    },
    # --- SCENE 5: MODULE 5 (SPARQL & SIMULATION) ---
    {
        "id": "sparql_step1_sim",
        "type": "app_screen",
        "screenshot": DOCS_DIR / "screenshot_5_sparql.png",
        "tag": "MODULE 5: W3C SPARQL CONSOLE & SIMULATION API",
        "action_badge": "▶ STEP 1: SIMULATION API",
        "action_title": "PLUGGING LIVE ONTOLOGY INTO WILLIAM'S SIMULATION FRAMEWORK",
        "action_desc": "Standard W3C SPARQL 1.1 endpoint (POST /api/v1/sparql) resolves alternative suppliers in < 15ms.",
        "highlight_box": [245, 195, 730, 890],
        "lower_title": "MODULE 5 // ZERO-FRICTION ERP & SIMULATION INTEGRATION",
        "lower_desc": "William's framework can query alternative suppliers across Canada, the UK, or the EU dynamically.",
        "narration": "And fifth is the SPARQL terminal. This is where William can plug the ontology directly into his supply chain simulation to test alternative suppliers across jurisdictions in under fifteen milliseconds.",
    },
    # --- SCENE 6: OUTRO ---
    {
        "id": "outro_1",
        "type": "title_card",
        "tag": "READY FOR LIVE DEMONSTRATION",
        "title": "READY TO DEMO & INTEGRATE",
        "subtitle": "Interactive Web App Live at http://127.0.0.1:8000/",
        "subsubtitle": "Available for a quick call or Civic Tech Saint John demo • Mohamed Sellamia",
        "action_badge": "▶ DEMO READY",
        "action_title": "LOCAL SOVEREIGN EXECUTION OR CLOUD RUN DEPLOYMENT",
        "action_desc": "Full REST API • SPARQL 1.1 • Vis.js Visual Graph • 6-Page Technical Brief Attached.",
        "lower_title": "NEXT STEPS // CONNECT FOR A 20-MINUTE LIVE WALKTHROUGH",
        "lower_desc": "Civic Tech Saint John or online screen share • Tuesday or Wednesday afternoon.",
        "narration": "The platform is live, responsive, and running locally. I'd love to connect with both of you this week for a live walkthrough. Thanks Phill, thanks William!",
    },
]


def init_fonts():
    return {
        "title_large": ImageFont.truetype(FONT_BOLD, 46),
        "title_med": ImageFont.truetype(FONT_BOLD, 32),
        "subtitle": ImageFont.truetype(FONT_REG, 24),
        "meta": ImageFont.truetype(FONT_REG, 20),
        "badge": ImageFont.truetype(FONT_BOLD, 15),
        "action_badge": ImageFont.truetype(FONT_BOLD, 16),
        "action_title": ImageFont.truetype(FONT_BOLD, 20),
        "action_desc": ImageFont.truetype(FONT_REG, 16),
        "lower_title": ImageFont.truetype(FONT_BOLD, 22),
        "lower_desc": ImageFont.truetype(FONT_REG, 17),
    }


def draw_header(draw: ImageDraw.ImageDraw, fonts, total_w=1920):
    draw.rectangle([0, 0, total_w, 65], fill=(5, 10, 20))
    draw.line([0, 65, total_w, 65], fill=(30, 41, 59), width=1)

    badge_x, badge_y = 35, 18
    draw.rounded_rectangle([badge_x, badge_y, badge_x + 195, badge_y + 30], radius=4, fill=(6, 40, 30), outline=(16, 185, 129), width=1)
    draw.text((badge_x + 10, badge_y + 7), "NATO / DEFENCE COMPLIANT", fill=(16, 185, 129), font=fonts["badge"])

    draw.text((badge_x + 215, badge_y + 5), "AERO-DEFENCE INTELLIGENCE ONTOLOGY", fill=(0, 242, 254), font=fonts["title_med"])

    stats_text = "32,723 Triples (OWL 2)   |   1,119 Capability Vectors   |   < 15ms Latency"
    draw.text((1240, badge_y + 8), stats_text, fill=(148, 163, 184), font=fonts["badge"])


def draw_action_banner(draw: ImageDraw.ImageDraw, fonts, action_badge: str, action_title: str, action_desc: str, total_w=1920):
    """Draws a floating dark-glass Action Banner explaining what is happening right now."""
    box_x1 = 247
    box_y1 = 126
    box_x2 = 1670
    box_y2 = 188

    # Dark translucent banner
    draw.rounded_rectangle([box_x1, box_y1, box_x2, box_y2], radius=6, fill=(11, 20, 38), outline=(0, 242, 254), width=1)

    # Action badge (Amber/Gold for high visibility)
    badge_w = 170
    draw.rounded_rectangle([box_x1 + 8, box_y1 + 8, box_x1 + 8 + badge_w, box_y1 + 32], radius=4, fill=(245, 158, 11))
    draw.text((box_x1 + 18, box_y1 + 12), action_badge, fill=(0, 0, 0), font=fonts["action_badge"])

    # Action title
    draw.text((box_x1 + 25 + badge_w, box_y1 + 11), action_title, fill=(255, 255, 255), font=fonts["action_title"])

    # Action detail subtitle
    draw.text((box_x1 + 14, box_y1 + 38), action_desc, fill=(148, 163, 184), font=fonts["action_desc"])


def draw_highlight_box(draw: ImageDraw.ImageDraw, box):
    """Draws a glowing neon outline around the specific UI element being operated."""
    if not box:
        return
    x1, y1, x2, y2 = box
    draw.rounded_rectangle([x1 - 2, y1 - 2, x2 + 2, y2 + 2], radius=8, outline=(0, 242, 254), width=1)
    draw.rounded_rectangle([x1, y1, x2, y2], radius=6, outline=(0, 242, 254), width=3)
    tick_len = 16
    draw.line([x1, y1, x1 + tick_len, y1], fill=(245, 158, 11), width=4)
    draw.line([x1, y1, x1, y1 + tick_len], fill=(245, 158, 11), width=4)
    draw.line([x2 - tick_len, y1, x2, y1], fill=(245, 158, 11), width=4)
    draw.line([x2, y1, x2, y1 + tick_len], fill=(245, 158, 11), width=4)
    draw.line([x1, y2 - tick_len, x1, y2], fill=(245, 158, 11), width=4)
    draw.line([x1, y2, x1 + tick_len, y2], fill=(245, 158, 11), width=4)
    draw.line([x2 - tick_len, y2, x2, y2], fill=(245, 158, 11), width=4)
    draw.line([x2, y2 - tick_len, x2, y2], fill=(245, 158, 11), width=4)


def draw_lower_third(draw: ImageDraw.ImageDraw, fonts, lower_title: str, lower_desc: str, scene_idx: int, total_scenes: int, total_w=1920):
    box_top = 945
    box_bottom = 1055
    draw.rounded_rectangle([35, box_top, total_w - 35, box_bottom], radius=10, fill=(7, 13, 26), outline=(0, 242, 254), width=2)

    draw.rounded_rectangle([35, box_top, 45, box_bottom], radius=4, fill=(0, 242, 254))

    draw.text((65, box_top + 16), lower_title, fill=(0, 242, 254), font=fonts["lower_title"])
    draw.text((65, box_top + 52), lower_desc, fill=(226, 232, 240), font=fonts["lower_desc"])

    # Progress segment bar
    bar_y = box_bottom - 10
    total_bar_w = total_w - 130
    seg_w = total_bar_w / total_scenes
    for i in range(total_scenes):
        sx = 65 + i * seg_w
        ex = sx + seg_w - 6
        color = (0, 242, 254) if i <= scene_idx else (30, 41, 59)
        draw.line([sx, bar_y, ex, bar_y], fill=color, width=3)


def render_title_slide(scene, scene_idx, total_scenes, fonts) -> Image.Image:
    im = Image.new("RGB", (1920, 1080), color=(8, 15, 30))
    draw = ImageDraw.Draw(im)

    for r in range(1200, 200, -100):
        draw.ellipse([960 - r, 540 - r, 960 + r, 540 + r], outline=(15, 23, 42))

    draw_header(draw, fonts)

    card_box = [160, 150, 1760, 880]
    draw.rounded_rectangle(card_box, radius=16, fill=(11, 20, 38), outline=(0, 242, 254), width=2)

    draw.rounded_rectangle([160, 150, 1760, 220], radius=16, fill=(15, 27, 50))
    draw.text((200, 175), scene["tag"], fill=(0, 242, 254), font=fonts["badge"])

    draw.text((200, 260), scene["title"], fill=(255, 255, 255), font=fonts["title_large"])
    draw.text((200, 335), scene["subtitle"], fill=(0, 242, 254), font=fonts["title_med"])
    draw.text((200, 400), scene["subsubtitle"], fill=(148, 163, 184), font=fonts["subtitle"])

    cols = [
        ("1. 360° Company Profiles", "Instant lookup by contractor name or CAGE code. Maps manufactured products, MRO services, and CGP compliance directly to Canadian KICs."),
        ("2. Leak-Proof Neural Matcher", "Natural language intent retrieval powered by dense sentence embeddings. Evaluates multi-criteria procurement without keyword friction."),
        ("3. Strategic Teaming & ITBs", "Automatically pairs Primes, Tier-1s, and Canadian SMEs. Maximizes Canadian Content Value and computes 2x to 5x ITB offset multipliers."),
    ]
    col_w = 460
    for i, (head, desc) in enumerate(cols):
        cx = 200 + i * (col_w + 50)
        cy = 490
        draw.rounded_rectangle([cx, cy, cx + col_w, cy + 320], radius=10, fill=(18, 32, 60), outline=(30, 41, 59), width=1)
        draw.rounded_rectangle([cx, cy, cx + col_w, cy + 45], radius=10, fill=(24, 42, 80))
        draw.text((cx + 18, cy + 14), head, fill=(0, 242, 254), font=fonts["badge"])

        words = desc.split()
        lines = []
        cur = []
        for w in words:
            cur.append(w)
            if len(" ".join(cur)) > 34:
                lines.append(" ".join(cur[:-1]))
                cur = [w]
        if cur:
            lines.append(" ".join(cur))
        for j, l in enumerate(lines[:6]):
            draw.text((cx + 18, cy + 65 + j * 28), l, fill=(203, 213, 225), font=fonts["meta"])

    draw_lower_third(draw, fonts, scene["lower_title"], scene["lower_desc"], scene_idx, total_scenes)
    return im


def render_app_slide(scene, scene_idx, total_scenes, fonts) -> Image.Image:
    im = Image.new("RGB", (1920, 1080), color=(8, 15, 30))
    draw = ImageDraw.Draw(im)

    draw_header(draw, fonts)

    frame_box = [50, 80, 1870, 930]
    draw.rounded_rectangle(frame_box, radius=10, fill=(11, 20, 38), outline=(30, 41, 59), width=1)

    chrome_h = 36
    draw.rounded_rectangle([50, 80, 1870, 80 + chrome_h], radius=10, fill=(15, 23, 42))
    draw.ellipse([65, 91, 77, 103], fill=(239, 68, 68))
    draw.ellipse([85, 91, 97, 103], fill=(245, 158, 11))
    draw.ellipse([105, 91, 117, 103], fill=(16, 185, 129))

    draw.rounded_rectangle([250, 85, 850, 109], radius=4, fill=(30, 41, 59))
    draw.text((270, 89), "http://127.0.0.1:8000/  —  Live Aerospace & Defence Knowledge Graph", fill=(148, 163, 184), font=fonts["badge"])

    draw.text((1400, 89), scene["tag"], fill=(0, 242, 254), font=fonts["badge"])

    ss_path = scene["screenshot"]
    if ss_path.exists():
        shot = Image.open(ss_path)
        target_w = 1818
        target_h = 800
        shot_ratio = shot.width / shot.height
        target_ratio = target_w / target_h

        if shot_ratio > target_ratio:
            new_w = target_w
            new_h = int(target_w / shot_ratio)
        else:
            new_h = target_h
            new_w = int(target_h * shot_ratio)

        shot_resized = shot.resize((new_w, new_h), Image.Resampling.LANCZOS)
        paste_x = 51 + (target_w - new_w) // 2
        paste_y = 80 + chrome_h + (target_h - new_h) // 2
        im.paste(shot_resized, (paste_x, paste_y))

    # Draw Floating Action Banner with Amber badge and white bold text
    draw_action_banner(draw, fonts, scene["action_badge"], scene["action_title"], scene["action_desc"])

    # Draw Glowing Focus Box over the active section
    if "highlight_box" in scene:
        draw_highlight_box(draw, scene["highlight_box"])

    draw_lower_third(draw, fonts, scene["lower_title"], scene["lower_desc"], scene_idx, total_scenes)
    return im


def generate_audio_for_scene(scene, idx: int) -> Path:
    out_aiff = TEMP_DIR / f"narration_{idx}.aiff"
    out_wav = TEMP_DIR / f"narration_{idx}.wav"

    cmd_say = ["say", "-v", "Daniel", "-r", "175", scene["narration"], "-o", str(out_aiff)]
    subprocess.run(cmd_say, check=True)

    cmd_ff = [
        FFMPEG, "-y", "-i", str(out_aiff),
        str(out_wav)
    ]
    subprocess.run(cmd_ff, check=True, capture_output=True)
    return out_wav


def get_audio_duration(wav_path: Path) -> float:
    with wave.open(str(wav_path), "rb") as w:
        frames = w.getnframes()
        rate = w.getframerate()
        return frames / float(rate)


def build_video():
    TEMP_DIR.mkdir(parents=True, exist_ok=True)
    fonts = init_fonts()

    total_scenes = len(SHOTS)
    subclip_paths = []

    print(f"Generating video scenes for {total_scenes} shots with on-screen action text...")

    for i, sc in enumerate(SHOTS):
        print(f"\n--- Shot {i+1}/{total_scenes}: {sc['id']} ---")

        # 1. Voice Narration
        wav_path = generate_audio_for_scene(sc, i)
        audio_dur = get_audio_duration(wav_path)
        scene_dur = audio_dur + 0.8
        print(f"Audio duration: {audio_dur:.2f}s | Clip duration: {scene_dur:.2f}s")

        # 2. Render Slide Image with Action Overlays
        if sc["type"] == "title_card":
            slide_im = render_title_slide(sc, i, total_scenes, fonts)
        else:
            slide_im = render_app_slide(sc, i, total_scenes, fonts)

        slide_path = TEMP_DIR / f"slide_{i}.png"
        slide_im.save(slide_path, quality=95)

        # 3. Render Scene Subclip with FFmpeg
        clip_path = TEMP_DIR / f"clip_{i}.mp4"
        cmd_clip = [
            FFMPEG, "-y",
            "-loop", "1", "-t", str(scene_dur), "-i", str(slide_path),
            "-i", str(wav_path),
            "-c:v", "libx264", "-tune", "stillimage",
            "-c:a", "aac", "-b:a", "192k",
            "-pix_fmt", "yuv420p",
            "-t", str(scene_dur),
            str(clip_path)
        ]
        subprocess.run(cmd_clip, check=True, capture_output=True)
        subclip_paths.append(clip_path)
        print(f"Rendered subclip: {clip_path.name}")

    # 4. Concatenate All Subclips
    concat_list = TEMP_DIR / "concat_list.txt"
    with open(concat_list, "w", encoding="utf-8") as f:
        for p in subclip_paths:
            f.write(f"file '{p.resolve()}'\n")

    print("\nAssembling final video with FFmpeg...")
    cmd_concat = [
        FFMPEG, "-y",
        "-f", "concat", "-safe", "0", "-i", str(concat_list),
        "-c", "copy",
        str(OUTPUT_VIDEO)
    ]
    subprocess.run(cmd_concat, check=True, capture_output=True)

    print(f"\n=======================================================")
    print(f"SUCCESS! Video created at: {OUTPUT_VIDEO}")
    print(f"File size: {OUTPUT_VIDEO.stat().st_size / (1024*1024):.2f} MB")
    print(f"=======================================================\n")


if __name__ == "__main__":
    build_video()
