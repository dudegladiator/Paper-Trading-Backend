from typing import List
from fastapi import APIRouter, Request, HTTPException, Header
from Dashboard.dashboard_service import portfolio, transaction, get_user, dashboard_result
from utils.loggings import log_creator
from routes.extension_routes import db

router = APIRouter(prefix="/api")

# Dependency to check user
def validate_user(db, api_key):
    user_data = get_user(db, api_key)
    if not user_data:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return user_data

@router.get("/portfolio", response_model=List[dict])
async def get_portfolio(request: Request, api_key: str = Header(...), stock: str = None):
    try:
        
        user_data = validate_user(db, api_key)
        return portfolio(db, api_key, stock)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/transaction", response_model=List[dict])
async def get_transaction(request: Request, api_key: str = Header(...), 
                          stock: str = None, transaction_type: str = None, 
                          start_date: str = None, end_date: str = None):
    try:
        
        user_data = validate_user(db, api_key)
        return transaction(db, api_key, stock, transaction_type, start_date, end_date)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/user", response_model=dict)
async def fetch_user(request: Request, api_key: str = Header(...)):
    try:
        
        return validate_user(db, api_key)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/dashboard", response_model=List[dict])
async def get_dashboard(request: Request, team: str = Header(...)):
    try:
        
        return dashboard_result(db, team)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))

