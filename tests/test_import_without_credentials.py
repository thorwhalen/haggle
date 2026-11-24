"""Importing haggle must not need Kaggle credentials (haggle#5)."""

import os
import subprocess
import sys


def _env_without_credentials(home):
    env = {
        k: v
        for k, v in os.environ.items()
        if not k.startswith("KAGGLE_") and k != "PYTHONSAFEPATH"
    }
    env["HOME"] = str(home)
    env["USERPROFILE"] = str(home)
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    env["PYTHONPATH"] = os.pathsep.join(p for p in (root, env.get("PYTHONPATH")) if p)
    return env


def test_import_needs_no_credentials(tmp_path):
    done = subprocess.run(
        [sys.executable, "-c", "import haggle.dacc"],
        env=_env_without_credentials(tmp_path),
        capture_output=True,
        text=True,
        timeout=120,
    )
    assert done.returncode == 0, done.stderr[-800:]


def test_first_use_without_credentials_is_an_informative_error(tmp_path):
    code = (
        "import haggle.dacc as d\n"
        "try:\n"
        "    d.KaggleDatasetInfoReader()._source\n"
        "except OSError as e:\n"
        "    print('TOKEN-HINT' if 'kaggle API token' in str(e) else 'NO-HINT')\n"
    )
    done = subprocess.run(
        [sys.executable, "-c", code],
        env=_env_without_credentials(tmp_path),
        capture_output=True,
        text=True,
        timeout=120,
    )
    assert "TOKEN-HINT" in done.stdout, done.stdout + done.stderr[-800:]
