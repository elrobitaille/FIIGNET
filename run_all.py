# File to run entire pipeline for the user 
# Be sure to fix the directories to where you would like them to go.

import subprocess

def main():
    raw_data_path = "/Users/edgarrobitaille/Desktop/FIIGNET/image_data/unprocessed/fish/white_spot/ich"
    raw_data_enhanced_path = "/Users/edgarrobitaille/Desktop/FIIGNET/image_data/processed/raw_image_enhanced"
    resized_data_path = "/Users/edgarrobitaille/Desktop/FIIGNET/image_data/unprocessed/resized"
    weights = "/Users/edgarrobitaille/Desktop/FIIGNET/preprocessing/yolo_tracking/runs/yolov8n_results6/weights/best.pt"
    cropped_data_path = "/Users/edgarrobitaille/Desktop/FIIGNET/image_data/unprocessed/segmented"
    cropped_data_enhanced_path = "/Users/edgarrobitaille/Desktop/FIIGNET/image_data/processed/crop_enhanced"
    height = "1080"
    width = "1980"

    commands = [
        f"make enhance input_dir={raw_data_path} output_dir={raw_data_enhanced_path}",
        f"make resize input_path={raw_data_enhanced_path} output_path={resized_data_path}",
       # f"make segment input_path={resized_data_path} weights={weights} height={height} width={width}",
       # f"make enhance input_dir={cropped_data_path} output_dir={cropped_data_enhanced_path}"
    ]

    # Run each command in sequence
    for command in commands:
        process = subprocess.Popen(command, shell=True)
        process.communicate()  # wait for the process to terminate

        if process.returncode != 0:
            print(f"Command '{command}' failed with return code: {process.returncode}")
            break

if __name__ == "__main__":
    main()
