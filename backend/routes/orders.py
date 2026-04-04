from mysql_connection import connection, cursor
from fastapi import APIRouter, HTTPException
import yfinance as yf
from datetime import datetime

def get_live_price(ticker, quantity):

    cleaned_ticker = str(ticker).upper()
    live_price = yf.Ticker(cleaned_ticker).info['currentPrice']
    value = live_price * int(quantity)

    return value

orders_router = APIRouter()

@orders_router.get("/orders")
async def get_orders():

    sql = """
    SELECT * FROM orders
    """

    cursor.execute(sql)
    result = cursor.fetchall()
    connection.commit()

    if result:
        return result
    else:
        raise(HTTPException(status_code=404,detail="Orders not found"))

@orders_router.get("/orders/{id}")
async def get_orders_by_id(id):

    sql = """
    SELECT * FROM orders
    WHERE id = %s
    """

    cursor.execute(sql, id)
    result = cursor.fetchone()
    connection.commit()

    if result:
        return result
    else:
        raise(HTTPException(status_code=404,detail=f"Order id {id} not found"))

@orders_router.post("/orders")
async def add_order(ticker, quantity, type):
    order_type = str(type).upper()

    sql_orders = """
    INSERT INTO orders (ticker, quantity, type, value, price)
    VALUES (%s, %s, %s, %s, %s);
    """

    live_price = get_live_price(ticker, quantity)
    value = live_price * int(quantity)
    values = (str(ticker).upper(), quantity, order_type, value, live_price)

    cursor.execute(sql_orders, values)

    sql_portfolio_new = """
    INSERT INTO PORTFOLIO (ticker, quantity)
    VALUES (%s, %s)
    """

    sql_portfolio_update = """
    UPDATE portfolio
    SET quantity = quantity + %s
    WHERE ticker = %s
    """

    sql_portfolio_exists = "SELECT * FROM portfolio WHERE ticker = %s"
    cursor.execute(sql_portfolio_exists, str(ticker).upper())

    check_result = cursor.fetchone() #check if ticker exists in portfolio

    if not check_result and order_type == 'SELL':
        raise HTTPException(status_code=404, detail="Cannot sell for ticker not owned")
    elif check_result:
        if order_type == 'SELL':
            if int(quantity) > int(check_result['quantity']):
                raise HTTPException(status_code=404, detail="Cannot sell more shares than owned")
            if int(quantity) == int(check_result['quantity']):
                cursor.execute("DELETE FROM portfolio WHERE ticker = %s", str(ticker).upper())
            quantity = int(quantity) * -1
        cursor.execute(sql_portfolio_update, (quantity, str(ticker).upper()))
    else:
        cursor.execute(sql_portfolio_new, (str(ticker).upper(), quantity))

    connection.commit()
    return({"message": f"Placed order for {str(ticker).upper()}"})
    
    
