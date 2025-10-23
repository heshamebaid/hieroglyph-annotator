# 🏺 Hieroglyph Manual Annotator

Interactive tool for annotating hieroglyph symbols from temple wall images using Gardiner classification.

## 🚀 Quick Start

### Install Dependencies
```bash
pip install opencv-python pillow numpy
```

### Run GUI Version (Recommended)
```bash
python hieroglyph_annotator_gui.py
```

### Run Command-Line Version
```bash
python hieroglyph_annotator.py
```

## 📖 How to Use

### GUI Version
1. **Load Images**: Place temple images in `Temple_Images/` folder
2. **Draw Boxes**: Click and drag to mark hieroglyph symbols
3. **Select Category**: Click from the Gardiner category list
4. **Save**: Click "Save Symbol" to save all boxes
5. **Navigate**: Use "Next/Previous" buttons

**Controls:**
- Mouse: Draw bounding boxes
- Mouse Wheel: Zoom in/out
- Search: Filter categories
- `N`: Next image, `P`: Previous, `S`: Save

### Command-Line Version
1. **Draw**: Left-drag to create boxes
2. **Pan**: Ctrl+drag to move view
3. **Zoom**: Mouse wheel
4. **Navigate**: Press `n` for next image
5. **Select**: Choose category number when prompted

## 🏷️ Gardiner Categories

| Code | Category |
|------|----------|
| A | Man and his occupations |
| B | Woman and her occupations |
| C | Anthropomorphic deities |
| D | Parts of the human body |
| E | Mammals |
| F | Parts of mammals |
| G | Birds |
| H | Parts of birds |
| I | Amphibious animals, reptiles |
| K | Fish and parts of fish |
| L | Invertebrates and lesser animals |
| M | Trees and plants |
| N | Sky, earth, water |
| O | Buildings, parts of buildings |
| P | Ships and parts of ships |
| Q | Domestic and funerary furniture |
| R | Temple furniture and sacred emblems |
| S | Crowns, dress, staves |
| T | Warfare, hunting, butchery |
| U | Agriculture, crafts, professions |
| V | Rope, fiber, baskets, bags |
| W | Vessels of stone and earthenware |
| X | Vessels of glass |
| Y | Writing, games, music |
| Z | Strokes, geometrical figures |
| Aa | Unclassified signs |

## 📁 File Structure
