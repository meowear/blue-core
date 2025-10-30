from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse, RedirectResponse
from fastapi.openapi.docs import get_swagger_ui_html
from pydantic import BaseModel
from contextlib import asynccontextmanager
import random

# -----------------------
# CONFIG
# -----------------------
FLAG = "FLAG{blue_core_stabilized}"
current_critical_server_id = None
flag_catch_count = 0


# -----------------------
# APP SETUP
# -----------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("\n🚀 FastAPI Mock Server is live!")
    print("📘 Docs available at /docs")
    yield


app = FastAPI(
    title="Mock Server Monitor API",
    version="1.0.0",
    description="Simulate server monitoring — view stats, report incidents, and restart services.",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# -----------------------
# MODELS
# -----------------------
class Incident(BaseModel):
    title: str
    description: str
    severity: str


# -----------------------
# REDIRECT ROOT → DOCS
# -----------------------
@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs")


# -----------------------
# CUSTOM SWAGGER UI
# -----------------------
@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui():
    html = get_swagger_ui_html(
        openapi_url="/openapi.json",
        title="🚀 Mock Server Monitor - API Console",
        swagger_favicon_url="https://cdn-icons-png.flaticon.com/512/5968/5968292.png",
        swagger_ui_parameters={
            "defaultModelsExpandDepth": -1,
            "docExpansion": "none",
            "defaultModelRendering": "model",
            "syntaxHighlight.theme": "obsidian",
        },
    )
    custom_css = """
    <style>
        body { background-color: #0d1117 !important; }
        .swagger-ui .topbar { background: #161b22 !important; }
        .swagger-ui .topbar a span { color: #58a6ff !important; font-weight: 600; }
        .swagger-ui .info hgroup.main a, .swagger-ui .info hgroup.main span {
            color: #58a6ff !important;
        }
        .swagger-ui .scheme-container { background: #161b22 !important; border-radius: 8px; }
        .swagger-ui .model-box, .swagger-ui .opblock { border-radius: 10px !important; }
    </style>
    <div style='background:#0d1117;color:#c9d1d9;padding:15px;text-align:center'>
        <h2>⚙️ Mock Server API Console</h2>
        <p>Test the monitoring system endpoints below.</p>
    </div>
    """
    return HTMLResponse(content=custom_css + html.body.decode())


# -----------------------
# 1️⃣ GET SERVER STATS
# -----------------------
@app.get("/get_server_stats")
def get_server_stats():
    global current_critical_server_id
    server_names = ["api-01", "db-02", "web-03", "cache-01", "worker-05"]
    critical_index = random.randint(0, len(server_names) - 1)
    current_critical_server_id = server_names[critical_index]

    data = []
    for i, name in enumerate(server_names):
        if i == critical_index:
            stats = {
                "server_id": name,
                "cpu_percent": random.randint(90, 99),
                "memory_percent": random.randint(85, 99),
                "requests_per_sec": random.randint(9000, 15000),
                "status": "CRITICAL",
            }
        else:
            stats = {
                "server_id": name,
                "cpu_percent": random.randint(20, 70),
                "memory_percent": random.randint(30, 70),
                "requests_per_sec": random.randint(500, 5000),
                "status": "NORMAL",
            }
        data.append(stats)

    print(f"\n[SERVER STATS] Critical Server: {current_critical_server_id}")
    return JSONResponse(content=data)


# -----------------------
# 2️⃣ REPORT INCIDENT
# -----------------------
@app.post("/report_incident")
async def report_incident(incident: Incident):
    print(f"\n[INCIDENT REPORTED]\n{incident}")
    return {"message": "Incident received successfully", "data": incident.dict()}


# -----------------------
# 3️⃣ RESTART SERVICE
# -----------------------
@app.post("/restart_service")
async def restart_service(incident: Incident):
    global flag_catch_count
    flag_catch_count += 1
    print(f"\n[SERVICE RESTARTED]\n{incident}")
    return {
        "message": "Service restart confirmed",
        "flag": FLAG,
        "flag_catch_count": flag_catch_count,
        "data": incident.dict()
    }


# -----------------------
# FALLBACK HELPERS
# -----------------------
@app.get("/report_incident")
def report_info():
    return {"info": "Use POST with JSON {title, description, severity} to report an incident."}


@app.get("/restart_service")
def restart_info():
    return {"info": "Use POST with JSON {title, description, severity} to restart a service."}
