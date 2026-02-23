import unittest

from QuoteEngine import QuoteModel


class TestQuoteModel(unittest.TestCase):

    def setUp(self):
        self.quote = QuoteModel('To be or not to be', 'Shakespeare')

    def test_str(self):
        self.assertEqual(str(self.quote), '"To be or not to be" - Shakespeare')

    def test_repr(self):
        self.assertIn('QuoteModel', repr(self.quote))

    def test_body_and_author_stored(self):
        self.assertEqual(self.quote.body, 'To be or not to be')
        self.assertEqual(self.quote.author, 'Shakespeare')


if __name__ == '__main__':
    unittest.main()
