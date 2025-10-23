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

### GUI Version (Recommended)
```bash
python hieroglyph_annotator_gui.py
```

**Controls:**
- **Mouse**: Click and drag to draw bounding boxes
- **Mouse Wheel**: Zoom in/out
- **Search Box**: Filter Gardiner categories
- **Category List**: Click to select classification
- **Save Button**: Save all boxes to selected category

**Keyboard Shortcuts:**
- `N` - Next image
- `P` - Previous image
- `R` - Reset view
- `C` - Clear boxes
- `S` - Save current symbol

### Command-Line Version
```bash
python hieroglyph_annotator.py
```

**Controls:**
- **Left-drag**: Draw bounding box
- **Ctrl+drag**: Pan view
- **Mouse wheel**: Zoom in/out
- **n**: Next image
- **r**: Reset boxes
- **q**: Skip image

## 🏷️ Gardiner Classification

The tool uses Gardiner's sign list, the standard classification system for Egyptian hieroglyphs:

| Category | Description |
|----------|-------------|
| A | Man and his occupations |
| B | Woman and her occupations |
| C | Anthropomorphic deities |
| D | Parts of the human body |
| E | Mammals |
| F | Parts of mammals |
| G | Birds |
| H | Parts of birds |
| I | Amphibious animals, reptiles, etc. |
| K | Fish and parts of fish |
| L | Invertebrates and lesser animals |
| M | Trees and plants |
| N | Sky, earth, water |
| O | Buildings, parts of buildings, etc. |
| P | Ships and parts of ships |
| Q | Domestic and funerary furniture |
| R | Temple furniture and sacred emblems |
| S | Crowns, dress, staves, etc. |
| T | Warfare, hunting, butchery |
| U | Agriculture, crafts, and professions |
| V | Rope, fiber, baskets, bags, etc. |
| W | Vessels of stone and earthenware |
| X | Vessels of glass and similar materials |
| Y | Writing, games, music |
| Z | Strokes, geometrical figures, etc. |
| Aa | Unclassified signs |

## 📁 File Structure
