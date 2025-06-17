# YOLO安全帽检测系统

基于YOLOv8和PyQt6的安全帽检测系统，采用MVVM架构设计。

## 功能特点

- 实时视频流安全帽检测
- 图片安全帽检测
- 检测结果可视化
- 支持多种检测模式（图片/视频/摄像头）
- 检测结果统计和导出

## 安装说明

1. 创建虚拟环境：
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

## 使用说明

1. 运行主程序：
```bash
python src/main.py
```

2. 选择检测模式（图片/视频/摄像头）
3. 开始检测
4. 查看检测结果和统计信息

## 项目结构

- `src/models/`: YOLO模型相关代码
- `src/views/`: PyQt6 GUI视图
- `src/viewmodels/`: MVVM架构中的ViewModel
- `src/utils/`: 工具函数
- `src/resources/`: 资源文件
- `tests/`: 单元测试

## 许可证

本项目采用 GNU Affero General Public License v3.0 (AGPL-3.0) 许可证。

### 许可证说明

AGPL-3.0 是一个强copyleft许可证，要求：
1. 任何使用、修改或分发本项目的代码都必须开源
2. 如果通过网络提供服务，必须提供源代码
3. 必须保留原始版权声明和许可证

### 依赖项许可证

- PyQt6: LGPL v3
- PyTorch: BSD License
- OpenCV: Apache 2.0
- YOLOv8: AGPL-3.0
- NumPy: BSD License
- Pillow: HPND License

## 贡献

欢迎提交 Issue 和 Pull Request 来改进这个项目。 