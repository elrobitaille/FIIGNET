from ultralytics import YOLO

model = YOLO('yolov8n.pt') 

results = model.train(
    data = 'custom.yaml',
    imgsz = (1920, 1080),
    epochs = 200,
    batch = 12,
    name = 'yolov8n_results',

)
