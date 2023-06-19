import cv2
import os
import argparse
import numpy as np
from scipy.signal import savgol_filter

def apply_gaussian_filter(img):
    return cv2.GaussianBlur(img, (5, 5), 0)

def sharpen_image(img, sigma=1.0, strength=1.5):
    blurred = cv2.GaussianBlur(img, (0, 0), sigma)
    sharpened = cv2.addWeighted(img, 1.0 + strength, blurred, -strength, 0)
    return sharpened

def smooth_image(img):
    return np.stack([savgol_filter(channel, window_length=5, polyorder=2) for channel in cv2.split(img.astype(float))], axis=-1)

def denoise_image(img):
    if img.dtype != np.uint8:
        img = cv2.normalize(img, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)
    return cv2.bilateralFilter(img, d=15, sigmaColor=75, sigmaSpace=75)

def upscale_image(img, scale_factor=2):
    return cv2.resize(img, None, fx=scale_factor, fy=scale_factor, interpolation=cv2.INTER_CUBIC)

def apply_clahe(img):
    img_yuv = cv2.cvtColor(img, cv2.COLOR_BGR2YUV)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    img_yuv[:,:,0] = clahe.apply(img_yuv[:,:,0])
    img_output = cv2.cvtColor(img_yuv, cv2.COLOR_YUV2BGR)
    return img_output

def edge_enhancement(img):
    kernel = np.array([[0, -1, 0],
                       [-1, 5,-1],
                       [0, -1, 0]])
    img_output = cv2.filter2D(img, -1, kernel)
    return img_output

def process_image(image_path, output_dir, filters):
    try:
        img = cv2.imread(image_path)
        if img is None:
            print(f"Failed to load image at path: {image_path}")
            return
        for name, function in filters.items():
            if function is not None:
                img = function(img)
        os.makedirs(output_dir, exist_ok=True)
        filename = os.path.basename(image_path)
        output_path = os.path.join(output_dir, filename)
        print(f"Saving image to path: {output_path}")
        cv2.imwrite(output_path, img)
    except Exception as e:
        print(f"An error occurred while processing image at path: {image_path}. Error: {str(e)}")

def process_directory(input_dir, output_dir, filters):
    for filename in os.listdir(input_dir):
        if filename.endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            file_path = os.path.join(input_dir, filename)
            process_image(file_path, output_dir, filters)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process images with various filters.')
    parser.add_argument('input_dir', help='Directory of input images.')
    parser.add_argument('output_dir', help='Directory to save processed images.')
    parser.add_argument('--gaussian', action='store_true', help='Apply Gaussian filter.')
    parser.add_argument('--sharpen', action='store_true', help='Apply Unsharp Mask sharpening.')
    parser.add_argument('--smooth', action='store_true', help='Apply Savitzky-Golay smoothing.')
    parser.add_argument('--denoise', action='store_true', help='Apply bilateral filter for denoising.')
    parser.add_argument('--upscale', action='store_true', help='Upscale image using bicubic interpolation.')
    parser.add_argument('--clahe', action='store_true', help='Apply CLAHE.')
    parser.add_argument('--edge_enhance', action='store_true', help='Apply edge enhancement.')
    args = parser.parse_args()
    filters = {
        'gaussian': apply_gaussian_filter if args.gaussian else None,
        'sharpen': sharpen_image if args.sharpen else None,
        'smooth': smooth_image if args.smooth else None,
        'denoise': denoise_image if args.denoise else None,
        'upscale': upscale_image if args.upscale else None,
        'clahe': apply_clahe if args.clahe else None,
        'edge_enhance': edge_enhancement if args.edge_enhance else None,
    }
    process_directory(args.input_dir, args.output_dir, filters)
