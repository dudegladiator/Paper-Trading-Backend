from datetime import datetime, timedelta
from typing import Dict, Union, Optional
from pytz import timezone

from fastapi import APIRouter, FastAPI, HTTPException, Header, Request
from pydantic import BaseModel
from DatabaseManagement.database import Database

from dotenv import load_dotenv

from utils.IST_Time import get_current_time_IST
from utils.loggings import log_creator
load_dotenv()

from DatabaseManagement.service import (
    create_stock, create_trade, delete_stock, get_stock, get_user, 
    update_balance, update_stock, update_user_token
)
from utils.util import create_token

extension = APIRouter()
db = Database()

chrome_extension_origin = "chrome-extension://hbocfhgkiadihfiiikhohblkdoahegkk"

# Authentication Model
class AuthResponse(BaseModel):
    token: str
    expiresAt: int

# User Data Model
class UserData(BaseModel):
    name: str
    balance: float

# Trade Model
class TradeRequest(BaseModel):
    action: str
    stockName: str
    stockPrice: float
    quantity: int
    balance: float
    date: datetime

class TradeResponse(BaseModel):
    success: bool
    message: str
    error: Optional[str]
    name: str
    stock: str
    qt: int
    balance: float

def validate_token(user_data, token):
    print(user_data, token)
    if user_data["token"] != token:
        raise HTTPException(status_code=401, detail="Invalid token")

    ist_timezone = timezone('Asia/Kolkata')
    token_expiry = user_data["token_expiry"].replace(tzinfo=ist_timezone)
    if token_expiry < get_current_time_IST():
        raise HTTPException(status_code=401, detail="Token expired")

def handle_trade(user_data, trade: TradeRequest):
    buy_charges = 0.0011842
    sell_charges = 0.0011842
    
    ist_timezone = timezone('Asia/Kolkata')
    trade_date = trade.date.astimezone(ist_timezone)
    # Check if the trade date is within the allowed time window
    if trade_date < get_current_time_IST() - timedelta(hours=0.5) or trade_date > get_current_time_IST() + timedelta(hours=0.5):
        raise HTTPException(status_code=400, detail="Invalid date and time")

    # Check for valid trading hours and days
    if not (9, 15) <= (trade_date.hour, trade_date.minute) <= (3, 30):
        raise HTTPException(status_code=400, detail="Trade time must be between 9:15 AM to 3:30 PM")

    if trade_date.weekday() >= 5:  # 0=Monday, 4=Friday, 5=Saturday
        raise HTTPException(status_code=400, detail="Trades can only be executed from Monday to Friday")
    
    if trade.action == "buy":
        return handle_buy(user_data, trade, buy_charges)
    elif trade.action == "sell":
        return handle_sell(user_data, trade, sell_charges)
    else:
        return {
            "success": False,
            "message": "Invalid action",
            "error": "Invalid action",
            "name": user_data["name"],
            "stock": trade.stockName,
            "qt": trade.quantity,
            "balance": user_data["balance"]
        }

def handle_buy(user_data, trade: TradeRequest, charges: float):
    cost = trade.quantity * trade.stockPrice * (1 + charges)
    print(trade)
    
    if user_data["balance"] < cost:
        return {
            "success": False,
            "message": "Insufficient balance",
            "error": "Not enough funds",
            "name": user_data["name"],
            "stock": trade.stockName,
            "qt": trade.quantity,
            "balance": user_data["balance"]
        }

    old_stock = get_stock(db, user_data["api_key"], trade.stockName)
    new_balance = user_data["balance"] - cost

    db.start_transaction()
    try:
        create_trade_result = create_trade(
            db, api_key=user_data["api_key"], name=user_data["name"], stock=trade.stockName, 
            stock_price=trade.stockPrice, quantity=trade.quantity, type=trade.action, 
            before_balance=user_data["balance"], after_balance=new_balance, time=get_current_time_IST()
        )
        if not create_trade_result["success"]:
            raise Exception(create_trade_result["message"])

        if old_stock:
            new_quantity = old_stock["quantity"] + trade.quantity
            update_stock_result = update_stock(db, user_data["api_key"], trade.stockName, new_quantity)
            
            if not update_stock_result["success"]:
                raise Exception(update_stock_result["message"])
        else:
            create_stock_result = create_stock(db, user_data["api_key"], user_data["name"], trade.stockName, trade.quantity)
            if not create_stock_result["success"]:
                raise Exception(create_stock_result["message"])

        update_balance_result = update_balance(db, user_data["api_key"], new_balance)
        if not update_balance_result["success"]:
            raise Exception(update_balance_result["message"])

        db.commit_transaction()
        return {
            "success": True,
            "message": f"Bought {trade.quantity} shares of {trade.stockName} successfully",
            "error": None,
            "name": user_data["name"],
            "stock": trade.stockName,
            "qt": trade.quantity,
            "balance": new_balance
        }
    except Exception as e:
        db.rollback_transaction()
        print(e)
        raise HTTPException(status_code=500, detail=str(e))

