# Challenge 2: Blue Core — Server Overload

# Objective

Your mission is to build an autonomous agent using n8n that monitors server statistics, uses an LLM to determine if a server is critically overloaded, and then performs the correct action to capture the `BLUE FLAG` .

# The Scenario

A fleet of our core servers is under heavy load. We need an autonomous agent to monitor the stats in real-time and take immediate action only when a server is in a critical failure state.

Your agent must distinguish between "high load" (which we just `REPORT`) and "critical overload" (which requires a `RESTART`).

# Agent Requirements

1. The "Critical" Logic

This is the core logic your agent's "brain" (the LLM) must follow.

Critical (RESTART): A server is considered "critical" if its CPU > 90% AND its Memory > 90%.

Warning (REPORT): Any other state. This includes servers that are "hot" (e.g., CPU 95%, Mem 88%) but not "critical," as well as healthy servers.

2. LLM Output Format

When you prompt your LLM, you must instruct it to return a JSON array where each object follows this format:

server_id (string): The ID of the server.

action (string): Either 'RESTART' or 'REPORT'.

justification (string): A brief (1-2 sentence) reason for the decision, based on its stats, and a guess of what would this server be used for.

# Challenge API Endpoints

The challenge is hosted on a live server. Your n8n workflow will interact with these two endpoints.

1. Get Your Problem

Your agent must first get its list of servers to analyze.

Endpoint: GET [GET](https://blue-core.onrender.com/get_server_batch)

Description: This will return a JSON array of servers, amongst which there will be critical servers.

2. Submit Your Answer

When your agent identifies a critical server, it must send its decision here.

Endpoint: [POST] (https://blue-core.onrender.com/submit_restart_attempt)

Description: You must POST your RESTART decision to this URL. The API will check your answer.

Required Body (JSON):

{
  "server_id": "THE_CRITICAL_SERVER_ID",
  "justification": "YOUR_LLM_JUSTIFICATION"
}

# Your Mission: Build the n8n Workflow
You must build an n8n workflow that automates this entire process. 

# How to Win

When your n8n workflow correctly identifies the critical server and POSTs the correct server_id and justification to the submit endpoint, the API will respond with the flag.

Good luck.
