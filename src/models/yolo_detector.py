import cv2
import numpy as np
from ultralytics import YOLO

class YOLODetector:
    def __init__(self, model_path='src/models/hard_helmet_det.pt'):
        """
        初始化YOLO检测器
        Args:
            model_path: YOLO模型路径
        """
        self.model = YOLO(model_path)
        self.class_names = ['helmet', 'no_helmet']  # 类别名称
        
    def detect(self, image):
        """
        对图像进行检测
        Args:
            image: 输入图像
        Returns:
            检测结果列表，每个结果包含类别、置信度和边界框
        """
        results = self.model(image)[0]
        detections = []
        
        for box in results.boxes:
            cls = int(box.cls[0])
            conf = float(box.conf[0])
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            
            detections.append({
                'class': self.class_names[cls],
                'confidence': conf,
                'bbox': (x1, y1, x2, y2)
            })
            
        return detections
        
    def draw_results(self, image, results):
        """
        在图像上绘制检测结果
        Args:
            image: 原始图像
            results: 检测结果列表
        Returns:
            绘制了检测结果的图像
        """
        image = image.copy()
        
        for result in results:
            x1, y1, x2, y2 = result['bbox']
            cls = result['class']
            conf = result['confidence']
            
            # 设置颜色（绿色表示戴安全帽，红色表示未戴安全帽）
            color = (0, 255, 0) if cls == 'helmet' else (0, 0, 255)
            
            # 绘制边界框
            cv2.rectangle(image, (x1, y1), (x2, y2), color, 2)
            
            # 绘制标签
            label = f'{cls}: {conf:.2f}'
            cv2.putText(image, label, (x1, y1 - 10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
            
        return image 