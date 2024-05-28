from datetime import datetime, timedelta
from typing import Any, Dict, Optional, Union

from DatabaseManagement.database import Database
from utils.IST_Time import get_current_time_IST
from utils.loggings import log_creator
from utils.util import create_api_key, create_token

def create_user(db: Any, name: str, team: str, balance: float, api_key: str, token: str, token_expiry: datetime) -> Dict[str, Union[bool, str]]:
    query = '''
    INSERT INTO users (name, team, balance, api_key, token, token_expiry) 
    VALUES (%s, %s, %s, %s, %s, %s)
    '''
    success = db.execute(query, (name, team, balance, api_key, token, token_expiry))
    if success is True:
        log_creator(api_key=api_key, name=name, log='User created', error=False)
        return {"success": True, "message": "User created"}
    else:
        log_creator(api_key=api_key, name=name, log='Failed to create user', error=True)
        return {"success": False, "message": "Failed to create user"}

def delete_user(db: Any, api_key: str) ->   Dict[str, Union[bool, str]]:
    query = '''
    DELETE FROM users WHERE api_key = %s
    '''
    success = db.execute(query, (api_key,))
    if success is True:
        log_creator(api_key=api_key, name='Unknown', log='User deleted', error=False)
        return {"success": True, "message": "User deleted"}
    else:
        log_creator(api_key=api_key, name='Unknown', log='Failed to delete user', error=True)
        return {"success": False, "message": "Failed to delete user"}


def get_user(db: Any, api_key: str) -> Optional[Dict[str, Union[str, float]]]:
    query = '''
    SELECT * FROM users WHERE api_key = %s
    '''
    result = db.fetch(query, (api_key,))
    if result not in [[]]:
        log_creator(api_key=api_key, name='Unknown', log='User data fetched', error=False)
        return {
            "api_key": result[0][0],
            "name": result[0][1],
            "team" : result[0][2],
            "balance": result[0][3],
            "token": result[0][4],
            "token_expiry": result[0][5]
        }
    else:
        log_creator(api_key="unknown", name='Unknown', log='Failed to fetch user data', error=True)
        return None


def update_user_token(db: Any, api_key: str, token: str, token_expiry: datetime) -> Dict[str, Union[bool, str]]:
    query = '''
    UPDATE users SET token = %s, token_expiry = %s WHERE api_key = %s 
    '''
    success = db.execute(query, (token, token_expiry, api_key))
    if success is True:
        log_creator(api_key=api_key, name='Unknown', log='User token updated', error=False)
        return {"success": True, "message": "User token updated"}
    else:
        log_creator(api_key=api_key, name='Unknown', log='Failed to update user token', error=True)
        return {"success": False, "message": "Failed to update user token"}
    

def update_balance(db: Any, api_key: str, new_balance: float) -> Dict[str, Union[bool, str]]:
    query = '''
    UPDATE users SET balance = %s WHERE api_key = %s
    '''
    success = db.execute(query, (new_balance, api_key))
    if success is True:
        log_creator(api_key=api_key, name='Unknown', log='Balance updated', error=False)
        return {"success": True, "message": "Balance updated"}
    else:
        log_creator(api_key=api_key, name='Unknown', log='Failed to update balance', error=True)
        return {"success": False, "message": "Failed to update balance"}


def create_trade(db: Any, api_key: str, name: str, stock: str, stock_price: float, quantity: int, type: str, before_balance: float, after_balance: float, time: datetime) -> Dict[str, Union[bool, str]]:
    query = '''
    INSERT INTO trades (api_key, name, stock, stock_price, quantity, type, before_balance, after_balance, time) 
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    '''
    success = db.execute(query, (api_key, name, stock, stock_price, quantity, type, before_balance, after_balance, time))
    if success is True:
        log_creator(api_key=api_key, name=name, log='Trade created', error=False)
        return {"success": True, "message": "Trade created"}
    else:
        log_creator(api_key=api_key, name=name, log='Failed to create trade', error=True)
        return {"success": False, "message": "Failed to create trade"}
    

def create_stock(db: Any, api_key: str, name: str, stock: str, quantity: int) -> Dict[str, Union[bool, str]]:
    query = '''
    INSERT INTO stocks (api_key, name, stock, quantity) 
    VALUES (%s, %s, %s, %s)
    '''
    success = db.execute(query, (api_key, name, stock, quantity))
    if success is True:
        log_creator(api_key=api_key, name=name, log='Stock portfolio created', error=False)
        return {"success": True, "message": "Stock portfolio created"}
    else:
        log_creator(api_key=api_key, name=name, log='Failed to create stock portfolio', error=True)
        return {"success": False, "message": "Failed to create stock portfolio"}

