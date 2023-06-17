.PHONY: run help clean

resize:
	python resize.py $(input_path) $(output_path)

yolo:
	python preprocessing/yolo_model/examples/track.py --source $(input_path) --yolo-model $(weights) $(if $(height),--img-height $(height),) $(if $(width),--img-width $(width),) --save

train:
	python classification/train.py --input_path $(input_path) --output_path $(output_path)

predict:
	python classification/predict.py --input_image $(image_image) --learner $(learner_file)

help:
	@echo "How to Run Commands:"
	@echo "Training dataset: make train input_path="/your/image/directory/path" output_path="/your/output/path.pkl""

# Target: clean
# Remove generated files
clean:
