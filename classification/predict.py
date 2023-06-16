import argparse
from fastai.vision.all import *
from fastai.vision.core import PILImage
import os

# python predict.py --img '/path/to/image.jpg' --learner '/path/to/learner.pkl'

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--img', type=str, required=True, help='Path to the image')
    parser.add_argument('--learner', type=str, required=True, help='Path to the learner')
    args = parser.parse_args()
    return args

def main():
    args = get_args()

    learn = load_learner(args.learner)

    # Load the image
    img = PILImage.create(args.img)

    pred_class, pred_idx, outputs = learn.predict(img)

    # Print the predicted class
    print(pred_class)

if __name__ == "__main__":
    main()
