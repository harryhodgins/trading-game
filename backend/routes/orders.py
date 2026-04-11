from mysql_connection import connection, cursor
from fastapi import APIRouter, HTTPException
import yfinance as yf
from datetime import datetime

def get_live_price(ticker):

    cleaned_ticker = str(ticker).upper()
    live_price = yf.Ticker(cleaned_ticker).info['currentPrice']

    return live_price

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
async def add_order(ticker, quantity, type, player_id):
    check_player_exists = "SELECT * FROM players WHERE player_id = %s"
    cursor.execute(check_player_exists, player_id)
    check_player = cursor.fetchone()
    if not check_player:
        raise(HTTPException(status_code=404,
                            detail=f"Player with id {player_id} not found"))

    order_type = str(type).upper()

    sql_orders = """
    INSERT INTO orders (ticker, quantity, type, value, price, player_id)
    VALUES (%s, %s, %s, %s, %s, %s);
    """

    live_price = get_live_price(ticker)
    value = live_price * int(quantity)
    values = (str(ticker).upper(), quantity, order_type, value, live_price, player_id)

    cursor.execute(sql_orders, values)

    sql_portfolio_new = """
    INSERT INTO PORTFOLIO (ticker, quantity, player_id)
    VALUES (%s, %s, %s)
    """

    sql_portfolio_update = """
    UPDATE portfolio
    SET quantity = quantity + %s
    WHERE ticker = %s
    AND player_id = %s
    """

    sql_update_player_balance = """
    UPDATE players
    SET balance = balance + %s
    WHERE player_id = %s
    """

    sql_portfolio_exists = "SELECT * FROM portfolio WHERE ticker = %s AND player_id = %s"

    cursor.execute(sql_portfolio_exists, (str(ticker).upper(), player_id))

    check_result = cursor.fetchone() #check if ticker exists in portfolio
    balance_change = value if order_type == 'SELL' else value * -1

    if not check_result and order_type == 'SELL':
        raise HTTPException(status_code=404, detail="Cannot sell for ticker not owned")
    elif check_result and check_player:
        if order_type == 'SELL':
            if int(quantity) > int(check_result['quantity']):
                raise HTTPException(status_code=404, detail="Cannot sell more shares than owned")
            if int(quantity) == int(check_result['quantity']):
                cursor.execute("""
                            DELETE FROM portfolio
                            WHERE ticker = %s
                            AND player_id = %s
                            """, (str(ticker).upper(), player_id))
            quantity = int(quantity) * -1
        cursor.execute(sql_portfolio_update, (quantity, str(ticker).upper(), player_id))
        cursor.execute(sql_update_player_balance, (balance_change, player_id))
    else:
        cursor.execute(sql_portfolio_new, (str(ticker).upper(), quantity, player_id))
        cursor.execute(sql_update_player_balance, (balance_change, player_id))
    connection.commit()
    return({"message": f"Placed order for {str(ticker).upper()}"})
    
    
