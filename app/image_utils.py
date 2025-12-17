from PIL import Image
import os


# dopasowane do A4 pion z marginesami
# PDF_MAX_WIDTH = 640  # px
PDF_MAX_WIDTH = 320  # px
JPEG_QUALITY = 85


def process_image(input_path: str) -> str:
    """
    Skaluje obraz do szerokości PDF (A4 pion),
    zachowuje proporcje, zapisuje jako JPEG.
    """

    img = Image.open(input_path)

    # poprawna orientacja (telefony!)
    try:
        exif = img._getexif()
        if exif:
            orientation = exif.get(274)
            if orientation == 3:
                img = img.rotate(180, expand=True)
            elif orientation == 6:
                img = img.rotate(270, expand=True)
            elif orientation == 8:
                img = img.rotate(90, expand=True)
    except Exception:
        pass

    # konwersja do RGB (PDF safe)
    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")

    width, height = img.size

    # skaluj tylko jeśli za szerokie
    if width > PDF_MAX_WIDTH:
        ratio = PDF_MAX_WIDTH / float(width)
        new_height = int(height * ratio)
        img = img.resize(
            (PDF_MAX_WIDTH, new_height),
            Image.LANCZOS
        )

    base, _ = os.path.splitext(input_path)
    output_path = f"{base}.jpg"

    img.save(
        output_path,
        "JPEG",
        quality=JPEG_QUALITY,
        optimize=True,
        progressive=True
    )

    if output_path != input_path:
        os.remove(input_path)

    return output_path
