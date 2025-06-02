from fastapi import FastAPI
from .routes import exchange, transactions

app = FastAPI(
    title="API de Intercambio de Monedas",
    description="API para conversión y transferencias entre monedas"
)

app.include_router(exchange.router)
app.include_router(transactions.router)

@app.get("/")
async def health_check():
    return {"status": "API operativa"}