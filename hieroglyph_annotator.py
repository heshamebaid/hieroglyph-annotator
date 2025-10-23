# ============================================
# 🏺 Hieroglyph Manual Annotator with Zoom & Labeling
# ============================================
# Author: Hesham
# Description:
# Interactive tool to zoom, pan, and draw bounding boxes
# for hieroglyph symbol extraction and labeling by Gardiner category.
# ============================================

import os
import cv2
import numpy as np

# -----------------------------
# 📁 CONFIGURATION
# -----------------------------
INPUT_DIR = "temple_images"           # Folder containing temple wall images
OUTPUT_DIR = "dataset_labeled"        # Folder to save extracted symbols
SAVE_SIZE = (224, 224)                # Crop output size

# -----------------------------
# 🏷️ Gardiner’s Main Categories
# -----------------------------
GARDINER_CATEGORIES = [
    "A. Man and his occupations",
    "B. Woman and her occupations",
    "C. Anthropomorphic deities",
    "D. Parts of the human body",
    "E. Mammals",
    "F. Parts of mammals",
    "G. Birds",
    "H. Parts of birds",
    "I. Amphibious animals, reptiles, etc.",
    "K. Fish and parts of fish",
    "L. Invertebrates and lesser animals",
    "M. Trees and plants",
    "N. Sky, earth, water",
    "O. Buildings, parts of buildings, etc.",
    "P. Ships and parts of ships",
    "Q. Domestic and funerary furniture",
    "R. Temple furniture and sacred emblems",
    "S. Crowns, dress, staves, etc.",
    "T. Warfare, hunting, butchery",
    "U. Agriculture, crafts, and professions",
    "V. Rope, fiber, baskets, bags, etc.",
    "W. Vessels of stone and earthenware",
    "X. Vessels of glass and similar materials",
    "Y. Writing, games, music",
    "Z. Strokes, geometrical figures, etc.",
    "Aa. Unclassified signs",
    "Not Listed"
]
CATEGORY_CODES = [cat.split(".")[0].strip() for cat in GARDINER_CATEGORIES]
for code in CATEGORY_CODES:
    os.makedirs(os.path.join(OUTPUT_DIR, code), exist_ok=True)

# -----------------------------
# 🖱️ Interaction Globals
# -----------------------------
drawing = False
ix, iy = -1, -1
boxes = []
zoom = 1.0
offset_x, offset_y = 0, 0
drag_start = None

def update_display():
    """Show current zoomed & panned view."""
    h, w = img.shape[:2]
    center_x = int(offset_x + w / (2 * zoom))
    center_y = int(offset_y + h / (2 * zoom))
    zoom_w, zoom_h = int(w / zoom), int(h / zoom)

    x1 = max(center_x - zoom_w // 2, 0)
    y1 = max(center_y - zoom_h // 2, 0)
    x2 = min(center_x + zoom_w // 2, w)
    y2 = min(center_y + zoom_h // 2, h)

    cropped = img[y1:y2, x1:x2]
    display = cv2.resize(cropped, (w, h))
    temp = display.copy()

    # Draw bounding boxes
    for (bx, by, bw, bh) in boxes:
        cv2.rectangle(temp, (bx, by), (bx+bw, by+bh), (0, 255, 0), 2)

    cv2.imshow("Annotator", temp)

def mouse_event(event, x, y, flags, param):
    global ix, iy, drawing, boxes, drag_start, offset_x, offset_y, zoom

    h, w = img.shape[:2]

    if event == cv2.EVENT_LBUTTONDOWN:
        if flags & cv2.EVENT_FLAG_CTRLKEY:
            drag_start = (x, y)
        else:
            drawing = True
            ix, iy = x, y

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            temp = img.copy()
            for (bx, by, bw, bh) in boxes:
                cv2.rectangle(temp, (bx, by), (bx+bw, by+bh), (0, 255, 0), 2)
            cv2.rectangle(temp, (ix, iy), (x, y), (0, 0, 255), 2)
            cv2.imshow("Annotator", temp)
        elif drag_start:
            dx, dy = x - drag_start[0], y - drag_start[1]
            offset_x -= dx / zoom
            offset_y -= dy / zoom
            drag_start = (x, y)
            update_display()

    elif event == cv2.EVENT_LBUTTONUP and drawing:
        drawing = False
        x1, y1, x2, y2 = min(ix, x), min(iy, y), max(ix, x), max(iy, y)
        boxes.append((x1, y1, x2 - x1, y2 - y1))
        update_display()

    elif event == cv2.EVENT_LBUTTONUP and drag_start:
        drag_start = None

    elif event == cv2.EVENT_MOUSEWHEEL:
        zoom += 0.1 if flags > 0 else -0.1
        zoom = max(0.5, min(zoom, 3.0))
        update_display()

# -----------------------------
# 🚀 Main Annotation Loop
# -----------------------------
image_files = [f for f in os.listdir(INPUT_DIR) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
print(f"Found {len(image_files)} images in '{INPUT_DIR}'")

for img_name in image_files:
    img_path = os.path.join(INPUT_DIR, img_name)
    img = cv2.imread(img_path)
    if img is None:
        print(f"⚠️ Skipping unreadable file: {img_name}")
        continue

    boxes.clear()
    zoom, offset_x, offset_y = 1.0, 0, 0

    cv2.namedWindow("Annotator", cv2.WINDOW_NORMAL)
    cv2.setMouseCallback("Annotator", mouse_event)

    update_display()
    print(f"\n🖼️ Now labeling: {img_name}")
    print("➡️ Controls:")
    print("   🖱️ Left-drag: draw box")
    print("   🖱️ Ctrl+drag: pan view")
    print("   🖱️ Wheel: zoom in/out")
    print("   ⌨️ n: next image, r: reset boxes, q: skip image")

    while True:
        key = cv2.waitKey(0) & 0xFF
        if key == ord('n'):
            break
        elif key == ord('r'):
            boxes.clear()
            update_display()
            print("↩️ Boxes reset.")
        elif key == ord('q'):
            boxes.clear()
            break

    cv2.destroyAllWindows()

    if not boxes:
        print("⏭️ No symbols saved for this image.")
        continue

    # Label and save symbols
    for i, (x, y, w, h) in enumerate(boxes):
        crop = img[y:y+h, x:x+w]
        crop_resized = cv2.resize(crop, SAVE_SIZE)

        print("\nSelect category for this symbol:")
        for idx, cat in enumerate(GARDINER_CATEGORIES, 1):
            print(f"{idx}. {cat}")
        try:
            choice = int(input("Enter category number (default=27 Not Listed): ") or 27)
        except ValueError:
            choice = 27
        choice = max(1, min(choice, len(GARDINER_CATEGORIES)))
        cat_code = CATEGORY_CODES[choice - 1]

        save_name = f"{os.path.splitext(img_name)[0]}_symbol_{i:03d}.png"
        save_path = os.path.join(OUTPUT_DIR, cat_code, save_name)
        cv2.imwrite(save_path, crop_resized)
        print(f"✅ Saved: {save_path}")

print("\n✅ Manual annotation completed successfully!")
