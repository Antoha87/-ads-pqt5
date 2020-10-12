from models.opencv_model.ad_insertion import AdInsertion
from models.segmentation_model.segmentation import SegmentationModel
from models.utils.video_capture import VideoCapture
import cv2 as cv
import numpy as np
from subprocess import Popen, PIPE
from pathlib import Path
import os
from time import sleep
import shutil


class ProcessingExecutor:
    """
    Performs video processing to find ad insertions contours

    :param video: video file name placed in output folder
    :param logo: logo file name placed in output folder
    :param config: dict with model configurations
    """

    def __init__(self, video, logo, config):
        self.video = video
        self.logo = logo
        self.config = config
        self.input_info = {}

    def __find_contours(self, capture, model):
        print('Searching contours...')

        SegmentationModel()

        frames = []
        for i in range(self.input_info['frames_count']):
            if not i % 500:
                print('%2d of the movie is loaded.' % (i / self.input_info['frames_count'] * 100))
            if np.random.rand() < 0.002:
                capture.set(cv.CAP_PROP_POS_FRAMES, i)
                _, frame = capture.read()
                frames.append(i)
                if len(frames) % 2 != 0:
                    cv.imwrite(f'output/instances/{len(frames[::2])}.png', frame)
            sleep(0.001)
        model.process(frames)

        print('Searching is completed.')

        message = 'Insert templates are ready. Please check the templates for further actions.'
        return message


    def process_video(self):
        """
        Execute AdInsertion model for logo insertion

        :return: message that describes function output
        """
        input_video_name = self.video.split('.')[0]
        output_path = str(Path.cwd()) + '/output'
        instances_path = output_path + '/instances'
        Path(output_path).mkdir(parents=True, exist_ok=True)
        Path(instances_path).mkdir(parents=True, exist_ok=True)

        video = VideoCapture(output_path + '/' + self.video)
        logo = cv.imread(output_path + '/' + self.logo, cv.IMREAD_UNCHANGED)

        if int(video.capture.get(cv.CAP_PROP_FPS)) == 0 or logo is None:
            message = 'ERROR WHILE ENTERING LOGO OR VIDEO PATH.'
            print(message)
        else:
            # Get input video info
            self.input_info = video.info
            self.input_info['video_name'] = input_video_name
            model = AdInsertion(self.config, self.input_info)

            # Finding contours
            message = self.__find_contours(video.capture, model)

        video.capture.release()
        return message


class InsertionExecutor:
    """
    Performs ads insertion and creating of video file

    :param video: video file name placed in output folder
    :param logo: logo file name placed in output folder
    :param config: dict with model configurations
    """

    def __init__(self, video, logo, config):
        self.video = video
        self.logo = logo
        self.config = config
        self.input_info = {}

    def insert_ads(self):
        """
       Model insertion method
       :return: message that describes insertion result
       """
        video_name, extension = self.video.rsplit('.', 1)
        output_path = str(Path.cwd()) + '/output'
        instances_path = output_path + '/instances'
        report_path = output_path + f'/report_{video_name}.txt'

        try:
            report = open(report_path)
            if len(report.readlines()) > 1:

                print('Insertion is running...')
                video = VideoCapture(output_path + '/' + self.video)

                self.input_info = video.info
                self.input_info['video_name'] = video_name
                self.input_info['extension'] = extension

                out = Popen('ffmpeg -y -hide_banner '
                            f'-f rawvideo -pix_fmt bgr24 -s {self.input_info["width"]}x{self.input_info["height"]} '
                            f'-r {self.input_info["fps"]} -i - '
                            f'-c:v h264 -pix_fmt yuv420p '
                            f'-an output/{video_name}-processed.mp4'.split(),
                            stdin=PIPE)

                for i in range(self.input_info['frames_count']):
                    ret, frame = video.capture.read()
                    if ret:
                        if not i % 500:
                            print('%2d of the movie is processed.' % (i / self.input_info['frames_count'] * 100))
                        out.stdin.write(frame.tobytes())
                    else:
                        break
                video.capture.release()
                out.stdin.close()
                out.wait()

                print('Insertion completed.')
                message = 'Video file has been processed.'
                print(message)

            else:
                message = 'There is nothing to insert. Please try different video file.'
                print(message)

        except FileNotFoundError:
            message = 'Please run Video Processing before Advertisement Insertion.'
            print(message)
        finally:
            report.close()
            os.remove(report_path)

        shutil.rmtree(instances_path)

        return message
