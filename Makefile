.PHONY: run help clean

resize:
	python preprocessing/sharpen_image/resize.py $(input_path) $(output_path)

yolo:
	python preprocessing/yolo_tracking/examples/track.py --source $(input_path) --yolo-model $(weights) $(if $(height),--img-height $(height),) $(if $(width),--img-width $(width),) --save

segment:
	python preprocessing/yolo_tracking/examples/segment.py --source $(input_path) --yolo-model $(weights) --img-height $(height) --img-width $(width) --output-dir $(output_path) --save

enhance:
	python preprocessing/sharpen_image/process_images.py $(input_dir) $(output_dir) --gaussian --sharpen --smooth --denoise --upscale --clahe --edge_enhance
	
esrgan:
	python A-ESRGAN/inference_aesrgan.py --model_path=A-ESRGAN/experiments/pretrained_models/A_ESRGAN_Single.pth --input $(input_dir) --output $(output_dir)

# train:
#	python classification/train.py --input_path $(input_path) --output_path $(output_path)

#predict:
#	python classification/predict.py --input_image $(input_image) --learner $(learner)

help:
	@echo "How to Run Commands:"

# Target: clean
# Remove generated files

# Sorry! Brace expansion wasn't working for me. I'll fix it later.
clean:
	rm -rf image_data/unprocessed/resized/*.jpg
	rm -rf image_data/unprocessed/resized/*.jpeg
	rm -rf image_data/unprocessed/resized/*.png
	rm -rf image_data/unprocessed/resized/*.JPG
	rm -rf image_data/unprocessed/resized/*.JPEG
	rm -rf image_data/unprocessed/resized/*.PNG
	
	rm -rf image_data/unprocessed/segmented/*.jpg
	rm -rf image_data/unprocessed/segmented/*.jpeg
	rm -rf image_data/unprocessed/segmented/*.png
	rm -rf image_data/unprocessed/segmented/*.JPG
	rm -rf image_data/unprocessed/segmented/*.JPEG
	rm -rf image_data/unprocessed/segmented/*.PNG
	
	rm -rf image_data/processed/crop_enhanced/*.jpg
	rm -rf image_data/processed/crop_enhanced/*.jpeg
	rm -rf image_data/processed/crop_enhanced/*.png
	rm -rf image_data/processed/crop_enhanced/*.JPG
	rm -rf image_data/processed/crop_enhanced/*.JPEG
	rm -rf image_data/processed/crop_enhanced/*.PNG
	
	rm -rf image_data/processed/raw_image_enhanced/*.jpg
	rm -rf image_data/processed/raw_image_enhanced/*.jpeg
	rm -rf image_data/processed/raw_image_enhanced/*.png
	rm -rf image_data/processed/raw_image_enhanced/*.JPG
	rm -rf image_data/processed/raw_image_enhanced/*.JPEG
	rm -rf image_data/processed/raw_image_enhanced/*.PNG
	
	rm -rf image_data/processed/yolo_output/*.jpg
	rm -rf image_data/processed/yolo_output/*.jpeg
	rm -rf image_data/processed/yolo_output/*.png
	rm -rf image_data/processed/yolo_output/*.JPG
	rm -rf image_data/processed/yolo_output/*.JPEG
	rm -rf image_data/processed/yolo_output/*.PNG