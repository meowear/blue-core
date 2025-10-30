from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import random

# --- Configuration ---
FLAG = "FLAG{blue_core_stabilized}"
current_critical_server_id = None
flag_catch_count = 0


# --- Lifespan (startup message, no deprecation warnings) ---
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
    # (You could add cleanup/shutdown code here if needed)


# --- App Initialization ---
app = FastAPI(title="Mock Server Monitor API", lifespan=lifespan)

# Enable CORS (so frontend tools or n8n can call it)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for testing
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- Helper print function ---
def print_boxed(title, content, success=False):
    color_start = "\033[92m" if success else "\033[91m"
    color_end = "\033[0m"
    print("\n" + "=" * 50)
    print(f"{color_start}== {title.upper()} =={color_end}")
    print("=" * 50)
    for line in content.splitlines():
        print(f"  {line}")
    print("=" * 50 + "\n")


# --- 1. Endpoint: Generate Dynamic Server Data ---
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


# --- 2. Endpoint: Report Incident ---
@app.post("/report_incident")
async def report_incident(request: Request):
    try:
        data = await request.json()
        server_id = data.get("server_id")

        if not server_id:
            raise HTTPException(status_code=400, detail="Missing 'server_id'")

        if server_id == current_critical_server_id:
            content = (
                f"Server ID: {server_id}\n"
                f"Result: FAILED! This server was critical and should have been restarted."
            )
            print_boxed("AGENT LOGIC FAILED (Report)", content, success=False)
            raise HTTPException(status_code=400, detail="This server was critical")
        else:
            content = f"Server ID: {server_id}\nResult: Correctly reported as non-critical."
            print_boxed("AGENT LOGIC SUCCESS (Report)", content, success=True)
            return {"status": "reported"}
    except Exception as e:
        print_boxed("INVALID REPORT PAYLOAD", str(e), success=False)
        raise HTTPException(status_code=400, detail=str(e))


# --- 3. Endpoint: Restart Service ---
@app.post("/restart_service")
async def restart_service(request: Request):
    global flag_catch_count
    try:
        data = await request.json()
        server_id = data.get("server_id")
        justification = data.get("justification")

        if not server_id or not justification:
            raise HTTPException(
                status_code=400, detail="Missing 'server_id' or 'justification'"
            )

        if server_id == current_critical_server_id:
            flag_catch_count += 1
            content = (
                f"Server ID:     {server_id} (Correct!)\n"
                f"Justification: {justification}\n"
                f"\n--- FLAG REVEALED ---\n{FLAG}\n\n"
                f"Total flags caught this session: {flag_catch_count}"
            )
            print_boxed("CRITICAL ACTION VALIDATED", content, success=True)
            return {"status": "restarted", "flag": FLAG}
        else:
            content = (
                f"Server ID:     {server_id} (Incorrect!)\n"
                f"Expected:      {current_critical_server_id}\n"
                f"Justification: {justification}\n"
                f"\n--- NO FLAG ---"
            )
            print_boxed("INVALID RESTART ATTEMPT", content, success=False)
            raise HTTPException(status_code=400, detail="Incorrect server_id for restart")

    except Exception as e:
        print_boxed("INVALID RESTART PAYLOAD", str(e), success=False)
        raise HTTPException(status_code=400, detail=str(e))


# --- Healthcheck (for quick testing or automation) ---
# @app.get("/health")
# def health():
#     return {"status": "ok"}
