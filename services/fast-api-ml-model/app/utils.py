from app.models import UserPermission


def check_permission(username, model_id):
    user = UserPermission.find_by_username(username=username)
    if not user:
        return False
    if user.permission != model_id:
        return False
    return True
