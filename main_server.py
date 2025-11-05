import uvicorn
import random
import json
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any

# --- Initialize FastAPI App ---
app = FastAPI(
    title="Blue Core Challenge Server",
    description="Provides server batches and checks flag submissions."
)

# --- POOL 1: Servers for "REPORT" (Non-Critical) ---
# Copied from your generate_batch.py
REPORT_POOL = [
    {"server_id": "srv-us-east-db-01", "cpu_percent": 95, "memory_percent": 88, "requests_per_sec": 9000},
    {"server_id": "srv-us-west-cache-01", "cpu_percent": 89, "memory_percent": 96, "requests_per_sec": 21000},
    {"server_id": "srv-eu-west-api-01", "cpu_percent": 88, "memory_percent": 89, "requests_per_sec": 18000},
    {"server_id": "srv-apac-batch-01", "cpu_percent": 98, "memory_percent": 75, "requests_per_sec": 500},
    {"server_id": "srv-eu-central-web-01", "cpu_percent": 80, "memory_percent": 75, "requests_per_sec": 9000},
    {"server_id": "srv-us-east-web-01", "cpu_percent": 65, "memory_percent": 70, "requests_per_sec": 8000},
    {"server_id": "srv-us-east-web-02", "cpu_percent": 72, "memory_percent": 65, "requests_per_sec": 8500},
    {"server_id": "srv-us-west-web-01", "cpu_percent": 50, "memory_percent": 68, "requests_per_sec": 7000},
    {"server_id": "srv-sa-east-web-01", "cpu_percent": 25, "memory_percent": 40, "requests_per_sec": 500},
    {"server_id": "srv-eu-west-api-02", "cpu_percent": 85, "memory_percent": 80, "requests_per_sec": 15000},
    {"server_id": "srv-apac-api-01", "cpu_percent": 82, "memory_percent": 78, "requests_per_sec": 14500},
    {"server_id": "srv-eu-central-api-01", "cpu_percent": 79, "memory_percent": 81, "requests_per_sec": 15200},
    {"server_id": "srv-us-east-app-01", "cpu_percent": 40, "memory_percent": 50, "requests_per_sec": 3000},
    {"server_id": "srv-us-east-app-02", "cpu_percent": 45, "memory_percent": 55, "requests_per_sec": 3200},
    {"server_id": "srv-us-west-app-01", "cpu_percent": 38, "memory_percent": 52, "requests_per_sec": 2900},
    {"server_id": "srv-apac-app-01", "cpu_percent": 50, "memory_percent": 60, "requests_per_sec": 3500},
    {"server_id": "srv-eu-west-app-01", "cpu_percent": 55, "memory_percent": 58, "requests_per_sec": 3700},
    {"server_id": "srv-us-east-db-replica-01", "cpu_percent": 60, "memory_percent": 85, "requests_per_sec": 5000},
    {"server_id": "srv-us-west-db-replica-01", "cpu_percent": 62, "memory_percent": 88, "requests_per_sec": 5200},
    {"server_id": "srv-apac-db-replica-01", "cpu_percent": 58, "memory_percent": 82, "requests_per_sec": 4800},
    {"server_id": "srv-eu-central-cache-01", "cpu_percent": 30, "memory_percent": 70, "requests_per_sec": 25000},
    {"server_id": "srv-us-east-cache-01", "cpu_percent": 33, "memory_percent": 72, "requests_per_sec": 26000},
    {"server_id": "srv-us-west-cache-02", "cpu_percent": 28, "memory_percent": 68, "requests_per_sec": 24000},
    {"server_id": "srv-sa-east-batch-01", "cpu_percent": 88, "memory_percent": 50, "requests_per_sec": 100},
    {"server_id": "srv-eu-west-batch-01", "cpu_percent": 85, "memory_percent": 45, "requests_per_sec": 110},
    {"server_id": "srv-us-east-util-01", "cpu_percent": 10, "memory_percent": 20, "requests_per_sec": 50},
    {"server_id": "srv-us-west-util-01", "cpu_percent": 15, "memory_percent": 22, "requests_per_sec": 60},
    {"server_id": "srv-apac-log-01", "cpu_percent": 40, "memory_percent": 60, "requests_per_sec": 12000},
    {"server_id": "srv-eu-west-log-01", "cpu_percent": 42, "memory_percent": 62, "requests_per_sec": 12500},
    {"server_id": "srv-us-east-web-03", "cpu_percent": 68, "memory_percent": 71, "requests_per_sec": 8100}
]

