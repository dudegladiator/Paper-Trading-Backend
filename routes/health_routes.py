from fastapi import APIRouter
from Dashboard.dashboard_service import get_user
from routes.extension_routes import db

router = APIRouter(prefix="/health")

@router.get("/ping")
def ping():
    return {"status": "ok"}

@router.get("/dbconnect")
def connect():
    db.connect()
    return {"status": "ok"}

@router.get("/dbclose")
def close():
    db.close()
    return {"status": "ok"}

@router.get("/dbhealth")
def db_health():
    try:
        data = get_user(db, "49127765")
        return {"status": "Database connected", "data": data}
    except Exception as e:
        return {"status": "Database connection failed", "error": str(e)}   