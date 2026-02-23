"""Flask web application for the Meme Generator."""

import os
import random
import tempfile

import requests
from flask import Flask, abort, render_template, request

from MemeGenerator import MemeEngine
from QuoteEngine import Ingestor, QuoteModel

app = Flask(__name__)

meme = MemeEngine('./static')


def setup():
    """Load all resources and return quotes and image paths."""
    quote_files = [
        './_data/DogQuotes/DogQuotesTXT.txt',
        './_data/DogQuotes/DogQuotesDOCX.docx',
        './_data/DogQuotes/DogQuotesPDF.pdf',
        './_data/DogQuotes/DogQuotesCSV.csv',
    ]

    quotes = []
    for f in quote_files:
        try:
            quotes.extend(Ingestor.parse(f))
        except Exception as e:
            print(f'Warning: could not parse {f}: {e}')

    images_path = './_data/photos/dog/'
    imgs = [
        os.path.join(root, name)
        for root, _dirs, files in os.walk(images_path)
        for name in files
    ]

    return quotes, imgs


quotes, imgs = setup()


@app.route('/')
def meme_rand():
    """Generate a random meme and render it."""
    img = random.choice(imgs)
    quote = random.choice(quotes)
    path = '/' + meme.make_meme(img, quote.body, quote.author).lstrip('./')
    return render_template('meme.html', path=path)


@app.route('/create', methods=['GET'])
def meme_form():
    """Render the user input form for custom memes."""
    return render_template('meme_form.html')


@app.route('/create', methods=['POST'])
def meme_post():
    """Create a user-defined meme from a submitted URL and quote."""
    image_url = request.form.get('image_url')
    body = request.form.get('body', '')
    author = request.form.get('author', '')

    if not image_url:
        abort(400, description='image_url is required')

    tmp_file = tempfile.NamedTemporaryFile(
        suffix='.jpg', delete=False
    )
    tmp_path = tmp_file.name
    tmp_file.close()

    try:
        response = requests.get(image_url, timeout=10)
        response.raise_for_status()
        with open(tmp_path, 'wb') as f:
            f.write(response.content)

        path = '/' + meme.make_meme(tmp_path, body, author).lstrip('./')
    except requests.RequestException as e:
        abort(400, description=f'Could not fetch image: {e}')
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)

    return render_template('meme.html', path=path)


if __name__ == '__main__':
    app.run()
