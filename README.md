
<p align="center">
  <img src="Logo2.png" alt="FIIGNET Logo" width="425" height="300">
</p>

# Full FIIGNET Pipeline 

## Starting Requirements 
Cloning the Repo:
`git clone https://github.com/EdgarRob/FIIGNET` 

Downloads all Requirements:
`pip install -r requirements.txt` 

## Running Part 1 of Pipeline (No Strong GPU Required)

### To Run the ENTIRE Part 1 Process:
1. Open `run_all.py` and change corresponding directories to your own (inputs and outputs) 
2. Run command:
`python run_all.py --(model_name) --(disease_type)`

### Where available model names and disease types are as follows: 
Model Names:
1. GAN (NVIDIA's StyleGAN to generate more abstract fish) 
`--gan`
2. Stable Diffusion (To generate more realistic fish)
`--stable_diffusion`
3. CVAE (Conditional Variational Auto Encoder)
`--cvae`
4. FIIGNET (Fish Illness Image Generator Network)
`--fiignet`

Diseases:
1. Ich (White Spot Disease) 
`--ich`
2. Red Spot Disease 
`--red_spot`

## To Run Parts Manually: 

1. ### Image Resizing 
Resizes a directory of images and outputs the given specified height and width dimensions. Used to allow the YOLO model to make better decisions and normalize images before processing. Note that height and width are optional, but default is 1980x1080.

To run the command:

`make resize input_path="path_to_input" output_path="path_to_output" width="?" height="?"`

2. ### Yolo Processing  
Processes input directory of images and outputs the corresponding YOLO output with red box around fish in a given image or video. Note that height and width are optional arguments if you would like to customize output size, though this may affect YOLO performance greatly. 

To run the command: 

`make yolo input_path="path_to_input" weights="path_to_weights" height="?" width="?"`

3. ### Yolo Segmentation  
Processes yolo image same way as previous command but segments the red YOLO boxes into separate images for each fish in a given image or video. Height and width are optional parameters. 

To run the command:

`make segment input_path="path_to_input" weights="path_to_weights" height="?" width="?" output_path="path_to_output"`

4. ### Facebook's Segment Anything Segmentation & Masking
Using Facebook's Segment Anything Segmentation (SAM), each individual item in an image can be segmented. From here, certain algorithms and assumptions can be used to determine what in the object is the fish, and thereby allow the creation of a mask that only contains the fish portion of the image. Note that this is passed through AFTER the YOLO Model. Note that facebook provides checkpoint pth models, this has been mainly tested with the vit_l model. Please check the repository for more information and pip requirements. 

Cloning the Repo:

`git clone https://github.com/facebookresearch/segment-anything`

Download Pip Requirements:

`pip install git+https://github.com/facebookresearch/segment-anything.git`

`pip install opencv-python pycocotools matplotlib onnxruntime onnx`

To run the command:

`make mask input_path="path_to_input" checkpoint_path="path_to_checkpoints.pth" output_path="path_to_output"`

5. ### Image Enhancer 
Processes the image to potentially enhance the quality. Uses methods/techniques such as the gaussian filter, unsharpen mask, denoising, Savitsky-Golay filter, to try to improve any low resolution images passed through or previously segmented. 

To run the command:

`make enhance input_path="/path/to/input" output_path="/path/to/output"`

6. ### ESRGAN Enhancer
Processes the image using an ESRGAN (Enhanced Super-Resolution Generative Adversarial Network) to enhance the quality of the image by filling in any details of the fish that may be off due to low resolution or quality.

Clone the A-ESRGAN Repo:

`git clone https://github.com/stroking-fishes-ml-corp/A-ESRGAN`

Move into this Repo:

`mv A-ESRGAN FIIGNET`

To run the command:

`make esrgan input_path="/path/to/input" output_path="/path/to/output"`


## Running Part 2 of Pipeline (Strong GPU Required)  
Clone NVIDIA's StyleGAN3 Repo:

`git clone https://github.com/NVlabs/stylegan3` 

Get Package for Virtual Environment:

`pip install virtualenv`

Create the virtual environment:

`python -m venv env_name`

### Activate the virtual environment:

MacOS/Unix: 

`source env_name/bin/activate`

Windows:

`.\env_name\Scripts\activate`

Install Requirements:

`pip install -r gan_requirements.txt`

### Use Make Resize (Part 1) 
Be sure to Make Images Square Size and Power of 2 (For Example: 256x256, 512x512)

### Creating the GAN ZIP file:
Please check the StyleGAN3 Repo for More Information.

`python dataset_tool.py --source="/path/to/input" --dest="/path/to/output.zip"`

### Training the GAN with ZIP file:
To run the command:

`python train.py --outdir=~/training-runs --cfg=stylegan3-t --data=/path/to/zip/file --gpus=? --batch=? --gamma=?`

### Generating Images with the Trained File:
To run the command:

`python gen_images.py --outdir=out --trunc=1 --seeds=2 --network=/path/to/trained/.pkl`

Be sure to check the training-runs directories for the results, and know that this process takes an extremely strong GPU. 

### To deactivate the virtual environment:
`deactivate`

## Running Part 3 of Pipeline (No Strong GPU Required)

1. ### Training with Real Images or GANs 
Trains a model using FastAI to create a classification model based on how images are separated by folder in the input directory. Will train a model that can predict what type of disease a given real picture or GAN fish has.

To run the command:

`make train input_path="/path/to/input" output_path="/path/to/output"`

2. ### Predicting with Real Images or GANs 
Performs predictions using the trained model with FastAI to predict what type of disease a given real picture or GAN fish has.

To run the command:

`make predict input_image="/path/to/input/image.jpg" learner="/path/to/learner.pkl"`

# License 
This code is licensed under the MIT license.

# Project Contributors
The following contributed to the ideation and building of the pipeline (alphabetical):
Edgar Robitaille, Amish Sethi, Harley Tran, Kai Wang, Katherine Yue, Kelvin Fong


# Questions? 
Feel free to contact me with any issues/questions: erobita1@jh.edu 

