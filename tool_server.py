#!/usr/bin/env python3
"""A dummy tool server for the IAM to proxy requests to.

The IAM verifies the agent's credentials and, if allowed, forwards the
request here as the "real" tool. Any request received here means the
agent's identity and permission already checked out at the IAM.
"""
from fastapi import FastAPI, Request

app = FastAPI(title="Dummy Tool Server")


@app.post("/")
@app.get("/")
async def handle(request: Request):
    body = await request.body()
    print(f"[tool_server] received {request.method} request, body: {body!r}")
    return {"message": "hey the agent request verified and reached"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=9000)
