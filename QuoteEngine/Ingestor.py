from typing import List

from .CSVIngestor import CSVIngestor
from .DocxIngestor import DocxIngestor
from .IngestorInterface import IngestorInterface
from .PDFIngestor import PDFIngestor
from .QuoteModel import QuoteModel
from .TextIngestor import TextIngestor


class Ingestor(IngestorInterface):
    """Unified interface that delegates to the correct ingestor by file type."""

    _ingestors = [TextIngestor, DocxIngestor, PDFIngestor, CSVIngestor]

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        for ingestor in cls._ingestors:
            if ingestor.can_ingest(path):
                return ingestor.parse(path)
        raise ValueError(f'No ingestor available for file: {path}')
