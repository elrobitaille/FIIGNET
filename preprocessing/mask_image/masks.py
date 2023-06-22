import torch
import cv2
import numpy as np
import argparse
import os
from segment_anything import sam_model_registry, SamAutomaticMaskGenerator, SamPredictor
import supervision as sv

def main(args):
    DEVICE = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
    MODEL_TYPE = "vit_l"

    sam = sam_model_registry[MODEL_TYPE](checkpoint=args.checkpoint_path)
    sam.to(device=DEVICE)

    mask_generator = SamAutomaticMaskGenerator(sam)
    mask_predictor = SamPredictor(sam)

    # Create directories for annotated images and masks
    annotated_dir = os.path.join(args.output_path, 'annotated_images')
    masks_dir = os.path.join(args.output_path, 'masks')

    os.makedirs(annotated_dir, exist_ok=True)
    os.makedirs(masks_dir, exist_ok=True)

    for filename in os.listdir(args.input_path):
        if filename.endswith(".jpg") or filename.endswith(".png") or filename.endswith(".jpeg") or filename.endswith(".JPG") or filename.endswith(".PNG") or filename.endswith(".JPEG"):
            image_path = os.path.join(args.input_path, filename)

            image_bgr = cv2.imread(image_path)
            image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
            result = mask_generator.generate(image_rgb)

            mask_annotator = sv.MaskAnnotator()
            detections = sv.Detections.from_sam(result)
            annotated_image = mask_annotator.annotate(image_bgr, detections)

            cv2.imwrite(os.path.join(annotated_dir, f'annotated_{filename}'), annotated_image)

            mask_predictor = SamPredictor(sam)
            mask_predictor.set_image(image_rgb)

            box = np.array([0, 0, image_rgb.shape[1], image_rgb.shape[0]])  # This needs to be dynamic for different images
            masks, scores, logits = mask_predictor.predict(
                box=box,
                multimask_output=True
            )

            for i, mask in enumerate(masks):
                # Convert the boolean mask to an image with values in [0, 255]
                mask_image = (mask * 255).astype(np.uint8)
    
                # Save the mask with a unique filename
                mask_filename = f'mask_{os.path.splitext(filename)[0]}_{i}.png'
                cv2.imwrite(os.path.join(masks_dir, mask_filename), mask_image)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_path', type=str, required=True, help='Directory containing input images')
    parser.add_argument('--checkpoint_path', type=str, required=True, help='Path to the checkpoint file')
    parser.add_argument('--output_path', type=str, required=True, help='Directory to output results')
    args = parser.parse_args()
    main(args)
