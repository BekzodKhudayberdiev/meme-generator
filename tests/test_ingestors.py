import os
import unittest

from QuoteEngine import (
    CSVIngestor, DocxIngestor, Ingestor, PDFIngestor, QuoteModel, TextIngestor,
)

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', '_data', 'DogQuotes')


class TestCanIngest(unittest.TestCase):

    def test_text_ingestor_accepts_txt(self):
        self.assertTrue(TextIngestor.can_ingest('file.txt'))

    def test_text_ingestor_rejects_csv(self):
        self.assertFalse(TextIngestor.can_ingest('file.csv'))

    def test_docx_ingestor_accepts_docx(self):
        self.assertTrue(DocxIngestor.can_ingest('file.docx'))

    def test_pdf_ingestor_accepts_pdf(self):
        self.assertTrue(PDFIngestor.can_ingest('file.pdf'))

    def test_csv_ingestor_accepts_csv(self):
        self.assertTrue(CSVIngestor.can_ingest('file.csv'))


class TestIngestorDispatch(unittest.TestCase):

    def test_raises_for_unsupported_type(self):
        with self.assertRaises(ValueError):
            Ingestor.parse('file.xyz')


class TestTextIngestor(unittest.TestCase):

    PATH = os.path.join(DATA_DIR, 'DogQuotesTXT.txt')

    def test_returns_list_of_quote_models(self):
        quotes = TextIngestor.parse(self.PATH)
        self.assertIsInstance(quotes, list)
        self.assertTrue(all(isinstance(q, QuoteModel) for q in quotes))

    def test_quotes_not_empty(self):
        quotes = TextIngestor.parse(self.PATH)
        self.assertGreater(len(quotes), 0)

    def test_raises_for_wrong_extension(self):
        with self.assertRaises(ValueError):
            TextIngestor.parse('file.csv')


class TestDocxIngestor(unittest.TestCase):

    PATH = os.path.join(DATA_DIR, 'DogQuotesDOCX.docx')

    def test_returns_list_of_quote_models(self):
        quotes = DocxIngestor.parse(self.PATH)
        self.assertIsInstance(quotes, list)
        self.assertTrue(all(isinstance(q, QuoteModel) for q in quotes))

    def test_quotes_not_empty(self):
        quotes = DocxIngestor.parse(self.PATH)
        self.assertGreater(len(quotes), 0)

    def test_raises_for_wrong_extension(self):
        with self.assertRaises(ValueError):
            DocxIngestor.parse('file.txt')


class TestPDFIngestor(unittest.TestCase):

    PATH = os.path.join(DATA_DIR, 'DogQuotesPDF.pdf')

    def test_returns_list_of_quote_models(self):
        quotes = PDFIngestor.parse(self.PATH)
        self.assertIsInstance(quotes, list)
        self.assertTrue(all(isinstance(q, QuoteModel) for q in quotes))

    def test_quotes_not_empty(self):
        quotes = PDFIngestor.parse(self.PATH)
        self.assertGreater(len(quotes), 0)

    def test_raises_for_wrong_extension(self):
        with self.assertRaises(ValueError):
            PDFIngestor.parse('file.txt')


class TestCSVIngestor(unittest.TestCase):

    PATH = os.path.join(DATA_DIR, 'DogQuotesCSV.csv')

    def test_returns_list_of_quote_models(self):
        quotes = CSVIngestor.parse(self.PATH)
        self.assertIsInstance(quotes, list)
        self.assertTrue(all(isinstance(q, QuoteModel) for q in quotes))

    def test_quotes_not_empty(self):
        quotes = CSVIngestor.parse(self.PATH)
        self.assertGreater(len(quotes), 0)

    def test_raises_for_wrong_extension(self):
        with self.assertRaises(ValueError):
            CSVIngestor.parse('file.txt')


class TestIngestor(unittest.TestCase):

    def test_parses_txt(self):
        quotes = Ingestor.parse(os.path.join(DATA_DIR, 'DogQuotesTXT.txt'))
        self.assertGreater(len(quotes), 0)

    def test_parses_docx(self):
        quotes = Ingestor.parse(os.path.join(DATA_DIR, 'DogQuotesDOCX.docx'))
        self.assertGreater(len(quotes), 0)

    def test_parses_pdf(self):
        quotes = Ingestor.parse(os.path.join(DATA_DIR, 'DogQuotesPDF.pdf'))
        self.assertGreater(len(quotes), 0)

    def test_parses_csv(self):
        quotes = Ingestor.parse(os.path.join(DATA_DIR, 'DogQuotesCSV.csv'))
        self.assertGreater(len(quotes), 0)


if __name__ == '__main__':
    unittest.main()
