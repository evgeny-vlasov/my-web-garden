import os
from pathlib import Path
import shutil
import sqlite3
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'webgarden-backup' / 'restore-test-webgarden.sh'


@unittest.skipUnless(os.name == 'posix' and shutil.which('bash'), 'Linux backup tooling')
class BackupValidationTests(unittest.TestCase):
    def test_application_archives_respect_exclusions(self):
        import tarfile
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            app = root / 'app'
            app.mkdir()
            (app / 'app.py').write_text('print("source")')
            for folder in ('venv', '.git', 'uploads'):
                (app / folder).mkdir()
                (app / folder / 'example').write_text('excluded')
            archive = root / 'source.tar.gz'
            result = subprocess.run([
                'bash', '-c', 'source "$1"; backup_app_source example "$2" "$3" "$2/uploads"',
                'test', str(ROOT / 'webgarden-backup/backup-webgarden.sh'), str(app), str(archive),
            ], capture_output=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            with tarfile.open(archive) as backup:
                names = backup.getnames()
            self.assertIn('./app.py', names)
            self.assertFalse(any(name.startswith(('./venv', './.git', './uploads')) for name in names))

    def test_corrupt_sqlite_fails_integrity_validation(self):
        with tempfile.TemporaryDirectory() as directory:
            database = Path(directory) / 'data.sqlite'
            database.write_bytes(b'corrupted database')
            result = subprocess.run(
                ['bash', '-c', 'source "$1"; verify_sqlite_copy "$2"', 'test',
                 str(SCRIPT), str(database)], capture_output=True,
            )
            self.assertNotEqual(result.returncode, 0)
            database.unlink()
            with sqlite3.connect(database) as connection:
                connection.execute('CREATE TABLE example (id INTEGER)')
            result = subprocess.run(
                ['bash', '-c', 'source "$1"; verify_sqlite_copy "$2"', 'test',
                 str(SCRIPT), str(database)], capture_output=True,
            )
            self.assertEqual(result.returncode, 0, result.stderr)

    def test_success_manifest_without_archives_fails(self):
        with tempfile.TemporaryDirectory() as directory:
            backup = Path(directory) / '20260101T010101Z'
            backup.mkdir()
            (backup / 'manifest.txt').write_text('status=success\n')
            result = subprocess.run(
                ['bash', '-c', 'source "$1"; require_root() { :; }; main', 'test', str(SCRIPT)],
                env={**os.environ, 'BACKUP_ROOT': directory}, capture_output=True,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn(b'no backup archives found', result.stderr)
