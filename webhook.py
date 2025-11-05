# from fastapi import FastAPI, Request
# from fastapi.responses import HTMLResponse
# import uvicorn
# import json
# from datetime import datetime

# # Create the FastAPI app instance
# app = FastAPI(title="Webhook.py Receiver")

# # --- Helper Function to Print a Fancy Box ---
# def print_boxed(title, content, success=False):
#     """Helper function to print formatted output to the console."""
#     color_start = '\033[92m' if success else '\033[93m' # Green for success, Yellow for info
#     color_end = '\033[0m'
    
#     print("\n" + "="*70)
#     print(f"{color_start}== {title.upper()} =={color_end}")
#     print("="*70)
#     for line in content.splitlines():
#         print(f"  {line}")
#     print("="*70 + "\n")

# @app.get("/", response_class=HTMLResponse)
# async def root():
#     """
#     Serves the homepage with instructions.
#     """
#     return """
#     <html>
#         <head>
#             <title>Webhook.py Receiver</title>
#             <style>
#                 body { font-family: 'Arial', sans-serif; background-color: #f4f4f9; color: #333; padding: 40px; }
#                 div { max-width: 700px; margin: 0 auto; background-color: #fff; padding: 30px; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.05); }
#                 h1 { color: #2a2a2a; }
#                 p { line-height: 1.6; }
#                 code { background-color: #eee; padding: 4px 8px; border-radius: 4px; font-family: 'Courier New', monospace; }
#                 strong { color: #d9534f; }
#             </style>
#         </head>
#         <body>
#             <div>
#                 <h1>Webhook.py Receiver is Running!</h1>
#                 <p>This server is successfully running and listening for incoming webhooks.</p>
#                 <p>Your universal webhook endpoint is:</p>
#                 <code><strong>http://127.0.0.1:8000/webhook</strong></code>
#                 <p>Point your services (n8n, GitHub, Stripe, etc.) to this URL to capture and inspect the incoming data.</p>
#                 <p>All received requests will be printed to the terminal where this script is running.</p>
#             </div>
#         </body>
#     </html>
#     """

# @app.api_route("/webhook", methods=["GET", "POST", "PUT", "PATCH", "DELETE"])
# async def receive_webhook(request: Request):
#     """
#     A universal webhook receiver that captures all data from any
#     request and prints it to the console.
#     """
#     now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#     title = f"REQUEST RECEIVED AT {now} [{request.method}]"
    
#     content = [f"Client: {request.client.host}:{request.client.port}"]
    
#     # Get Query Parameters
#     query_params = dict(request.query_params)
#     if query_params:
#         content.append("\n--- Query Parameters ---")
#         content.append(json.dumps(query_params, indent=2))
        
#     # Get Headers
#     headers = dict(request.headers)
#     if headers:
#         content.append("\n--- Headers ---")
#         content.append(json.dumps(headers, indent=2))

#     # Get Body
#     # We use a try-except block because request.json() will fail
#     # if the body is empty or not valid JSON (e.g., form-data).
#     body_content = ""
#     try:
#         # Try to parse as JSON first
#         body_json = await request.json()
#         body_content = json.dumps(body_json, indent=2)
#         content.append("\n--- Body (JSON) ---")
#     except Exception:
#         # Fallback to reading raw bytes
#         body_bytes = await request.body()
#         if body_bytes:
#             try:
#                 # Try to decode as text (e.g., for form data)
#                 body_content = body_bytes.decode('utf-8')
#                 content.append("\n--- Body (Text/Form-Data) ---")
#             except Exception:
#                 # Fallback for non-text data
#                 body_content = f"<{len(body_bytes)} bytes of binary data>"
#                 content.append("\n--- Body (Binary) ---")

#     if body_content:
#         content.append(body_content)
#     else:
#         content.append("\n--- Body (Empty) ---")

#     # Print the formatted box to the terminal
#     print_boxed(title, "\n".join(content), success=True)
    
#     return {"status": "success", "message": "Webhook received"}

# if __name__ == "__main__":
#     print("Starting FastAPI server on http://127.0.0.1:8000")
#     uvicorn.run(app, host="127.0.0.1", port=8000)