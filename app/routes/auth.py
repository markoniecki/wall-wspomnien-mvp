from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from starlette.status import HTTP_303_SEE_OTHER

from app.db import get_db
from app.models import User

router = APIRouter()

@router.get("/login", response_class=HTMLResponse)
def login_page():
    return """
    <h2>Logowanie</h2>
    <form method="post">
        <input type="email" name="email" required placeholder="Email"><br><br>
        <input type="password" name="password" required placeholder="Hasło"><br><br>
        <button>Zaloguj</button>
    </form>
    """
@router.post("/login")
def login(
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == email).first()

    if not user or not user.check_password(password):
        return HTMLResponse("Nieprawidłowe dane", status_code=401)

    response = RedirectResponse("/dashboard", status_code=HTTP_303_SEE_OTHER)
    response.set_cookie("user_id", str(user.id), httponly=True)

    return response

@router.get("/logout")
def logout():
    response = RedirectResponse("/login", status_code=303)
    response.delete_cookie("user_id")
    return response