import cv2
import glob
import os
import argparse
import re

# python video.py path_to_your_images
# python video.py path_to_your_images --video_name my_video.mp4 --fps 24

def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    return [atoi(c) for c in re.split(r'(\d+)', text)]

def create_video(image_folder, video_name, fps):
    """
    Create a video out of images saved in a folder

    Args:
    image_folder : str
        The folder containing images
    video_name : str
        The name of the video file to create
    fps : int
        Frames per second of the output video
    """

    images = glob.glob(os.path.join(image_folder, "*.jpg"))
    images.sort(key=natural_keys)
    frame = cv2.imread(images[0])
    height, width, _ = frame.shape

    video = cv2.VideoWriter(video_name, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width,height))

    for image in images:
        video.write(cv2.imread(image))

    video.release()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Create a video from a series of images.')
    parser.add_argument('image_folder', type=str, help='The directory containing images')
    parser.add_argument('--video_name', type=str, default='output.mp4', help='The name of the output video file')
    parser.add_argument('--fps', type=int, default=30, help='Frames per second of the output video')

    args = parser.parse_args()

    create_video(args.image_folder, args.video_name, args.fps)
