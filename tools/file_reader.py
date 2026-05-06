def read_file(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        return content[:5000]
    except Exception as e:
        return f"FILE ERROR: {e}"
