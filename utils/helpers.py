from config import OWNER_ID


def is_owner(update):
    return update.effective_user.id == OWNER_ID


def format_channel_text(data, text):
    return f"💖 {text}"


def next_job_id(data):
    nums = []

    for item in data["scheduled_posts"]:
        try:
            nums.append(int(item["id"].replace("job_", "")))
        except:
            pass

    return f"job_{max(nums, default=0)+1}"
