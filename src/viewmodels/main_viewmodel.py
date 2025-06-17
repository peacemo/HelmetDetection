from PyQt6.QtCore import QObject, pyqtSignal
import cv2
import torch
from ultralytics import YOLO

class MainViewModel(QObject):
    # 定义信号
    frame_processed = pyqtSignal(object)  # 发送处理后的帧
    detection_results = pyqtSignal(list)  # 发送检测结果
    
    def __init__(self):
        super().__init__()
        self.model = None
        self.is_detecting = False
        self.video_source = None
        self.cap = None
        
    def load_model(self, model_path):
        """加载YOLO模型"""
        self.model = YOLO(model_path)
        
    def start_detection(self):
        """开始检测"""
        self.is_detecting = True
        
    def stop_detection(self):
        """停止检测"""
        self.is_detecting = False
        
    def process_frame(self, frame):
        """处理视频帧"""
        if not self.is_detecting or self.model is None:
            return frame
            
        # 执行检测
        results = self.model(frame)
        
        # 处理检测结果
        processed_frame = self.draw_detections(frame, results[0])
        
        # 发送信号
        self.frame_processed.emit(processed_frame)
        self.detection_results.emit(results[0].boxes.data.tolist())
        
        return processed_frame
        
    def draw_detections(self, frame, results):
        """在帧上绘制检测结果"""
        # 实现检测框的绘制
        return frame 