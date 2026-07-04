#!/usr/bin/env python3
"""A dummy tool server for the IAM to proxy requests to.

The IAM verifies the agent's credentials and, if allowed, forwards the
request here as the "real" tool. Any request received here means the
agent's identity and permission already checked out at the IAM.
"""
from fastapi import FastAPI, Request

app = FastAPI(title="Dummy Tool Server")


def _log(request: Request, body: bytes) -> None:
    print(f"[tool_server] {request.method} {request.url.path} body: {body!r}")


@app.post("/")
@app.get("/")
async def handle(request: Request):
    body = await request.body()
    _log(request, body)
    return {"message": "hey the agent request verified and reached"}


@app.post("/say_hi")
@app.get("/say_hi")
async def say_hi(request: Request):
    body = await request.body()
    _log(request, body)
    return {"message": "you called the say_hi tool"}


@app.post("/read")
@app.get("/read")
async def read(request: Request):
    body = await request.body()
    _log(request, body)
    return {"message": "you called the read tool"}


@app.post("/write")
@app.get("/write")
async def write(request: Request):
    body = await request.body()
    _log(request, body)
    return {"message": "you called the write tool"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=9000)
