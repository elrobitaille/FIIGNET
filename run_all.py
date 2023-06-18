# File to run entire pipeline for the user 
# Be sure to fix the directories to where you would like them to go.

import subprocess

def main():
    raw_data_path = "/home/ugrad/serius/edgarrobitaille/AquaFinity-main/fish-data/data/healthy/images"
    raw_data_enhanced_path = "/home/ugrad/serius/edgarrobitaille/FIIGNET/image_data/processed/raw_image_enhanced"
    resized_data_path = "/home/ugrad/serius/edgarrobitaille/FIIGNET/image_data/unprocessed/resized"
    weights = "/home/ugrad/serius/edgarrobitaille/FIIGNET/preprocessing/yolo_tracking/YOLO/runs/detect/yolov8n_results2/weights/best.pt"
    cropped_data_path = "/home/ugrad/serius/edgarrobitaille/FIIGNET/image_data/unprocessed/segmented"
    cropped_data_enhanced_path = "/home/ugrad/serius/edgarrobitaille/FIIGNET/image_data/processed/crop_enhanced"

    height = "1080"
    width = "1980"

    commands = [
        #f"make enhance input_dir={raw_data_path} output_dir={raw_data_enhanced_path}",
        #f"make resize input_path={raw_data_enhanced_path} output_path={resized_data_path}",
        f"make segment input_path={resized_data_path} weights={weights} height={height} width={width} output_path={cropped_data_path}",
        f"make enhance input_dir={cropped_data_path} output_dir={cropped_data_enhanced_path}"
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
