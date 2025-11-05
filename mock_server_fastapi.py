# from fastapi import FastAPI, HTTPException
# from fastapi.responses import JSONResponse, HTMLResponse
# from fastapi.middleware.cors import CORSMiddleware
# from pydantic import BaseModel
# import random

# # --- Configuration ---
# FLAG = "FLAG{blue_core_stabilized}"
# current_critical_server_id = None
# flag_catch_count = 0

# # --- App Initialization ---
# app = FastAPI(
#     title="Mock Server Monitor API",
#     description="Interactive API for server monitoring simulation.",
#     version="1.1.0",
#     contact={"name": "Blue Core"},
# )

# # Allow frontend/n8n access
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


# # --- Models ---
# class ReportIncidentRequest(BaseModel):
#     server_id: str
#     justification: str


# class RestartServiceRequest(BaseModel):
#     server_id: str
#     justification: str


# # --- Root Landing Page ---
# @app.get("/", response_class=HTMLResponse)
# def root():
#     return """
#     <html>
#         <head>
#             <title>Mock Server Monitor API</title>
#             <style>
#                 body {
#                     font-family: 'Segoe UI', sans-serif;
#                     background-color: #0d1117;
#                     color: #c9d1d9;
#                     text-align: center;
#                     padding-top: 10%;
#                 }
#                 h1 { color: #58a6ff; }
#                 a {
#                     color: #58a6ff;
#                     font-size: 1.2rem;
#                     text-decoration: none;
#                     border: 1px solid #58a6ff;
#                     padding: 10px 15px;
#                     border-radius: 10px;
#                 }
#                 a:hover {
#                     background-color: #58a6ff;
#                     color: #0d1117;
#                 }
#             </style>
#         </head>
#         <body>
#             <h1>🚀 Mock Server Monitor API</h1>
#             <p>Server simulation for Blue Core monitoring system.</p>
#             <a href="/docs">Go to API Docs</a>
#         </body>
#     </html>
#     """


# # --- 1. GET: Generate Server Stats ---
# @app.get("/get_server_stats")
# def get_server_stats():
#     global current_critical_server_id
#     server_names = ["api-01", "db-02", "web-03", "cache-01", "worker-05"]

#     data = []
#     critical_server_index = random.randint(0, len(server_names) - 1)
#     current_critical_server_id = server_names[critical_server_index]

#     for i, name in enumerate(server_names):
#         if i == critical_server_index:
#             stats = {
#                 "server_id": name,
#                 "cpu_percent": random.randint(91, 99),
#                 "memory_percent": random.randint(91, 99),
#                 "requests_per_sec": random.randint(10000, 20000),
#                 "critical": True,
#             }
#         else:
#             stats = {
#                 "server_id": name,
#                 "cpu_percent": random.randint(30, 85),
#                 "memory_percent": random.randint(30, 80),
#                 "requests_per_sec": random.randint(1000, 8000),
#                 "critical": False,
#             }
#         data.append(stats)

#     print(f"🟢 Generated Server Stats — Critical: {current_critical_server_id}")
#     return JSONResponse(content=data)


# # --- 2. POST: Report Incident ---
# @app.post("/report_incident")
# def report_incident(payload: ReportIncidentRequest):
#     server_id = payload.server_id
#     justification = payload.justification

#     if not server_id:
#         raise HTTPException(status_code=400, detail="Missing 'server_id'")

#     if server_id == current_critical_server_id:
#         print(f"🔴 Incorrect report: {server_id} was critical!")
#         raise HTTPException(status_code=400, detail="This server was critical")
#     else:
#         print(f"🟢 Incident reported successfully: {server_id}")
#         return {"status": "incident_reported", "server_id": server_id, "justification": justification}
