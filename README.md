# 🏺 Hieroglyph Manual Annotator

Interactive tool for annotating hieroglyph symbols from temple wall images using the complete Gardiner classification system with 700+ symbols and descriptions.

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
3. **Select Symbol**: Choose from 700+ symbols with descriptions
4. **View Details**: See symbol name and description in dedicated display
5. **Save**: Click "Save Symbol" to save all boxes
6. **Navigate**: Use "Next/Previous" buttons or keyboard shortcuts

**Enhanced Features:**
- **Complete Symbol Database**: 700+ hieroglyph symbols with Gardiner descriptions
- **Smart Search**: Filter by symbol code (A1) or description (seated man)
- **Symbol Information**: Dedicated display showing symbol name and description
- **Visual Organization**: Clear categorization with proper labels

**Controls:**
- **Mouse**: Draw bounding boxes, right-drag to pan
- **Mouse Wheel**: Zoom in/out
- **Arrow Keys**: Pan image (← → ↑ ↓)
- **Keyboard**: `N`/`P` (next/previous), `S` (save), `R` (reset), `C` (clear)
- **Search**: Real-time filtering of symbol list

### Command-Line Version
1. **Draw**: Left-drag to create boxes
2. **Pan**: Ctrl+drag to move view
3. **Zoom**: Mouse wheel
4. **Navigate**: Press `n` for next image
5. **Select**: Choose category number when prompted

## 🏷️ Complete Gardiner Symbol Database

The tool includes the complete Gardiner classification system with **700+ symbols** and their descriptions:

| Code | Category | Examples |
|------|----------|----------|
| **A** | Man and his occupations | A1 (Seated man), A2 (Man with hand to mouth), A3 (Man sitting on heel) |
| **Aa** | Unclassified signs | Aa1 (Placenta?), Aa2 (Pustule or gland?), Aa3 (Aa2 with substance issuing) |
| **B** | Woman and her occupations | B1 (Seated Woman), B2 (Pregnant woman), B3 (Woman giving birth) |
| **C** | Anthropomorphic deities | C1 (God with sun-disk and uraeus), C2 (God with falcon head), C3 (God with ibis head) |
| **D** | Parts of the human body | D1 (Head), D4 (Eye), D21 (Mouth), D36 (Arm), D54 (Legs walking) |
| **E** | Mammals | E1 (Bull), E13 (Cat), E14 (Dog), E22 (Lion), E25 (Hippopotamus) |
| **F** | Parts of mammals | F1 (Head of ox), F18 (Tusk of elephant), F34 (Heart), F46 (Intestine) |
| **G** | Birds | G1 (Vulture), G5 (Falcon), G17 (Owl), G25 (Crested Ibis), G43 (Quail chick) |
| **H** | Parts of birds | H1 (Head of duck), H5 (Wing), H6 (Feather), H8 (Egg) |
| **I** | Amphibious animals, reptiles | I1 (Lizard), I3 (Crocodile), I7 (Frog), I9 (Horned viper), I10 (Cobra) |
| **K** | Fish and parts of fish | K1 (Bulti fish), K4 (Oxyrhynchus fish), K6 (Fish scale) |
| **L** | Invertebrates and lesser animals | L1 (Scarab beetle), L2 (Bee), L7 (Scorpion) |
| **M** | Trees and plants | M1 (Tree), M13 (Papyrus stem), M23 (Sedge), M33 (Grain) |
| **N** | Sky, earth, water | N1 (Sky), N5 (Sun), N9 (Moon), N14 (Star), N35 (Water ripple) |
| **O** | Buildings, parts of buildings | O1 (House plan), O25 (Obelisk), O31 (Door), O40 (Stairway) |
| **P** | Ships and parts of ships | P1 (Boat on water), P3 (Sacred bark), P6 (Mast), P8 (Oar) |
| **Q** | Domestic and funerary furniture | Q1 (Seat), Q3 (Stool), Q4 (Headrest), Q7 (Brazier with flame) |
| **R** | Temple furniture and sacred emblems | R1 (Table with jug and loaves), R8 (Flag), R12 (Standard) |
| **S** | Crowns, dress, staves | S1 (White crown of Upper Egypt), S3 (Red crown of Lower Egypt), S38 (Crook) |
| **T** | Warfare, hunting, butchery | T1 (Angular headed mace), T3 (Pear shaped mace), T9 (Bow), T30 (Knife) |
| **U** | Agriculture, crafts, professions | U1 (Sickle), U6 (Hoe), U13 (Plow), U19 (Adze), U28 (Fire drill) |
| **V** | Rope, fiber, baskets, bags | V1 (Rope coil), V10 (Oval cartouche), V30 (Basket), V33 (Linen bag) |
| **W** | Vessels of stone and earthenware | W1 (Oil jar), W6 (Vessel), W14 (Tall jar), W24 (Bowl) |
| **X** | Vessels of glass and similar materials | X1 (Small bread loaf), X2 (Tall bread loaf), X8 (Conical Loaf) |
| **Y** | Writing, games, music | Y1 (Papyrus scroll), Y5 (Game board), Y7 (Harp), Y8 (Sistrum) |
| **Z** | Strokes, geometrical figures | Z1 (Stroke), Z2 (Triple stroke), Z9 (Crossed sticks) |

### 🔍 **Smart Search Features**
- Search by **symbol code**: Type "A1" to find "Seated man"
- Search by **description**: Type "seated" to find all seated figures
- **Real-time filtering**: Results update as you type
- **Case-insensitive**: Works with any capitalization

## 📁 File Structure

```
hieroglyph-annotator/
├── hieroglyph_annotator.py      # Command-line version
├── hieroglyph_annotator_gui.py  # GUI version
├── Temple_Images/               # Put your images here
└── dataset_labeled/             # Output folder (auto-created)
    ├── A/                       # Category A symbols
    ├── B/                       # Category B symbols
    └── ...                      # Other categories
```

## 🎯 What It Does

- **Input**: Temple wall images with hieroglyphs
- **Process**: Draw boxes around symbols, select from 700+ Gardiner symbols with descriptions
- **Output**: Cropped 224x224 symbol images organized by category with proper naming

## ✨ Key Features

- **📚 Complete Database**: 700+ hieroglyph symbols with official Gardiner descriptions
- **🔍 Smart Search**: Find symbols by code or description
- **📋 Symbol Information**: Dedicated display showing symbol name and description
- **🎨 Enhanced GUI**: Professional interface with clear organization
- **⌨️ Keyboard Shortcuts**: Efficient navigation and control
- **🖱️ Advanced Controls**: Pan, zoom, and precise box drawing
- **💾 Organized Output**: Automatically creates category folders and saves with proper naming

## 📞 Contact

**Hesham Ebaid** - [@heshamebaid](https://github.com/heshamebaid)

Project: [https://github.com/heshamebaid/hieroglyph-annotator](https://github.com/heshamebaid/hieroglyph-annotator)
