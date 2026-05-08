import subprocess
import tempfile
import os


def run_python(code):
    """Jalankan kode Python dan kembalikan outputnya."""
    # Blokir import berbahaya
    blocked = ["os.system", "subprocess", "shutil.rmtree", "__import__", "eval(", "exec("]
    for b in blocked:
        if b in code:
            return f"Kode diblokir karena mengandung '{b}' yang tidak diizinkan."

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
        if not output:
            return "Kode berjalan tanpa output."
        return output[:2000]

    except subprocess.TimeoutExpired:
        return "TIMEOUT: Kode terlalu lama dieksekusi (maks 10 detik)."
    except Exception as e:
        return f"CODE RUNNER ERROR: {e}"
