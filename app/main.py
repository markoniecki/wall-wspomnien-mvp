from fastapi import FastAPI
from app.db import engine
from app import models
from app.routes import event
from fastapi.responses import HTMLResponse

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(event.router)
from fastapi.staticfiles import StaticFiles

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
        <body>
            <h1>Wall Wspomnień</h1>

            <form method="post" action="/event/create">
                <label>Tytuł wydarzenia</label><br>
                <input type="text" name="title" required><br><br>

                <label>Email organizatora</label><br>
                <input type="email" name="organizer_email" required><br><br>

                <label>Czas trwania walla</label><br>
                <select name="validity_minutes" required>
                    <option value="1">1 minuta (test)</option>
                    <option value="60">1 godzina</option>
                    <option value="180">3 godziny</option>
                    <option value="360">6 godzin</option>
                    <option value="720">12 godzin</option>
                    <option value="1440" selected>24 godziny</option>
                </select><br><br>

                <button type="submit">Utwórz wall</button>
            </form>
        </body>
    </html>
    """

