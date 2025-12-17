from fastapi import APIRouter, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy.orm.session import Session

from app.auth_utils import get_current_user
from app.db import get_db

router = APIRouter()
@router.get("/dashboard", response_class=HTMLResponse)
def dashboard(
    user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not user:
        return HTMLResponse("Zaloguj się", status_code=401)

    rows = ""
    for event in user.events:
        rows += f"""
        <h2>➕ Utwórz nowy wall</h2>

<form method="post" action="/event/create">
    <input type="text" name="title" required placeholder="Tytuł walla"><br><br>

    <input type="email" name="organizer_email"
           required placeholder="Email organizatora"><br><br>

    <select name="validity_minutes" required>
        <option value="1">1 minuta</option>
        <option value="60">1 godzina</option>
        <option value="180">3 godziny</option>
        <option value="360">6 godzin</option>
        <option value="720">12 godzin</option>
        <option value="1440">24 godziny</option>
    </select><br><br>

    <button type="submit">Utwórz wall</button>
</form>

<hr>

        <tr>
            <td>{event.title}</td>
            <td>{event.status}</td>
            <td>
                <a href="/event/{event.token}">Wall</a> |
                <a href="/admin/{event.admin_token}">Admin</a>
                <a href="/logout">Wyloguj</a>
            </td>
        </tr>
        """

    return f"""
    <h1>Dashboard</h1>
    <p>Zalogowany jako: {user.email}</p>

    <table border="1" cellpadding="8">
        <tr>
            <th>Tytuł</th>
            <th>Status</th>
            <th>Linki</th>
        </tr>
        {rows}
    </table>

    <br>
    <a href="/">➕ Utwórz nowy wall</a>
    """

