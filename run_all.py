import subprocess
import argparse

def main(model, background):
    raw_data_path = "/home/ugrad/serius/edgarrobitaille/ICH" 
    raw_data_enhanced_path = "image_data/processed/raw_image_enhanced" 
    resized_data_path = "image_data/unprocessed/resized" 
    facebook_checkpts = "/home/ugrad/serius/edgarrobitaille/segment-anything/sam_vit_l_0b3195.pth"
    facebook_mask_output = "preprocessing/mask_image"
    facebook_color_output = "preprocessing/mask_image/colored_masks"
    cropped_data_path = "image_data/unprocessed/segmented"
    square_resized_path = "image_data/processed/square_resize"
    colored_mask_path = "preprocessing/mask_image/colored_masks"

    resize_height = 512
    resize_width = 512
    square_size = 512

    gan_output = "/GAN_output"
    stable_diffusion_output = "/SD_output"

    commands = [
        f"make resize input_path={raw_data_path} output_path={resized_data_path} height={resize_height} width={resize_width}",
        f"make crop input_path={resized_data_path} output_path={cropped_data_path}"
    ]

    if not background:
        commands.append(f"make mask input_path={cropped_data_path} checkpoint_path={facebook_checkpts} output_path={facebook_mask_output}")

    if model == "gan":
        commands.append(f"make resize input_path={cropped_data_path} output_path={square_resized_path} height={square_size} width={square_size}")
        commands.append(f"make enhance input_path={square_resized_path} output_path={gan_output}")

    if model == "stable_diffusion":
        if background:
            commands.append(f"make enhance input_path={cropped_data_path} output_path={stable_diffusion_output}")
        else:
            commands.append(f"make enhance input_path={facebook_color_output} output_path={stable_diffusion_output}")

    for command in commands:
        process = subprocess.Popen(command, shell=True)
        process.communicate()  

        if process.returncode != 0:
            print(f"Command '{command}' failed with return code: {process.returncode}")
            break

    print("Pipeline Part 1 is complete!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--gan', dest='model', action='store_const', const='gan',
                        help='run GAN model')
    group.add_argument('--stable_diffusion', dest='model', action='store_const', const='stable_diffusion',
                        help='run Stable Diffusion model')
    group.add_argument('--cvae', dest='model', action='store_const', const='cvae',
                        help='run CVAE model')
    group.add_argument('--fiignet', dest='model', action='store_const', const='fiignet',
                        help='run FIIGNET model')

    parser.add_argument('--background', dest='background', action='store_true',
                        help='skip background removal')

    args = parser.parse_args()
    main(args.model, args.background)
