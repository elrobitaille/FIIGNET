import torch
import cv2
import numpy as np
import argparse
import os
from segment_anything import sam_model_registry, SamAutomaticMaskGenerator, SamPredictor
import supervision as sv

CENTROID_REGION_PERCENT = 0.3 # Change for different centroid region
AREA_MIN_PERCENT = 0.15 # Change for different area minimum

def mask_centroid_and_area(mask):
    moments = cv2.moments(mask)
    area = moments['m00']
    centroid = (moments['m10']/area, moments['m01']/area)
    return centroid, area

def main(args):
    try:
        DEVICE = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
        MODEL_TYPE = "vit_l"

        sam = sam_model_registry[MODEL_TYPE](checkpoint=args.checkpoint_path)
        sam.to(device=DEVICE)

        mask_generator = SamAutomaticMaskGenerator(sam)
        mask_predictor = SamPredictor(sam)

        annotated_dir = os.path.join(args.output_path, 'annotated_images')
        masks_dir = os.path.join(args.output_path, 'masks')
        colored_masks_dir = os.path.join(args.output_path, 'colored_masks')

        os.makedirs(annotated_dir, exist_ok=True)
        os.makedirs(masks_dir, exist_ok=True)
        os.makedirs(colored_masks_dir, exist_ok=True)

        for filename in os.listdir(args.input_path):
            if filename.endswith((".jpg", ".png", ".jpeg", ".JPG", ".PNG", ".JPEG")):
                image_path = os.path.join(args.input_path, filename)

                image_bgr = cv2.imread(image_path)
                if image_bgr is None:
                    print(f"Failed to read image at {image_path}")
                    continue

                image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
                result = mask_generator.generate(image_rgb)

                mask_annotator = sv.MaskAnnotator()
                detections = sv.Detections.from_sam(result)
                annotated_image = mask_annotator.annotate(image_bgr, detections)

                cv2.imwrite(os.path.join(annotated_dir, f'annotated_{filename}'), annotated_image)

                mask_predictor.set_image(image_rgb)

                box = np.array([0, 0, image_rgb.shape[1], image_rgb.shape[0]])  
                masks, scores, logits = mask_predictor.predict(box=box, multimask_output=True)

                max_area = 0
                best_mask = None
                for i, mask in enumerate(masks):
                    mask_image = (mask * 255).astype(np.uint8)

                    centroid, area = mask_centroid_and_area(mask_image)
                    
                    central_region = (image_rgb.shape[1]*CENTROID_REGION_PERCENT, image_rgb.shape[0]*CENTROID_REGION_PERCENT, image_rgb.shape[1]*(1-CENTROID_REGION_PERCENT), image_rgb.shape[0]*(1-CENTROID_REGION_PERCENT))
                    if central_region[0] < centroid[0] < central_region[2] and central_region[1] < centroid[1] < central_region[3]:
                        if area > image_rgb.shape[0] * image_rgb.shape[1] * AREA_MIN_PERCENT and area > max_area:
                            max_area = area
                            best_mask = mask_image

                if best_mask is not None:
                    # Save the best mask
                    mask_filename = f'mask_{os.path.splitext(filename)[0]}.png'
                    cv2.imwrite(os.path.join(masks_dir, mask_filename), best_mask)

                    # Save the colored segmentation
                    colored_mask = cv2.bitwise_and(image_bgr, image_bgr, mask=best_mask)
                    colored_mask_filename = f'colored_mask_{os.path.splitext(filename)[0]}.png'
                    cv2.imwrite(os.path.join(colored_masks_dir, colored_mask_filename), colored_mask)
    except Exception as e:
        print(f"Exception occurred: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_path', type=str, required=True, help='Directory containing input images')
    parser.add_argument('--checkpoint_path', type=str, required=True, help='Path to the checkpoint file')
    parser.add_argument('--output_path', type=str, required=True, help='Directory to output results')
    args = parser.parse_args()
    main(args)
