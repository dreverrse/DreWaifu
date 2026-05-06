def select_model(task="chat"):
    models = {
        "chat": "openai/gpt-4o-mini",
        "code": "deepseek/deepseek-chat",
        "vision": "openai/gpt-4.1",
        "creative": "google/gemini-2.5-pro",
    }
    return models.get(task, models["chat"])
