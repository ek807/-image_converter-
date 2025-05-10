# -image_converter-
一款基于Python和PyQt6开发的图形界面工具，支持多种图片格式之间的相互转换，包括： - JPG/JPEG - PNG - BMP - GIF - TIFF - WEBP - ICO


# 图片格式转换器


## 功能简介

一款基于Python和PyQt6开发的图形界面工具，支持多种图片格式之间的相互转换，包括：
- JPG/JPEG
- PNG
- BMP
- GIF
- TIFF
- WEBP
- ICO

## 特色功能

✔ 简洁直观的用户界面  
✔ 实时预览转换效果  
✔ 批量转换支持（拖放操作）  
✔ 高质量格式转换  
✔ 自定义输出参数（质量/分辨率）  

## 安装指南

### 通过可执行文件（推荐）

1. 从[Release页面]下载最新版
2. 解压ZIP文件
3. 双击运行 `ImageConverter.exe`

### 通过源代码运行

```bash
# 克隆仓库

# 运行程序
python image_converter.py
```

## 使用说明

1. 点击"选择图片"按钮或拖放图片到窗口
2. 从下拉菜单选择目标格式
3. 点击"转换并保存"按钮
4. 选择输出位置（默认保存在原文件同目录）

## 技术栈

- Python 3.10+
- PyQt6 (GUI框架)
- Pillow (图像处理)
- PyInstaller (打包工具)

## 构建指南

```bash
# 安装依赖
pip install pyinstaller pillow pyqt6

# 打包为单文件exe
pyinstaller --onefile --windowed --icon=appicon.ico image_converter.py
```

## 常见问题

Q: 转换后图片质量下降怎么办？  
A: 程序默认使用85%质量保存，如需调整请修改代码中的`quality`参数

Q: 如何支持更多图片格式？  
A: 在代码的`SUPPORTED_FORMATS`集合中添加新格式（需Pillow支持）

Q: 杀毒软件误报怎么办？  
A: 这是PyInstaller打包的常见问题，可[提交文件到病毒检测](https://www.virustotal.com/)验证安全性

## 贡献指南

欢迎提交Pull Request！请确保：
1. 遵循现有代码风格
2. 提交前运行测试
3. 更新文档说明

## 开源协议

本项目采用 [AGPL-3.0 License](LICENSE)

## 联系方式

开发者：林治宏  
邮箱：lzh437951@gmail.com  
项目主页：(https://github.com/ek807/-image_converter-)
```
