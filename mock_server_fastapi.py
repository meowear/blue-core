from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
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
# APP INITIALIZATION
# -----------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("\n🚀 FastAPI Mock Server is running on Render!")
    print("📘 Swagger Docs available at: /docs")
    yield

app = FastAPI(
    title="Mock Server Monitor API",
    version="1.1.0",
    description="Simulated monitoring API for testing incident reports and restarts.",
    lifespan=lifespan,
)

# Enable CORS (for n8n or frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------
# SCHEMA
# -----------------------
class Incident(BaseModel):
    title: str
    description: str
    severity: str


# -----------------------
# HELPER
# -----------------------
def print_boxed(title, content, success=False):
    color = "\033[92m" if success else "\033[91m"
    print("\n" + "=" * 60)
    print(f"{color}{title}{'\033[0m'}")
    print("=" * 60)
    print(content)
    print("=" * 60 + "\n")


# -----------------------
# HOMEPAGE (UI)
# -----------------------
@app.get("/", response_class=HTMLResponse)
def home():
    html = """
    <html>
        <head>
            <title>Mock Server Monitor API</title>
            <style>
                body {
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    background-color: #0d1117;
                    color: #c9d1d9;
                    text-align: center;
                    margin: 0;
                    padding: 0;
                }
                h1 {
                    color: #58a6ff;
                    margin-top: 60px;
                }
                .container {
                    margin: 40px auto;
                    width: 80%;
                    max-width: 600px;
                    background-color: #161b22;
                    border-radius: 12px;
                    padding: 30px;
                    box-shadow: 0 0 12px rgba(56,139,253,0.2);
                }
                a {
                    color: #58a6ff;
                    text-decoration: none;
                    font-weight: 500;
                }
                a:hover {
                    text-decoration: underline;
                }
                .endpoint {
                    background-color: #21262d;
                    border-radius: 8px;
                    padding: 12px;
                    margin: 12px 0;
                    font-family: monospace;
                }
            </style>
        </head>
        <body>
            <h1>Mock Server Monitor API</h1>
            <div class="container">
                <p>This API simulates a monitoring system with three endpoints:</p>
                <div class="endpoint">GET /get_server_stats → Get live server stats</div>
                <div class="endpoint">POST /report_incident → Report an incident</div>
                <div class="endpoint">POST /restart_service → Restart a service</div>
                <p>Use the <a href="/docs">Swagger UI</a> for interactive testing.</p>
            </div>
        </body>
    </html>
    """
    return HTMLResponse(content=html)


# -----------------------
# 1️⃣ Get Server Stats
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

    print_boxed(f"SERVER STATS GENERATED (Critical: {current_critical_server_id})", str(data), success=True)
    return JSONResponse(content=data)


# -----------------------
# 2️⃣ Report Incident
# -----------------------
@app.post("/report_incident")
async def report_incident(incident: Incident):
    print_boxed("INCIDENT REPORTED", str(incident), success=True)
    return {"message": "Incident received successfully", "data": incident.dict()}


# -----------------------
# 3️⃣ Restart Service
# -----------------------
@app.post("/restart_service")
async def restart_service(incident: Incident):
    global flag_catch_count
    flag_catch_count += 1
    print_boxed("SERVICE RESTARTED", str(incident), success=True)
    return {
        "message": "Service restart confirmed",
        "flag": FLAG,
        "flag_catch_count": flag_catch_count,
        "data": incident.dict()
    }


# -----------------------
# Optional GET Fallbacks (prevents 405)
# -----------------------
@app.get("/report_incident")
def report_info():
    return {"info": "Use POST with JSON {title, description, severity} to report an incident."}

@app.get("/restart_service")
def restart_info():
    return {"info": "Use POST with JSON {title, description, severity} to restart a service."}
