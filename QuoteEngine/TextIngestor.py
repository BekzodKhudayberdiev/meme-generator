from typing import List

from .IngestorInterface import IngestorInterface
from .QuoteModel import QuoteModel


class TextIngestor(IngestorInterface):
    """Ingest quotes from .txt files. Expected format: ``body - author``"""

    allowed_extensions = ['txt']

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        if not cls.can_ingest(path):
            raise ValueError(f'Cannot ingest file type: {path}')

        quotes = []
        with open(path, 'r', encoding='utf-8-sig') as f:
            for line in f:
                line = line.strip()
                if ' - ' not in line:
                    continue
                body, author = line.rsplit(' - ', 1)
                body = body.strip().strip('"')
                author = author.strip()
                if body and author:
                    quotes.append(QuoteModel(body, author))
        return quotes
