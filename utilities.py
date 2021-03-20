from converter import Converter
import os
import json


'''
Settings
'''
with open("settings.json") as all_settings:
    settings = json.load(all_settings)
    general_settings = settings["GeneralSettings"]


'''
Constants
'''
ROOT_DIR = general_settings["root_directory"]
ASSET_DIR = general_settings["assets_folder"]
ASSET_PATH = ROOT_DIR + ASSET_DIR


"""
converts .avi file to .mp4
optional: removes .avi file after conversion
"""
def avi_to_mp4(filepath, remove=False):
    converter = Converter()

    # first convert to mp4 and remove ".avi" between
    convert = converter.convert(filepath, filepath[:-4] + '.mp4', {
        'format': 'mp4',
        'video': {
            'codec': 'h264',
            'width': 1280,
            'height': 720,
            'fps': 5
        }
    })
    try:
        for part in convert:
            print(part)

    except Exception as e:
        print(e)
        # add some additional verbose stuff/notification here
        # sometimes converter.ConverterError: Zero-length media occurs

    if remove:
        # then delete old file
        os.remove(filepath)


'''
create directory for assets to check if no asset folder initialized and existing
'''
def check_asset_folder():
    if not os.path.exists(ASSET_PATH):
        os.mkdir(ASSET_PATH)


'''
create directory for detection/conversion files if no folder initialized and existing
'''
def check_detection_folder():
    if not os.path.exists(ASSET_PATH + "/converted"):
        os.mkdir(ASSET_PATH + "/converted")