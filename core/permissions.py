from config import OWNER_ID


def is_owner(user_id):
    return user_id == OWNER_ID


def check_permission(update, level="owner"):
    user_id = update.effective_user.id
    if level == "owner":
        return user_id == OWNER_ID
    return True
