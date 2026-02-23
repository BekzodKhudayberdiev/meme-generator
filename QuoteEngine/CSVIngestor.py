from typing import List

import pandas as pd

from .IngestorInterface import IngestorInterface
from .QuoteModel import QuoteModel


class CSVIngestor(IngestorInterface):
    """Ingest quotes from .csv files. Expected columns: ``body``, ``author``"""

    allowed_extensions = ['csv']

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        if not cls.can_ingest(path):
            raise ValueError(f'Cannot ingest file type: {path}')

        df = pd.read_csv(path, header=0)
        return [
            QuoteModel(row['body'], row['author'])
            for _, row in df.iterrows()
        ]
