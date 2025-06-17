import sys
from PyQt6.QtWidgets import QApplication
from views.main_window import MainWindow
from viewmodels.main_viewmodel import MainViewModel

def main():
    app = QApplication(sys.argv)
    
    # 创建ViewModel和View
    view_model = MainViewModel()
    window = MainWindow(view_model)
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main() 