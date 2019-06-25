import telethon.tl.types as telethon_types
from tools import Tools
import datetime


class Methods:
    def __init__(self, client):
        print('Connecting to telegram...')

        self.client = client
        print('Getting dialogs...')
        self.dialogs = self.client.get_dialogs(limit=50)
        print('Done. Sorting chats & dialogs...')
        self.important_chats = self.__sort_important_chats()
        self.important_dialogs = self.__sort_important_dialogs()

        print("Done!", {
            "data": {
                "important_chats": len(self.important_chats),
                "important_dialogs": len(self.important_dialogs)
            }
        })

    def __sort_important_dialogs(self):
        result = [dialog for dialog in self.dialogs if isinstance(dialog.entity, telethon_types.User) and Tools.get_important_user_by_id(dialog.entity.id)]
        return result

    def __sort_important_chats(self):
        result = []
        for dialog in self.dialogs:
            if isinstance(dialog.entity, telethon_types.Chat):
                participants = self.client.get_participants(dialog)
                is_important = False

                for participant in participants:
                    if Tools.get_important_user_by_id(participant.id):
                        is_important = True
                        break

                if is_important:
                    result.append(dialog)
        return result

    def get_job_messages(self):
        print("Getting important messages...")
        important_messages = self.__get_important_messages()
        print("Done! Getting mentioned messages...")
        mentioned_messages = self.__get_mentioned_messages()
        print("Done!")
        mentioned_count = len(mentioned_messages)
        important_count = len(important_messages)

        return {
            "important_messages":
                {"count": important_count, "data": important_messages},
            "mentioned_messages":
                {"count": mentioned_count, "data": mentioned_messages}
        }

    def __get_important_messages(self):
        important_dialogs = self.__get_important_dialogs()
        unread_messages = self.__get_unread_messages(important_dialogs)
        return unread_messages

    def __get_important_dialogs(self):
        result = []
        for dialog in self.important_dialogs:
            if dialog.unread_count:
                result.append(dialog)

        return result

    def __get_unread_messages(self, dialogs):
        result = []
        for dialog in dialogs:
            messages = self.client.get_messages(dialog.entity, dialog.unread_count)
            for message in messages:
                user_info = Tools.user_info_to_dict(message.from_id, self.client)
                temp = {"dialog": {
                    "name": dialog.name,
                }, "message": {
                    "message": message.message,
                    "user": user_info
                }}

                result.append(temp)

        return result

    def __get_mentioned_dialogs(self):
        result = []
        for index, dialog in enumerate(self.important_chats):
            if dialog.unread_count:
                result.append(dialog)

        return result

    def __get_mentioned_messages(self):
        dialogs = self.__get_mentioned_dialogs()
        result = []
        for index, dialog in enumerate(dialogs):
            messages = self.client.get_messages(dialog.entity, dialog.unread_count)
            for message in messages:
                if datetime.datetime.today().day - 2 > message.date.day:
                    break
                if message.mentioned:
                    user_info = Tools.user_info_to_dict(message.from_id, self.client)

                    temp = {"dialog": {
                        "name": dialog.name,
                    }, "message": {
                        "message": message.message,
                        "user": user_info
                    }}

                    result.append(temp)
                    break

        return result
