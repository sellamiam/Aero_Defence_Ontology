"""
FastAPI Application Entrypoint for Aerospace & Defence Knowledge Graph & Matching Engine.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from api.routes import router

from fastapi.responses import HTMLResponse
from api.dashboard import DASHBOARD_HTML

app = FastAPI(
    title="Aerospace & Defence Ontology & Matching Engine API",
    description=(
        "Production REST and SPARQL 1.1 query interface for the Canadian, US, UK, EU, "
        "Australian, New Zealand, and Indian Aerospace & Defence ontology, company profiles, "
        "products, services, capabilities, and matching engine."
    ),
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Mount local static assets
static_dir = Path(__file__).resolve().parent.parent / "static"
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

# Enable CORS for external application integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api/v1")


@app.get("/", response_class=HTMLResponse)
def root_dashboard():
    """Serves the Executive Visual Command Center directly at root URL."""
    return HTMLResponse(content=DASHBOARD_HTML, status_code=200)
