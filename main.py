import VideoDetector
import Notification
import utilities
import time
import os


def run_detection():
    # filter all remaining asset files (all video files to check)
    assets_files = sorted([asset for asset in os.listdir(utilities.ASSET_PATH) if asset[-3:] == "avi"])

    # if no assets found: try again in 30 seconds
    if len(assets_files) == 0:
        time.sleep(30)
    else:
        # run detection/conversion/notification for each asset file
        for asset in assets_files:

            # run detection
            vd = VideoDetector.VideoDetector(utilities.ASSET_PATH + "/" + asset)

            # converted file incl. detection rectangle
            final_file = vd.detect_and_convert()

            # send file and remove afterwards
            if vd.found:
                try:
                    Notification.send_notification(
                        filepath=final_file,
                        notification_text=vd.creation_date
                    )
                except Exception as e:
                    print(e)


if __name__ == '__main__':
    utilities.check_asset_folder()
    utilities.check_detection_folder()

    while True:
        run_detection()
