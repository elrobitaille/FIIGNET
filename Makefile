.PHONY: run help clean

resize:
	if [ "$(padding)" = "" ]; then \
		python preprocessing/sharpen_image/resize.py $(input_path) $(output_path) --width=$(width) --height=$(height); \
	else \
		python preprocessing/sharpen_image/resize.py $(input_path) $(output_path) --width=$(width) --height=$(height) --padding; \
	fi

inflate:
	python preprocessing/data_aug/inflate_data.py -i $(input_path) -o $(output_path)

crop:
	python preprocessing/Detectron/detector.py --input_path $(input_path) --output_path $(output_path)

mask:
	python preprocessing/mask_image/masks.py --input_path $(input_path) --checkpoint_path $(checkpoint_path) --output_path $(output_path)

enhance:
	python preprocessing/sharpen_image/process_images.py $(input_path) $(output_path) --sharpen --clahe
	
package:
	python /home/ugrad/serius/edgarrobitaille/stylegan3/dataset_tool.py --source $(input_path) --dest $(output_path)

train:
	python classification/train.py --input_path $(input_path) --output_path $(output_path)

predict:
	python classification/predict.py --input_image $(input_image) --learner $(learner)

help:
	@echo "Please check the README.md file for more information."

# OPTIONAL PARAMETERS TO PLAY WITH

# YOLO just gives the output red boxes, segment will splice images of red boxes separately and save them in the output directory
yolo:
	python preprocessing/yolo_tracking/examples/track.py --source $(input_path) --yolo-model $(weights) $(if $(height),--img-height $(height),) $(if $(width),--img-width $(width),) --save

segment:
	python preprocessing/yolo_tracking/examples/segment.py --source $(input_path) --yolo-model $(weights) --img-height $(height) --img-width $(width) --output-dir $(output_path) --save

esrgan:
	python A-ESRGAN/inference_aesrgan.py --model_path=A-ESRGAN/experiments/pretrained_models/A_ESRGAN_Single.pth --input $(input_dir) --output $(output_dir)

# Target: clean
# Remove generated files

