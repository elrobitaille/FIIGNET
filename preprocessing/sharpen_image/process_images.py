import cv2
import os
import argparse
import numpy as np
from scipy.signal import savgol_filter

def apply_gaussian_filter(img):
    return cv2.GaussianBlur(img, (5, 5), 0)

def sharpen_image(img):
    lap = cv2.Laplacian(img, cv2.CV_64F)
    lap = cv2.normalize(lap, None, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)
    lap = cv2.convertScaleAbs(lap)
    return cv2.subtract(img, lap)

def smooth_image(img):
    # The Savitzky-Golay filter can only process 1D arrays, but images are 2D (grayscale) or 3D (color).
    # Process each color channel separately.
    return np.stack([savgol_filter(channel, window_length=5, polyorder=2) for channel in cv2.split(img.astype(float))], axis=-1)

def process_image(image_path, output_dir, filters):
    # Load the image
    img = cv2.imread(image_path)

    # Check if the image has loaded correctly
    if img is None:
        print(f"Failed to load image at path: {image_path}")
        return

    # Apply each filter in sequence
    for name, function in filters.items():
        if function is not None:
            img = function(img)

    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Prepare the output path
    filename = os.path.basename(image_path)
    output_path = os.path.join(output_dir, filename)

    # Save the output image
    cv2.imwrite(output_path, img)



def process_directory(input_dir, output_dir, filters):
    # Iterate over all files in the input directory
    for filename in os.listdir(input_dir):
        if filename.endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            file_path = os.path.join(input_dir, filename)
            process_image(file_path, output_dir, filters)

if __name__ == "__main__":
    # Define and parse command-line arguments
    parser = argparse.ArgumentParser(description='Process images with various filters.')
    parser.add_argument('input_dir', help='Directory of input images.')
    parser.add_argument('output_dir', help='Directory to save processed images.')
    parser.add_argument('--gaussian', action='store_true', help='Apply Gaussian filter.')
    parser.add_argument('--sharpen', action='store_true', help='Apply Laplacian sharpening.')
    parser.add_argument('--smooth', action='store_true', help='Apply Savitzky-Golay smoothing.')
    args = parser.parse_args()

    # Define filters
    filters = {
        'gaussian': apply_gaussian_filter if args.gaussian else None,
        'sharpen': sharpen_image if args.sharpen else None,
        'smooth': smooth_image if args.smooth else None,
    }

    # Process images in the input directory
    process_directory(args.input_dir, args.output_dir, filters)

