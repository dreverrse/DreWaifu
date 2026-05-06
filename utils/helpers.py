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
    return f"job_{max(nums, default=0) + 1}"


def next_habit_id(habits_list):
    nums = []
    for h in habits_list:
        try:
            nums.append(int(h["id"].replace("habit_", "")))
        except:
            pass
    return f"habit_{max(nums, default=0) + 1}"


def next_alert_id(alerts_list):
    nums = []
    for a in alerts_list:
        try:
            nums.append(int(a["id"].replace("alert_", "")))
        except:
            pass
    return f"alert_{max(nums, default=0) + 1}"
