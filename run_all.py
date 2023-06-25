# File to run entire pipeline for the user 
# Be sure to fix the directories to where you would like them to go.

import subprocess
import argparse

def main(use_gpu, model, disease, background):
    raw_data_path = "/home/ugrad/serius/edgarrobitaille/ichtest/00000" # Change this to the path of the raw image data
    raw_data_enhanced_path = "image_data/processed/raw_image_enhanced" # Change this to the path of the enhanced images
    resized_data_path = "image_data/unprocessed/resized" # Change this to the path of the resized images
    facebook_checkpts = "/home/ugrad/serius/edgarrobitaille/segment-anything/sam_vit_l_0b3195.pth" # Change this to the path of the Facebook checkpoints
    facebook_mask_output = "preprocessing/mask_image" # Change this to the path of the output for Facebook's model
    cropped_data_path = "image_data/unprocessed/segmented" # Change this to the path of the segmented images
   # esrgan_output_path = "image_data/processed/ESRGAN_output" # Change this to the path of the ESRGAN output images
    square_resized_path = "image_data/processed/square_resize" # Change this to the path of the square resized images for the GAN in Part 2
    colored_mask_path = "preprocessing/mask_image/colored_masks" # Change this to the path of the colored masks for the GAN in Part 2
    stable_diffusion_output = "image_data/processed/stable_diffusion/SD_input" # Change this to the path of the output for the Stable Diffusion model (to be input in Part 2)


    # If using YOLOv8, uncomment:
    # yolo_weights = "preprocessing/yolo_tracking/YOLO/runs/detect/yolov8n_results2/weights/best.pt" # Change this to the path of the YOLO weights
    # yolo_height = 608
    # yolo_width = 608
    # COMMAND TO RUN:
    # f"make segment input_path={resized_data_path} weights={yolo_weights} height={height} width={width} output_path={cropped_data_path}",

    height = 800 # Change for output size of Part 1 
    width = 1333 # Change for output size of Part 1 
    square_size = 512 # Size for square images for GAN or SD
        
    commands = [ # Change if you would like to change the ran commands based on Makefile
        # f"make enhance input_path={raw_data_path} output_path={raw_data_enhanced_path}",
        f"make resize input_path={raw_data_enhanced_path} output_path={resized_data_path} height={yolo_height} width={yolo_width}",
    ]
    
    if not background:
        commands.append(f"make mask input_path={cropped_data_path} checkpoint_path={facebook_checkpts} output_path={facebook_mask_output}")

    if model == "gan" or model == "stable_diffusion":
        if yolo_height != height or yolo_width != width:
            commands.append(f"make resize input_path={colored_mask_path} output_path={square_resized_path} height={height} width={width}")
    if model == "gan":
        commands.append(f"make package input_path={square_resized_path} output_path={stable_diffusion_output}")
    if model == "cvae":
        pass 
    if model == "fiignet":
        pass

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

    print("Pipeline Part 1 is complete!")

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
    group_diseases.add_argument('--healthy', dest='disease', action='store_const', const='healthy',
                        help='run code for healthy fish')
    group_diseases.add_argument('--ich', dest='disease', action='store_const', const='ich',
                        help='run code for ICH')
    group_diseases.add_argument('--red_spot', dest='disease', action='store_const', const='red_spot',
                        help='run code for Red Spot')

    parser.add_argument('--background', action='store_true', 
                        help='Use this flag to skip the "make mask" command and save the background.')

    args = parser.parse_args()
    main(args.gpu, args.model, args.disease, args.background)
