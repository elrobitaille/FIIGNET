.PHONY: run help clean

resize:
	python preprocessing/sharpen_image/resize.py $(input_path) $(output_path) $(if $(width),$(width),) $(if $(height),$(height),)

inflate:
	python preprocessing/data_aug/inflate_data.py -d $(input_path) -b $(brightness) -r $(angle)

yolo:
	python preprocessing/yolo_tracking/examples/track.py --source $(input_path) --yolo-model $(weights) $(if $(height),--img-height $(height),) $(if $(width),--img-width $(width),) --save

segment:
	python preprocessing/yolo_tracking/examples/segment.py --source $(input_path) --yolo-model $(weights) --img-height $(height) --img-width $(width) --output-dir $(output_path) --save

mask:
	python preprocessing/mask_image/masks.py --input_path $(input_path) --checkpoint_path $(checkpoint_path) --output_path $(output_path)

enhance:
	python preprocessing/sharpen_image/process_images.py $(input_path) $(output_path) --gaussian --sharpen --smooth --denoise --upscale --clahe --edge_enhance
	
esrgan:
	python A-ESRGAN/inference_aesrgan.py --model_path=A-ESRGAN/experiments/pretrained_models/A_ESRGAN_Single.pth --input $(input_path) --output $(output_path)

train:
	python classification/train.py --input_path $(input_path) --output_path $(output_path)

predict:
	python classification/predict.py --input_image $(input_image) --learner $(learner)

help:
	@echo "Please check the README.md file for more information."

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
	
	