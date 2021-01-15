from imageai.Detection import VideoObjectDetection
from converter import Converter
import os


class VideoDetector:
    def __init__(self, identifier):
        self.identifier = identifier
        self.video_detector = VideoObjectDetection()
        self.video_detector.setModelTypeAsYOLOv3()
        self.video_detector.setModelPath("yolo.h5")
        self.video_detector.loadModel()


    def run_convert_avi(self, filepath):
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

        # then delete old file
        os.remove(filepath)


    def run_detection(self, filename):
        custom_objects = self.video_detector.CustomObjects(
            car=True,
            person=True
        )

        new_path = self.video_detector.detectCustomObjectsFromVideo(
            input_file_path=filename,
            custom_objects=custom_objects,
            minimum_percentage_probability=40,
            log_progress=True,
            output_file_path=filename + "detection"
        )

        print(new_path)


    def detect_and_convert(self, filename):
        # first detect from .avi file
        self.run_detection(filename)

        # delete old video file
        os.remove(filename)

        # convert detection file and remove non-detection file
        self.run_convert_avi(filename + "detection.avi")


if __name__ == '__main__':
    vd = VideoDetector("Outdoor")
    vd.detect_and_convert("Videos/example_person_night.avi")
