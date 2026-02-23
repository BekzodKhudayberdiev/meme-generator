import os
import random

from PIL import Image, ImageDraw, ImageFont


class MemeEngine:
    """Generate captioned meme images using Pillow."""

    def __init__(self, output_dir: str) -> None:
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def make_meme(
        self,
        img_path: str,
        text: str,
        author: str,
        width: int = 500
    ) -> str:
        """Resize image to max width and overlay a quote caption. Returns output path."""
        ext = img_path.rsplit('.', 1)[-1].lower()
        if ext not in ('jpg', 'jpeg', 'png'):
            raise ValueError(f'Unsupported image format: {ext}')

        if not os.path.exists(img_path):
            raise FileNotFoundError(f'Image not found: {img_path}')

        with Image.open(img_path) as img:
            ratio = width / img.width
            img = img.resize((width, int(img.height * ratio)), Image.LANCZOS)

            draw = ImageDraw.Draw(img)

            try:
                font = ImageFont.truetype('/Library/Fonts/Arial.ttf', size=20)
                small_font = ImageFont.truetype('/Library/Fonts/Arial.ttf', size=16)
            except OSError:
                font = ImageFont.load_default()
                small_font = font

            x = random.randint(10, max(10, img.width - 300))
            y = random.randint(10, max(10, img.height - 80))

            caption = f'"{text}"'
            attribution = f'- {author}'

            draw.text((x + 1, y + 1), caption, fill='black', font=font)
            draw.text((x, y), caption, fill='white', font=font)
            draw.text((x + 1, y + 26), attribution, fill='black', font=small_font)
            draw.text((x, y + 25), attribution, fill='white', font=small_font)

            out_path = os.path.join(
                self.output_dir, f'meme_{random.randint(0, 1_000_000)}.jpg'
            )
            img.save(out_path)
            return out_path