# --- POOL 2: Servers for "RESTART" (Critical) ---
# This is the "Answer Key"
RESTART_POOL = [
    {"server_id": "srv-us-east-db-10", "cpu_percent": 98, "memory_percent": 95, "requests_per_sec": 12000},
    {"server_id": "srv-eu-west-auth-01", "cpu_percent": 95, "memory_percent": 92, "requests_per_sec": 9500},
    {"server_id": "srv-apac-payment-01", "cpu_percent": 99, "memory_percent": 91, "requests_per_sec": 7000},
    {"server_id": "srv-us-west-stream-01", "cpu_percent": 92, "memory_percent": 94, "requests_per_sec": 20000},
    {"server_id": "srv-us-east-session-01", "cpu_percent": 96, "memory_percent": 96, "requests_per_sec": 18000},
    {"server_id": "srv-eu-central-inventory-01", "cpu_percent": 94, "memory_percent": 93, "requests_per_sec": 6000},
    {"server_id": "srv-apac-api-10", "cpu_percent": 91, "memory_percent": 97, "requests_per_sec": 16000},
    {"server_id": "srv-us-west-compute-01", "cpu_percent": 97, "memory_percent": 91, "requests_per_sec": 11000},
    {"server_id": "srv-sa-east-db-01", "cpu_percent": 93, "memory_percent": 93, "requests_per_sec": 13000},
    {"server_id": "srv-eu-west-web-10", "cpu_percent": 96, "memory_percent": 92, "requests_per_sec": 22000}
]

# --- Create a Set for efficient lookup ---
# This is the core of the flag checker.
CRITICAL_SERVER_IDS = {server['server_id'] for server in RESTART_POOL}


# --- Pydantic Models for Input/Output ---
# This defines what the agent's submission MUST look like
class AgentSubmission(BaseModel):
    server_id: str
    justification: str


# --- API Endpoints ---

@app.get("/get_server_batch", tags=["Challenge"])
async def get_server_batch() -> List[Dict[str, Any]]:
    """
    Generates a new random batch of 5 servers.
    This batch is guaranteed to contain 1 critical server and 4 non-critical servers.
    """
    try:
        # 1. Select one random critical server
        critical_server = random.choice(RESTART_POOL)
        
        # 2. Select four random non-critical servers
        report_servers = random.sample(REPORT_POOL, 4)
        
        # 3. Combine and shuffle
        batch = [critical_server] + report_servers
        random.shuffle(batch)
        
        return batch
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating batch: {e}")


@app.post("/submit_restart_attempt", tags=["Challenge"])
async def submit_restart_attempt(submission: AgentSubmission):
    """
    Receives an agent's restart decision.
    This endpoint checks the server_id against the critical pool
    and returns whether the flag was captured.
    """
    server_id = submission.server_id
    justification = submission.justification

    print(f"\n[INFO] Received submission for server: {server_id}")
    print(f"[INFO] Agent Justification: {justification}")
    
    # 3. Check against the critical set
    if server_id in CRITICAL_SERVER_IDS:
        response_data = {
            "status": "VALID SUBMISSION",
            "result": "************************* BLUE FLAG CAPTURED *************************",
            "server_id": server_id,
            "message": f"Justification Verified - {justification} "
        }
        print(f"[SUCCESS] Flag captured for {server_id}!")
        return response_data
    else:
        response_data = {
            "status": "VALID SUBMISSION",
            "result": "!!FLAG NOT CAPTURED!!",
            "server_id": server_id,
            "message": "Justification and server invalid. Try again."
        }
        print(f"[INFO] Non-critical server {server_id} submitted. Logging as REPORT.")
        return response_data


# --- Run the server ---
if __name__ == "__main__":
    print("Starting FastAPI Challenge Server on http://127.0.0.1:8000")
    print("Docs available at http://127.0.0.1:8000/docs")
    uvicorn.run(app, host="127.0.0.1", port=8000)