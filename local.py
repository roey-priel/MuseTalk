import cProfile

import argparse



# from moviepy.editor import *
from musetalk.utils.timer import close_file

from app import inference 
#, download_model, audio_processor, vae, unet, pe, device, timesteps


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
