from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, 
                           QHBoxLayout, QPushButton, QLabel, QFileDialog)
from PyQt6.QtCore import Qt
from .components.video_widget import VideoWidget
from .components.detection_widget import DetectionWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("安全帽检测系统")
        self.setMinimumSize(1200, 800)
        
        # 创建主窗口部件
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        
        # 创建主布局
        layout = QHBoxLayout(main_widget)
        
        # 左侧控制面板
        control_panel = QWidget()
        control_layout = QVBoxLayout(control_panel)
        
        # 添加控制按钮
        self.btn_open_video = QPushButton("打开视频")
        self.btn_open_camera = QPushButton("打开摄像头")
        self.btn_start_detection = QPushButton("开始检测")
        self.btn_stop_detection = QPushButton("停止检测")
        
        control_layout.addWidget(self.btn_open_video)
        control_layout.addWidget(self.btn_open_camera)
        control_layout.addWidget(self.btn_start_detection)
        control_layout.addWidget(self.btn_stop_detection)
        control_layout.addStretch()
        
        # 右侧视频显示区域
        self.video_widget = VideoWidget()
        self.detection_widget = DetectionWidget()
        
        # 添加部件到主布局
        layout.addWidget(control_panel, 1)
        layout.addWidget(self.video_widget, 4)
        layout.addWidget(self.detection_widget, 1) 