clean:
	rm -rf image_data/unprocessed/resized/*.jpg
	rm -rf image_data/unprocessed/resized/*.jpeg
	rm -rf image_data/unprocessed/resized/*.png
	rm -rf image_data/unprocessed/resized/*.JPG
	rm -rf image_data/unprocessed/resized/*.JPEG
	rm -rf image_data/unprocessed/resized/*.PNG
	rm -rf image_data/unprocessed/resized/*.png
	
	rm -rf image_data/unprocessed/segmented/*.jpg
	rm -rf image_data/unprocessed/segmented/*.jpeg
	rm -rf image_data/unprocessed/segmented/*.png
	rm -rf image_data/unprocessed/segmented/*.JPG
	rm -rf image_data/unprocessed/segmented/*.JPEG
	rm -rf image_data/unprocessed/segmented/*.PNG
	rm -rf image_data/unprocessed/segmented/*.png
	
	rm -rf image_data/processed/crop_enhanced/*.jpg
	rm -rf image_data/processed/crop_enhanced/*.jpeg
	rm -rf image_data/processed/crop_enhanced/*.png
	rm -rf image_data/processed/crop_enhanced/*.JPG
	rm -rf image_data/processed/crop_enhanced/*.JPEG
	rm -rf image_data/processed/crop_enhanced/*.PNG
	rm -rf image_data/processed/crop_enhanced/*.png
	
	rm -rf image_data/processed/raw_image_enhanced/*.jpg
	rm -rf image_data/processed/raw_image_enhanced/*.jpeg
	rm -rf image_data/processed/raw_image_enhanced/*.png
	rm -rf image_data/processed/raw_image_enhanced/*.JPG
	rm -rf image_data/processed/raw_image_enhanced/*.JPEG
	rm -rf image_data/processed/raw_image_enhanced/*.PNG
	rm -rf image_data/processed/raw_image_enhanced/*.png 
	
	rm -rf image_data/processed/yolo_output/*.jpg
	rm -rf image_data/processed/yolo_output/*.jpeg
	rm -rf image_data/processed/yolo_output/*.png
	rm -rf image_data/processed/yolo_output/*.JPG
	rm -rf image_data/processed/yolo_output/*.JPEG
	rm -rf image_data/processed/yolo_output/*.PNG
	rm -rf image_data/processed/yolo_output/*.png

	rm -rf image_data/processed/ESRGAN_output/enhanced/*.jpg
	rm -rf image_data/processed/ESRGAN_output/enhanced/*.jpeg
	rm -rf image_data/processed/ESRGAN_output/enhanced/*.png
	rm -rf image_data/processed/ESRGAN_output/enhanced/*.JPG
	rm -rf image_data/processed/ESRGAN_output/enhanced/*.JPEG
	rm -rf image_data/processed/ESRGAN_output/enhanced/*.PNG
	rm -rf image_data/processed/ESRGAN_output/enhanced/*.png

	rm -rf image_data/processed/ESRGAN_output/raw/*.jpg
	rm -rf image_data/processed/ESRGAN_output/raw/*.jpeg
	rm -rf image_data/processed/ESRGAN_output/raw/*.png
	rm -rf image_data/processed/ESRGAN_output/raw/*.JPG
	rm -rf image_data/processed/ESRGAN_output/raw/*.JPEG
	rm -rf image_data/processed/ESRGAN_output/raw/*.PNG
	rm -rf image_data/processed/ESRGAN_output/raw/*.png

	rm -rf image_data/processed/square_resize/*.jpg
	rm -rf image_data/processed/square_resize/*.jpeg
	rm -rf image_data/processed/square_resize/*.png
	rm -rf image_data/processed/square_resize/*.JPG
	rm -rf image_data/processed/square_resize/*.JPEG
	rm -rf image_data/processed/square_resize/*.PNG
	rm -rf image_data/processed/square_resize/*.png

	rm -rf preprocessing/mask_image/annotated_images/*.jpg
	rm -rf preprocessing/mask_image/annotated_images/*.jpeg
	rm -rf preprocessing/mask_image/annotated_images/*.png
	rm -rf preprocessing/mask_image/annotated_images/*.JPG
	rm -rf preprocessing/mask_image/annotated_images/*.JPEG
	rm -rf preprocessing/mask_image/annotated_images/*.PNG
	rm -rf preprocessing/mask_image/annotated_images/*.png

	rm -rf preprocessing/mask_image/masks/*.jpg
	rm -rf preprocessing/mask_image/masks/*.jpeg
	rm -rf preprocessing/mask_image/masks/*.png
	rm -rf preprocessing/mask_image/masks/*.JPG
	rm -rf preprocessing/mask_image/masks/*.JPEG
	rm -rf preprocessing/mask_image/masks/*.PNG
	rm -rf preprocessing/mask_image/masks/*.png

	rm -rf image_data/unprocessed/raw/*.jpg
	rm -rf image_data/unprocessed/raw/*.jpeg
	rm -rf image_data/unprocessed/raw/*.png
	rm -rf image_data/unprocessed/raw/*.JPG
	rm -rf image_data/unprocessed/raw/*.JPEG
	rm -rf image_data/unprocessed/raw/*.PNG
	rm -rf image_data/unprocessed/raw/*.png
	
	rm -rf preprocessing/mask_image/colored_masks/*.jpg
	rm -rf preprocessing/mask_image/colored_masks/*.jpeg
	rm -rf preprocessing/mask_image/colored_masks/*.png
	rm -rf preprocessing/mask_image/colored_masks/*.JPG
	rm -rf preprocessing/mask_image/colored_masks/*.JPEG
	rm -rf preprocessing/mask_image/colored_masks/*.PNG
	rm -rf preprocessing/mask_image/colored_masks/*.png
	
	rm -rf preprocessing/Detectron/detect_outputs/*.jpg
	rm -rf preprocessing/Detectron/detect_outputs/*.jpeg
	rm -rf preprocessing/Detectron/detect_outputs/*.png
	rm -rf preprocessing/Detectron/detect_outputs/*.JPG
	rm -rf preprocessing/Detectron/detect_outputs/*.JPEG
	rm -rf preprocessing/Detectron/detect_outputs/*.PNG
	rm -rf preprocessing/Detectron/detect_outputs/*.png

	rm -rf SD_output/*.jpg
	rm -rf SD_output/*.jpeg
	rm -rf SD_output/*.png
	rm -rf SD_output/*.JPG
	rm -rf SD_output/*.JPEG
	rm -rf SD_output/*.PNG

	rm -rf image_data/unprocessed/augmented/*.jpg
	rm -rf image_data/unprocessed/augmented/*.jpeg
	rm -rf image_data/unprocessed/augmented/*.png
	rm -rf image_data/unprocessed/augmented/*.JPG
	rm -rf image_data/unprocessed/augmented/*.JPEG
	rm -rf image_data/unprocessed/augmented/*.PNG

	rm -rf GAN_output/*.jpg
	rm -rf GAN_output/*.jpeg
	rm -rf GAN_output/*.png
	rm -rf GAN_output/*.JPG
	rm -rf GAN_output/*.JPEG
	rm -rf GAN_output/*.PNG
	


	
	
	
