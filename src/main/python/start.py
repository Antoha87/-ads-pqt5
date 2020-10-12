"""
This file you can use as example of usage executor's module
"""

from ad_insertion_executor import ProcessingExecutor, InsertionExecutor

if __name__ == '__main__':
    # Example of input data
    video = 'test_video.mp4'
    logo = 'test_logo.png'
    cfg = {
        'contour_threshold': 1.5,
        'conf_threshold': 0.6,
        'banner_size': 0.2,
        'background': False,
        'allowed_ram_size': 1000,
        'use_segmentation': True,
        'device': 'gpu'
    }

    # To run processing executor (finds places to insert ads and creates data)
    processing_executor = ProcessingExecutor(video, logo, cfg)
    processing_executor.process_video()

    # To run insertion executor (generates video file with inserted ads)
    insertion_executor = InsertionExecutor(video, logo, cfg)
    insertion_executor.insert_ads()
