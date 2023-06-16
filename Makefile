.PHONY: run help clean

train:
	python classification/train.py --input_path $(input_path) --output_path $(output_path)

help:
	@echo "How to Run Commands:"
	@echo "Training dataset: make train input_path="/your/image/directory/path" output_path="/your/output/path.pkl""

# Target: clean
# Remove generated files
clean:
