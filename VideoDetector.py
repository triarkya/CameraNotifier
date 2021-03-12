from imageai.Detection import VideoObjectDetection
from converter import Converter
import os
import json


# Settings
with open("settings.json", "r") as settings:
    all_settings = json.load(settings)
    detection_settings = all_settings["DetectionSettings"]


class VideoDetector:
    def __init__(self, filepath):
        self.filepath = filepath
        self.video_detector = VideoObjectDetection()

        self.video_detector.setModelTypeAsYOLOv3()
        self.video_detector.setModelPath("yolo.h5")
        self.video_detector.loadModel(detection_speed="fastest")
        self.converted_detection_path = ""
        self.to_find = ["person"]
        self.found = False


    """
    converts .avi file to .mp4
    optional: removes .avi file after conversion
    """
    def run_convert_avi(self, filepath, remove=False):
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


    """
    run object detection on object filepath
    currently: car/person
    """
    def run_detection(self):
        splitted_filepath = self.filepath.split("/")
        output_filepath = "/".join(splitted_filepath[:-1]) + "/converted/" + splitted_filepath[-1] + "detection"

        # filepath for videofile with enabled object detection
        new_path = self.video_detector.detectObjectsFromVideo(
            input_file_path=self.filepath,
            minimum_percentage_probability=40,
            log_progress=True,
            output_file_path=output_filepath,
            per_frame_function=self.forFrame
        )

        print(new_path)
        if not self.found:
            os.remove(output_filepath)



    def detect_and_convert(self):
        # first detect from .avi file
        self.run_detection()

        # delete old video file
        if detection_settings["DeleteInitialFile"]:
            os.remove(self.filepath)

        if self.found:
            # convert detection file and remove non-detection file
            splitted_filepath = self.filepath.split("/")
            self.run_convert_avi("/".join(splitted_filepath[:-1]) + "/converted/" + splitted_filepath[-1] + "detection.avi", remove=True)
            self.converted_detection_path = "/".join(splitted_filepath[:-1]) + "/converted/" + splitted_filepath[-1] + "detection.mp4"

        return self.converted_detection_path


    # method for each frame
    def forFrame(self, frame_number, output_array, output_count):
        if any(key in self.to_find for key in output_count.keys()):
            print("FOUND")
            self.found = True


if __name__ == '__main__':
    vd = VideoDetector("video.avi")
    print(vd.detect_and_convert())
