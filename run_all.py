# File to run entire pipeline for the user 
# Be sure to fix the directories to where you would like them to go.

import subprocess
import argparse

def main(use_gpu, model, disease):
    raw_data_path = "image_data/unprocessed/raw" # Change this to the path of the raw image data
    raw_data_enhanced_path = "image_data/processed/raw_image_enhanced" # Change this to the path of the enhanced images
    resized_data_path = "image_data/unprocessed/resized" # Change this to the path of the resized images
    yolo_weights = "preprocessing/yolo_tracking/YOLO/runs/detect/yolov8n_results2/weights/best.pt" # Change this to the path of the YOLO weights
    facebook_checkpts = "segment-anything/sam_vit_l_0b3195.pth" # Change this to the path of the Facebook checkpoints
    facebook_mask_output = "preprocessing/mask_image" # Change this to the path of the output for Facebook's model
    cropped_data_path = "image_data/unprocessed/segmented" # Change this to the path of the segmented images
    esrgan_output_path = "image_data/processed/ESRGAN_output" # Change this to the path of the ESRGAN output images
    square_resized_path = "image_data/processed/square_resize" # Change this to the path of the square resized images for the GAN in Part 2
    colored_mask_path = "preprocessing/mask_image/colored_masks" # Change this to the path of the colored masks for the GAN in Part 2

    height = 512 # Change for output size of Part 1 
    width = 512 # Change for output size of Part 1 

    commands = [ # Change if you would like to change the ran commands based on Makefile
        f"make enhance input_path={raw_data_path} output_path={raw_data_enhanced_path}",
        f"make resize input_path={raw_data_enhanced_path} output_path={resized_data_path}",
        f"make segment input_path={resized_data_path} weights={yolo_weights} height={height} width={width} output_path={cropped_data_path}",
        f"make mask input_path={cropped_data_path} checkpoint_path={facebook_checkpts} output_path={facebook_mask_output}",
        f"make resize input_path={colored_mask_path} output_path={square_resized_path} height={height} width={width}"
    ]

    # Run each command in sequence
    for command in commands:
        process = subprocess.Popen(command, shell=True)
        process.communicate()  # wait for the process to terminate

        if process.returncode != 0:
            print(f"Command '{command}' failed with return code: {process.returncode}")
            break

    if use_gpu:
        pass
    else:
        print("A high-performance GPU is needed to train the GAN, such as a NVIDIA Tesla P100 GPU or better. Please refer to the instructions in the README.md file for more information. ")

    if model == 'gan' and use_gpu:
        print("Running GAN code")
        if disease == 'ich':
            pass
        elif disease == 'red_spot':
            pass
       
    elif model == 'stable_diffusion' and use_gpu:
        print("Running Stable Diffusion code")
        if disease == 'ich':
            pass
        elif disease == 'red_spot':
            pass
        
    elif model == 'cvae' and use_gpu:
        print("Running CVAE code")
        if disease == 'ich':
            pass
        elif disease == 'red_spot':
            pass
       
    elif model == 'fiignet' and use_gpu:
        print("Running FIIGNET code")
        if disease == 'ich':
            pass
        elif disease == 'red_spot':
            pass

    print("Full pipeline complete!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--gpu', dest='gpu', action='store_true',
                        help='use GPU for processing')

    # Model group
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--gan', dest='model', action='store_const', const='gan',
                        help='run GAN model')
    group.add_argument('--stable_diffusion', dest='model', action='store_const', const='stable_diffusion',
                        help='run Stable Diffusion model')
    group.add_argument('--cvae', dest='model', action='store_const', const='cvae',
                        help='run CVAE model')
    group.add_argument('--fiignet', dest='model', action='store_const', const='fiignet',
                        help='run FIIGNET model')

    # Diseases group
    group_diseases = parser.add_mutually_exclusive_group(required=True)
    group_diseases.add_argument('--ich', dest='disease', action='store_const', const='ich',
                        help='run code for ICH')
    group_diseases.add_argument('--red_spot', dest='disease', action='store_const', const='red_spot',
                        help='run code for Red Spot')

    args = parser.parse_args()
    main(args.gpu, args.model, args.disease)




