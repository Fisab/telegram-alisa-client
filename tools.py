from settings import Settings


class Tools:

    @staticmethod
    def get_important_user_by_id(user_id):
        for important_user in Settings.IMPORTANT_USER_IDS:
            if important_user.get('user_id') == user_id:
                return important_user
        return False

    @staticmethod
    def user_info_to_dict(user_id, client):
        user_info = Tools.get_important_user_by_id(user_id)
        if not user_info:
            user_info = client.get_entity(user_id)
            user_info = {
                "username": user_info.username,
                "user_id": user_info.id,
                "name": "{0} {1}".format(user_info.first_name, user_info.last_name)
            }

        return user_info

