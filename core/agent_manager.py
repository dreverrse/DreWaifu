# Agent manager: routing ke agent yang tepat berdasarkan task

from core.router import select_model


def get_agent_for_task(task):
    model = select_model(task)
    return {"task": task, "model": model}
