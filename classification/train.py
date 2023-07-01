from fastai.vision.all import *
from fastai.vision.augment import FlipItem
import os
import argparse
import matplotlib.pyplot as plt

# python train.py --input_path '/path/to/image/directory' --output_path '/path/to/learner.pkl'

def main(args):
    path = args.input_path

    data = ImageDataLoaders.from_folder(path, train='train', valid='validate',
                                        item_tfms=Resize(460),
                                        batch_tfms=[*aug_transforms(size=224, min_scale=0.75), 
                                                    Normalize.from_stats(*imagenet_stats),
                                                    FlipItem(p=0.5)])

    learn = cnn_learner(data, resnet152, metrics=accuracy, wd=0.1)

    learn.model = nn.Sequential(*[learn.model, nn.Dropout(0.5)])

    learn.lr_find()

    learn.recorder.plot_lr_find()

    lr = 1e-5

    learn.fit_one_cycle(4, slice(lr))

    learn.unfreeze()
    
    learn.fit_one_cycle(100, slice(lr/100, lr))

    interp = ClassificationInterpretation.from_learner(learn)
    interp.plot_confusion_matrix()

    learn.export(args.output_path)

    test_path = os.path.join(path, 'test')
    test_dl = data.test_dl(get_image_files(test_path))

    result = learn.validate(dl=test_dl)
   # print("Result: ", result)

    # Plot the losses and save the figure
    learn.recorder.plot_loss()
    plt.savefig(os.path.join(path, 'loss_plot.png'))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Train a CNN for image classification.')
    parser.add_argument('--input_path', type=str, required=True, help='Input path for images')
    parser.add_argument('--output_path', type=str, required=True, help='Output path for the model')
    
    args = parser.parse_args()

    main(args)