def get_stock(db: Any, api_key: str, stock: str) -> Optional[Dict[str, Union[str, float]]]:
    query = '''
    SELECT * FROM stocks WHERE api_key = %s AND stock = %s 
    '''
    result = db.fetch(query, (api_key, stock))
    if result not in [[]]:
        log_creator(api_key=api_key, name='Unknown', log='Stock data fetched', error=False)
        return {
            "api_key": result[0][1],
            "name": result[0][2],
            "stock": result[0][3],
            "quantity": result[0][4]
        }
    else:
        log_creator(api_key=api_key, name='Unknown', log='Failed to fetch stock data', error=True)
        return None


def update_stock(db: Any, api_key: str, stock: str, quantity: int) -> Dict[str, Union[bool, str]]:
    query = '''
    UPDATE stocks SET quantity = %s WHERE api_key = %s AND stock = %s
    '''
    success = db.execute(query, (quantity, api_key, stock))
    if success is True:
        log_creator(api_key=api_key, name='Unknown', log='Stock updated', error=False)
        return {"success": True, "message": "Stock updated"}
    else:
        log_creator(api_key=api_key, name='Unknown', log='Failed to update stock', error=True)
        return {"success": False, "message": "Failed to update stock"}
    
def delete_stock(db: Any, api_key: str, stock: str) -> Dict[str, Union[bool, str]]:
    query = '''
    DELETE FROM stocks WHERE api_key = %s AND stock = %s
    '''
    success = db.execute(query, (api_key, stock))
    if success is True:
        log_creator(api_key=api_key, name='Unknown', log='Stock deleted', error=False)
        return {"success": True, "message": "Stock deleted"}
    else:
        log_creator(api_key=api_key, name='Unknown', log='Failed to delete stock', error=True)
        return {"success": False, "message": "Failed to delete stock"}
    
if __name__ == "__main__":
    db = Database()
    
    # create users 
    
    # db.start_transaction()
    # names = ["Saksham", "Krish", "Jatin", "Palak", "Raghuveer", "Harshavarda", "Meghav", "Atul", "Aditya 1", "Antariksh", "Pranjal", "Imad", "Udit", "Gaurang", "Lalit", "Aakriti", "Utsab", "Krishnav", "Aditya 2", "Kiran", "Harsh", "Pratyush", "Nitin", "Aayush", "Valabh", "Adway", "Ajsal", "Daksh", "Archisha", "Apurba"]
    # for name in names:
    #     api = create_api_key(name)
    #     print(name, api)
    #     user = create_user(db, name=name, team="QCTrainees", balance=100000, token=create_token(api, get_current_time_IST() + timedelta(hours=7)), api_key=api, token_expiry=get_current_time_IST() + timedelta(hours=7))
    #     if user["success"] is False:    
    #         print(user)
    # db.commit_transaction()
        
    
    # create_some_more
    # db.start_transaction()
    names = ["tester1", "tester2", "tester3", "tester4", "tester5", "tester6", "tester7", "tester8", "tester9", "tester10", "tester11", "tester12", "tester13", "tester14", "tester15", "tester16", "tester17", "tester18", "tester19", "tester20"]
    db.start_transaction()
    for name in names:
        api = create_api_key(name)
        print(name, api)
        user = create_user(db, name=name, team="tester", balance=100000, token=create_token(api, get_current_time_IST() + timedelta(hours=7)), api_key=api, token_expiry=get_current_time_IST() + timedelta(hours=7))
        if user["success"] is False:    
            print(user)
    db.commit_transaction()
    
    # # Insert a user
    # db.start_transaction()
    # user_api_key = "45harsh45"
    # # print(create_user(db, "Test User 2", 1000.0, user_api_key, "token12345", get_current_time_IST() + timedelta(days=30)))
    # # db.commit_transaction()
    # # # Fetch user data
    # print(get_user(db, user_api_key))
    
    # db.start_transaction()
    # # Update user token
    # # print(update_user_token(db, user_api_key, "newtoken123", get_current_time_IST() + timedelta(days=60)))
    
    # # Update balance
    # print(update_balance(db, user_api_key, 1500.0))
    
    # # # Create a trade
    # # print(create_trade(db, user_api_key, "Test User 2", "AAPL", 150.0, 10, 'sell', 1000.0, 850.0, get_current_time_IST()))
    
    # # # Create a stock portfolio
    # # print(create_stock(db, user_api_key, "Test User 2", "AAPL", 10))
    # db.commit_transaction()
    # # Fetch stock data
    # print(get_stock(db, user_api_key, "AAPL"))
    
    # db.start_transaction()
    # Update stock
    # print(update_stock(db, user_api_key, "AAPL", 15))
    
    # db.commit_transaction()
    
    
    pass