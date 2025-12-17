import os
from playwright.sync_api import sync_playwright
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="app/templates")
import os
from copy import deepcopy

import os
from playwright.sync_api import sync_playwright
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="app/templates")


def generate_event_pdf(event, posts):
    import os
    from copy import deepcopy

    os.makedirs("pdfs", exist_ok=True)
    file_path = os.path.abspath(f"pdfs/event_{event.id}.pdf")

    safe_posts = []

    for post in posts:
        post_copy = deepcopy(post)

        if post_copy.image_path:
            post_copy.image_url = (
                "http://127.0.0.1:8000/" + post_copy.image_path.replace("\\", "/")
            )
        else:
            post_copy.image_url = None

        safe_posts.append(post_copy)

    html_content = templates.get_template("pdf_event.html").render(
        event=event,
        posts=safe_posts
    )

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.set_content(html_content, wait_until="networkidle")
        page.wait_for_timeout(500)

        page.pdf(
            path=file_path,
            format="A4",
            print_background=True
        )

        browser.close()

    return file_path





# def generate_event_pdf(event, posts):
#     os.makedirs("pdfs", exist_ok=True)
#
#     file_path = f"pdfs/event_{event.id}.pdf"
#
#     html_content = templates.get_template("pdf_event.html").render(
#         event=event,
#         posts=posts
#     )
#
#     with sync_playwright() as p:
#         browser = p.chromium.launch()
#         page = browser.new_page()
#         page.set_content(html_content)
#         page.pdf(path=file_path, format="A4")
#         browser.close()
#
#     return file_path
