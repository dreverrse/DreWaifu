import subprocess
import tempfile
import os


def run_python(code):
    try:
        with tempfile.NamedTemporaryFile(
            suffix=".py", delete=False, mode="w", encoding="utf-8"
        ) as f:
            f.write(code)
            tmp = f.name

        result = subprocess.run(
            ["python3", tmp],
            capture_output=True,
            text=True,
            timeout=10,
        )
        os.unlink(tmp)

        output = result.stdout or result.stderr
        return output[:3000] if output else "Tidak ada output."
    except subprocess.TimeoutExpired:
        return "TIMEOUT: Kode terlalu lama."
    except Exception as e:
        return f"CODE ERROR: {e}"
