from pathlib import Path
from ultralytics import YOLO
import cv2
import os
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="YOLOv8 detection and FLOPs calculation")
    parser.add_argument(
        "--image_path",
        type=str,
        default="./Heridal-1/valid/images",
        help="Path to the folder containing input images"
    )
    parser.add_argument(
        "--label_path",
        type=str,
        default="./labels",
        help="Path to the folder for saving prediction labels"
    )

    return parser.parse_args()


if __name__=="__main__":

    args = parse_args()
    IMAGE_PATH = args.image_path
    LABEL_PATH = args.label_path
    os.makedirs(LABEL_PATH, exist_ok=True)

    # использую yolov8s
    model = YOLO('best.pt')

    image_files = list(Path(IMAGE_PATH).glob('*.*'))

    for path in image_files:
        label_path = Path(LABEL_PATH) / (path.stem + '.txt')
        img = cv2.imread(str(path))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        height, width = img.shape[:2]
        predictions = []

        # предсказание
        results = model(img)

        for result in results:
            boxes = result.boxes
            for box in boxes:
                class_id = int(box.cls)
                x_center, y_center, box_width, box_height = box.xywh[0].tolist()
                confidence = box.conf.item()
                
                # нормализация
                x_center = x_center / width
                y_center = y_center / height
                box_width = box_width / width
                box_height = box_height / height

                predictions.append({
                    'class_id': class_id,
                    'x_center': x_center,
                    'y_center': y_center,
                    'width': box_width,
                    'height': box_height,
                    'confidence': confidence
                })
        
        with open(label_path, 'w', encoding='utf-8') as f:
            for pred in predictions:
                line = f"{pred['class_id']} {pred['x_center']} {pred['y_center']} {pred['width']} {pred['height']} {pred['confidence']}\n"
                f.write(line)


    model_info = model.info()
    print(f"Total FLOPs: {model_info[3]} GFLOPs")
    print(f"Total MACs: {model_info[3] /  2} GMACs")
