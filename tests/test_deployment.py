import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'deploy' / 'soccl-deploy.sh'


@unittest.skipUnless(os.name == 'posix' and shutil.which('bash'), 'Linux deployment tooling')
class DeploymentHealthTests(unittest.TestCase):
    def run_check(self, mode, fail_english=False):
        with tempfile.TemporaryDirectory() as directory:
            log = Path(directory) / 'requests.txt'
            script = """
source "$1"
systemctl() { return 0; }
curl() {
    printf '%s\n' "$*" >> "$CHECK_LOG"
    if [[ "$FAIL_ENGLISH" == 1 && "$*" == *schoolofcode.ca* ]]; then
        printf 502
    elif [[ "$*" == *sample-scratch-build-week* ]]; then
        printf 404
    else
        printf 200
    fi
}
"$2"
"""
            result = subprocess.run(
                ['bash', '-c', script, 'test', str(SCRIPT), mode],
                env={**os.environ, 'CHECK_LOG': str(log), 'FAIL_ENGLISH': str(int(fail_english))},
                capture_output=True,
            )
            return result.returncode, log.read_text() if log.exists() else ''

    def test_activation_and_rollback_check_both_domains(self):
        for mode in ('target_health_once', 'rollback_health_once'):
            with self.subTest(mode=mode):
                status, requests = self.run_check(mode)
                self.assertEqual(status, 0)
                for host in ('shkolakoda.com', 'schoolofcode.ca'):
                    self.assertIn('Host: ' + host, requests)
                    self.assertIn('https://' + host + '/', requests)

    def test_english_failure_rejects_release(self):
        for mode in ('target_health_once', 'rollback_health_once'):
            with self.subTest(mode=mode):
                status, _ = self.run_check(mode, fail_english=True)
                self.assertNotEqual(status, 0)
