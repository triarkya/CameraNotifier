import VideoDetector
import Notification
import time
import json
import os


with open("settings.json") as all_settings:
    settings = json.load(all_settings)
    general_settings = settings["GeneralSettings"]


def run_detection():
    # filter all remaining asset files
    assets_files = os.listdir(general_settings["root_directory"] + general_settings["assets_folder"])
    assets_files = sorted([asset for asset in assets_files if asset[-3:] == "avi"])

    if len(assets_files) == 0:
        # no assets found: try again in 30 seconds
        time.sleep(30)
    else:
        # run detection/conversion/notification for each asset file
        for asset in assets_files:
            # run detection
            vd = VideoDetector.VideoDetector(
                general_settings["root_directory"] + general_settings["assets_folder"] + "/" + asset
            )
            final_file = vd.detect_and_convert()

            # send file and remove afterwards
            if vd.found:
                Notification.send_notification(filepath=final_file)
            else:
                os.remove(final_file)


if __name__ == '__main__':
    # create directory for assets to check
    if not os.path.exists(general_settings["root_directory"] + general_settings["assets_folder"]):
        os.mkdir(general_settings["root_directory"] + general_settings["assets_folder"])

    # create directory for detection/conversion files
    if not os.path.exists(general_settings["root_directory"] + general_settings["assets_folder"] + "/converted"):
        os.mkdir(general_settings["root_directory"] + general_settings["assets_folder"] + "/converted")

    while True:
        run_detection()
