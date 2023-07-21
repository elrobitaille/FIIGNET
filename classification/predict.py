import argparse
from fastai.vision.all import *
from fastai.vision.core import PILImage
import os

# python predict.py --learner '/path/to/learner.pkl'

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--learner', type=str, required=True, help='Path to the learner')
    args = parser.parse_args()
    return args

def predict_all_images():
    #healthy_path = '/home/ugrad/serius/edgarrobitaille/FIIGNET/classification/GSrealgantest/test/healthy'
    #sick_path = '/home/ugrad/serius/edgarrobitaille/FIIGNET/classification/GSrealgantest/test/ich'
    healthy_path = '/home/ugrad/serius/edgarrobitaille/test/healthy'
    sick_path = '/home/ugrad/serius/edgarrobitaille/test/ich'
    args = get_args()

    learn = load_learner(args.learner)
    total = 0
    num_correct = 0
    #iterate through all images in healthy_path folder
    for filename in os.listdir(healthy_path):
        total += 1
        img = PILImage.create(os.path.join(healthy_path, filename))
        pred_class, pred_idx, outputs = learn.predict(img)
        print(f'Image Count: {total}, Predicted Class: {pred_class}')
        if(pred_class == "healthy"):
            print("Correct")
            num_correct += 1
        else:
            print("Incorrect")
    for filename in os.listdir(sick_path):
        total += 1
        img = PILImage.create(os.path.join(sick_path, filename))
        pred_class, pred_idx, outputs = learn.predict(img)
        print(f'Image Count: {total}, Predicted Class: {pred_class}')
        if(pred_class == "ich"):
            print("Correct")
            num_correct += 1
        else:
            print("Incorrect")
    accuracy = float(num_correct) / total
    print("Total: ", total)
    print("Correct: ", num_correct)
    print(f"Accuracy: {accuracy * 100:.2f}%")  
    return accuracy

if __name__ == "__main__":
    predict_all_images()
