import argparse
import subprocess
import random
import time

def main(prompt, num_images):
    # Generate images
    for i in range(1, num_images + 1):
        print(f"Generating image {i}")
        full_path_to_invokeai = "/home/ugrad/serius/edgarrobitaille/invokeai"
        seed = random.randint(1, 1000000)  # Generate a random seed
        process = subprocess.Popen(full_path_to_invokeai, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
        time.sleep(5)  # Give some time for invokeai to initialize
        process.communicate(input=f"{prompt} -n1 -s{seed}\nq\n".encode())

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate images with invokeai')
    parser.add_argument('--prompt', type=str, required=True,
                        help='The prompt to feed into the invokeai command')
    parser.add_argument('--num_images', type=int, default=10,
                        help='The number of images to generate')
    args = parser.parse_args()
    main(args.prompt, args.num_images)  

