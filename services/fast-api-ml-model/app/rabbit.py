import json

from app.models import UserPermission


def update_permission(ch, method, properties, body):
    updated_user_json = json.loads(body)
    updated_user = UserPermission.find_by_username(username=updated_user_json["username"])
    updated_user.permission = updated_user_json["permission"]
    updated_user.save_to_db()
