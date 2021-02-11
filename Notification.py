import telegram
import os
import traceback
import json


def send_notification(filepath):
    with open("settings.json", "r") as settings:
        all_settings = json.load(settings)
        tgb_token = all_settings["NotificationSettings"]["Telegram_Token"]
        tgb_chat = all_settings["NotificationSettings"]["Telegram_Chat_ID"]

    tgb = telegram.Bot(token=tgb_token)
    try:
        tgb.send_video(
            tgb_chat,
            open(filepath, "rb"),
        )

    # any more elegant possibility to catch all network related errors?
    except Exception as e:
        print("Connection Error\n", e)
        print(traceback.format_exc())

    # remove bot and converted file
    del tgb
    os.remove(filepath)
