from fastapi import FastAPI

from warehouse.routers.v1 import items, stores

app = FastAPI(title="Warehouse API")

app.include_router(stores.router, prefix="/api/v1")
app.include_router(items.router, prefix="/api/v1")


@app.get("/health")
async def health():
    return {"status": "ok"}
