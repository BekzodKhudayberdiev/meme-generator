"""QuoteEngine package for ingesting and representing quotes from various file formats."""

from .QuoteModel import QuoteModel
from .IngestorInterface import IngestorInterface
from .TextIngestor import TextIngestor
from .DocxIngestor import DocxIngestor
from .PDFIngestor import PDFIngestor
from .CSVIngestor import CSVIngestor
from .Ingestor import Ingestor

__all__ = [
    'QuoteModel',
    'IngestorInterface',
    'TextIngestor',
    'DocxIngestor',
    'PDFIngestor',
    'CSVIngestor',
    'Ingestor',
]
