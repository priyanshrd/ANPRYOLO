from ultralytics import YOLO


model = YOLO('yolov8x.yaml')




results = model.train(data='config.yaml', epochs=512, imgsz=320)
results = model.val()
results = model("")
success = model.export(format="onnx")