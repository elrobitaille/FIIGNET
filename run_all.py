import subprocess
import argparse
import json

def load_config(config_file="config.json"):
    with open(config_file, "r") as file:
        return json.load(file)

CONFIG = load_config()

IMAGE_DATA_PATH = f"{CONFIG['base_path']}/image_data"
UNPROCESSED_PATH = f"{IMAGE_DATA_PATH}/unprocessed"
PROCESSED_PATH = f"{IMAGE_DATA_PATH}/processed"

resize_height = CONFIG['resize']['height']
resize_width = CONFIG['resize']['width']
square_size = CONFIG['square_size']

PATHS = {
    'raw_data': f"{UNPROCESSED_PATH}/raw/ich",
    'augmented_data': f"{UNPROCESSED_PATH}/augmented",
    'cropped_data': f"{UNPROCESSED_PATH}/segmented",
    'square_resized': f"{PROCESSED_PATH}/square_resize",
    'mask_output': "preprocessing/mask_image",
    'mask_color_output': "preprocessing/mask_image/colored_masks",
    'facebook_checkpts': f"{CONFIG['segment_anything_path']}/sam_vit_l_0b3195.pth",
    'results': f"{CONFIG['base_path']}/results",
}

def generate_commands(model, skip_background):
    commands = [
        # f"make inflate input_path={PATHS['raw_data']} output_path={PATHS['augmented_data']}",
        f"make crop input_path={PATHS['raw_data']} output_path={PATHS['cropped_data']}"
    ]

    if not skip_background:
        commands.append(f"make mask input_path={PATHS['cropped_data']} checkpoint_path={PATHS['facebook_checkpts']} output_path={PATHS['mask_output']}")

    if model == "gan":
        commands.extend([
            f"make resize input_path={PATHS['cropped_data']} output_path={PATHS['square_resized']} width={square_size} height={square_size} padding=1",
            f"make enhance input_path={PATHS['square_resized']} output_path={PATHS['results']}"
        ])
    elif model == "stable_diffusion":
        enhance_input = PATHS['mask_color_output'] if not skip_background else PATHS['cropped_data']
        commands.append(f"make enhance input_path={enhance_input} output_path={PATHS['results']}")

    # Extend for future models 

    return commands

def run_commands(commands):
    for command in commands:
        process = subprocess.Popen(command, shell=True)
        process.communicate()  

        if process.returncode != 0:
            print(f"Command '{command}' failed with return code: {process.returncode}")
            break

    print("Pipeline Part 1 is complete!")

def main():
    parser = argparse.ArgumentParser(description='Process images using specified models.')

    group = parser.add_mutually_exclusive_group(required=True)
    models = ['gan', 'stable_diffusion', 'cvae', 'fiignet']
    for model in models:
        group.add_argument(f'--{model}', dest='model', action='store_const', const=model, help=f'run {model.upper()} model')

    parser.add_argument('--background', dest='skip_background', action='store_true', help='skip background removal')

    args = parser.parse_args()

    commands = generate_commands(args.model, args.skip_background)
    run_commands(commands)

if __name__ == "__main__":
    main()
