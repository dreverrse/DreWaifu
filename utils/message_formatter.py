import re

CODE_BLOCK_PATTERN = r"```[\s\S]*?```"


def split_message(text, limit=4000):

    messages = []

    code_blocks = re.findall(
        CODE_BLOCK_PATTERN,
        text
    )

    # Kalau ada code block
    if code_blocks:

        for block in code_blocks:

            messages.append(block)

            text = text.replace(
                block,
                ""
            )

        # sisa text biasa
        if text.strip():

            chunks = [
                text[i:i + limit]
                for i in range(
                    0,
                    len(text),
                    limit
                )
            ]

            messages.extend(chunks)

        return messages

    # kalau bukan code
    return [
        text[i:i + limit]
        for i in range(
            0,
            len(text),
            limit
        )
    ]