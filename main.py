from fastapi import FastAPI, Request, HTTPException

from contextlib import asynccontextmanager

import uvicorn


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("서버접속")
    yield
    print("서버종료")


app = FastAPI(lifespan=lifespan)


ALLOWED_IPS = {"52.89.214.238", "34.212.75.30", "54.218.53.128", "52.32.178.7"}


@app.middleware("http")
async def ip_filter_middleware(request: Request, call_next):
    client_ip = request.client.host
    if client_ip not in ALLOWED_IPS:
        raise HTTPException(status_code=403, detail="IP Address not allowed")
    response = await call_next(request)
    return response


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
