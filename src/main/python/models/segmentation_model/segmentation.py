import torch


class SegmentationModel:
    def __init__(self):
        if torch.cuda.is_available():
            print('Segmentation will processed on GPU')
        else:
            print('Segmentation will processed on CPU')
