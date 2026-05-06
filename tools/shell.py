import subprocess


def run_shell(command):
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=10,
        )
        return (result.stdout or result.stderr)[:3000]
    except Exception as e:
        return f"SHELL ERROR: {e}"
