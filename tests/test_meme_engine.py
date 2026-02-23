import os
import tempfile
import unittest

from MemeGenerator import MemeEngine

IMG_PATH = os.path.join(os.path.dirname(__file__), '..', '_data', 'photos', 'dog', 'xander_1.jpg')


class TestMemeEngine(unittest.TestCase):

    IMG_PATH = IMG_PATH

    def setUp(self):
        self.output_dir = tempfile.mkdtemp()
        self.engine = MemeEngine(self.output_dir)

    def test_output_dir_created(self):
        new_dir = os.path.join(self.output_dir, 'sub')
        MemeEngine(new_dir)
        self.assertTrue(os.path.isdir(new_dir))

    def test_make_meme_returns_path(self):
        path = self.engine.make_meme(self.IMG_PATH, 'Woof', 'Doggo')
        self.assertIsInstance(path, str)

    def test_make_meme_file_exists(self):
        path = self.engine.make_meme(self.IMG_PATH, 'Woof', 'Doggo')
        self.assertTrue(os.path.isfile(path))

    def test_make_meme_respects_width(self):
        from PIL import Image
        path = self.engine.make_meme(self.IMG_PATH, 'Woof', 'Doggo', width=300)
        with Image.open(path) as img:
            self.assertEqual(img.width, 300)

    def test_make_meme_default_width(self):
        from PIL import Image
        path = self.engine.make_meme(self.IMG_PATH, 'Woof', 'Doggo')
        with Image.open(path) as img:
            self.assertEqual(img.width, 500)

    def test_make_meme_raises_for_missing_file(self):
        with self.assertRaises(FileNotFoundError):
            self.engine.make_meme('nonexistent.jpg', 'Woof', 'Doggo')

    def test_make_meme_raises_for_unsupported_format(self):
        with self.assertRaises(ValueError):
            self.engine.make_meme('file.gif', 'Woof', 'Doggo')


if __name__ == '__main__':
    unittest.main()
