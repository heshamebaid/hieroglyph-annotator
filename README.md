# 🏺 Hieroglyph Manual Annotator

An interactive tool for manually annotating hieroglyph symbols from temple wall images using the Gardiner classification system. Features both command-line and GUI versions for drawing bounding boxes, zooming, panning, and categorizing hieroglyph symbols.

![Python](https://img.shields.io/badge/python-v3.7+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![GUI](https://img.shields.io/badge/GUI-tkinter-orange.svg)

## 📋 Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Gardiner Classification](#gardiner-classification)
- [File Structure](#file-structure)
- [Contributing](#contributing)
- [License](#license)

## ✨ Features

### 🖥️ GUI Version (`hieroglyph_annotator_gui.py`)
- **Interactive Image Viewer**: Zoom, pan, and navigate through temple wall images
- **Bounding Box Drawing**: Click and drag to mark hieroglyph symbols
- **Searchable Category List**: Filter Gardiner categories with real-time search
- **Batch Processing**: Save multiple symbols at once to selected categories
- **Progress Tracking**: Visual progress indicator showing current image
- **Keyboard Shortcuts**: Quick navigation and control options

### 💻 Command-Line Version (`hieroglyph_annotator.py`)
- **OpenCV-based Interface**: Direct image manipulation with mouse controls
- **Zoom and Pan**: Mouse wheel zoom, Ctrl+drag to pan
- **Interactive Annotation**: Draw bounding boxes with visual feedback
- **Category Selection**: Console-based Gardiner category selection
- **Automated Workflow**: Process multiple images sequentially

## 🚀 Installation

### Prerequisites
- Python 3.7 or higher
- OpenCV (`cv2`)
- PIL/Pillow
- tkinter (usually included with Python)

### Install Dependencies
```bash
pip install opencv-python pillow numpy
```

### Clone Repository
```bash
git clone https://github.com/heshamebaid/hieroglyph-annotator.git
cd hieroglyph-annotator
```

## 📖 Usage

### GUI Versio
