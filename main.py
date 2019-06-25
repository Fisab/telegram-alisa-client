from telethon import TelegramClient, events, sync
import sys
import socks

from settings import Settings
from Methods import Methods

print("Connecting to proxy...")
proxy = (socks.SOCKS4, Settings.HOST, Settings.PORT)

print("Connecting to telegram client...")
client = TelegramClient('session_name', Settings.API_ID, Settings.API_HASH, proxy=proxy)
client.connect()

Methods = Methods(client)
job_messages = Methods.get_job_messages()
print("Job messages: ", job_messages)
