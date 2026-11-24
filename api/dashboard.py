"""
Executive Interactive Web Dashboard for Aerospace & Defence Knowledge Graph.
A C-Suite command center inspired by Palantir Gotham and defense intelligence terminals.
Features:
- Live 360-Degree Company Profile Explorer (Products, Services & Capabilities)
- Real-Time Hybrid Procurement Matching Simulator
- Strategic Consortium Teaming Generator
- C-Suite Intelligence Dossier Viewer
- Live SPARQL 1.1 Analytical Terminal
- Live Interactive 3D/2D Graph Visualization (Vis.js Canvas)
"""

DASHBOARD_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AERO-DEFENCE INTELLIGENCE // Enterprise Knowledge Graph</title>
    <!-- Modern Styling & Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;800&family=Inter:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
    <script src="/static/vis-network.min.js"></script>
    <script>if(typeof vis === 'undefined'){document.write('<script src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"><\\/script>')}</script>
    <style>
        :root {
            --bg-primary: #070a10;
            --bg-secondary: #0d131f;
            --bg-card: #131c2e;
            --bg-card-hover: #18233a;
            --accent-cyan: #00f2fe;
            --accent-blue: #4facfe;
            --accent-gold: #f59e0b;
            --accent-emerald: #10b981;
            --accent-red: #ef4444;
            --accent-purple: #a855f7;
            --text-primary: #f8fafc;
            --text-secondary: #94a3b8;
            --border-color: #1e293b;
        }

        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            background-color: var(--bg-primary);
            color: var(--text-primary);
            overflow-x: hidden;
            display: flex;
            flex-direction: column;
            min-height: 100vh;
        }

        /* Top Military Nav - Centered Container */
        header {
            background-color: rgba(13, 19, 31, 0.95);
            backdrop-filter: blur(12px);
            border-bottom: 1px solid var(--border-color);
            position: sticky;
            top: 0;
            z-index: 1000;
            width: 100%;
        }

        .header-inner {
            max-width: 1720px;
            margin: 0 auto;
            padding: 14px 28px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .brand {
            display: flex;
            align-items: center;
            gap: 14px;
        }

        .badge-live {
            background: rgba(16, 185, 129, 0.15);
            color: var(--accent-emerald);
            border: 1px solid var(--accent-emerald);
            padding: 4px 10px;
            border-radius: 4px;
            font-size: 11px;
            font-family: 'JetBrains Mono', monospace;
            font-weight: 700;
            letter-spacing: 0.6px;
        }

        .brand h1 {
            font-size: 18px;
            font-weight: 800;
            letter-spacing: 0.8px;
            text-transform: uppercase;
            background: linear-gradient(135deg, #00f2fe 0%, #4facfe 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .header-stats {
            display: flex;
            gap: 24px;
            font-family: 'JetBrains Mono', monospace;
            font-size: 12px;
        }

        .stat-item {
            display: flex;
            flex-direction: column;
            align-items: flex-end;
        }
        .stat-val { color: var(--accent-cyan); font-weight: 800; font-size: 14px; }
        .stat-lbl { color: var(--text-secondary); font-size: 10px; letter-spacing: 0.5px; }

        /* Main Workspace Layout - Centered with Max Width */
        .workspace-container {
            max-width: 1720px;
            margin: 0 auto;
            width: 100%;
            flex: 1;
            display: flex;
            border-left: 1px solid var(--border-color);
            border-right: 1px solid var(--border-color);
            background: var(--bg-secondary);
            box-shadow: 0 10px 40px rgba(0,0,0,0.6);
            height: calc(100vh - 67px);
            overflow: hidden;
            min-height: 0;
        }

        .workspace {
            display: grid;
            grid-template-columns: 580px 1fr;
            width: 100%;
            height: 100%;
            overflow: hidden;
            min-height: 0;
        }

        /* Sidebar Panels */
        .sidebar {
            background: var(--bg-secondary);
            border-right: 1px solid var(--border-color);
            display: flex;
            flex-direction: column;
            overflow-y: auto;
        }

        .tabs {
            display: flex;
            border-bottom: 1px solid var(--border-color);
            background: rgba(0,0,0,0.3);
            position: sticky;
            top: 0;
            z-index: 50;
        }

        .tab-btn {
            flex: 1;
            padding: 14px 6px;
            background: transparent;
            border: none;
            color: var(--text-secondary);
            font-weight: 700;
            font-size: 11.5px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            cursor: pointer;
            transition: all 0.2s;
            border-bottom: 2px solid transparent;
            text-align: center;
        }

        .tab-btn:hover {
            color: #fff;
            background: rgba(255, 255, 255, 0.02);
        }

        .tab-btn.active {
            color: var(--accent-cyan);
            border-bottom-color: var(--accent-cyan);
            background: rgba(0, 242, 254, 0.06);
        }

        .panel-content {
            padding: 22px;
            display: none;
            flex-direction: column;
            gap: 16px;
        }

        .panel-content.active { display: flex; }

        /* Form Controls */
        .form-group {
            display: flex;
            flex-direction: column;
            gap: 6px;
        }

        label {
            font-size: 11px;
            text-transform: uppercase;
            color: var(--text-secondary);
            font-weight: 700;
            letter-spacing: 0.6px;
        }

        textarea, input, select {
            width: 100%;
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            color: #fff;
            padding: 10px 12px;
            border-radius: 6px;
            font-family: inherit;
            font-size: 13px;
            outline: none;
            transition: border-color 0.2s, box-shadow 0.2s;
        }

        textarea:focus, input:focus, select:focus {
            border-color: var(--accent-cyan);
            box-shadow: 0 0 0 2px rgba(0, 242, 254, 0.15);
        }

        .btn-action {
            background: linear-gradient(135deg, #00f2fe 0%, #4facfe 100%);
            color: #050b14;
            font-weight: 800;
            border: none;
            padding: 12px;
            border-radius: 6px;
            cursor: pointer;
            text-transform: uppercase;
            font-size: 12px;
            letter-spacing: 0.8px;
            box-shadow: 0 4px 15px rgba(0, 242, 254, 0.25);
            transition: transform 0.1s, opacity 0.2s;
        }

        .btn-action:hover { opacity: 0.92; }
        .btn-action:active { transform: scale(0.98); }

        /* Results Display */
        .results-container {
            display: flex;
            flex-direction: column;
            gap: 12px;
            margin-top: 10px;
        }

        .match-card {
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 6px;
            padding: 14px;
            display: flex;
            flex-direction: column;
            gap: 8px;
            transition: border-color 0.2s, transform 0.1s;
            cursor: pointer;
        }

        .match-card:hover {
            border-color: var(--accent-cyan);
            background: var(--bg-card-hover);
            transform: translateY(-2px);
        }

        .match-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .match-title {
            font-weight: 700;
            font-size: 14px;
            color: #fff;
        }

        .score-pill {
            background: rgba(0, 242, 254, 0.15);
            color: var(--accent-cyan);
            border: 1px solid var(--accent-cyan);
            padding: 3px 10px;
            border-radius: 12px;
            font-size: 12px;
            font-family: 'JetBrains Mono', monospace;
            font-weight: 700;
        }

        .match-meta {
            font-size: 11px;
            color: var(--text-secondary);
            display: flex;
            gap: 12px;
            flex-wrap: wrap;
        }

        .match-capability {
            font-size: 12px;
            color: #e2e8f0;
            background: rgba(255,255,255,0.03);
            padding: 8px 10px;
            border-radius: 4px;
            border-left: 2px solid var(--accent-cyan);
        }

        /* Profile Cards & Components */
        .quick-pills {
            display: flex;
            gap: 6px;
            flex-wrap: wrap;
            margin-top: 6px;
        }

        .pill-btn {
            background: rgba(255,255,255,0.04);
            border: 1px solid var(--border-color);
            color: var(--text-secondary);
            font-size: 11px;
            padding: 4px 8px;
            border-radius: 14px;
            cursor: pointer;
            transition: all 0.15s;
        }
        .pill-btn:hover, .pill-btn.active {
            background: rgba(0,242,254,0.12);
            color: var(--accent-cyan);
            border-color: var(--accent-cyan);
        }

        .profile-card {
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 18px;
            display: flex;
            flex-direction: column;
            gap: 14px;
        }

        .profile-header {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            border-bottom: 1px solid rgba(255,255,255,0.07);
            padding-bottom: 12px;
        }

        .profile-name {
            font-size: 18px;
            font-weight: 800;
            color: #fff;
            letter-spacing: 0.3px;
        }

        .profile-subtitle {
            font-size: 12px;
            color: var(--text-secondary);
            margin-top: 3px;
        }

        .tier-badge {
            background: rgba(0, 242, 254, 0.12);
            border: 1px solid var(--accent-cyan);
            color: var(--accent-cyan);
            padding: 4px 10px;
            border-radius: 4px;
            font-size: 11px;
            font-family: 'JetBrains Mono', monospace;
            font-weight: 700;
        }

        .grid-2col {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 10px;
            font-size: 11px;
            background: rgba(0,0,0,0.25);
            padding: 12px;
            border-radius: 6px;
            border: 1px solid rgba(255,255,255,0.04);
        }

        .grid-item-lbl { color: var(--text-secondary); margin-bottom: 2px; }
        .grid-item-val { font-weight: 700; color: #fff; }

        .section-subhead {
            font-size: 11px;
            text-transform: uppercase;
            font-weight: 800;
            letter-spacing: 0.6px;
            color: var(--accent-cyan);
            margin-bottom: 4px;
            display: flex;
            align-items: center;
            gap: 6px;
        }

        .item-chip {
            background: rgba(79, 172, 254, 0.1);
            border: 1px solid rgba(79, 172, 254, 0.3);
            color: #93c5fd;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 11px;
            display: inline-block;
        }

        .cap-box {
            background: rgba(255,255,255,0.02);
            border: 1px solid var(--border-color);
            border-left: 3px solid var(--accent-cyan);
            padding: 10px 12px;
            border-radius: 4px;
            display: flex;
            flex-direction: column;
            gap: 4px;
        }

        .cap-title {
            font-weight: 700;
            font-size: 12.5px;
            color: #fff;
            display: flex;
            justify-content: space-between;
        }

        .cap-desc {
            font-size: 11.5px;
            color: var(--text-secondary);
            line-height: 1.4;
        }

        /* Right Canvas Area */
        .canvas-container {
            position: relative;
            background: radial-gradient(circle at center, #111a2d 0%, #080c14 100%);
            width: 100%;
            height: 100%;
            overflow: hidden;
            min-height: 0;
            display: flex;
            justify-content: center;
            align-items: center;
        }

        #graph-network {
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            width: 100%;
            height: 100%;
            overflow: hidden;
        }

        /* High-Tech Knowledge Graph Visualizer Styling */
        .graph-toolbar {
            position: absolute;
            top: 14px;
            left: 16px;
            right: 16px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            z-index: 25;
            pointer-events: none;
        }

        .graph-modes {
            display: flex;
            gap: 4px;
            background: rgba(13, 19, 31, 0.88);
            backdrop-filter: blur(12px);
            padding: 4px;
            border-radius: 8px;
            border: 1px solid var(--border-color);
            pointer-events: auto;
            box-shadow: 0 4px 20px rgba(0,0,0,0.5);
        }

        .graph-mode-btn {
            padding: 6px 12px;
            font-size: 11px;
            font-weight: 700;
            border: 1px solid transparent;
            background: transparent;
            color: var(--text-secondary);
            border-radius: 6px;
            cursor: pointer;
            transition: all 0.2s;
            font-family: inherit;
        }

        .graph-mode-btn:hover {
            color: #ffffff;
            background: rgba(255, 255, 255, 0.05);
        }

        .graph-mode-btn.active {
            color: var(--accent-cyan);
            background: rgba(0, 242, 254, 0.12);
            border-color: rgba(0, 242, 254, 0.4);
            box-shadow: 0 0 10px rgba(0, 242, 254, 0.2);
        }

        .graph-actions {
            display: flex;
            gap: 8px;
            align-items: center;
            pointer-events: auto;
        }

        .graph-actions select {
            background: rgba(13, 19, 31, 0.88);
            backdrop-filter: blur(12px);
            border: 1px solid var(--border-color);
            color: #fff;
            padding: 6px 10px;
            border-radius: 6px;
            font-size: 11.5px;
            font-weight: 600;
            cursor: pointer;
            outline: none;
            box-shadow: 0 4px 15px rgba(0,0,0,0.4);
        }

        .btn-tool {
            background: rgba(13, 19, 31, 0.88);
            backdrop-filter: blur(12px);
            border: 1px solid var(--border-color);
            color: var(--text-secondary);
            padding: 6px 12px;
            border-radius: 6px;
            font-size: 11px;
            font-weight: 700;
            cursor: pointer;
            font-family: inherit;
            transition: all 0.2s;
            box-shadow: 0 4px 15px rgba(0,0,0,0.4);
        }

        .btn-tool:hover {
            color: var(--accent-cyan);
            border-color: var(--accent-cyan);
            background: rgba(0, 242, 254, 0.08);
        }

        .graph-status-badge {
            position: absolute;
            top: 60px;
            left: 16px;
            background: rgba(13, 19, 31, 0.85);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.08);
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 10.5px;
            font-family: 'JetBrains Mono', monospace;
            color: var(--text-secondary);
            display: flex;
            align-items: center;
            gap: 8px;
            z-index: 15;
            box-shadow: 0 4px 15px rgba(0,0,0,0.5);
            pointer-events: none;
        }

        .live-dot {
            width: 7px;
            height: 7px;
            background: var(--accent-emerald);
            border-radius: 50%;
            box-shadow: 0 0 8px var(--accent-emerald);
            animation: pulse 2s infinite;
        }

        @keyframes pulse {
            0%, 100% { opacity: 1; transform: scale(1); }
            50% { opacity: 0.5; transform: scale(0.85); }
        }

        /* Floating Interactive Node HUD */
        .node-hud-card {
            position: absolute;
            bottom: 56px;
            left: 20px;
            width: 320px;
            background: rgba(13, 19, 31, 0.95);
            backdrop-filter: blur(16px);
            border: 1px solid rgba(0, 242, 254, 0.4);
            box-shadow: 0 10px 35px rgba(0,0,0,0.8), 0 0 20px rgba(0, 242, 254, 0.15);
            border-radius: 8px;
            padding: 14px;
            z-index: 30;
            display: flex;
            flex-direction: column;
            gap: 10px;
            animation: fadeIn 0.25s ease-out;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(8px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .node-hud-header {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            gap: 8px;
            border-bottom: 1px solid rgba(255,255,255,0.08);
            padding-bottom: 8px;
        }

        .node-hud-title {
            font-weight: 800;
            font-size: 13px;
            color: #ffffff;
            line-height: 1.3;
        }

        .node-hud-close {
            background: transparent;
            border: none;
            color: var(--text-secondary);
            font-size: 14px;
            cursor: pointer;
            padding: 0 4px;
        }

        .node-hud-close:hover { color: #fff; }

        .node-hud-meta {
            font-size: 11px;
            color: var(--text-secondary);
            line-height: 1.5;
            display: flex;
            flex-direction: column;
            gap: 4px;
        }

        .node-hud-actions {
            display: flex;
            gap: 8px;
            margin-top: 4px;
        }

        .btn-hud-primary {
            flex: 1;
            background: linear-gradient(135deg, #00f2fe 0%, #4facfe 100%);
            color: #050b14;
            font-weight: 800;
            border: none;
            padding: 8px;
            border-radius: 4px;
            font-size: 10.5px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            cursor: pointer;
        }

        .btn-hud-secondary {
            flex: 1;
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid var(--border-color);
            color: #fff;
            font-weight: 700;
            padding: 8px;
            border-radius: 4px;
            font-size: 10.5px;
            cursor: pointer;
        }

        .btn-hud-secondary:hover {
            border-color: var(--accent-cyan);
            color: var(--accent-cyan);
        }

        /* Bottom Legend Bar */
        .graph-legend-bar {
            position: absolute;
            bottom: 14px;
            left: 50%;
            transform: translateX(-50%);
            background: rgba(13, 19, 31, 0.88);
            backdrop-filter: blur(12px);
            border: 1px solid var(--border-color);
            border-radius: 20px;
            padding: 6px 18px;
            display: flex;
            align-items: center;
            gap: 16px;
            font-size: 10.5px;
            z-index: 15;
            box-shadow: 0 4px 20px rgba(0,0,0,0.6);
            pointer-events: none;
        }

        .legend-item {
            display: flex;
            align-items: center;
            gap: 6px;
            color: var(--text-secondary);
            font-weight: 600;
        }

        .legend-dot {
            width: 8px;
            height: 8px;
            border-radius: 50%;
        }

        pre {
            background: #090d14;
            padding: 14px;
            border-radius: 6px;
            font-family: 'JetBrains Mono', monospace;
            font-size: 11px;
            overflow-x: auto;
            border: 1px solid var(--border-color);
            color: #38bdf8;
            max-height: 480px;
        }

        /* Structured SPARQL Result Table */
        .sparql-table {
            width: 100%;
            border-collapse: collapse;
            font-family: 'JetBrains Mono', monospace;
            font-size: 11px;
            margin-top: 10px;
        }
        .sparql-table th {
            background: rgba(0, 242, 254, 0.1);
            color: var(--accent-cyan);
            text-align: left;
            padding: 8px 10px;
            border: 1px solid var(--border-color);
            font-weight: 700;
        }
        .sparql-table td {
            padding: 8px 10px;
            border: 1px solid var(--border-color);
            color: #e2e8f0;
        }
        .sparql-table tr:nth-child(even) {
            background: rgba(255,255,255,0.02);
        }
    </style>
</head>
<body>

    <header>
        <div class="header-inner">
            <div class="brand">
                <span class="badge-live">NATO / DEFENCE COMPLIANT</span>
                <h1>Aero-Defence Intelligence Ontology</h1>
            </div>
            <div class="header-stats">
                <div class="stat-item">
                    <span class="stat-val" id="stat-triples">32,723</span>
                    <span class="stat-lbl">RDF TRIPLES (OWL 2)</span>
                </div>
                <div class="stat-item">
                    <span class="stat-val" id="stat-entities">1,119</span>
                    <span class="stat-lbl">CAPABILITY VECTORS</span>
                </div>
                <div class="stat-item">
                    <span class="stat-val" id="stat-latency">&lt; 15ms</span>
                    <span class="stat-lbl">HYBRID LATENCY</span>
                </div>
            </div>
        </div>
    </header>

    <div class="workspace-container">
        <div class="workspace">
            <!-- Left Intelligence Control Panel -->
            <div class="sidebar">
                <div class="tabs">
                    <button class="tab-btn active" data-tab="profile" onclick="switchTab('profile', this)">1. Profile</button>
                    <button class="tab-btn" data-tab="match" onclick="switchTab('match', this)">2. Match RFP</button>
                    <button class="tab-btn" data-tab="consortium" onclick="switchTab('consortium', this)">3. Consortium</button>
                    <button class="tab-btn" data-tab="dossier" onclick="switchTab('dossier', this)">4. Dossier</button>
                    <button class="tab-btn" data-tab="sparql" onclick="switchTab('sparql', this)">5. SPARQL</button>
                </div>

                <!-- Tab 1: 360-Degree Company Profile (Products, Services & Capabilities) -->
                <div id="tab-profile" class="panel-content active">
                    <div class="form-group">
                        <label>Lookup Company Profile (Name or CAGE Code)</label>
                        <div style="position:relative;">
                            <div style="display:flex; gap:8px;">
                                <input type="text" id="profile-search-input" value="Flying Colours Corp." placeholder="Type company name or CAGE (e.g. MDA Space, Magellan, L2108)..." onkeydown="if(event.key==='Enter') loadProfile(this.value)" oninput="handleSearchSuggestions(this.value)">
                                <button class="btn-action" style="padding: 10px 18px; white-space:nowrap;" onclick="loadProfile(document.getElementById('profile-search-input').value)">Load Profile</button>
                            </div>
                            <div id="search-suggestions" style="position:absolute; top:42px; left:0; right:110px; background:var(--bg-card); border:1px solid var(--accent-cyan); border-radius:6px; z-index:100; max-height:220px; overflow-y:auto; display:none; box-shadow:0 8px 24px rgba(0,0,0,0.6);"></div>
                        </div>
                        <div class="quick-pills">
                            <span class="pill-btn active" onclick="loadProfile('L2108')">Flying Colours (L2108)</span>
                            <span class="pill-btn" onclick="loadProfile('L2391')">Magellan Aerospace (L2391)</span>
                            <span class="pill-btn" onclick="loadProfile('L3842')">Bombardier (L3842)</span>
                            <span class="pill-btn" onclick="loadProfile('L0429')">CAE Inc. (L0429)</span>
                            <span class="pill-btn" onclick="loadProfile('L0642')">MDA Space (L0642)</span>
                            <span class="pill-btn" onclick="loadProfile('L4102')">Pegasus Imagery (L4102)</span>
                            <span class="pill-btn" onclick="loadProfile('L1734')">Draganfly (L1734)</span>
                        </div>
                    </div>

                    <div id="profile-card-container">
                        <!-- Loaded dynamically -->
                    </div>
                </div>

                <!-- Tab 2: Procurement Matching -->
                <div id="tab-match" class="panel-content">
                    <div class="form-group">
                        <label>Tender / Capability Requirement (Natural Language)</label>
                        <textarea id="match-query" rows="3">Tactical uncrewed aerial systems (UAS) composite aerostructures and long-endurance electric propulsion in Ontario</textarea>
                    </div>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
                        <div class="form-group">
                            <label>Min Readiness (TRL)</label>
                            <select id="match-trl">
                                <option value="">Any TRL</option>
                                <option value="7">TRL 7 (Prototype Flight)</option>
                                <option value="8" selected>TRL 8 (Flight Qualified)</option>
                                <option value="9">TRL 9 (Combat Proven)</option>
                            </select>
                        </div>
                        <div class="form-group">
                            <label>Controlled Goods</label>
                            <select id="match-cgp">
                                <option value="true" selected>Mandatory (CGP)</option>
                                <option value="false">Optional</option>
                            </select>
                        </div>
                    </div>
                    <button class="btn-action" onclick="runMatching()">Execute Leak-Proof Match</button>

                    <div id="match-results" class="results-container">
                        <!-- Populated dynamically -->
                    </div>
                </div>

                <!-- Tab 3: Strategic Consortium Teaming -->
                <div id="tab-consortium" class="panel-content">
                    <div class="form-group">
                        <label>Major Defence Program Title</label>
                        <input type="text" id="consortium-title" value="Canadian Multi-Mission Aircraft (CMMA) / Strategic UAS Patrol Teaming">
                    </div>
                    <div class="form-group">
                        <label>Required Capability Work Packages (One per line)</label>
                        <textarea id="consortium-wps" rows="4">Tactical UAS Airframe Integration & Systems Assembly
Secure NATO Tactical Datalink & Electronic Warfare Sensor Pods
Autonomous Flight Control Software & Edge AI Video Processing</textarea>
                    </div>
                    <button class="btn-action" onclick="assembleConsortium()">Generate Winning Teaming Proposal</button>
                    <div id="consortium-results" style="margin-top: 10px;"></div>
                </div>

                <!-- Tab 4: Executive Dossier -->
                <div id="tab-dossier" class="panel-content">
                    <div class="form-group">
                        <label>Contractor CAGE / NCAGE Code</label>
                        <input type="text" id="dossier-cage" value="L2391" placeholder="e.g. L2391 (Magellan), L2108 (Flying Colours), 3A183 (CAE)">
                    </div>
                    <button class="btn-action" onclick="fetchDossier()">Generate C-Suite Dossier</button>
                    <div id="dossier-results" style="margin-top: 12px;"></div>
                </div>

                <!-- Tab 5: Raw SPARQL 1.1 -->
                <div id="tab-sparql" class="panel-content">
                    <div class="form-group">
                        <label>Oxigraph SPARQL 1.1 Query Console</label>
                        <textarea id="sparql-query" rows="7">PREFIX aero: <https://w3id.org/aerospace-defence#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?companyName ?city ?province ?cage ?capabilityTitle ?trl WHERE {
    ?c aero:cageCode ?cage ;
       aero:legalName ?companyName ;
       aero:headquartersCountry "CAN" ;
       aero:holdsCertification aero:Cert_CGP_Canada ;
       aero:holdsCertification aero:Cert_AS9100D ;
       aero:hasCapability ?cap .
    ?cap rdfs:label ?capabilityTitle ;
         aero:trlValue ?trl .
    OPTIONAL { ?c aero:headquartersCity ?city . }
    OPTIONAL { ?c aero:headquartersProvince ?province . }
    FILTER(?trl >= 8)
} ORDER BY ?companyName LIMIT 8</textarea>
                    </div>
                    <button class="btn-action" onclick="runSparql()">Execute Graph Query</button>
                    <div id="sparql-output-container" style="margin-top:10px;">
                        <pre id="sparql-output">Query results will render here...</pre>
                    </div>
                </div>
            </div>

            <!-- Right Visual Knowledge Graph Canvas -->
            <div class="canvas-container">
                <!-- Top Command Bar for Graph Navigation & Filtering -->
                <div class="graph-toolbar">
                    <div class="graph-modes">
                        <button class="graph-mode-btn active" data-mode="ecosystem" onclick="setGraphMode('ecosystem', this)">🌐 Allied Ecosystem</button>
                        <button class="graph-mode-btn" data-mode="tier" onclick="setGraphMode('tier', this)">⚡ Supply Chain Tiers</button>
                        <button class="graph-mode-btn" data-mode="platform" onclick="setGraphMode('platform', this)">✈️ Platforms</button>
                        <button class="graph-mode-btn" data-mode="company" id="btn-mode-company" onclick="setGraphMode('company', this)">🎯 Contractor Focus</button>
                    </div>
                    <div class="graph-actions">
                        <select id="graph-country-select" onchange="onGraphFilterChange()">
                            <option value="ALL">All Jurisdictions</option>
                            <option value="CAN">Canada (CAN)</option>
                            <option value="GBR">United Kingdom (GBR)</option>
                            <option value="EU">European Union (EU)</option>
                        </select>
                        <button class="btn-tool" onclick="togglePhysics()" id="btn-physics" title="Pause / Resume Physics">⏸ Freeze</button>
                        <button class="btn-tool" onclick="fitGraph()" title="Center Graph">⌖ Fit</button>
                        <button class="btn-tool" onclick="reloadGraph()" title="Reload Knowledge Graph">🔄</button>
                    </div>
                </div>

                <!-- Live Status & Density Counter -->
                <div class="graph-status-badge" id="graph-status-badge">
                    <span class="live-dot"></span>
                    <span id="graph-status-text">Live Triplestore Sync &bull; Initializing...</span>
                </div>

                <!-- Floating Interactive Node Inspection HUD (appears on click) -->
                <div class="node-hud-card" id="node-hud-card" style="display:none;">
                    <div class="node-hud-header">
                        <div class="node-hud-title" id="hud-title">Entity Name</div>
                        <button class="node-hud-close" onclick="closeNodeHud()">✕</button>
                    </div>
                    <div class="node-hud-meta" id="hud-meta">
                        <!-- Populated dynamically on click -->
                    </div>
                    <div class="node-hud-actions">
                        <button class="btn-hud-primary" id="hud-btn-profile" onclick="hudOpenProfile()">Inspect Profile</button>
                        <button class="btn-hud-secondary" id="hud-btn-focus" onclick="hudFocusNode()">Focus Ego-Net</button>
                    </div>
                </div>

                <!-- Bottom Entity Legend -->
                <div class="graph-legend-bar">
                    <div class="legend-item"><span class="legend-dot" style="background:#00f2fe; box-shadow:0 0 8px #00f2fe;"></span> Prime</div>
                    <div class="legend-item"><span class="legend-dot" style="background:#10b981; box-shadow:0 0 8px #10b981;"></span> Tier-1</div>
                    <div class="legend-item"><span class="legend-dot" style="background:#f59e0b; box-shadow:0 0 8px #f59e0b;"></span> Tier-2 / SME</div>
                    <div class="legend-item"><span class="legend-dot" style="background:#ec4899; box-shadow:0 0 8px #ec4899;"></span> Capability</div>
                    <div class="legend-item"><span class="legend-dot" style="background:#3b82f6; box-shadow:0 0 8px #3b82f6;"></span> Product</div>
                    <div class="legend-item"><span class="legend-dot" style="background:#a855f7; box-shadow:0 0 8px #a855f7;"></span> Platform</div>
                </div>

                <div id="graph-network"></div>
            </div>
        </div>
    </div>

    <script>
        function switchTab(tabId, el) {
            document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
            document.querySelectorAll('.panel-content').forEach(p => p.classList.remove('active'));
            const btn = el || document.querySelector(`.tab-btn[data-tab="${tabId}"]`);
            if (btn) btn.classList.add('active');
            const panel = document.getElementById('tab-' + tabId);
            if (panel) panel.classList.add('active');
        }

        // Knowledge Graph Interactive Controller & Dynamic Sync
        let network = null;
        let graphNodes = null;
        let graphEdges = null;
        let currentMode = 'ecosystem';
        let currentCountry = 'ALL';
        let currentCage = null;
        let physicsEnabled = true;
        let selectedNodeData = null;

        function initGraph() {
            const container = document.getElementById('graph-network');
            graphNodes = new vis.DataSet([]);
            graphEdges = new vis.DataSet([]);

            const options = {
                nodes: {
                    font: { color: '#ffffff', face: 'Inter', size: 12 },
                    borderWidth: 2,
                    shadow: { enabled: true, color: 'rgba(0,0,0,0.6)', size: 10, x: 0, y: 4 }
                },
                edges: {
                    font: { color: '#94a3b8', size: 10, align: 'middle' },
                    arrows: { to: { enabled: true, scaleFactor: 0.6 } },
                    smooth: { type: 'continuous' }
                },
                physics: {
                    barnesHut: { gravitationalConstant: -4000, springLength: 120, centralGravity: 0.15, damping: 0.09 },
                    stabilization: { iterations: 100 }
                },
                interaction: {
                    hover: true,
                    tooltipDelay: 150,
                    selectable: true,
                    multiselect: false
                }
            };

            network = new vis.Network(container, { nodes: graphNodes, edges: graphEdges }, options);

            // Handle node selection for floating HUD
            network.on('click', function(params) {
                if (params.nodes.length > 0) {
                    const nodeId = params.nodes[0];
                    const nodeData = graphNodes.get(nodeId);
                    if (nodeData) {
                        showNodeHud(nodeData);
                    }
                } else {
                    closeNodeHud();
                }
            });

            // Double click to focus or inspect profile
            network.on('doubleClick', function(params) {
                if (params.nodes.length > 0) {
                    const nodeData = graphNodes.get(params.nodes[0]);
                    if (nodeData && nodeData.cage) {
                        loadProfile(nodeData.cage);
                    }
                }
            });

            // Initial load of ecosystem graph
            loadGraphSubgraph({ mode: 'ecosystem', country: 'ALL' });
        }

        async function loadGraphSubgraph(params = {}) {
            const mode = params.mode || currentMode || 'ecosystem';
            const country = params.country || currentCountry || 'ALL';
            const cage = params.cage || currentCage || '';

            currentMode = mode;
            currentCountry = country;
            if (cage) currentCage = cage;

            const badgeText = document.getElementById('graph-status-text');
            if (badgeText) badgeText.innerHTML = 'Querying Oxigraph Triplestore...';

            let url = `/api/v1/graph/subgraph?mode=${encodeURIComponent(mode)}&country=${encodeURIComponent(country)}&limit=60`;
            if (cage && mode === 'company') {
                url += `&cage=${encodeURIComponent(cage)}`;
            }

            try {
                const res = await fetch(url);
                if (!res.ok) throw new Error('Failed to load subgraph from server');
                const data = await res.json();

                graphNodes.clear();
                graphEdges.clear();

                graphNodes.add(data.nodes);
                graphEdges.add(data.edges);

                if (badgeText) {
                    const modeLabel = mode === 'company' ? (data.stats.focused_name || 'Contractor Focus') : (mode === 'platform' ? 'Platform Clusters' : (mode === 'tier' ? 'Supply Tiers' : 'Allied Ecosystem'));
                    badgeText.innerHTML = `Live Sync &bull; <b>${modeLabel}</b> &bull; ${data.stats.total_nodes} Entities | ${data.stats.total_edges} Edges`;
                }

                network.fit({ animation: { duration: 700, easingFunction: 'easeInOutQuad' } });
            } catch (err) {
                if (badgeText) badgeText.innerHTML = `<span style="color:var(--accent-red)">Sync Error: ${err.message}</span>`;
            }
        }

        function showNodeHud(node) {
            selectedNodeData = node;
            const hud = document.getElementById('node-hud-card');
            const title = document.getElementById('hud-title');
            const meta = document.getElementById('hud-meta');
            const btnProfile = document.getElementById('hud-btn-profile');
            const btnFocus = document.getElementById('hud-btn-focus');

            if (!hud) return;

            title.innerText = node.label || 'Entity';
            
            let metaHtml = '';
            if (node.cage) {
                metaHtml += `<div>CAGE / NCAGE: <b style="color:var(--accent-cyan);">${node.cage}</b></div>`;
                metaHtml += `<div>Tier: <b style="color:#fff;">${node.tier || 'Enterprise'}</b></div>`;
                metaHtml += `<div>Country: <b style="color:#fff;">${node.country || 'CAN'}</b></div>`;
                btnProfile.style.display = 'block';
                btnFocus.style.display = 'block';
            } else {
                metaHtml += `<div>Classification: <b style="color:#fff;">${node.group || 'Resource'}</b></div>`;
                if (node.title) metaHtml += `<div style="font-size:10px; color:var(--text-secondary); margin-top:2px;">${node.title}</div>`;
                btnProfile.style.display = 'none';
                btnFocus.style.display = 'none';
            }

            meta.innerHTML = metaHtml;
            hud.style.display = 'flex';
        }

        function closeNodeHud() {
            const hud = document.getElementById('node-hud-card');
            if (hud) hud.style.display = 'none';
            selectedNodeData = null;
        }

        function hudOpenProfile() {
            if (selectedNodeData && selectedNodeData.cage) {
                switchTab('profile');
                loadProfile(selectedNodeData.cage);
                closeNodeHud();
            }
        }

        function hudFocusNode() {
            if (selectedNodeData && selectedNodeData.cage) {
                setGraphMode('company', document.getElementById('btn-mode-company'));
                loadGraphSubgraph({ cage: selectedNodeData.cage, mode: 'company' });
                closeNodeHud();
            }
        }

        function setGraphMode(mode, btn) {
            document.querySelectorAll('.graph-mode-btn').forEach(b => b.classList.remove('active'));
            if (btn) btn.classList.add('active');
            currentMode = mode;
            loadGraphSubgraph({ mode: mode, country: currentCountry, cage: currentCage });
        }

        function onGraphFilterChange() {
            const sel = document.getElementById('graph-country-select');
            currentCountry = sel ? sel.value : 'ALL';
            loadGraphSubgraph({ mode: currentMode, country: currentCountry, cage: currentCage });
        }

        function togglePhysics() {
            physicsEnabled = !physicsEnabled;
            network.setOptions({ physics: { enabled: physicsEnabled } });
            const btn = document.getElementById('btn-physics');
            if (btn) {
                btn.innerHTML = physicsEnabled ? '⏸ Freeze' : '▶ Unfreeze';
                btn.style.color = physicsEnabled ? 'var(--text-secondary)' : 'var(--accent-gold)';
            }
        }

        function fitGraph() {
            if (network) network.fit({ animation: { duration: 700, easingFunction: 'easeInOutQuad' } });
        }

        function reloadGraph() {
            loadGraphSubgraph({ mode: currentMode, country: currentCountry, cage: currentCage });
        }

        // Search Auto-Suggestions
        let searchTimeout = null;
        function handleSearchSuggestions(val) {
            clearTimeout(searchTimeout);
            const box = document.getElementById('search-suggestions');
            if (!val || val.trim().length < 2) {
                if (box) box.style.display = 'none';
                return;
            }
            searchTimeout = setTimeout(async () => {
                try {
                    const res = await fetch(`/api/v1/companies?q=${encodeURIComponent(val.trim())}&limit=6`);
                    const data = await res.json();
                    if (!data.companies || data.companies.length === 0) {
                        box.style.display = 'none';
                        return;
                    }
                    box.innerHTML = data.companies.map(c => `
                        <div style="padding:8px 12px; cursor:pointer; border-bottom:1px solid rgba(255,255,255,0.05); font-size:12px;" 
                             onmouseover="this.style.background='rgba(0,242,254,0.1)'" 
                             onmouseout="this.style.background='transparent'" 
                             onclick="loadProfile('${c.cage}'); document.getElementById('search-suggestions').style.display='none';">
                            <span style="font-weight:700; color:#fff;">${c.name}</span>
                            <span style="color:var(--accent-cyan); font-family:'JetBrains Mono'; font-size:11px; margin-left:6px;">(${c.cage})</span>
                            <span style="color:var(--text-secondary); font-size:10.5px; float:right;">${c.city || ''}, ${c.province || c.country}</span>
                        </div>
                    `).join('');
                    box.style.display = 'block';
                } catch (e) {
                    if (box) box.style.display = 'none';
                }
            }, 180);
        }

        document.addEventListener('click', function(e) {
            const box = document.getElementById('search-suggestions');
            const inp = document.getElementById('profile-search-input');
            if (box && !box.contains(e.target) && e.target !== inp) {
                box.style.display = 'none';
            }
        });

        // Load 360-degree Company Profile (by Name or CAGE)
        async function loadProfile(query) {
            if (!query) return;
            const box = document.getElementById('search-suggestions');
            if (box) box.style.display = 'none';
            
            const cleanQuery = query.trim();
            const container = document.getElementById('profile-card-container');
            container.innerHTML = '<div style="color:var(--accent-cyan); font-size:12px; padding:12px;">Querying W3C Knowledge Graph for ' + cleanQuery + '...</div>';

            try {
                const response = await fetch(`/api/v1/companies/${encodeURIComponent(cleanQuery)}`);
                if (!response.ok) throw new Error('Contractor \\'' + cleanQuery + '\\' not found in Knowledge Graph.');
                const p = await response.json();

                document.getElementById('profile-search-input').value = p.legal_name + ' (' + p.cage_code + ')';

                // Highlight quick pill if matches
                document.querySelectorAll('.pill-btn').forEach(btn => {
                    btn.classList.toggle('active', btn.textContent.includes(p.cage_code));
                });

                let html = `
                    <div class="profile-card">
                        <div class="profile-header">
                            <div>
                                <div class="profile-name">${p.legal_name}</div>
                                <div class="profile-subtitle">
                                    <b>DBA:</b> ${p.trade_name || p.legal_name} &bull; 
                                    <b>HQ:</b> ${p.city}, ${p.province ? p.province + ', ' : ''}${p.country} &bull; 
                                    <a href="${p.website}" target="_blank" style="color:var(--accent-cyan); text-decoration:none;">${p.website ? p.website.replace('https://', '') : 'Portal'} &#8599;</a>
                                </div>
                            </div>
                            <div style="display:flex; flex-direction:column; align-items:flex-end; gap:6px;">
                                <span class="tier-badge">${p.tier}</span>
                                <span style="font-family:'JetBrains Mono'; font-size:11px; color:var(--text-secondary);">CAGE: <b style="color:#fff;">${p.cage_code}</b></span>
                            </div>
                        </div>

                        <!-- 4-Grid Regulatory & Security Posture -->
                        <div class="grid-2col">
                            <div>
                                <div class="grid-item-lbl">Controlled Goods (CGP)</div>
                                <div class="grid-item-val" style="color:${p.controlled_goods ? 'var(--accent-emerald)' : 'var(--accent-red)'}">
                                    ${p.controlled_goods ? '&#10003; VERIFIED REGISTERED' : '&times; NON-CGP'}
                                </div>
                            </div>
                            <div>
                                <div class="grid-item-lbl">ITAR / EAR Posture</div>
                                <div class="grid-item-val" style="color:${p.itar_compliant ? 'var(--accent-cyan)' : 'var(--text-secondary)'}">
                                    ${p.itar_compliant ? '&#10003; ITAR COMPLIANT' : 'COMMERCIAL ONLY'}
                                </div>
                            </div>
                            <div>
                                <div class="grid-item-lbl">Security Classification</div>
                                <div class="grid-item-val" style="color:var(--accent-gold);">
                                    ${p.controlled_goods ? 'CLASS-A DEFENCE' : 'STANDARD COMMERCIAL'}
                                </div>
                            </div>
                            <div>
                                <div class="grid-item-lbl">Corporate Ownership</div>
                                <div class="grid-item-val">
                                    ${p.parent_company ? 'Subsidiary of ' + p.parent_company : 'Independent Entity'}
                                </div>
                            </div>
                        </div>

                        <!-- Quality & Aerospace Certifications -->
                        <div>
                            <div class="section-subhead">&#128737; Quality & Defence Certifications (${p.certifications.length})</div>
                            <div style="display:flex; gap:6px; flex-wrap:wrap;">
                                ${p.certifications.length > 0 ? p.certifications.map(c => `<span class="item-chip">${c}</span>`).join('') : '<span style="color:var(--text-secondary); font-size:11px;">No public certifications codified.</span>'}
                            </div>
                        </div>

                        <!-- Manufactured Products -->
                        <div>
                            <div class="section-subhead">&#9881; Manufactured Products & Hardware Systems (${p.products.length})</div>
                            ${p.products.length > 0 ? p.products.map(prod => `
                                <div style="background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.06); padding:8px 10px; border-radius:4px; font-size:12px; font-weight:600; color:#fff; margin-bottom:4px; display:flex; justify-content:space-between;">
                                    <span>${prod}</span>
                                    <span style="font-size:10px; color:var(--accent-purple); font-family:'JetBrains Mono';">HARDWARE SYSTEM</span>
                                </div>
                            `).join('') : '<span style="color:var(--text-secondary); font-size:11px;">Specialized engineered subsystem component provider.</span>'}
                        </div>

                        <!-- Operational Services -->
                        <div>
                            <div class="section-subhead">&#128295; Operational Services & In-Service Support (${(p.services || []).length})</div>
                            ${(p.services && p.services.length > 0) ? p.services.map(s => `
                                <div style="background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.06); padding:8px 10px; border-radius:4px; font-size:12px; color:#e2e8f0; margin-bottom:4px;">
                                    ${s}
                                </div>
                            `).join('') : '<div style="background:rgba(255,255,255,0.02); padding:6px 10px; border-radius:4px; font-size:11px; color:var(--text-secondary);">Depot-Level In-Service Support (ISS), Engineering Integration & Maintenance Overhaul.</div>'}
                        </div>

                        <!-- Technical Capabilities & TRL Readiness -->
                        <div>
                            <div class="section-subhead">&#128640; Codified Technical Capabilities & TRL Readiness (${p.capabilities.length})</div>
                            <div style="display:flex; flex-direction:column; gap:8px;">
                                ${p.capabilities.map(cap => `
                                    <div class="cap-box">
                                        <div class="cap-title">
                                            <span>${cap.title}</span>
                                            <span style="color:var(--accent-gold); font-family:'JetBrains Mono'; font-size:11px;">TRL ${cap.trl || '9'}/9</span>
                                        </div>
                                        <div class="cap-desc">${cap.desc}</div>
                                        <div style="font-size:10px; color:var(--accent-cyan); font-family:'JetBrains Mono'; margin-top:2px;">
                                            KIC: ${(cap.kic || 'ISED Priority Domain').split('#').pop().replace('KIC_', '')}
                                        </div>
                                    </div>
                                `).join('')}
                            </div>
                        </div>

                        <!-- Quick Strategic Actions -->
                        <div style="display:flex; gap:8px; margin-top:4px;">
                            <button class="btn-action" style="flex:1; padding:8px; font-size:11px;" onclick="document.getElementById('dossier-cage').value='${p.cage_code}'; switchTab('dossier'); fetchDossier();">View Intelligence Dossier</button>
                            <button class="btn-action" style="flex:1; padding:8px; font-size:11px; background:linear-gradient(135deg, #f59e0b 0%, #d97706 100%);" onclick="document.getElementById('consortium-title').value='Strategic Bid with ' + '${p.legal_name}'; switchTab('consortium'); assembleConsortium();">Add to Consortium</button>
                        </div>
                    </div>
                `;
                container.innerHTML = html;

                // Automatically synchronize and focus the visual Knowledge Graph
                currentCage = p.cage_code;
                const compBtn = document.getElementById('btn-mode-company');
                if (compBtn) {
                    document.querySelectorAll('.graph-mode-btn').forEach(b => b.classList.remove('active'));
                    compBtn.classList.add('active');
                }
                loadGraphSubgraph({ cage: p.cage_code, mode: 'company' });
            } catch (e) {
                container.innerHTML = `<div style="color:var(--accent-red); font-size:12px; padding:12px;">Error: ${e.message}</div>`;
            }
        }

        async function runMatching() {
            const query = document.getElementById('match-query').value;
            const trl = document.getElementById('match-trl').value;
            const cgp = document.getElementById('match-cgp').value === 'true';

            const payload = {
                query_text: query,
                min_trl: trl ? parseInt(trl) : null,
                require_controlled_goods: cgp,
                top_k: 5
            };

            const resDiv = document.getElementById('match-results');
            resDiv.innerHTML = '<div style="color:var(--accent-cyan); font-size:12px;">Computing semantic embeddings and graph constraints...</div>';

            try {
                const response = await fetch('/api/v1/match', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                });
                const data = await response.json();

                let html = `<div style="font-size:11px; color:var(--text-secondary); margin-bottom:6px;"><b>Intent:</b> ${data.parsed_intent.cleaned_query} | <b>Geo:</b> ${data.parsed_intent.target_country || 'ALL'} (${data.parsed_intent.target_region || 'National'}) | <b>Latency:</b> ${data.execution_time_ms}ms</div>`;

                data.top_matches.forEach(m => {
                    html += `
                        <div class="match-card" onclick="loadProfile('${m.cage_code}'); switchTab('profile');">
                            <div class="match-header">
                                <span class="match-title">#${m.rank} ${m.legal_name}</span>
                                <span class="score-pill">${(m.overall_score * 100).toFixed(1)}%</span>
                            </div>
                            <div class="match-meta">
                                <span><b>CAGE:</b> ${m.cage_code}</span>
                                <span>${m.city}, ${m.province || m.country}</span>
                                <span>${m.tier}</span>
                                <span style="color:${m.controlled_goods ? 'var(--accent-emerald)' : 'var(--accent-red)'}"><b>${m.controlled_goods ? 'CGP CLEARED' : 'NON-CGP'}</b></span>
                            </div>
                            <div class="match-capability">${m.matched_capability_title}</div>
                            <div style="font-size:10.5px; color:var(--accent-cyan); text-align:right;">Click to view 360&deg; Company Profile &#8594;</div>
                        </div>
                    `;
                });
                resDiv.innerHTML = html;
            } catch (e) {
                resDiv.innerHTML = `<div style="color:var(--accent-red);">Error: ${e.message}</div>`;
            }
        }

        async function assembleConsortium() {
            const title = document.getElementById('consortium-title').value;
            const wps = document.getElementById('consortium-wps').value.split('\\n').filter(x => x.trim().length > 0);

            const resDiv = document.getElementById('consortium-results');
            resDiv.innerHTML = '<div style="color:var(--accent-cyan); font-size:12px;">Assembling prime & SME consortium...</div>';

            try {
                const response = await fetch('/api/v1/consortium', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ program_title: title, required_capabilities: wps, target_country: 'CAN' })
                });
                const data = await response.json();

                let html = `
                    <div style="background:var(--bg-card); border:1px solid var(--border-color); border-radius:6px; padding:14px; margin-top:8px;">
                        <div style="color:var(--accent-gold); font-size:11px; font-weight:800; text-transform:uppercase;">Proposed Strategic Consortium</div>
                        <div style="font-size:14px; font-weight:700; margin:4px 0 8px;">${data.program_title}</div>
                        <div style="display:grid; grid-template-columns:1fr 1fr; gap:8px; font-size:11px; margin-bottom:12px;">
                            <div>Coverage: <b style="color:var(--accent-emerald)">${data.capability_coverage_pct}%</b></div>
                            <div>Canadian Content: <b style="color:var(--accent-cyan)">${data.estimated_canadian_content_value}%</b></div>
                            <div>ITB Multiplier: <b>${data.total_itb_multiplier_score}x</b></div>
                            <div>Compliance: <b style="color:var(--accent-emerald)">100% CGP</b></div>
                        </div>
                        <div style="font-size:11px; font-weight:700; color:#fff; margin-bottom:4px;">Lead Prime Integrator:</div>
                        <div style="background:rgba(0,242,254,0.1); padding:8px; border-radius:4px; font-size:12px; margin-bottom:8px; cursor:pointer;" onclick="loadProfile('${data.lead_prime.cage_code}'); switchTab('profile');">
                            <b>${data.lead_prime.legal_name}</b> (${data.lead_prime.city}, ${data.lead_prime.province}) - ${data.lead_prime.role}
                        </div>
                        <div style="font-size:11px; font-weight:700; color:#fff; margin-bottom:4px;">Teaming Partners & SMEs:</div>
                        ${data.teaming_partners.map(p => `
                            <div style="background:rgba(255,255,255,0.03); padding:8px; border-radius:4px; font-size:11px; margin-bottom:4px; border-left:2px solid var(--accent-gold); cursor:pointer;" onclick="loadProfile('${p.cage_code}'); switchTab('profile');">
                                <b>${p.legal_name}</b> (${p.city}, ${p.province}) - ${p.role}<br/>
                                <span style="color:var(--text-secondary)">Assigned: ${p.assigned_capabilities.join(', ')}</span>
                            </div>
                        `).join('')}
                    </div>
                `;
                resDiv.innerHTML = html;
            } catch (e) {
                resDiv.innerHTML = `<div style="color:var(--accent-red);">Error: ${e.message}</div>`;
            }
        }

        async function fetchDossier() {
            const cage = document.getElementById('dossier-cage').value.trim();
            const resDiv = document.getElementById('dossier-results');
            resDiv.innerHTML = '<div style="color:var(--accent-cyan); font-size:12px;">Compiling intelligence dossier for ' + cage + '...</div>';

            try {
                const response = await fetch(`/api/v1/dossier/${cage}`);
                if (!response.ok) throw new Error('Contractor CAGE code not found');
                const data = await response.json();
                
                let p = data.profile;
                let html = `
                    <div style="background:var(--bg-card); border:1px solid var(--border-color); border-radius:6px; padding:16px;">
                        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
                            <div>
                                <span style="font-size:16px; font-weight:800; color:#fff;">${p.legal_name}</span>
                                <div style="font-size:11px; color:var(--text-secondary); margin-top:2px;">CAGE: <b style="color:var(--accent-cyan);">${p.cage_code}</b> | HQ: ${p.city}, ${p.country}</div>
                            </div>
                            <span class="badge-live" style="color:var(--accent-cyan); border-color:var(--accent-cyan);">${p.tier}</span>
                        </div>
                        
                        <div style="display:grid; grid-template-columns:1fr 1fr; gap:8px; font-size:11px; margin-bottom:12px; background:rgba(0,0,0,0.25); padding:10px; border-radius:4px;">
                            <div>Rating: <b style="color:var(--accent-emerald)">${data.metrics.compliance_rating}</b></div>
                            <div>Average TRL: <b style="color:var(--accent-gold)">TRL ${data.metrics.average_trl} / 9.0</b></div>
                            <div>CGP Clearance: <b style="color:${p.controlled_goods ? 'var(--accent-emerald)' : 'var(--accent-red)'}">${p.controlled_goods ? 'VERIFIED' : 'NONE'}</b></div>
                            <div>ITAR Posture: <b style="color:var(--accent-cyan)">${p.itar_compliant ? 'COMPLIANT' : 'N/A'}</b></div>
                        </div>

                        <div style="font-size:11px; font-weight:700; color:#fff; margin-bottom:4px;">Active Quality & Defence Certifications:</div>
                        <div style="display:flex; gap:6px; flex-wrap:wrap; margin-bottom:12px;">
                            ${p.certifications.map(c => `<span style="font-size:10px; background:rgba(79,172,254,0.15); border:1px solid rgba(79,172,254,0.4); color:#93c5fd; padding:3px 7px; border-radius:4px;">${c}</span>`).join('')}
                        </div>

                        <div style="font-size:11px; font-weight:700; color:#fff; margin-bottom:4px;">Core Capabilities & Products:</div>
                        ${p.capabilities.map(cap => `
                            <div style="background:rgba(255,255,255,0.03); padding:8px; border-radius:4px; font-size:11px; margin-bottom:6px; border-left:2px solid var(--accent-cyan);">
                                <b>${cap.title}</b> (TRL ${cap.trl})<br/>
                                <span style="color:var(--text-secondary)">${cap.desc}</span>
                            </div>
                        `).join('')}
                    </div>
                `;
                resDiv.innerHTML = html;
            } catch (e) {
                resDiv.innerHTML = `<div style="color:var(--accent-red);">Error: ${e.message}</div>`;
            }
        }

        async function runSparql() {
            const query = document.getElementById('sparql-query').value;
            const container = document.getElementById('sparql-output-container');
            container.innerHTML = '<div style="color:var(--accent-cyan); font-size:12px;">Executing SPARQL graph query...</div>';

            try {
                const response = await fetch('/api/v1/sparql', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ query: query })
                });
                const data = await response.json();
                
                if (!data.results || data.results.length === 0) {
                    container.innerHTML = '<pre>Query returned 0 rows.</pre>';
                    return;
                }

                // Render clean data table
                const keys = Object.keys(data.results[0]);
                let tableHtml = `
                    <div style="font-size:11px; color:var(--text-secondary); margin-bottom:6px;">Returned <b>${data.row_count}</b> graph records across Oxigraph triplestore:</div>
                    <div style="max-height:420px; overflow-y:auto; border:1px solid var(--border-color); border-radius:6px;">
                        <table class="sparql-table">
                            <thead>
                                <tr>${keys.map(k => `<th>${k}</th>`).join('')}</tr>
                            </thead>
                            <tbody>
                                ${data.results.map(row => `
                                    <tr>${keys.map(k => `<td>${row[k] || ''}</td>`).join('')}</tr>
                                `).join('')}
                            </tbody>
                        </table>
                    </div>
                `;
                container.innerHTML = tableHtml;
            } catch (e) {
                container.innerHTML = `<pre style="color:var(--accent-red);">Error: ${e.message}</pre>`;
            }
        }

        window.onload = function() {
            initGraph();
            loadProfile('L2108'); // Default load Flying Colours Corp
        };
    </script>
</body>
</html>
"""
