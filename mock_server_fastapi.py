from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from pydantic import BaseModel
import random

# --- Configuration ---
FLAG = "FLAG{blue_core_stabilized}"
current_critical_server_id = None
flag_catch_count = 0

# --- Define Incident Schema ---
class Incident(BaseModel):
    title: str
    description: str
    severity: str

class ServerAction(BaseModel):
    server_id: str
    justification: str | None = None

# --- Lifespan ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("\n" + "*" * 50)
    print("🚀 FastAPI Mock Server is RUNNING")
    print("Visit interactive docs at: http://127.0.0.1:8000/docs")
    print("\nEndpoints:")
    print("  1. GET  → /get_server_stats")
    print("  2. POST → /restart_service")
    print("  3. POST → /report_incident")
    print("*" * 50 + "\n")
    yield

# --- App Initialization ---
app = FastAPI(title="Mock Server Monitor API", lifespan=lifespan)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Helper ---
def print_boxed(title, content, success=False):
    color_start = "\033[92m" if success else "\033[91m"
    color_end = "\033[0m"
    print("\n" + "=" * 50)
    print(f"{color_start}== {title.upper()} =={color_end}")
    print("=" * 50)
    for line in content.splitlines():
        print(f"  {line}")
    print("=" * 50 + "\n")

# --- 1. GET: Generate Dynamic Server Data ---
@app.get("/get_server_stats")
def get_server_stats():
    global current_critical_server_id

    server_names = ["api-01", "db-02", "web-03", "cache-01", "worker-05"]
    data = []

    critical_server_index = random.randint(0, len(server_names) - 1)
    current_critical_server_id = server_names[critical_server_index]

    for i, name in enumerate(server_names):
        if i == critical_server_index:
            stats = {
                "server_id": name,
                "cpu_percent": random.randint(91, 99),
                "memory_percent": random.randint(91, 99),
                "requests_per_sec": random.randint(10000, 20000),
            }
        else:
            stats = {
                "server_id": name,
                "cpu_percent": random.randint(20, 89),
                "memory_percent": random.randint(30, 89),
                "requests_per_sec": random.randint(500, 9000),
            }
        data.append(stats)

    print_boxed(
        f"DATA GENERATED (Critical: {current_critical_server_id})",
        f"{data}",
        success=True,
    )
    return JSONResponse(content=data)

# --- 2. POST: Report Incident ---
@app.post("/report_incident")
async def report_incident(incident: Incident):
    global current_critical_server_id
    print_boxed("INCIDENT REPORTED", f"{incident.model_dump()}", success=True)
    return {"message": "Incident received", "data": incident}

# --- 3. POST: Restart Service ---
@app.post("/restart_service")
async def restart_service(action: ServerAction):
    global flag_catch_count, current_critical_server_id

    if not action.server_id:
        raise HTTPException(status_code=400, detail="Missing 'server_id'")

    if action.server_id == current_critical_server_id:
        flag_catch_count += 1
        content = (
            f"Server ID:     {action.server_id} (Correct!)\n"
            f"Justification: {action.justification}\n"
            f"\n--- FLAG REVEALED ---\n{FLAG}\n\n"
            f"Total flags caught this session: {flag_catch_count}"
        )
        print_boxed("CRITICAL ACTION VALIDATED", content, success=True)
        return {"status": "restarted", "flag": FLAG}
    else:
        content = (
            f"Server ID:     {action.server_id} (Incorrect!)\n"
            f"Expected:      {current_critical_server_id}\n"
            f"Justification: {action.justification}\n"
            f"\n--- NO FLAG ---"
        )
        print_boxed("INVALID RESTART ATTEMPT", content, success=False)
        raise HTTPException(status_code=400, detail="Incorrect server_id for restart")

# --- Health Check ---
@app.get("/health")
def health():
    return {"status": "ok"}
