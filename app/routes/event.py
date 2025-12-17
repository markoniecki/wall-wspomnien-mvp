# from fastapi import APIRouter, Depends, Request, Form
# from fastapi.responses import HTMLResponse
# from sqlalchemy.orm import Session
#
# from app.db import get_db
# from app.models import Event, Post
#
# from app.pdf import generate_event_pdf
#
# from fastapi.responses import FileResponse
# from fastapi import UploadFile, File
# import os
# import uuid
# from app.image_utils import process_image
# from fastapi.responses import JSONResponse
#
# from fastapi import Form
#
# from fastapi import HTTPException
#
# from fastapi.responses import RedirectResponse
# from starlette.status import HTTP_303_SEE_OTHER
#
# router = APIRouter()
#
# @router.post("/event/create", response_class=HTMLResponse)
#
# def create_event(
#     request: Request,
#     title: str = Form(...),
#     organizer_email: str = Form(...),
#     validity_minutes: int = Form(...),
#     db: Session = Depends(get_db)
# ):
#     ALLOWED_PERIODS = {1, 60, 180, 360, 720, 1440}
#
#     if validity_minutes not in ALLOWED_PERIODS:
#         return HTMLResponse(
#             "<h3>Nieprawidłowy czas trwania walla</h3>",
#             status_code=400
#         )
#     event = Event.create(
#         title=title,
#         organizer_email=organizer_email,
#         validity_minutes=validity_minutes
#     )
#
#     db.add(event)
#     db.commit()
#     db.refresh(event)
#
#     base_url = str(request.base_url).rstrip("/")
#
#     public_url = f"{base_url}/event/{event.token}"
#     admin_url = f"{base_url}/admin/{event.admin_token}"
#     pdf_admin_url = f"{base_url}/admin/{event.admin_token}/pdf"
#
#     return f"""
#     <html>
#         <body>
#             <h2>Wall utworzony 🎉</h2>
#             <p><strong>Link dla gości:</strong></p>
#             <a href="{public_url}">{public_url}</a>
#
#             <p><strong>Link admina:</strong></p>
#             <a href="{admin_url}">{admin_url}</a>
#             <p><strong>Pobierz PDF (po zamknięciu walla):</strong></p>
#             <a href="{pdf_admin_url}">{pdf_admin_url}</a>
#
#         </body>
#     </html>
#     """
#
#
# from fastapi.responses import HTMLResponse
# from sqlalchemy.orm import Session
# from fastapi import Depends
#
#
# @router.get("/event/{token}", response_class=HTMLResponse)
# def view_event(token: str, db: Session = Depends(get_db)):
#     event = db.query(Event).filter(Event.token == token).first()
#
#     if not event:
#         return "<h2>Nie znaleziono wydarzenia</h2>"
#
#     event.close_if_expired()
#     db.commit()
#
#     posts_html = ""  # ← MUSI BYĆ TU, lokalnie w funkcji
#
#     for post in event.posts:
#         image_html = ""
#         if post.image_path:
#             image_html = f"""
#             <img src="/{post.image_path}"
#                  style="max-width:300px; display:block; margin-top:10px;">
#             """
#
#         posts_html += f"""
#         <div style="border:1px solid #ccc; padding:10px; margin-bottom:10px;">
#             <strong>{post.author_name or "Anonim"}</strong><br>
#             <p>{post.content}</p>
#             {image_html}
#             <small>{post.created_at.strftime('%Y-%m-%d %H:%M')}</small>
#         </div>
#         """
#
#     expires_at_iso = event.expires_at.isoformat()
#     form_html = f"""
#     <p><strong>Pozostały czas:</strong> <span id="countdown">...</span></p>
#
#         <form method="post"
#               action="/event/{token}/post"
#               enctype="multipart/form-data"
#               id="post-form">
#             <input type="text"
#                        name="author_name"
#                        placeholder="Twoje imię"
#                        maxlength="50">
#
#             <textarea name="content"
#                       required
#                       minlength="3"
#                       maxlength="1000"
#                       placeholder="Twoje wspomnienie (max 1000 znaków)"></textarea>
#
#             <input type="file"
#                        name="image"
#                        accept="image/*">
#             <br><br>
#             <button type="submit">Dodaj wpis</button>
#         </form>
#
#
#     <script>
#         (function () {{
#             const expiresAt = new Date("{expires_at_iso}Z").getTime();
#             const countdownEl = document.getElementById("countdown");
#             const formEl = document.getElementById("post-form");
#
#             let wallClosed = false;
#
#             function closeWallUI(message) {{
#                 wallClosed = true;
#                 if (countdownEl) countdownEl.innerText = message;
#                 if (formEl) formEl.style.display = "none";
#             }}
#
#             function updateCountdown() {{
#                 if (wallClosed) return;
#
#                 const now = Date.now();
#                 const diff = expiresAt - now;
#
#                 if (diff <= 0) {{
#                     closeWallUI("Wall został zamknięty");
#                     return;
#                 }}
#
#                 const seconds = Math.floor(diff / 1000);
#                 const minutes = Math.floor(seconds / 60);
#                 const hours = Math.floor(minutes / 60);
#
#                 let text = "";
#                 if (hours > 0) text += hours + "h ";
#                 if (minutes % 60 > 0) text += (minutes % 60) + "m ";
#                 text += (seconds % 60) + "s";
#
#                 if (countdownEl) countdownEl.innerText = text;
#             }}
#
#             async function pollStatus() {{
#                 try {{
#                     const res = await fetch("/event/{token}/status");
#                     if (!res.ok) return;
#
#                     const data = await res.json();
#                     if (data.status === "closed") {{
#                         closeWallUI("Wall został zamknięty przez organizatora");
#                     }}
#                 }} catch (e) {{
#                     // silent
#                 }}
#             }}
#
#             updateCountdown();
#             setInterval(updateCountdown, 1000);
#             setInterval(pollStatus, 5000);
#         }})();
#         </script>
#
#     """
#
#     return f"""
#
#     <html>
#         <body>
#             <h1>{event.title}</h1>
#             {form_html}
#             <hr>
#             {posts_html or "<p>Brak wpisów. Bądź pierwszy!</p>"}
#         </body>
#     </html>
#     """
#
# @router.get("/admin/{admin_token}/pdf")
# def admin_download_pdf(admin_token: str, db: Session = Depends(get_db)):
#     event = db.query(Event).filter(Event.admin_token == admin_token).first()
#
#     if not event:
#         return {"error": "Nie znaleziono wydarzenia"}
#
#     # zamknij jeśli wygasł
#     event.close_if_expired()
#     db.commit()
#
#     if event.status != "closed":
#         return {
#             "status": "active",
#             "message": "Wall jeszcze aktywny. PDF będzie dostępny po zakończeniu."
#         }
#
#     # jeśli PDF jeszcze nie wygenerowany – generuj TERAZ
#     if not event.pdf_path:
#         from app.pdf import generate_event_pdf
#         pdf_path = generate_event_pdf(event, event.posts)
#
#         event.pdf_path = pdf_path
#         db.commit()
#
#     # TU JUŻ MUSI ISTNIEĆ
#     if not event.pdf_path or not os.path.exists(event.pdf_path):
#         return {"error": "Nie udało się wygenerować PDF"}
#
#     return FileResponse(
#         path=event.pdf_path,
#         filename=f"{event.title}.pdf",
#         media_type="application/pdf"
#     )
#
#
# from fastapi import Form
# from fastapi.responses import RedirectResponse
# from starlette.status import HTTP_303_SEE_OTHER
#
#
# @router.post("/event/{token}/post")
# def add_post(
#     token: str,
#     author_name: str = Form(None),
#     content: str = Form(...),
#     image: UploadFile = File(None),
#     db: Session = Depends(get_db)
# ):
#     event = db.query(Event).filter(Event.token == token).first()
#
#     if not event:
#         return RedirectResponse("/", status_code=HTTP_303_SEE_OTHER)
#
#     event.close_if_expired()
#     db.commit()
#
#     if event.status != "active":
#         return RedirectResponse(
#             url=f"/event/{token}",
#             status_code=HTTP_303_SEE_OTHER
#         )
#
#     image_path = None
#
#     if image and image.content_type.startswith("image/"):
#         os.makedirs("uploads", exist_ok=True)
#
#         ext = os.path.splitext(image.filename)[1]
#         filename = f"{uuid.uuid4()}{ext}"
#         file_path = os.path.join("uploads", filename)
#
#         with open(file_path, "wb") as f:
#             f.write(image.file.read())
#
#         image_path = image_path = process_image(file_path)
#
#     post = Post(
#         event_id=event.id,
#         author_name=author_name,
#         content=content,
#         image_path=image_path
#     )
#
#     db.add(post)
#     db.commit()
#
#     return RedirectResponse(
#         url=f"/event/{token}",
#         status_code=HTTP_303_SEE_OTHER
#     )
#
#
#
# @router.get("/event/{token}/pdf")
# def generate_pdf(token: str, db: Session = Depends(get_db)):
#     event = db.query(Event).filter(Event.token == token).first()
#
#     if not event:
#         return {"error": "Event not found"}
#
#     event.close_if_expired()
#     db.commit()
#
#     pdf_path = generate_event_pdf(event, event.posts)
#
#     return {
#         "status": "ok",
#         "pdf": pdf_path
#     }
#
#
# @router.get("/admin/{admin_token}/pdf")
# def admin_download_pdf(admin_token: str, db: Session = Depends(get_db)):
#     event = db.query(Event).filter(Event.admin_token == admin_token).first()
#
#     if not event:
#         return {"error": "Nie znaleziono wydarzenia"}
#
#     # jeśli jeszcze nie zamknięty → zamknij
#     event.close_if_expired()
#     db.commit()
#
#     # jeśli nadal aktywny – PDF jeszcze niedostępny
#     if event.status != "closed":
#         return {
#             "status": "active",
#             "message": "Wall jeszcze aktywny. PDF będzie dostępny po 24h."
#         }
#
#     # jeśli PDF jeszcze nie wygenerowany → wygeneruj
#     if not event.pdf_path:
#         from app.pdf import generate_event_pdf
#         pdf_path = generate_event_pdf(event, event.posts)
#         event.pdf_path = pdf_path
#         db.commit()
#
#     if not os.path.exists(event.pdf_path):
#         return {"error": "Plik PDF nie istnieje"}
#
#     return FileResponse(
#         path=event.pdf_path,
#         filename=f"{event.title}.pdf",
#         media_type="application/pdf"
#     )
# @router.get("/admin/{admin_token}", response_class=HTMLResponse)
# def admin_panel(admin_token: str, db: Session = Depends(get_db)):
#     event = db.query(Event).filter(Event.admin_token == admin_token).first()
#
#     if not event:
#         return HTMLResponse("<h2>Nie znaleziono wydarzenia</h2>", status_code=404)
#
#     event.close_if_expired()
#     db.commit()
#
#     posts_count = len(event.posts)
#
#     close_button = ""
#     pdf_button = ""
#
#     if event.status == "active":
#         close_button = f"""
#         <form method="post" action="/admin/{admin_token}/close"
#               onsubmit="return confirm('Czy na pewno zamknąć wall?');">
#             <button type="submit">🔒 Zamknij wall</button>
#         </form>
#         """
#     else:
#         pdf_button = f"""
#         <a href="/admin/{admin_token}/pdf">
#             <button>📄 Pobierz PDF</button>
#         </a>
#         """
#
#     return f"""
#     <html>
#         <body style="font-family: Arial; max-width: 600px; margin: 40px auto;">
#             <h1>Panel admina</h1>
#
#             <h2>{event.title}</h2>
#
#             <p><strong>Status:</strong> {event.status}</p>
#             <p><strong>Czas trwania:</strong> {event.validity_label()}</p>
#             <p><strong>Liczba wpisów:</strong> {posts_count}</p>
#
#             <hr>
#
#             {close_button}
#             {pdf_button}
#
#             <br><br>
#             <small>Link admina – zachowaj go w bezpiecznym miejscu</small>
#         </body>
#     </html>
#     """
# @router.post("/admin/{admin_token}/close")
# def admin_close_wall(admin_token: str, db: Session = Depends(get_db)):
#     event = db.query(Event).filter(Event.admin_token == admin_token).first()
#
#     if not event:
#         return HTMLResponse("Nie znaleziono wydarzenia", status_code=404)
#
#     event.status = "closed"
#     db.commit()
#
#     return RedirectResponse(
#         url=f"/admin/{admin_token}",
#         status_code=HTTP_303_SEE_OTHER
#     )
# @router.get("/event/{token}/status")
# def event_status(token: str, db: Session = Depends(get_db)):
#     event = db.query(Event).filter(Event.token == token).first()
#
#     if not event:
#         return JSONResponse({"status": "not_found"}, status_code=404)
#
#     event.close_if_expired()
#     db.commit()
#
#     return {
#         "status": event.status,
#         "expires_at": event.expires_at.isoformat()
#     }

