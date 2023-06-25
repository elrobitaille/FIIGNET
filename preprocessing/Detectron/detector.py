import argparse
import cv2
import os
import traceback

from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2 import model_zoo
from detectron2.data import MetadataCatalog
from detectron2.utils.visualizer import ColorMode, Visualizer

class Detector():
    def __init__(self):
        self.cfg = get_cfg()

        self.cfg.merge_from_file(model_zoo.get_config_file("COCO-Detection/retinanet_R_101_FPN_3x.yaml"))
        self.cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url("COCO-Detection/retinanet_R_101_FPN_3x.yaml")


        self.cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.99
        self.cfg.MODEL.DEVICE = 'cuda'

        self.predictor = DefaultPredictor(self.cfg)

    def onImage(self, imagePath, output_dir):
        try:
            image = cv2.imread(imagePath)
            if image is None:
                print(f"Failed to read image at {imagePath}")
                pass

            predictions = self.predictor(image)
            instances = predictions["instances"].to("cpu")
            if len(instances) == 0:
                print(f"No instances detected in the image: {imagePath}")
                pass

            for i, box in enumerate(instances.pred_boxes):
                x1, y1, x2, y2 = box.int().numpy()
                cropped_image = image[y1:y2, x1:x2]
                filename = os.path.splitext(os.path.basename(imagePath))[0]
                cv2.imwrite(os.path.join(output_dir, f"{filename}_crop_{i}.jpg"), cropped_image)

        except Exception as e:
            print(f"Failed to process image at {imagePath} due to {str(e)}")
            traceback.print_exc()  # This will print the full traceback

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_path", type=str, help="Directory path for input images.")
    parser.add_argument("--output_path", type=str, help="Directory path for output cropped images.")
    args = parser.parse_args()

    detector = Detector()

    # get list of all image files in the input directory
    image_files = [os.path.join(args.input_path, f) for f in os.listdir(args.input_path) if f.endswith(('.png', '.jpg', '.jpeg'))]
    
    print(f"Found {len(image_files)} image files.")

    for i, imagePath in enumerate(image_files):
        print(f"Processing image {i+1}/{len(image_files)}: {imagePath}...")
        detector.onImage(imagePath, args.output_path)