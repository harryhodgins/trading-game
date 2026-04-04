from fastapi import FastAPI
import uvicorn
from routes.portfolio import portfolio_router
from routes.orders import orders_router

app = FastAPI()
app.include_router(portfolio_router)
app.include_router(orders_router)

@app.get("/health")
async def health():
    return {"status": "ok",
            "message": "FastAPI app is running"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)