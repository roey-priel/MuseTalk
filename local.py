import os
import time
import pdb
import re

import gradio as gr
import spaces
import numpy as np
import cProfile
import sys
import subprocess

from huggingface_hub import snapshot_download
import requests

import argparse
import os
from omegaconf import OmegaConf
import numpy as np
import cv2
import torch
import glob
import pickle
from tqdm import tqdm
import copy
from argparse import Namespace
import shutil
import gdown
import imageio
import ffmpeg
from moviepy.editor import *
from musetalk.utils.timer import timeit, close_file
from musetalk.utils.utils import load_all_model

from app import inference, download_model, print_directory_contents, ProjectDir, CheckpointsDir, check_video



download_model()  # for huggingface deployment.


# load model weights
audio_processor,vae,unet,pe  = load_all_model()
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
timesteps = torch.tensor([0], device=device)



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--audio_path", type=str, default="trimmed_audio.wav")
    parser.add_argument("--video_path", type=str, default="twenty_sec.mp4")
    parser.add_argument("--bbox_shift", type=int, default=0)
    parser.add_argument("--batch_size", type=int, default=16)
    args = parser.parse_args()
    inference(args.audio_path, args.video_path, args.bbox_shift, batch_size=args.batch_size)

if __name__ == "__main__":
    cProfile.run('main()', 'profile.prof')
    close_file()
