import requests

from app.models import UserPermission


def get_username_by_token(token):
    # requests.post(
    #     url="user-service:8080/username-by-token",
    #     data={"token": token}
    # )
    return "strahinjademic"


def check_permission(username, model_id):
    user = UserPermission.find_by_username(username=username)
    if not user:
        return False
    if user.permission != model_id:
        return False
    return True
