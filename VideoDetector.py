from imageai.Detection import VideoObjectDetection
import os
import time
import json
import utilities


# Settings
with open("settings.json", "r") as settings:
    all_settings = json.load(settings)
    detection_settings = all_settings["DetectionSettings"]


class VideoDetector:
    def __init__(self, filepath):
        self.filepath = filepath
        self.creation_date = time.ctime(os.path.getctime(self.filepath))
        self.video_detector = VideoObjectDetection()

        self.video_detector.setModelTypeAsYOLOv3()
        self.video_detector.setModelPath("yolo.h5")
        self.video_detector.loadModel(detection_speed="fastest")
        self.converted_detection_path = ""
        self.to_find = ["person"]
        self.found = False
        print(self.creation_date)


    """
    run object detection on object filepath
    currently: car/person
    """
    def run_video_detection(self):
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

        # remove file if nothing relevant found
        if not self.found:
            os.remove(output_filepath + ".avi")



    def detect_and_convert(self):
        # first detect from .avi file
        self.run_video_detection()

        # delete old video file
        if detection_settings["DeleteInitialFile"]:
            os.remove(self.filepath)

        if self.found:
            # convert detection file and remove non-detection file
            splitted_filepath = self.filepath.split("/")
            utilities.avi_to_mp4("/".join(splitted_filepath[:-1]) + "/converted/" + splitted_filepath[-1] + "detection.avi", remove=True)
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
