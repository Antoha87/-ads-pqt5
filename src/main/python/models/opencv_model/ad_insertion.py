
import math


class AdInsertion:
    """
    The model provides advertisement insertion with OpenCV package
    :param config: dict with configurations of model
    :param video_info: dict with params of input file
    """

    def __init__(self, config, video_info):
        self.video_info = video_info
        self.cfg = config

    def __find_time(self, frames):
        with open('output/report_{}.txt'.format(self.video_info['video_name']), 'w') as report:
            report.write('Total amount of insertions: {} \n'.format(len(frames)))
            for i, contour in enumerate(frames):
                report.write('Period {}: \n'.format(i + 1))
                begin = int(contour[0] / math.ceil(self.video_info['fps']))
                b_time = divmod(begin, 60)
                end = math.ceil(contour[-1] / math.ceil(self.video_info['fps']))
                e_time = divmod(end, 60)
                report.write('BEGIN: {} minutes {} seconds, END: {} minutes {} seconds \n'.format(b_time[0],
                                                                                                  b_time[1],
                                                                                                  e_time[0],
                                                                                                  e_time[1]))

    def process(self, frames):
        frames = [frames[i:i+2] for i in range(0, len(frames), 2)]
        self.__find_time(frames)
