import VideoDetector
import os


if __name__ == '__main__':
    # create directory for assets to check
    if not os.path.exists("assets"):
        os.mkdir("assets")

    # create directory for detection/conversion files
    if not os.path.exists("assets/converted"):
        os.mkdir("assets/converted")

    # filter all remaining asset files
    assets_files = os.listdir("assets")
    assets_files = [asset for asset in assets_files if asset[-3:] == "avi"]

    # run detection/conversion/notification for each asset file
    for asset in assets_files:
        vd = VideoDetector.VideoDetector("assets/" + asset)
        final_file = vd.detect_and_convert()
        print("finished", final_file)

        # send file and remove afterwards
