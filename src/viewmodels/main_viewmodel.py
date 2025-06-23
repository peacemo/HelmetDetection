from PyQt6.QtCore import QObject, pyqtSignal, QThread
import cv2
import numpy as np
from models.yolo_detector import YOLODetector

class DetectionThread(QThread):
    image_updated = pyqtSignal(np.ndarray)
    stats_updated = pyqtSignal(str)
    finished = pyqtSignal()
    
    def __init__(self, detector, image):
        super().__init__()
        self.detector = detector
        self.image = image
        
    def run(self):
        # 进行检测
        results = self.detector.detect(self.image)
        processed_image = self.detector.draw_results(self.image, results)
        
        # 更新统计信息
        stats = self._get_detection_stats(results)
        
        # 发送信号
        self.image_updated.emit(processed_image)
        self.stats_updated.emit(stats)
        self.finished.emit()
        
    def _get_detection_stats(self, results):
        if not results:
            return "无检测结果"
            
        helmet_count = sum(1 for r in results if r['class'] == 'helmet')
        no_helmet_count = sum(1 for r in results if r['class'] == 'no_helmet')
        
        return f"安全帽: {helmet_count} | 未戴安全帽: {no_helmet_count}"

class MainViewModel(QObject):
    # 定义信号
    image_updated = pyqtSignal(np.ndarray)
    stats_updated = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.detector = YOLODetector()
        self.detection_mode = '图片检测'
        self.source = None
        self.is_detecting = False
        self.cap = None
        self.detection_thread = None
        # 文件夹检测相关
        self.folder_path = None
        self.image_list = []
        self.current_index = 0
        
    def set_detection_mode(self, mode):
        self.detection_mode = mode
        if self.cap is not None:
            self.cap.release()
            self.cap = None
        if mode != '文件夹检测':
            self.folder_path = None
            self.image_list = []
            self.current_index = 0
        
    def set_source(self, source):
        self.source = source
        if self.cap is not None:
            self.cap.release()
            
        if self.detection_mode == '图片检测':
            # 加载并显示原图
            image = cv2.imread(source)
            if image is not None:
                self.image_updated.emit(image)
        elif self.detection_mode in ['视频检测', '摄像头检测']:
            self.cap = cv2.VideoCapture(source if self.detection_mode == '视频检测' else 0)
            
    def set_folder_source(self, folder_path):
        import os
        self.folder_path = folder_path
        # 获取所有图片文件
        exts = ('.jpg', '.jpeg', '.png', '.bmp')
        self.image_list = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.lower().endswith(exts)]
        self.image_list.sort()
        self.current_index = 0
        if self.image_list:
            image = cv2.imread(self.image_list[0])
            if image is not None:
                self.image_updated.emit(image)
            self.stats_updated.emit('')
        else:
            self.image_updated.emit(np.zeros((600, 800, 3), dtype=np.uint8))
            self.stats_updated.emit('文件夹中无图片')
        
    def prev_image(self):
        if not self.image_list:
            return
        self.current_index = (self.current_index - 1) % len(self.image_list)
        self._show_current_image()
    def next_image(self):
        if not self.image_list:
            return
        self.current_index = (self.current_index + 1) % len(self.image_list)
        self._show_current_image()
    def _show_current_image(self):
        image = cv2.imread(self.image_list[self.current_index])
        if image is not None:
            if self.is_detecting:
                self._detect_image(image)
            else:
                self.image_updated.emit(image)
                self.stats_updated.emit('')
    def start_detection(self):
        if self.detection_mode == '文件夹检测':
            self.is_detecting = True
            if self.image_list:
                image = cv2.imread(self.image_list[self.current_index])
                self._detect_image(image)
        elif not self.source and self.detection_mode != '摄像头检测':
            return
            
        self.is_detecting = True
        if self.detection_mode == '图片检测':
            self._process_image()
        else:
            self._process_video()
            
    def stop_detection(self):
        self.is_detecting = False
        if self.cap is not None:
            self.cap.release()
            self.cap = None
            
    def _process_image(self):
        if not self.source:
            return
            
        image = cv2.imread(self.source)
        if image is None:
            return
            
        # 创建并启动检测线程
        self.detection_thread = DetectionThread(self.detector, image)
        self.detection_thread.image_updated.connect(self.image_updated.emit)
        self.detection_thread.stats_updated.connect(self.stats_updated.emit)
        self.detection_thread.finished.connect(self._on_detection_finished)
        self.detection_thread.start()
        
    def _process_video(self):
        if self.cap is None:
            return
            
        while self.is_detecting:
            ret, frame = self.cap.read()
            if not ret:
                break
                
            # 进行检测
            results = self.detector.detect(frame)
            processed_frame = self.detector.draw_results(frame, results)
            
            # 更新统计信息
            stats = self._get_detection_stats(results)
            
            # 发送信号
            self.image_updated.emit(processed_frame)
            self.stats_updated.emit(stats)
            
            # 控制帧率
            cv2.waitKey(1)
            
    def _get_detection_stats(self, results):
        if not results:
            return "无检测结果"
            
        helmet_count = sum(1 for r in results if r['class'] == 'helmet')
        no_helmet_count = sum(1 for r in results if r['class'] == 'no_helmet')
        
        return f"安全帽: {helmet_count} | 未戴安全帽: {no_helmet_count}"

    def _detect_image(self, image):
        # 创建并启动检测线程
        self.detection_thread = DetectionThread(self.detector, image)
        self.detection_thread.image_updated.connect(self.image_updated.emit)
        self.detection_thread.stats_updated.connect(self.stats_updated.emit)
        self.detection_thread.finished.connect(self._on_detection_finished)
        self.detection_thread.start()

    def _on_detection_finished(self):
        self.detection_thread = None 