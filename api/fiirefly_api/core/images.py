from io import BytesIO
from pathlib import Path

from django.core.files.base import ContentFile
from PIL import Image, ImageOps


def square_webp(file, size=512, quality=80):
    """Crop en carré (centre) + resize + webp, sinon les photos sont enormes."""
    img = Image.open(file)
    # les photos de tel sont souvent tournées via l'EXIF
    img = ImageOps.exif_transpose(img)
    img = ImageOps.fit(img.convert('RGB'), (size, size), Image.Resampling.LANCZOS)
    buf = BytesIO()
    img.save(buf, 'WEBP', quality=quality)
    name = Path(getattr(file, 'name', '') or 'photo').stem
    return ContentFile(buf.getvalue(), name=f'{name}.webp')
