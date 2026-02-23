import os
import random

from PIL import Image, ImageDraw, ImageFont


class MemeEngine:
    """Generate captioned meme images using Pillow."""

    def __init__(self, output_dir: str) -> None:
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def _load_and_resize(self, img_path: str, width: int) -> Image.Image:
        """Load image from disk and resize to max width."""
        ext = img_path.rsplit('.', 1)[-1].lower()
        if ext not in ('jpg', 'jpeg', 'png'):
            raise ValueError(f'Unsupported image format: {ext}')
        if not os.path.exists(img_path):
            raise FileNotFoundError(f'Image not found: {img_path}')
        img = Image.open(img_path)
        ratio = width / img.width
        return img.resize((width, int(img.height * ratio)), Image.LANCZOS)

    def _get_font(self, size: int) -> ImageFont.FreeTypeFont:
        """Load a TrueType font, falling back to default."""
        try:
            return ImageFont.truetype('/Library/Fonts/Arial.ttf', size=size)
        except OSError:
            return ImageFont.load_default()

    def _add_caption(self, img: Image.Image, text: str, author: str) -> None:
        """Draw the quote caption at a random position."""
        draw = ImageDraw.Draw(img)
        font = self._get_font(20)
        small_font = self._get_font(16)
        x = random.randint(10, max(10, img.width - 300))
        y = random.randint(10, max(10, img.height - 80))
        caption = f'"{text}"'
        attribution = f'- {author}'
        draw.text((x + 1, y + 1), caption, fill='black', font=font)
        draw.text((x, y), caption, fill='white', font=font)
        draw.text((x + 1, y + 26), attribution, fill='black', font=small_font)
        draw.text((x, y + 25), attribution, fill='white', font=small_font)

    def _save(self, img: Image.Image) -> str:
        """Save image to output directory and return the path."""
        out_path = os.path.join(
            self.output_dir, f'meme_{random.randint(0, 1_000_000)}.jpg'
        )
        img.save(out_path)
        return out_path

    def make_meme(self, img_path: str, text: str, author: str, width: int = 500) -> str:
        """Generate a captioned meme. Returns the output path."""
        img = self._load_and_resize(img_path, width)
        self._add_caption(img, text, author)
        return self._save(img)
