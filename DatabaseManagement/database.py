import os
from typing import Optional
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

load_dotenv()

class Database:
    def __init__(self):
        self.connection = None
        self.cursor = None
        self.transaction_active = False
        self.connect()
    
    def connect(self) -> dict:
        message = {"success": False, "message": ""}
        try:
            self.connection = mysql.connector.connect(
                host=os.getenv("MYSQL_HOST"),
                user=os.getenv("MYSQL_USER"),
                password=os.getenv("MYSQL_PASSWORD"),
                database=os.getenv("MYSQL_DATABASE"),
                port=os.getenv("MYSQL_PORT")
            )
            if self.connection.is_connected():
                self.cursor = self.connection.cursor(buffered=True)
                print("Successfully connected to the database")
                message["success"] = True
                message["message"] = "Successfully connected to the database"
        except Error as e:
            print(f"Error while connecting to MySQL: {e}")
            message["message"] = str(e)
        return message
    
    def start_transaction(self):
        """Starts a new transaction."""
        if self.connection:
            self.connection.start_transaction()
            print(self.connection.in_transaction)
            print("Transaction started")
        else:
            print("Transaction already in progress")
    
    def commit_transaction(self):
        """Commits the current transaction."""
        if self.connection:
            # print(self.connection.in_transaction)
            self.connection.commit()
            print(self.connection.in_transaction)
            self.transaction_active = False
            print("Transaction committed")
        else:
            print("No active transaction to commit")
    
    def rollback_transaction(self):
        """Rolls back the current transaction."""
        if self.connection:
            self.connection.rollback()
            self.transaction_active = False
            print("Transaction rolled back")
        else:
            print("No active transaction to rollback")
    
    def delete_table(self, table_name):
        try:
            query = f"DROP TABLE IF EXISTS {table_name}"
            result = self.execute_final(query)
            print(f"Table {table_name} deleted")
            if result is not True:
                raise Error("Failed to delete table")
            return True
        except Error as e:
            return e
        
    def create_index(self, table_name, index_name, columns):
        try:
            column_list = ', '.join(columns)
            query = f"CREATE INDEX {index_name} ON {table_name} ({column_list})"
            result = self.execute_final(query)
            if result is not True:
                raise Error("Failed to create index")
            return True
        except Error as e:
            print(f"Error creating index: {e}")
            return e
    
    def execute(self, query: str, params: tuple = ()) -> bool:
        try:
            self.cursor.execute(query, params)
            return True
        except Error as e:
            print(f"Error executing query: {e}")
            return e
        
    def execute_final(self, query: str, params: tuple = ()) -> bool:
        try:
            self.cursor.execute(query, params)
            self.connection.commit()
            return True
        except Error as e:
            print(f"Error executing query: {e}")
            return e

    def fetch(self, query: str, params: tuple = ()) -> Optional[list]:
        try:
            self.cursor.execute(query, params)
            result = self.cursor.fetchall()
            self.connection.commit()
            print("Data fetched successfully")
            return result
        except Error as e:
            print(f"Error fetching data: {e}")
            return e

    def close(self) -> None:
        if self.connection.is_connected():
            self.cursor.close()
            self.connection.close()
            print("MySQL connection is closed")

if __name__ == "__main__":
    db = Database()
    
    db.start_transaction()
    # Perform some DML operations
    db.execute("INSERT INTO test_table (data) VALUES (%s)", ("Test data",))
    # Rollback the transaction
    # db.rollback_transaction()
    db.commit_transaction()
    
    # Check if data is present in test_table (should be empty if rollback worked)
    result = db.fetch("SELECT * FROM test_table")
    print("Test table data after rollback:", result)  # Should print an empty list if rollback succeeded

    db.close()
