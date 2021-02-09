from imageai.Detection import VideoObjectDetection
from converter import Converter
import os


class VideoDetector:
    def __init__(self, filepath):
        self.filepath = filepath
        self.video_detector = VideoObjectDetection()
        self.video_detector.setModelTypeAsYOLOv3()
        self.video_detector.setModelPath("yolo.h5")
        self.video_detector.loadModel()
        self.converted_detection_path = ""


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
        custom_objects = self.video_detector.CustomObjects(
            car=True,
            person=True
        )

        splitted_filepath = self.filepath.split("/")

        # filepath for videofile with enabled object detection
        new_path = self.video_detector.detectCustomObjectsFromVideo(
            input_file_path=self.filepath,
            custom_objects=custom_objects,
            minimum_percentage_probability=40,
            log_progress=True,
            output_file_path=splitted_filepath[0] + "/converted/" + splitted_filepath[1] + "detection"
        )

        print(new_path)


    def detect_and_convert(self):
        # first detect from .avi file
        self.run_detection()

        # delete old video file
        # os.remove(self.filepath)

        # convert detection file and remove non-detection file
        splitted_filepath = self.filepath.split("/")
        self.run_convert_avi(splitted_filepath[0] + "/converted/" + splitted_filepath[1] + "detection.avi", remove=True)
        self.converted_detection_path = splitted_filepath[0] + "/converted/" + splitted_filepath[1] + "detection.mp4"
        return self.converted_detection_path


if __name__ == '__main__':
    vd = VideoDetector("video.avi")
    print(vd.detect_and_convert())
