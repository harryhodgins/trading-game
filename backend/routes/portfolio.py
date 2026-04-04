from mysql_connection import connection, cursor
from fastapi import APIRouter, HTTPException

portfolio_router = APIRouter()

@portfolio_router.get("/portfolio")
async def get_portfolio():
    
    sql = "SELECT * FROM portfolio"
    cursor.execute(sql)
    connection.commit()
    result = cursor.fetchall()

    return result

@portfolio_router.get("/portfolio/{ticker}")
async def get_portfolio_by_ticker(ticker):
    sql = "SELECT * FROM portfolio WHERE ticker = %s"

    cursor.execute(sql,(ticker))
    connection.commit()

    result = cursor.fetchall()

    if result:
        return result
    else:
        raise(HTTPException(status_code=404, detail="Portfolio entry not found"))

@portfolio_router.delete("/portfolio/{ticker}")
async def delete_portfolio_by_ticker(ticker):

    sql = """
    DELETE from portfolio
    WHERE ticker = %s
    """

    cursor.execute(sql, (ticker))
    connection.commit()

    if cursor.rowcount == 0:
        raise HTTPException(status_code=404,detail="Portfolio entry not found")
    
    return({"message" : f"Deleted {ticker} from portfolio"})