import os
import uuid
from datetime import datetime
from app.auth_utils import get_current_user

from fastapi import (
    APIRouter,
    Depends,
    Form,
    UploadFile,
    File,
    HTTPException,
    Request
)
from fastapi.responses import (
    HTMLResponse,
    RedirectResponse,
    FileResponse,
    JSONResponse
)
from starlette.status import HTTP_303_SEE_OTHER
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import Event, Post
from app.image_utils import process_image
from app.pdf import generate_event_pdf

router = APIRouter()

# =========================
# CREATE EVENT
# =========================

@router.post("/event/create", response_class=HTMLResponse)
def create_event(
    title: str = Form(...),
    organizer_email: str = Form(...),
    validity_minutes: int = Form(...),
    user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not user:
        return HTMLResponse("Zaloguj się", status_code=401)
    ALLOWED_PERIODS = {1, 60, 180, 360, 720, 1440}

    if validity_minutes not in ALLOWED_PERIODS:
        return HTMLResponse("Nieprawidłowy czas trwania", status_code=400)

    event = Event.create(
        title=title.strip(),
        organizer_email=organizer_email.strip(),
        validity_minutes=validity_minutes
    )
    event.user_id = user.id

    db.add(event)
    db.commit()

    return HTMLResponse(f"""
    <h2>Wall utworzony 🎉</h2>
    <p><a href="/event/{event.token}">👉 Przejdź do walla</a></p>
    <p><strong>Link admina:</strong><br>
       <a href="/admin/{event.admin_token}">
       /admin/{event.admin_token}
       </a>
    </p>
    """)


# =========================
# VIEW EVENT (WALL)
# =========================

@router.get("/event/{token}", response_class=HTMLResponse)
def view_event(token: str, db: Session = Depends(get_db)):
    event = db.query(Event).filter(Event.token == token).first()

    if not event:
        return HTMLResponse("<h2>Nie znaleziono walla</h2>", status_code=404)

    event.close_if_expired()
    db.commit()

    expires_at_iso = event.expires_at.isoformat()

    # POSTS
    posts_html = ""
    for post in event.posts:
        image_html = ""
        if post.image_path:
            image_html = f"""
            <img src="/{post.image_path}"
                 style="max-width:300px; margin-top:10px;">
            """

        posts_html += f"""
        <div style="border:1px solid #ccc; padding:10px; margin-bottom:10px;">
            <strong>{post.author_name or "Anonim"}</strong><br>
            <p>{post.content}</p>
            {image_html}
            <small>{post.created_at.strftime('%Y-%m-%d %H:%M')}</small>
        </div>
        """

    # FORM
    form_html = ""
    if event.status == "active":
        form_html = f"""
        <p><strong>Pozostały czas:</strong> <span id="countdown">...</span></p>

        <form method="post"
              action="/event/{token}/post"
              enctype="multipart/form-data"
              id="post-form">

            <input type="text" name="author_name"
                   placeholder="Twoje imię"
                   maxlength="50"><br><br>

            <textarea name="content"
                      required
                      minlength="3"
                      maxlength="1000"
                      placeholder="Twoje wspomnienie (max 1000 znaków)"></textarea><br><br>

            <input type="file" name="image" accept="image/*"><br><br>

            <button type="submit">Dodaj wpis</button>
        </form>

        <script>
        (function () {{
            const expiresAt = new Date("{expires_at_iso}Z").getTime();
            const countdownEl = document.getElementById("countdown");
            const formEl = document.getElementById("post-form");
            let wallClosed = false;

            function closeWallUI(message) {{
                wallClosed = true;
                if (countdownEl) countdownEl.innerText = message;
                if (formEl) formEl.style.display = "none";
            }}

            function updateCountdown() {{
                if (wallClosed) return;

                const diff = expiresAt - Date.now();
                if (diff <= 0) {{
                    closeWallUI("Wall został zamknięty");
                    return;
                }}

                const s = Math.floor(diff / 1000);
                const m = Math.floor(s / 60);
                const h = Math.floor(m / 60);

                let text = "";
                if (h > 0) text += h + "h ";
                if (m % 60 > 0) text += (m % 60) + "m ";
                text += (s % 60) + "s";

                countdownEl.innerText = text;
            }}

            async function pollStatus() {{
                try {{
                    const res = await fetch("/event/{token}/status");
                    if (!res.ok) return;
                    const data = await res.json();
                    if (data.status === "closed") {{
                        closeWallUI("Wall został zamknięty przez organizatora");
                    }}
                }} catch (e) {{}}
            }}

            updateCountdown();
            setInterval(updateCountdown, 1000);
            setInterval(pollStatus, 5000);
        }})();
        </script>
        """
    else:
        form_html = f"""
        <p><strong>Wall jest zamknięty</strong></p>
        <p>Ten wall działał przez <strong>{event.validity_label()}</strong></p>
        """

    return HTMLResponse(f"""
    <html>
        <body style="font-family:Arial; max-width:600px; margin:40px auto;">
            <h1>{event.title}</h1>
            {form_html}
            <hr>
            {posts_html}
        </body>
    </html>
    """)


# =========================
# ADD POST
# =========================

@router.post("/event/{token}/post")
def add_post(
    token: str,
    author_name: str = Form(None),
    content: str = Form(...),
    image: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    event = db.query(Event).filter(Event.token == token).first()

    if not event:
        return RedirectResponse("/", status_code=HTTP_303_SEE_OTHER)

    event.close_if_expired()
    db.commit()

    if event.status != "active":
        return RedirectResponse(f"/event/{token}", status_code=HTTP_303_SEE_OTHER)

    content = content.strip()
    if len(content) < 3 or len(content) > 1000:
        raise HTTPException(400, "Nieprawidłowa długość wpisu")

    if author_name:
        author_name = author_name.strip()
        if len(author_name) > 50:
            raise HTTPException(400, "Imię za długie")

    image_path = None
    if image:
        if not image.content_type.startswith("image/"):
            raise HTTPException(400, "Nieprawidłowy typ pliku")

        data = image.file.read()
        if len(data) > 5 * 1024 * 1024:
            raise HTTPException(400, "Zdjęcie za duże (max 5MB)")

        image.file.seek(0)
        os.makedirs("uploads", exist_ok=True)

        ext = os.path.splitext(image.filename)[1]
        filename = f"{uuid.uuid4()}{ext}"
        raw_path = os.path.join("uploads", filename)

        with open(raw_path, "wb") as f:
            f.write(data)

        image_path = process_image(raw_path)

    post = Post(
        event_id=event.id,
        author_name=author_name,
        content=content,
        image_path=image_path
    )

    db.add(post)
    db.commit()

    return RedirectResponse(f"/event/{token}", status_code=HTTP_303_SEE_OTHER)


# =========================
# EVENT STATUS (POLLING)
# =========================

@router.get("/event/{token}/status")
def event_status(token: str, db: Session = Depends(get_db)):
    event = db.query(Event).filter(Event.token == token).first()

    if not event:
        return JSONResponse({"status": "not_found"}, status_code=404)

    event.close_if_expired()
    db.commit()

    return {
        "status": event.status,
        "expires_at": event.expires_at.isoformat()
    }


# =========================
# ADMIN PANEL
# =========================

@router.get("/admin/{admin_token}", response_class=HTMLResponse)
def admin_panel(admin_token: str, db: Session = Depends(get_db)):
    event = db.query(Event).filter(Event.admin_token == admin_token).first()

    if not event:
        return HTMLResponse("<h2>Nie znaleziono wydarzenia</h2>", status_code=404)

    event.close_if_expired()
    db.commit()

    close_btn = ""
    pdf_btn = ""

    if event.status == "active":
        close_btn = f"""
        <form method="post" action="/admin/{admin_token}/close"
              onsubmit="return confirm('Zamknąć wall?');">
            <button>🔒 Zamknij wall</button>
        </form>
        """
    else:
        pdf_btn = f"""
        <a href="/admin/{admin_token}/pdf">
            <button>📄 Pobierz PDF</button>
        </a>
        """

    return f"""
    <html>
        <body style="font-family:Arial; max-width:600px; margin:40px auto;">
            <h1>Panel admina</h1>
            <h2>{event.title}</h2>

            <p>Status: <strong>{event.status}</strong></p>
            <p>Czas trwania: {event.validity_label()}</p>
            <p>Wpisów: {len(event.posts)}</p>

            <hr>
            {close_btn}
            {pdf_btn}
        </body>
    </html>
    """


# =========================
# ADMIN CLOSE
# =========================

@router.post("/admin/{admin_token}/close")
def admin_close_wall(admin_token: str, db: Session = Depends(get_db)):
    event = db.query(Event).filter(Event.admin_token == admin_token).first()

    if not event:
        return HTMLResponse("Nie znaleziono", status_code=404)

    event.status = "closed"
    db.commit()

    return RedirectResponse(f"/admin/{admin_token}", status_code=HTTP_303_SEE_OTHER)


# =========================
# ADMIN PDF
# =========================

@router.get("/admin/{admin_token}/pdf")
def admin_download_pdf(admin_token: str, db: Session = Depends(get_db)):
    event = db.query(Event).filter(Event.admin_token == admin_token).first()

    if not event:
        return {"error": "Nie znaleziono wydarzenia"}

    event.close_if_expired()
    db.commit()

    if event.status != "closed":
        return {"message": "Wall jeszcze aktywny"}

    if not event.pdf_path:
        pdf_path = generate_event_pdf(event, event.posts)
        event.pdf_path = pdf_path
        db.commit()

    if not event.pdf_path or not os.path.exists(event.pdf_path):
        return {"error": "Nie udało się wygenerować PDF"}

    return FileResponse(
        path=event.pdf_path,
        filename=f"{event.title}.pdf",
        media_type="application/pdf"
    )
