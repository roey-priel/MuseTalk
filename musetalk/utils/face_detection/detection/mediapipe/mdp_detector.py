import os
import cv2
from torch.utils.model_zoo import load_url
import torch
import mediapipe as mp
import numpy as np
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from musetalk.utils.face_detection.detection.core import FaceDetector as BaseFaceDetector


BaseOptions = mp.tasks.BaseOptions
FaceDetector = mp.tasks.vision.FaceDetector
FaceDetectorOptions = mp.tasks.vision.FaceDetectorOptions
VisionRunningMode = mp.tasks.vision.RunningMode

# Create a face detector instance with the video mode:
options = FaceDetectorOptions(
    base_options=BaseOptions(model_asset_path='/home/ubuntu/github/MuseTalk/models/Blaze Face Detection.tflite'),
    running_mode=VisionRunningMode.VIDEO
)

from musetalk.utils.timer import timeit

models_urls = {
    's3fd': 'https://www.adrianbulat.com/downloads/python-fan/s3fd-619a316812.pth',
}

from ..sfd.net_s3fd import s3fd
from ..sfd.bbox import *
from ..sfd.detect import *

class MDPDetector(BaseFaceDetector):
    def __init__(self, device):
        super(MDPDetector, self).__init__(device, True)
        self.detector = FaceDetector.create_from_options(options)
        self.timestamp_ms = 0
        path_to_detector=os.path.join(os.path.dirname(os.path.abspath(__file__)), 's3fd.pth')

        # Initialise the face detector
        if not os.path.isfile(path_to_detector):
            model_weights = load_url(models_urls['s3fd'])
        else:
            model_weights = torch.load(path_to_detector)

        self.face_detector = s3fd()
        self.face_detector.load_state_dict(model_weights)
        self.face_detector.to(device)
        self.face_detector.eval()

    @timeit
    def detect_from_image(self, tensor_or_path):
        image = self.tensor_or_path_to_ndarray(tensor_or_path)

        bboxlist = detect(self.face_detector, image, device=self.device)
        keep = nms(bboxlist, 0.3)
        bboxlist = bboxlist[keep, :]
        bboxlist = [x for x in bboxlist if x[-1] > 0.5]

        return bboxlist

    @timeit
    def detect_from_batch(self, images: list[np.ndarray]) -> list[np.ndarray]:
        bboxlists = []
        for image in images:
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=image)
            face_detector_result = self.detector.detect_for_video(mp_image, self.timestamp_ms)
            self.timestamp_ms += 40
            bbox = face_detector_result.detections[0].bounding_box
            res = np.array([bbox.origin_x, bbox.origin_y, bbox.origin_x+bbox.width, bbox.origin_y+bbox.height, 1])
            bboxlists.append([res])
        # bboxlists = batch_detect(self.face_detector, images, device='cuda:0')
        # keeps = [nms(bboxlists[:, i, :], 0.3) for i in range(bboxlists.shape[1])]
        # bboxlists = [bboxlists[keep, i, :] for i, keep in enumerate(keeps)]
        # bboxlists = [[x for x in bboxlist if x[-1] > 0.5] for bboxlist in bboxlists]

        return bboxlists
