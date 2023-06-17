from ultralytics import YOLO

model = YOLO('yolov8n.pt') 

results = model.train(
    data = 'custom.yaml',
    imgsz = 1280,
    epochs = 50,
    batch = 8,
    name = 'yolov8n_results',

)