import sys
import os
from pathlib import Path
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QComboBox,
    QVBoxLayout, QHBoxLayout, QFileDialog, QMessageBox
)
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtCore import Qt
from PIL import Image
import traceback


class ImageConverter(QWidget):
    SUPPORTED_FORMATS = {'JPG', 'PNG', 'BMP', 'GIF', 'TIFF', 'WEBP', 'ICO'}
    PREVIEW_SIZE = (400, 300)
    WINDOW_SIZE = (600, 500)

    def __init__(self):
        super().__init__()
        self.image_path: Path | None = None

        # 在 ImageConverter 类的 setup_window 方法中修改图标设置
        def setup_window(self):
            """Configure window properties"""
            self.setWindowTitle("图片格式转换器")
            # 修改为使用本地图标文件（确保有appicon.ico文件）
            self.setWindowIcon(QIcon("appicon.ico"))
            self.setFixedSize(*self.WINDOW_SIZE)

        self.init_ui()

    def setup_window(self):
        """Configure window properties"""
        self.setWindowTitle("图片格式转换器")
        self.setWindowIcon(QIcon(":/icons/image.ico"))
        self.setFixedSize(*self.WINDOW_SIZE)
        self.setStyleSheet("""
            QWidget {
                background: #f5f5f5;
                font-family: Arial;
            }
            QLabel {
                color: #333333;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QComboBox {
                padding: 5px;
                border: 1px solid #ddd;
                border-radius: 4px;
            }
        """)

    def init_ui(self):
        """Initialize user interface components"""
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        # Title
        title_label = QLabel("图片格式转换器")
        title_label.setStyleSheet("font-size: 20px; font-weight: bold;")
        main_layout.addWidget(title_label, alignment=Qt.AlignmentFlag.AlignCenter)

        # Image preview area
        self.preview_label = QLabel("请选择一张图片")
        self.preview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.preview_label.setFixedSize(*self.PREVIEW_SIZE)
        self.preview_label.setStyleSheet("""
            background-color: white;
            border: 2px dashed #ccc;
            border-radius: 5px;
            color: #999;
        """)
        main_layout.addWidget(self.preview_label)

        # Button and format selection
        control_layout = QHBoxLayout()

        # Select button
        self.choose_button = QPushButton("选择图片")
        self.choose_button.setFixedWidth(120)
        self.choose_button.clicked.connect(self.choose_image)
        control_layout.addWidget(self.choose_button)

        # Format selection
        format_layout = QHBoxLayout()
        format_label = QLabel("目标格式：")
        self.format_combo = QComboBox()
        self.format_combo.addItems(sorted(self.SUPPORTED_FORMATS))
        self.format_combo.setCurrentText("BMP")  # Default to BMP as shown in image
        self.format_combo.setFixedWidth(100)
        format_layout.addWidget(format_label)
        format_layout.addWidget(self.format_combo)
        control_layout.addLayout(format_layout)

        # Convert button
        self.convert_button = QPushButton("转换并保存")
        self.convert_button.setFixedWidth(120)
        self.convert_button.clicked.connect(self.convert_image)
        control_layout.addWidget(self.convert_button)

        main_layout.addLayout(control_layout)

        # Status message
        self.status_label = QLabel()
        self.status_label.setStyleSheet("color: #666; font-size: 12px;")
        self.status_label.setWordWrap(True)
        main_layout.addWidget(self.status_label)

        # Add stretch to push content up
        main_layout.addStretch()

        # Footer info
        footer_label = QLabel("作者: 林治宏 | 协议: AGPL")
        footer_label.setStyleSheet("color: #999; font-size: 15px;")
        footer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(footer_label)

        self.setLayout(main_layout)

    def choose_image(self):
        """Handle image selection and preview"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "选择图片",
            "",
            "图像文件 (*.jpg *.jpeg *.png *.bmp *.gif *.tiff *.webp *.ico)"
        )
        if not file_path:
            return

        try:
            self.image_path = Path(file_path)
            pixmap = QPixmap(file_path).scaled(
                *self.PREVIEW_SIZE,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            self.preview_label.setPixmap(pixmap)
            self.preview_label.setText("")
            self.status_label.setText(f"已选择：{self.image_path.name}")
            self.status_label.setStyleSheet("color: #4CAF50;")
        except Exception as e:
            self.show_error(f"无法加载图片：{e}")
            self.image_path = None
            self.preview_label.setPixmap(QPixmap())
            self.preview_label.setText("请选择一张图片")

    def convert_image(self):
        """Handle image conversion and saving"""
        if not self.image_path:
            self.show_warning("请先选择一张图片！")
            return

        target_format = self.format_combo.currentText().lower()
        try:
            with Image.open(self.image_path) as img:
                target_mode = 'RGBA' if target_format in {'png', 'webp', 'gif'} else 'RGB'
                if img.mode != target_mode:
                    img = img.convert(target_mode)

                output_path = self.image_path.with_stem(f"{self.image_path.stem}_converted")
                output_path = output_path.with_suffix(f".{target_format}")
                output_path.parent.mkdir(parents=True, exist_ok=True)

                pillow_format = 'JPEG' if target_format == 'jpg' else target_format.upper()
                save_options = {'quality': 85, 'optimize': True} if target_format == 'jpg' else {}
                img.save(output_path, pillow_format, **save_options)

            self.status_label.setText(f"转换成功！已保存为：{output_path.name}")
            self.status_label.setStyleSheet("color: #4CAF50;")
            QMessageBox.information(self, "成功", f"图片已保存为：{output_path}")

        except Exception as e:
            self.show_error(f"转换失败：{str(e)}")
            print(traceback.format_exc())

    def show_error(self, message: str):
        """Show error message"""
        self.status_label.setText(message)
        self.status_label.setStyleSheet("color: #f44336;")
        QMessageBox.critical(self, "错误", message)

    def show_warning(self, message: str):
        """Show warning message"""
        self.status_label.setText(message)
        self.status_label.setStyleSheet("color: #ff9800;")
        QMessageBox.warning(self, "警告", message)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = ImageConverter()
    window.show()
    sys.exit(app.exec())