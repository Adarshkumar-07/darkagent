from __future__ import annotations

import subprocess


def run_python(code: str, timeout_seconds: int = 8) -> str:
    proc = subprocess.run(
        ["python", "-c", code],
        capture_output=True,
        text=True,
        timeout=timeout_seconds,
    )
    stdout = proc.stdout.strip()
    stderr = proc.stderr.strip()
    return f"exit={proc.returncode}\nstdout:\n{stdout}\nstderr:\n{stderr}"