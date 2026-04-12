from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from routes.portfolio import portfolio_router
from routes.orders import orders_router
from routes.players import players_router
from mysql_connection import cursor, connection

app = FastAPI()

origins = [
    "http://localhost:5173",
    "localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(portfolio_router)
app.include_router(orders_router)
app.include_router(players_router)

@app.delete("/reset")
async def reset_database():
    cursor.execute("DELETE FROM orders")
    cursor.execute("DELETE FROM portfolio")
    cursor.execute("DELETE FROM players")
    cursor.execute("ALTER TABLE orders AUTO_INCREMENT = 1")
    cursor.execute("ALTER TABLE players AUTO_INCREMENT = 1")

    connection.commit()

    return {"message": "Reset database"}

@app.get("/health")
async def health():
    return {"status": "ok",
            "message": "FastAPI app is running"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)