def handle_sell(user_data, trade: TradeRequest, charges: float):
    old_stock = get_stock(db, user_data["api_key"], trade.stockName)
    dp_charge = 15
    if not old_stock or old_stock["quantity"] < trade.quantity:
        return {
            "success": False,
            "message": "Insufficient stock",
            "error": "Not enough shares",
            "name": user_data["name"],
            "stock": trade.stockName,
            "qt": trade.quantity,
            "balance": user_data["balance"]
        }

    sell = trade.quantity * trade.stockPrice * (1 - charges) - dp_charge
    new_balance = user_data["balance"] + sell

    db.start_transaction()
    try:
        create_trade_result = create_trade(
            db, api_key=user_data["api_key"], name=user_data["name"], stock=trade.stockName, 
            stock_price=trade.stockPrice, quantity=trade.quantity, type=trade.action, 
            before_balance=user_data["balance"], after_balance=new_balance, time=get_current_time_IST()
        )
        if not create_trade_result["success"]:
            raise Exception(create_trade_result["message"])

        new_quantity = old_stock["quantity"] - trade.quantity
        if new_quantity == 0:
            update_stock_result = delete_stock(db, user_data["api_key"], trade.stockName)
        else:
            update_stock_result = update_stock(db, user_data["api_key"], trade.stockName, new_quantity)

        if not update_stock_result["success"]:
            raise Exception(update_stock_result["message"])

        update_balance_result = update_balance(db, user_data["api_key"], new_balance)
        if not update_balance_result["success"]:
            raise Exception(update_balance_result["message"])

        db.commit_transaction()
        return {
            "success": True,
            "message": f"Sold {trade.quantity} shares of {trade.stockName} successfully",
            "error": None,
            "name": user_data["name"],
            "stock": trade.stockName,
            "qt": trade.quantity,
            "balance": new_balance
        }
    except Exception as e:
        db.rollback_transaction()
        raise HTTPException(status_code=500, detail=str(e))

# Authentication endpoint
@extension.post("/authenticate", response_model=AuthResponse)
async def authenticate(request:Request, api_key: str):
    if request.headers.get("Origin") != chrome_extension_origin:
        print(request.headers.get("Origin"))
        raise HTTPException(status_code=500, detail="Invalid origin")
    print(request.headers.get("Origin"))
    try:
        user_data = get_user(db, api_key)
        if not user_data:
            raise HTTPException(status_code=401, detail="Invalid API key")
        
        # log_creator(api_key=api_key, name='Unknown', log='User data fetched', error=False)
        expiration_time = get_current_time_IST() + timedelta(hours=7)
        token = create_token(api_key, expiration_time)
        update_result = update_user_token(db, api_key, token, expiration_time)
        if not update_result["success"]:
            raise HTTPException(status_code=500, detail=update_result["message"])
        
        return {"token": token, "expiresAt": int(expiration_time.timestamp())}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Get user data endpoint
@extension.get("/user", response_model=UserData)
async def get_user_data(request:Request, api_key: str = Header(...), token: str = Header(...)):
    print(api_key, token)
    try:
        user_data = get_user(db, api_key)
        if not user_data:
            raise HTTPException(status_code=401, detail="Invalid API key")
        
        validate_token(user_data, token)
        
        return {"name": user_data["name"], "balance": user_data["balance"]}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))

# Execute trade endpoint
@extension.post("/trade", response_model=TradeResponse)
async def execute_trade(
    request:Request, 
    trade: TradeRequest,
    api_key: str = Header(...),
    token: str = Header(...)
):
    if request.headers.get("Origin") != chrome_extension_origin:
        print(request.headers.get("Origin"))
        raise HTTPException(status_code=500, detail="Invalid origin")
    print(trade, api_key, token)
    try:
        user_data = get_user(db, api_key)
        if not user_data:
            raise HTTPException(status_code=401, detail="Invalid API key")

        validate_token(user_data, token)
        
        response = handle_trade(user_data, trade)
        return response
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))
    
@extension.get("/dbhealth")
def db_health():
    try:
        data = get_user(db, "49127765")
        return {"status": "Database connected", "data": data}
    except Exception as e:
        return {"status": "Database connection failed", "error": str(e)}    
