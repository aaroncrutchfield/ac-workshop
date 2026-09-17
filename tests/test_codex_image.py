import importlib.util
from pathlib import Path
import tempfile
import unittest
import uuid

SCRIPT = Path(__file__).resolve().parents[1] / 'skills/codex-images/scripts/codex_image.py'
spec = importlib.util.spec_from_file_location('codex_image', SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

class ArtifactSelection(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.home = Path(self.tmp.name)
        self.thread = str(uuid.uuid4())
        self.directory = self.home / 'generated_images' / self.thread
        self.directory.mkdir(parents=True)
        self.events = [{'type': 'thread.started', 'thread_id': self.thread}]

    def test_only_current_thread_selected(self):
        expected = self.directory / 'one.png'
        expected.write_bytes(b'image')
        other = self.home / 'generated_images' / str(uuid.uuid4())
        other.mkdir()
        (other / 'newer.png').write_bytes(b'unrelated')
        self.assertEqual(module.select_image(self.events, self.home), expected.resolve())

    def test_no_image_fails(self):
        with self.assertRaises(ValueError):
            module.select_image(self.events, self.home)

    def test_multiple_images_fail(self):
        for name in ['one.png', 'two.png']:
            (self.directory / name).write_bytes(b'image')
        with self.assertRaises(ValueError):
            module.select_image(self.events, self.home)

    def test_missing_thread_fails(self):
        with self.assertRaises(ValueError):
            module.select_image([], self.home)

    def test_path_traversal_fails(self):
        with self.assertRaises(ValueError):
            module.select_image([{'type': 'thread.started', 'thread_id': '../other'}], self.home)

    def test_symlink_image_not_selected(self):
        target = self.home / 'outside.png'
        target.write_bytes(b'image')
        (self.directory / 'link.png').symlink_to(target)
        with self.assertRaises(ValueError):
            module.select_image(self.events, self.home)

if __name__ == '__main__':
    unittest.main()
