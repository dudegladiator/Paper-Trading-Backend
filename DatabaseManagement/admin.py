from typing import Any, Dict, Union
from database import Database

def create_users_table(db: Any) -> Dict[str, Union[bool, str]]:
    query = '''
    CREATE TABLE IF NOT EXISTS users (
        api_key VARCHAR(255) PRIMARY KEY,
        name VARCHAR(255),
        team VARCHAR(255),
        balance FLOAT,
        token VARCHAR(255),
        token_expiry DATETIME
    )
    '''
    success = db.execute_final(query)
    db.create_index("users", "api_key_index_1", ["api_key"])
    db.create_index("users", "team_1", ["team"])
    return {"success": success, "message": "Users table created" if success is True else "Failed to create users table"}


def create_trades_table(db: Any) -> Dict[str, Union[bool, str]]:
    query = '''
    CREATE TABLE IF NOT EXISTS trades (
        id INT AUTO_INCREMENT PRIMARY KEY,
        api_key VARCHAR(255),
        name VARCHAR(255),
        stock VARCHAR(255),
        stock_price FLOAT,
        quantity INT,
        type ENUM('buy', 'sell'),
        before_balance FLOAT,
        after_balance FLOAT,
        time DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (api_key) REFERENCES users(api_key)
    )
    '''
    success = db.execute_final(query)
    db.create_index("trades", "api_key_index_2", ["api_key"])
    return {"success": success, "message": "Trades table created" if success is True else "Failed to create trades table"}


def create_stocks_table(db: Any) -> Dict[str, Union[bool, str]]:
    query = '''
    CREATE TABLE IF NOT EXISTS stocks (
        id INT AUTO_INCREMENT PRIMARY KEY,
        api_key VARCHAR(255),
        name VARCHAR(255),
        stock VARCHAR(255),
        quantity INT,
        FOREIGN KEY (api_key) REFERENCES users(api_key)
    )
    '''
    success = db.execute_final(query)
    db.create_index("stocks", "api_key_index_3", ["api_key"])
    db.create_index("stocks", "stock_index_1", ["stock"])
    return {"success": success, "message": "Stocks table created" if success is True else "Failed to create stocks table"}

def create_log_table(db: Any) -> Dict[str, Union[bool, str]]:
    query = '''
    CREATE TABLE IF NOT EXISTS logs (
        id INT AUTO_INCREMENT PRIMARY KEY,
        api_key VARCHAR(255),
        name VARCHAR(255),
        log VARCHAR(255),
        time DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (api_key) REFERENCES users(api_key)
    )
    '''
    success = db.execute_final(query)
    db.create_index("logs", "api_key_index_4", ["api_key"])
    return {"success": success, "message": "Logs table created" if success is True else "Failed to create logs table"}

if __name__ == "__main__":
    db = Database()
    
    # print(db.delete_table("stocks"))
    # print(db.delete_table("trades"))
    # # print(db.delete_table("logs"))
    # print(db.delete_table("users"))
    
    # print(create_users_table(db))
    # # print(create_log_table(db))
    # print(create_trades_table(db))
    # print(create_stocks_table(db))