from imageai.Detection import VideoObjectDetection
from converter import Converter
import os
import json


with open("settings.json", "r") as settings:
    all_settings = json.load(settings)
    detection_settings = all_settings["DetectionSettings"]


class VideoDetector:
    def __init__(self, filepath):
        self.filepath = filepath
        self.video_detector = VideoObjectDetection()
        self.video_detector.setModelTypeAsYOLOv3()
        self.video_detector.setModelPath("yolo.h5")
        self.video_detector.loadModel()
        self.converted_detection_path = ""
        self.to_find = ["car", "person"]
        self.found = False


    """
    converts .avi file to .mp4
    optional: removes .avi file
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
        for part in convert:
            print(part)

        if remove:
            # then delete old file
            os.remove(filepath)


    """
    run object detection on object filepath
    currently: car/person
    """
    def run_detection(self):
        splitted_filepath = self.filepath.split("/")

        # filepath for videofile with enabled object detection
        new_path = self.video_detector.detectObjectsFromVideo(
            input_file_path=self.filepath,
            minimum_percentage_probability=40,
            log_progress=True,
            output_file_path="/".join(splitted_filepath[:-1]) + "/converted/" + splitted_filepath[-1] + "detection",
            per_frame_function=self.forFrame
        )

        print(new_path)


    def detect_and_convert(self):
        # first detect from .avi file
        self.run_detection()

        # delete old video file
        if detection_settings["DeleteInitialFile"]:
            os.remove(self.filepath)

        # convert detection file and remove non-detection file
        splitted_filepath = self.filepath.split("/")
        self.run_convert_avi("/".join(splitted_filepath[:-1]) + "/converted/" + splitted_filepath[-1] + "detection.avi", remove=True)
        self.converted_detection_path = "/".join(splitted_filepath[:-1]) + "/converted/" + splitted_filepath[-1] + "detection.mp4"
        return self.converted_detection_path


    def forFrame(self, frame_number, output_array, output_count):
        print("FOR FRAME ", frame_number)
        if any(key in self.to_find for key in output_count.keys()):
            print("FOUND")
            self.found = True
        print("------------END OF A FRAME --------------")


if __name__ == '__main__':
    vd = VideoDetector("video.avi")
    print(vd.detect_and_convert())
