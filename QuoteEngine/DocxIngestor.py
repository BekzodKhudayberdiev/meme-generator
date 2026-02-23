from typing import List

import docx

from .IngestorInterface import IngestorInterface
from .QuoteModel import QuoteModel


class DocxIngestor(IngestorInterface):
    """Ingest quotes from .docx files. Expected format: ``body - author``"""

    allowed_extensions = ['docx']

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        if not cls.can_ingest(path):
            raise ValueError(f'Cannot ingest file type: {path}')

        quotes = []
        doc = docx.Document(path)
        for paragraph in doc.paragraphs:
            line = paragraph.text.strip()
            if ' - ' not in line:
                continue
            body, author = line.rsplit(' - ', 1)
            body = body.strip().strip('"')
            author = author.strip()
            if body and author:
                quotes.append(QuoteModel(body, author))
        return quotes
