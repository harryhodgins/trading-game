from fastapi import APIRouter, HTTPException
from mysql_connection import cursor, connection

players_router = APIRouter()

@players_router.get("/players")
async def get_players():
    sql = "SELECT * FROM players"

    cursor.execute(sql)
    result = cursor.fetchall()
    connection.commit()

    if result:
        return result
    else:
        raise(HTTPException(status_code=404,detail="Failed to fetch players"))
    
@players_router.post("/players")
async def add_player(playerName: str, isBot: bool = False, balance: float = 10000.00):
    
    check_player_exists = "SELECT * FROM players WHERE player_name = %s"

    cursor.execute(check_player_exists, playerName)
    check_result = cursor.fetchone()

    sql = """
    INSERT INTO players (player_name, balance, is_bot)
    VALUES (%s, %s, %s)
    """

    if not check_result:
        cursor.execute(sql, (playerName, balance, isBot))
    else:
        raise(HTTPException(status_code=404, detail="Player with this name already exists"))
    
    connection.commit()

    return {"message": f"Created player {playerName} with balance {balance}"}



