"""
ReAct Agent Loop
Think -> Act (tool) -> Observe -> Answer

Maksimal MAX_STEPS iterasi agar tidak loop tak terbatas.
"""

import logging
from core.tool_parser import parse_tool_call, has_tool_call
from core.tool_executor import execute_tool

logger = logging.getLogger(__name__)

MAX_STEPS = 5


def run_agent(ask_fn, user_id, user_text, persona, telegram_name):
    """
    ask_fn: fungsi LLM yang menerima (user_id, user_text, persona, telegram_name)
    Mengembalikan string jawaban akhir.
    """
    current_input = user_text
    steps = 0
    observations = []

    while steps < MAX_STEPS:
        steps += 1

        # Tambahkan observasi sebelumnya ke input jika ada
        if observations:
            obs_text = "\n".join(
                [f"Tool Result {i+1}:\n{o}" for i, o in enumerate(observations)]
            )
            current_input = (
                f"{user_text}\n\n"
                f"{obs_text}\n\n"
                f"Berdasarkan hasil di atas, jawab pertanyaan user secara natural dan ramah."
            )

        response = ask_fn(
            user_id=user_id,
            user_text=current_input,
            persona=persona,
            telegram_name=telegram_name,
        )

        if not has_tool_call(response):
            # Tidak ada tool call, ini jawaban akhir
            logger.info(f"Agent selesai dalam {steps} langkah.")
            return response

        # Ada tool call, eksekusi
        tool_call = parse_tool_call(response)
        if not tool_call:
            return response

        tool_name = tool_call["tool"]
        argument = tool_call["argument"]

        logger.info(f"Agent step {steps}: tool={tool_name}, arg={argument[:100]}")

        result = execute_tool(tool_name, argument, user_id=user_id)
        observations.append(f"[{tool_name}({argument[:80]})]\n{result}")

    # Fallback jika sudah MAX_STEPS
    logger.warning("Agent mencapai batas maksimum langkah.")
    if observations:
        last_obs = observations[-1]
        fallback_input = (
            f"Hasil tool terakhir:\n{last_obs}\n\n"
            f"Rangkum dan sampaikan ke user dengan ramah."
        )
        return ask_fn(
            user_id=user_id,
            user_text=fallback_input,
            persona=persona,
            telegram_name=telegram_name,
        )

    return "Maaf sayang, aku kesulitan menjawab ini. Coba tanya dengan cara lain ya 🥺"
