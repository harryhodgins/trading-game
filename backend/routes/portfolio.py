from mysql_connection import connection, cursor
from fastapi import APIRouter, HTTPException
import yfinance as yf

router = APIRouter()

def get_live_price(ticker, quantity):

    cleaned_ticker = str(ticker).upper()
    live_price = yf.Ticker(cleaned_ticker).info['currentPrice']
    value = live_price * int(quantity)

    return value

@router.get("/portfolio")
async def get_portfolio():
    
    sql = "SELECT * FROM portfolio"
    cursor.execute(sql)
    connection.commit()
    result = cursor.fetchall()

    return result

@router.get("/portfolio/{ticker}")
async def get_portfolio_by_ticker(ticker):
    sql = "SELECT * FROM portfolio WHERE ticker = %s"

    cursor.execute(sql,(ticker))
    connection.commit()

    result = cursor.fetchall()

    if result:
        return result
    else:
        raise(HTTPException(status_code=404, detail="Portfolio entry not found"))

@router.post("/portfolio")
async def add_to_portfolio(ticker, quantity):
    sql = """
    INSERT INTO portfolio (ticker, quantity, value)
    VALUES (%s, %s, %s)
    """

    value = get_live_price(ticker, quantity)

    values = (ticker, quantity, value)
    cursor.execute(sql, values)
    connection.commit()
    
    return({"message": "added to portfolio"})

@router.put("/portfolio/{ticker}")
async def update_portfolio_by_ticker(ticker,quantity):

    sql = """
    UPDATE portfolio
    SET quantity = quantity + %s, value = value + %s
    WHERE ticker = %s
    """

    add_value = get_live_price(ticker, quantity)
    values = (quantity, add_value, ticker)

    cursor.execute(sql, values)
    connection.commit()

    return({"message": f"updated {ticker}"})

@router.delete("/portfolio/{ticker}")
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