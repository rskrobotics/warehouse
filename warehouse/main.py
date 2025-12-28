from fastapi import FastAPI

app = FastAPI(title="Warehouse API")


@app.get("/health")
async def health():
    return {"status": "ok"}
