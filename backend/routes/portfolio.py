from mysql_connection import connection, cursor
from fastapi import APIRouter

router = APIRouter()

@router.get("/portfolio")
async def get_portfolio():
    
    sql = "SELECT * FROM portfolio"
    cursor.execute(sql)
    connection.commit()
    result = cursor.fetchall()

    return result

@router.post("/portfolio")
async def add_to_portfolio(ticker, quantity):
    sql = """
    INSERT INTO portfolio (ticker, quantity)
    VALUES (%s, %s)
    """
    values = (ticker, quantity)
    cursor.execute(sql, values)
    connection.commit()
    
    return({"message": "added to portfolio"})