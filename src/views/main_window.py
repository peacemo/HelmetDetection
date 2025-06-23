from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QLabel, QComboBox, QFileDialog)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QImage, QPixmap
import cv2
import numpy as np

class MainWindow(QMainWindow):
    def __init__(self, view_model):
        super().__init__()
        self.view_model = view_model
        # 连接信号到槽
        self.view_model.image_updated.connect(self.update_image)
        self.view_model.stats_updated.connect(self.update_stats)
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle('安全帽检测系统')
        self.setGeometry(100, 100, 1200, 800)
        
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建主布局
        main_layout = QHBoxLayout(central_widget)
        
        # 左侧控制面板
        control_panel = QWidget()
        control_layout = QVBoxLayout(control_panel)
        
        # 检测模式选择
        mode_label = QLabel('检测模式:')
        self.mode_combo = QComboBox()
        self.mode_combo.addItems(['图片检测', '视频检测', '摄像头检测', '文件夹检测'])
        self.mode_combo.currentTextChanged.connect(self.on_mode_changed)
        
        # 文件选择按钮
        self.file_btn = QPushButton('选择文件')
        self.file_btn.clicked.connect(self.on_file_selected)
        
        # 开始检测按钮
        self.detect_btn = QPushButton('开始检测')
        self.detect_btn.clicked.connect(self.on_detect_clicked)
        
        # 停止检测按钮
        self.stop_btn = QPushButton('停止检测')
        self.stop_btn.clicked.connect(self.on_stop_clicked)
        self.stop_btn.setEnabled(False)
        
        # 添加控件到控制面板
        control_layout.addWidget(mode_label)
        control_layout.addWidget(self.mode_combo)
        control_layout.addWidget(self.file_btn)
        control_layout.addWidget(self.detect_btn)
        control_layout.addWidget(self.stop_btn)
        control_layout.addStretch()
        
        # 右侧显示区域
        display_panel = QWidget()
        display_layout = QVBoxLayout(display_panel)
        
        # 图像显示标签
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setMinimumSize(800, 600)
        self.image_label.setStyleSheet("border: 1px solid #cccccc;")
        
        # 新增上一张、下一张按钮
        nav_layout = QHBoxLayout()
        self.prev_btn = QPushButton('上一张')
        self.next_btn = QPushButton('下一张')
        self.prev_btn.clicked.connect(self.on_prev_clicked)
        self.next_btn.clicked.connect(self.on_next_clicked)
        self.prev_btn.setEnabled(False)
        self.next_btn.setEnabled(False)
        nav_layout.addWidget(self.prev_btn)
        nav_layout.addWidget(self.next_btn)
        
        # 统计信息显示
        self.stats_label = QLabel('检测统计:')
        self.stats_label.setStyleSheet("font-size: 14px;")
        
        display_layout.addWidget(self.image_label)
        display_layout.addLayout(nav_layout)
        display_layout.addWidget(self.stats_label)
        
        # 添加左右面板到主布局
        main_layout.addWidget(control_panel, 1)
        main_layout.addWidget(display_panel, 4)
        
    def on_mode_changed(self, mode):
        self.view_model.set_detection_mode(mode)
        if mode == '文件夹检测':
            self.file_btn.setText('选择文件夹')
            self.prev_btn.setEnabled(False)
            self.next_btn.setEnabled(False)
        else:
            self.file_btn.setText('选择文件')
            self.prev_btn.setEnabled(False)
            self.next_btn.setEnabled(False)
        self.file_btn.setEnabled(mode != '摄像头检测')
        
    def on_file_selected(self):
        mode = self.mode_combo.currentText()
        if mode == '图片检测':
            file_path, _ = QFileDialog.getOpenFileName(
                self, '选择图片', '', 'Images (*.png *.jpg *.jpeg)')
            if file_path:
                self.view_model.set_source(file_path)
        elif mode == '文件夹检测':
            folder_path = QFileDialog.getExistingDirectory(self, '选择文件夹', '')
            if folder_path:
                self.view_model.set_folder_source(folder_path)
                self.prev_btn.setEnabled(True)
                self.next_btn.setEnabled(True)
        else:
            file_path, _ = QFileDialog.getOpenFileName(
                self, '选择视频', '', 'Videos (*.mp4 *.avi)')
            if file_path:
                self.view_model.set_source(file_path)
        
    def on_detect_clicked(self):
        self.detect_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.view_model.start_detection()
        
    def on_stop_clicked(self):
        self.detect_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.view_model.stop_detection()
        
    def on_prev_clicked(self):
        self.view_model.prev_image()
    def on_next_clicked(self):
        self.view_model.next_image()
        
    def update_image(self, image):
        if isinstance(image, np.ndarray):
            # 将BGR转换为RGB
            rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            height, width, channel = rgb_image.shape
            bytes_per_line = 3 * width
            q_image = QImage(rgb_image.data.tobytes(), width, height, bytes_per_line, QImage.Format.Format_RGB888)
            pixmap = QPixmap.fromImage(q_image)
            self.image_label.setPixmap(pixmap.scaled(
                self.image_label.size(), Qt.AspectRatioMode.KeepAspectRatio))
            
    def update_stats(self, stats):
        self.stats_label.setText(f'检测统计: {stats}') 