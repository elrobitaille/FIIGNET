import subprocess
import argparse

def main(use_gpu, model, disease, background):
    raw_data_path = "/home/ugrad/serius/edgarrobitaille/ICH" 
    raw_data_enhanced_path = "image_data/processed/raw_image_enhanced" 
    resized_data_path = "image_data/unprocessed/resized" 
    facebook_checkpts = "/home/ugrad/serius/edgarrobitaille/segment-anything/sam_vit_l_0b3195.pth"
    facebook_mask_output = "preprocessing/mask_image"
    cropped_data_path = "image_data/unprocessed/segmented"
    square_resized_path = "image_data/processed/square_resize"
    colored_mask_path = "preprocessing/mask_image/colored_masks"

    resize_height = 512
    resize_width = 512
    square_size = 512

    commands = [
       # f"make resize input_path={raw_data_path} output_path={resized_data_path} height={resize_height} width={resize_width}",
        f"make crop input_path={raw_data_path} output_path={cropped_data_path}"
    ]

    commands.append(f"make mask input_path={cropped_data_path} checkpoint_path={facebook_checkpts} output_path={facebook_mask_output}")
    commands.append(f"make resize input_path={cropped_data_path} output_path={square_resized_path} height={square_size} width={square_size}")
    commands.append(f"make enhance input_path={square_resized_path} output_path={raw_data_enhanced_path}")

    for command in commands:
        process = subprocess.Popen(command, shell=True)
        process.communicate()  

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

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--gan', dest='model', action='store_const', const='gan',
                        help='run GAN model')
    group.add_argument('--stable_diffusion', dest='model', action='store_const', const='stable_diffusion',
                        help='run Stable Diffusion model')
    group.add_argument('--cvae', dest='model', action='store_const', const='cvae',
                        help='run CVAE model')
    group.add_argument('--fiignet', dest='model', action='store_const', const='fiignet',
                        help='run FIIGNET model')

    group_diseases = parser.add_mutually_exclusive_group(required=True)
    group_diseases.add_argument('--healthy', dest='disease', action='store_const', const='healthy',
                        help='run code for healthy fish')
    group_diseases.add_argument('--ich', dest='disease', action='store_const', const='ich',
                        help='run code for ICH')
    group_diseases.add_argument('--red_spot', dest='disease', action='store_const', const='red_spot',
                        help='run code for Red Spot')

    args = parser.parse_args()
    main(args.gpu, args.model, args.disease, False)
