# Meme Generator

A Python web application that generates captioned meme images from dog photos and inspirational quotes. Quotes are ingested from multiple file formats (TXT, DOCX, PDF, CSV) and overlaid onto images using Pillow. The app is runnable as both a Flask web server and a CLI tool.

---

## Overview

The project is split into two core modules:

- **QuoteEngine** – ingests quotes from various file types and models them as `QuoteModel` objects.
- **MemeGenerator** – loads images, resizes them, and overlays a quote caption using Pillow.

An `app.py` Flask server and a `meme.py` CLI tool bring these two modules together.

---

## Setup and Running

### Prerequisites

- Python 3.8+
- `pdftotext` CLI utility (part of the `poppler` suite)
  - macOS: `brew install poppler`
  - Ubuntu: `sudo apt-get install poppler-utils`

### Install dependencies

```bash
python -m venv venv
source venv/bin/activate       # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Run the Flask web server

```bash
flask --app app run
# or
python app.py
```

Open [http://localhost:5000](http://localhost:5000) in your browser.

### Run the CLI meme generator

```bash
python meme.py                          # fully random
python meme.py --path image.jpg         # custom image
python meme.py --body "Woof" --author "Dog"           # custom quote
python meme.py --path image.jpg --body "Woof" --author "Dog"
```

Prints the path of the generated meme image.

---

## Module Descriptions

### `QuoteEngine/`

Provides classes for loading quotes from different file formats.

| Class | File | Description |
|---|---|---|
| `QuoteModel` | `QuoteModel.py` | Data class holding `body` and `author` string fields. `str()` renders `"body" - author`. |
| `IngestorInterface` | `IngestorInterface.py` | Abstract base class. Defines `can_ingest(path)` classmethod and abstract `parse(path)` classmethod. |
| `TextIngestor` | `TextIngestor.py` | Parses `.txt` files. Each line: `body - author`. No third-party dependencies. |
| `DocxIngestor` | `DocxIngestor.py` | Parses `.docx` files using **python-docx**. Each paragraph: `body - author`. |
| `PDFIngestor` | `PDFIngestor.py` | Parses `.pdf` files using the **pdftotext** CLI via `subprocess`. Manages a temporary text file. |
| `CSVIngestor` | `CSVIngestor.py` | Parses `.csv` files using **pandas**. Expects `body` and `author` columns. |
| `Ingestor` | `Ingestor.py` | Encapsulates all ingestors. `Ingestor.parse(path)` auto-detects and delegates to the correct ingestor. |

**Example:**

```python
from QuoteEngine import Ingestor, QuoteModel

quotes = Ingestor.parse('./_data/DogQuotes/DogQuotesCSV.csv')
for q in quotes:
    print(q)  # "Chase the mailman" - Skittle
```

### `MemeGenerator/`

Provides the `MemeEngine` class for producing captioned images.

| Class | File | Description |
|---|---|---|
| `MemeEngine` | `MemeEngine.py` | Loads an image, resizes it to ≤500 px wide (maintaining aspect ratio), and overlays a quote caption at a random position. Depends on **Pillow**. |

**Signature:**

```python
MemeEngine(output_dir: str)
make_meme(img_path, text, author, width=500) -> str  # returns saved image path
```

**Example:**

```python
from MemeGenerator import MemeEngine

engine = MemeEngine('./output')
path = engine.make_meme('photo.jpg', 'To bork or not to bork', 'Bork')
print(path)  # ./output/meme_123456.jpg
```

### `app.py`

Flask web application with three routes:

| Route | Method | Description |
|---|---|---|
| `/` | GET | Displays a randomly generated meme. |
| `/create` | GET | Renders the meme creation form. |
| `/create` | POST | Fetches an image from a URL, generates a custom meme, and displays it. |

### `meme.py`

CLI entry point. Accepts optional `--path`, `--body`, and `--author` arguments and prints the path to the generated meme.

---

## Dependencies

See `requirements.txt`. Key packages:

- `Flask` – web framework
- `Pillow` – image processing
- `pandas` – CSV parsing
- `python-docx` – DOCX parsing
- `requests` – HTTP image fetching
