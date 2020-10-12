import cv2 as cv


class VideoCapture:
    def __init__(self, video_path):
        self.capture = cv.VideoCapture(video_path)
        self.info = self.__get_info()

    def __get_info(self):
        """Gets video information from capture object"""
        frames_count = int(self.capture.get(cv.CAP_PROP_FRAME_COUNT))
        fps = self.capture.get(cv.CAP_PROP_FPS)
        frame_width = int(self.capture.get(cv.CAP_PROP_FRAME_WIDTH))
        frame_height = int(self.capture.get(cv.CAP_PROP_FRAME_HEIGHT))

        return {'fps': fps,
                'width': frame_width,
                'height': frame_height,
                'frames_count': frames_count}
