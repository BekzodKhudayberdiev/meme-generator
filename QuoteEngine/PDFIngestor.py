import os
import re
import subprocess
import tempfile
from typing import List

from .IngestorInterface import IngestorInterface
from .QuoteModel import QuoteModel


class PDFIngestor(IngestorInterface):
    """Ingest quotes from .pdf files via the pdftotext CLI utility."""

    allowed_extensions = ['pdf']

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        if not cls.can_ingest(path):
            raise ValueError(f'Cannot ingest file type: {path}')

        tmp_file = tempfile.NamedTemporaryFile(suffix='.txt', delete=False)
        tmp_path = tmp_file.name
        tmp_file.close()

        try:
            result = subprocess.run(
                ['pdftotext', path, tmp_path],
                capture_output=True,
                text=True
            )
            if result.returncode != 0:
                raise RuntimeError(
                    f'pdftotext failed for {path}: {result.stderr}'
                )

            with open(tmp_path, 'r', encoding='utf-8') as f:
                text = f.read()

            quotes = []
            for match in re.finditer(r'"([^"]+)"\s*-\s*([^\n"]+)', text):
                body = match.group(1).strip()
                author = match.group(2).strip()
                if body and author:
                    quotes.append(QuoteModel(body, author))
            return quotes
        finally:
            os.remove(tmp_path)
