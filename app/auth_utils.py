from fastapi import Request, Depends
from sqlalchemy.orm import Session
from app.db import get_db
from app.models import User

def get_current_user(
    request: Request,
    db: Session = Depends(get_db)
):
    user_id = request.cookies.get("user_id")

    if not user_id:
        return None

    return db.query(User).filter(User.id == int(user_id)).first()
