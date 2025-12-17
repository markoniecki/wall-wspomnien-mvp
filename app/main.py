from fastapi import FastAPI, Depends
from starlette.responses import RedirectResponse

from app.db import engine
from app import models
from app.routes import event
from fastapi.responses import HTMLResponse
from fastapi import Request
from fastapi.responses import HTMLResponse
from app.auth_utils import get_current_user

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(event.router)
from fastapi.staticfiles import StaticFiles
from app.routes import auth, dashboard

app.include_router(auth.router)
app.include_router(dashboard.router)

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

@app.get("/", response_class=HTMLResponse)
def home(request: Request, user = Depends(get_current_user)):
    if user:
        return RedirectResponse("/dashboard", status_code=303)

    return """
    <h1>Wall Wspomnień</h1>
    <p>Zbieraj życzenia, zdjęcia i wspomnienia w jednym miejscu.</p>

    <a href="/login"><button>Zaloguj się</button></a>
    """

