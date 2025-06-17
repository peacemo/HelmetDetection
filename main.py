import sys
from PyQt6.QtWidgets import QApplication
from src.views.main_window import MainWindow
from src.viewmodels.main_viewmodel import MainViewModel

def main():
    app = QApplication(sys.argv)
    
    # 创建视图和视图模型
    view_model = MainViewModel()
    window = MainWindow()
    
    # 连接信号和槽
    window.btn_start_detection.clicked.connect(view_model.start_detection)
    window.btn_stop_detection.clicked.connect(view_model.stop_detection)
    view_model.frame_processed.connect(window.video_widget.update_frame)
    
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
