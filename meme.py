"""CLI tool for generating a random or custom captioned meme image."""

import argparse
import os
import random

from MemeGenerator import MemeEngine
from QuoteEngine import Ingestor, QuoteModel


def generate_meme(path=None, body=None, author=None):
    """Generate a meme given an optional image path and quote.

    :param path: Path to the image file; random if not provided.
    :param body: Quote body text; random if not provided.
    :param author: Quote author; required when body is provided.
    :return: Path to the generated meme image.
    :raises Exception: If body is given without author.
    """
    if path is None:
        images = './_data/photos/dog/'
        imgs = [
            os.path.join(root, name)
            for root, _dirs, files in os.walk(images)
            for name in files
        ]
        img = random.choice(imgs)
    else:
        img = path

    if body is None:
        quote_files = [
            './_data/DogQuotes/DogQuotesTXT.txt',
            './_data/DogQuotes/DogQuotesDOCX.docx',
            './_data/DogQuotes/DogQuotesPDF.pdf',
            './_data/DogQuotes/DogQuotesCSV.csv',
        ]
        quotes = []
        for f in quote_files:
            quotes.extend(Ingestor.parse(f))
        quote = random.choice(quotes)
    else:
        if author is None:
            raise ValueError('Author is required when body is provided.')
        quote = QuoteModel(body, author)

    meme = MemeEngine('./tmp')
    return meme.make_meme(img, quote.body, quote.author)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Generate a captioned meme image.'
    )
    parser.add_argument(
        '--path', type=str, default=None,
        help='Path to an image file (optional).'
    )
    parser.add_argument(
        '--body', type=str, default=None,
        help='Quote body text (optional).'
    )
    parser.add_argument(
        '--author', type=str, default=None,
        help='Quote author (required if --body is given).'
    )
    args = parser.parse_args()
    print(generate_meme(args.path, args.body, args.author))
