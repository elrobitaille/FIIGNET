from fastai.vision.all import *
from sklearn.metrics import roc_auc_score, auc, roc_curve, precision_recall_curve
import os
import argparse
import matplotlib.pyplot as plt

def main(args):
    path_train = args.input_path_train
    path_valid = args.input_path_valid
    path_test = args.input_path_test
    model_path = args.model_path

    # Assert that directories exist
    assert os.path.isdir(path_train), f"Training path {path_train} does not exist."
    assert os.path.isdir(path_valid), f"Validation path {path_valid} does not exist."
    assert os.path.isdir(path_test), f"Test path {path_test} does not exist."
    assert os.path.isfile(model_path), f"Model path {model_path} does not exist."

    # Get all image files recursively
    train_files = get_image_files(path_train)
    valid_files = get_image_files(path_valid)
    test_files = get_image_files(path_test)

    print(f"Number of files in training directory: {len(train_files)}")
    print(f"Number of files in validation directory: {len(valid_files)}")
    print(f"Number of files in test directory: {len(test_files)}")

    # Load the model
    try:
        learn = load_learner(model_path)
    except Exception as e:
        print(f"Error while loading model: {e}")
        return

    # Create a DataLoader for each dataset
    train_dl = learn.dls.test_dl(train_files, with_labels=True)
    valid_dl = learn.dls.test_dl(valid_files, with_labels=True)
    test_dl = learn.dls.test_dl(test_files, with_labels=True)

    # Make predictions for each set
    train_preds, train_targs = learn.get_preds(dl=train_dl)
    valid_preds, valid_targs = learn.get_preds(dl=valid_dl)
    test_preds, test_targs = learn.get_preds(dl=test_dl)

    # Binary case, adjust for your case
    train_scores = train_preds[:, 1]
    valid_scores = valid_preds[:, 1]
    test_scores = test_preds[:, 1]

    # Compute ROC AUC for each set
    train_roc_auc = roc_auc_score(train_targs, train_scores)
    valid_roc_auc = roc_auc_score(valid_targs, valid_scores)
    test_roc_auc = roc_auc_score(test_targs, test_scores)

    # Compute Precision-Recall curve and AUPR for each set
    train_precision, train_recall, _ = precision_recall_curve(train_targs, train_scores)
    train_aupr = auc(train_recall, train_precision)
    valid_precision, valid_recall, _ = precision_recall_curve(valid_targs, valid_scores)
    valid_aupr = auc(valid_recall, valid_precision)
    test_precision, test_recall, _ = precision_recall_curve(test_targs, test_scores)
    test_aupr = auc(test_recall, test_precision)

    # Compute ROC curve for each set
    train_fpr, train_tpr, _ = roc_curve(train_targs, train_scores)
    valid_fpr, valid_tpr, _ = roc_curve(valid_targs, valid_scores)
    test_fpr, test_tpr, _ = roc_curve(test_targs, test_scores)

    # Plot Precision-Recall curve and ROC curve for each set
    for set_name, precision, recall, aupr, fpr, tpr in zip(
        ['train', 'valid', 'test'], 
        [train_precision, valid_precision, test_precision],
        [train_recall, valid_recall, test_recall],
        [train_aupr, valid_aupr, test_aupr],
        [train_fpr, valid_fpr, test_fpr],
        [train_tpr, valid_tpr, test_tpr]
    ):
        plt.figure()
        plt.plot(recall, precision, color='blue', lw=2, label='PR curve (AUC = %0.2f)' % aupr)
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('Recall')
        plt.ylabel('Precision')
        plt.title(f'Precision-Recall curve - {set_name.capitalize()}')
        plt.legend(loc="lower right")
        plt.savefig(f'pr_curve_{set_name}.png')

        plt.figure()
        plt.plot(fpr, tpr, color='green', lw=2, label='ROC curve (AUC = %0.2f)' % auc(fpr, tpr))
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title(f'ROC curve - {set_name.capitalize()}')
        plt.legend(loc="lower right")
        plt.savefig(f'roc_curve_{set_name}.png')

    print(f'Train - ROC AUC: {train_roc_auc}, AUPR: {train_aupr}')
    print(f'Validation - ROC AUC: {valid_roc_auc}, AUPR: {valid_aupr}')
    print(f'Test - ROC AUC: {test_roc_auc}, AUPR: {test_aupr}')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Test a CNN for image classification.')
    parser.add_argument('--input_path_train', type=str, required=True, help='Input path for train images')
    parser.add_argument('--input_path_valid', type=str, required=True, help='Input path for validation images')
    parser.add_argument('--input_path_test', type=str, required=True, help='Input path for test images')
    parser.add_argument('--model_path', type=str, required=True, help='Path for the model')

    args = parser.parse_args()

    main(args)
