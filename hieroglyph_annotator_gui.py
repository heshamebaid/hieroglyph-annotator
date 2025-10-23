# ============================================
# 🏺 Hieroglyph Manual Annotator - GUI Version
# ============================================
# Author: Hesham
# Description:
# Interactive GUI tool to zoom, pan, and draw bounding boxes
# for hieroglyph symbol extraction and labeling by Gardiner category.
# ============================================

import os
import cv2
import numpy as np
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
import threading

class HieroglyphAnnotatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🏺 Hieroglyph Manual Annotator")
        self.root.geometry("1400x900")
        self.root.configure(bg='#2b2b2b')
        
        # Configuration
        self.INPUT_DIR = "Temple_Images"  # Updated to match your folder
        self.OUTPUT_DIR = "dataset_labeled"
        self.SAVE_SIZE = (224, 224)
        
        # Gardiner Categories
        self.GARDINER_CATEGORIES = [
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
        
        self.CATEGORY_CODES = [cat.split(".")[0].strip() for cat in self.GARDINER_CATEGORIES]
        
        # Create output directories
        for code in self.CATEGORY_CODES:
            os.makedirs(os.path.join(self.OUTPUT_DIR, code), exist_ok=True)
        
        # State variables
        self.current_image = None
        self.current_image_path = None
        self.image_files = []
        self.current_image_index = 0
        self.boxes = []
        self.zoom = 1.0
        self.offset_x = 0
        self.offset_y = 0
        self.drawing = False
        self.start_x = 0
        self.start_y = 0
        self.current_box = None
        
        self.setup_gui()
        self.load_images()
        
    def setup_gui(self):
        """Setup the GUI layout"""
        # Main frame
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left panel - Image viewer
        left_frame = ttk.Frame(main_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Image canvas with scrollbars
        canvas_frame = ttk.Frame(left_frame)
        canvas_frame.pack(fill=tk.BOTH, expand=True)
        
        self.image_canvas = tk.Canvas(canvas_frame, bg='#1e1e1e', highlightthickness=0)
        self.image_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(canvas_frame, orient=tk.VERTICAL, command=self.image_canvas.yview)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.image_canvas.configure(yscrollcommand=v_scrollbar.set)
        
        h_scrollbar = ttk.Scrollbar(left_frame, orient=tk.HORIZONTAL, command=self.image_canvas.xview)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.image_canvas.configure(xscrollcommand=h_scrollbar.set)
        
        # Image controls
        controls_frame = ttk.Frame(left_frame)
        controls_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(controls_frame, text="🔍 Zoom In", command=self.zoom_in).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(controls_frame, text="🔍 Zoom Out", command=self.zoom_out).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(controls_frame, text="🔄 Reset View", command=self.reset_view).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(controls_frame, text="🗑️ Clear Boxes", command=self.clear_boxes).pack(side=tk.LEFT, padx=(0, 5))
        
        # Right panel - Symbol list and controls
        right_frame = ttk.Frame(main_frame, width=400)
        right_frame.pack(side=tk.RIGHT, fill=tk.Y)
        right_frame.pack_propagate(False)
        
        # Image info
        info_frame = ttk.LabelFrame(right_frame, text="📷 Current Image", padding=10)
        info_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.image_info_label = ttk.Label(info_frame, text="No image loaded")
        self.image_info_label.pack()
        
        self.progress_label = ttk.Label(info_frame, text="")
        self.progress_label.pack()
        
        # Symbol list
        symbol_frame = ttk.LabelFrame(right_frame, text="🏷️ Gardiner Categories", padding=10)
        symbol_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Search box
        search_frame = ttk.Frame(symbol_frame)
        search_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(search_frame, text="🔍 Search:").pack(side=tk.LEFT)
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self.filter_categories)
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var)
        search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 0))
        
        # Category listbox with scrollbar
        listbox_frame = ttk.Frame(symbol_frame)
        listbox_frame.pack(fill=tk.BOTH, expand=True)
        
        self.category_listbox = tk.Listbox(listbox_frame, height=15, font=('Arial', 10))
        self.category_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        listbox_scrollbar = ttk.Scrollbar(listbox_frame, orient=tk.VERTICAL, command=self.category_listbox.yview)
        listbox_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.category_listbox.configure(yscrollcommand=listbox_scrollbar.set)
        
        # Populate category list
        self.populate_categories()
        
        # Selected category display
        selected_frame = ttk.Frame(symbol_frame)
        selected_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Label(selected_frame, text="Selected:").pack(side=tk.LEFT)
        self.selected_category_label = ttk.Label(selected_frame, text="None", foreground='#4CAF50')
        self.selected_category_label.pack(side=tk.LEFT, padx=(5, 0))
        
        # Action buttons
        action_frame = ttk.LabelFrame(right_frame, text="⚡ Actions", padding=10)
        action_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(action_frame, text="💾 Save Symbol", command=self.save_current_symbol).pack(fill=tk.X, pady=(0, 5))
        ttk.Button(action_frame, text="➡️ Next Image", command=self.next_image).pack(fill=tk.X, pady=(0, 5))
        ttk.Button(action_frame, text="⬅️ Previous Image", command=self.previous_image).pack(fill=tk.X, pady=(0, 5))
        ttk.Button(action_frame, text="📁 Open Folder", command=self.open_output_folder).pack(fill=tk.X)
        
        # Bind events
        self.image_canvas.bind("<Button-1>", self.on_canvas_click)
        self.image_canvas.bind("<B1-Motion>", self.on_canvas_drag)
        self.image_canvas.bind("<ButtonRelease-1>", self.on_canvas_release)
        self.image_canvas.bind("<MouseWheel>", self.on_canvas_scroll)
        self.image_canvas.bind("<Button-4>", self.on_canvas_scroll)  # Linux
        self.image_canvas.bind("<Button-5>", self.on_canvas_scroll)  # Linux
        
        self.category_listbox.bind("<<ListboxSelect>>", self.on_category_select)
        
        # Keyboard shortcuts
        self.root.bind("<Key>", self.on_key_press)
        self.root.focus_set()
        
    def populate_categories(self):
        """Populate the category listbox"""
        self.category_listbox.delete(0, tk.END)
        for i, category in enumerate(self.GARDINER_CATEGORIES):
            self.category_listbox.insert(tk.END, f"{i+1:2d}. {category}")
    
    def filter_categories(self, *args):
        """Filter categories based on search text"""
        search_text = self.search_var.get().lower()
        self.category_listbox.delete(0, tk.END)
        
        for i, category in enumerate(self.GARDINER_CATEGORIES):
            if search_text in category.lower():
                self.category_listbox.insert(tk.END, f"{i+1:2d}. {category}")
    
    def on_category_select(self, event):
        """Handle category selection"""
        selection = self.category_listbox.curselection()
        if selection:
            index = selection[0]
            # Get the actual category index from the filtered list
            search_text = self.search_var.get().lower()
            filtered_categories = [cat for cat in self.GARDINER_CATEGORIES if search_text in cat.lower()]
            if index < len(filtered_categories):
                selected_category = filtered_categories[index]
                self.selected_category_label.config(text=selected_category)
    
    def load_images(self):
        """Load image files from input directory"""
        if not os.path.exists(self.INPUT_DIR):
            messagebox.showerror("Error", f"Input directory '{self.INPUT_DIR}' not found!")
            return
            
        self.image_files = [f for f in os.listdir(self.INPUT_DIR) 
                           if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        
        if not self.image_files:
            messagebox.showwarning("Warning", f"No images found in '{self.INPUT_DIR}'!")
            return
            
        self.current_image_index = 0
        self.load_current_image()
    
    def load_current_image(self):
        """Load the current image"""
        if not self.image_files:
            return
            
        image_path = os.path.join(self.INPUT_DIR, self.image_files[self.current_image_index])
        self.current_image_path = image_path
        
        # Load image with OpenCV
        img = cv2.imread(image_path)
        if img is None:
            messagebox.showerror("Error", f"Could not load image: {image_path}")
            return
            
        # Convert BGR to RGB
        self.current_image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        # Update UI
        self.update_image_info()
        self.reset_view()
        self.clear_boxes()
        self.display_image()
    
    def update_image_info(self):
        """Update image information display"""
        if self.current_image is not None:
            filename = os.path.basename(self.current_image_path)
            progress = f"{self.current_image_index + 1} / {len(self.image_files)}"
            self.image_info_label.config(text=filename)
            self.progress_label.config(text=progress)
    
    def display_image(self):
        """Display the current image on canvas"""
        if self.current_image is None:
            return
            
        # Calculate display area
        canvas_width = self.image_canvas.winfo_width()
        canvas_height = self.image_canvas.winfo_height()
        
        if canvas_width <= 1 or canvas_height <= 1:
            # Canvas not ready, schedule for later
            self.root.after(100, self.display_image)
            return
        
        # Apply zoom and offset
        h, w = self.current_image.shape[:2]
        center_x = int(self.offset_x + w / (2 * self.zoom))
        center_y = int(self.offset_y + h / (2 * self.zoom))
        zoom_w, zoom_h = int(w / self.zoom), int(h / self.zoom)
        
        x1 = max(center_x - zoom_w // 2, 0)
        y1 = max(center_y - zoom_h // 2, 0)
        x2 = min(center_x + zoom_w // 2, w)
        y2 = min(center_y + zoom_h // 2, h)
        
        # Crop and resize
        cropped = self.current_image[y1:y2, x1:x2]
        display_img = Image.fromarray(cropped)
        display_img = display_img.resize((canvas_width, canvas_height), Image.Resampling.LANCZOS)
        
        # Convert to PhotoImage
        self.photo = ImageTk.PhotoImage(display_img)
        
        # Clear canvas and display image
        self.image_canvas.delete("all")
        self.image_canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)
        
        # Draw bounding boxes
        self.draw_boxes()
    
    def draw_boxes(self):
        """Draw all bounding boxes on the canvas"""
        if not self.boxes:
            return
            
        canvas_width = self.image_canvas.winfo_width()
        canvas_height = self.image_canvas.winfo_height()
        
        for i, (x, y, w, h) in enumerate(self.boxes):
            # Convert image coordinates to canvas coordinates
            canvas_x1 = int((x - self.offset_x) * self.zoom)
            canvas_y1 = int((y - self.offset_y) * self.zoom)
            canvas_x2 = int((x + w - self.offset_x) * self.zoom)
            canvas_y2 = int((y + h - self.offset_y) * self.zoom)
            
            # Only draw if box is visible
            if (canvas_x2 > 0 and canvas_x1 < canvas_width and 
                canvas_y2 > 0 and canvas_y1 < canvas_height):
                
                self.image_canvas.create_rectangle(
                    canvas_x1, canvas_y1, canvas_x2, canvas_y2,
                    outline='#00FF00', width=2, tags=f"box_{i}"
                )
                # Add box number
                self.image_canvas.create_text(
                    canvas_x1 + 5, canvas_y1 + 5,
                    text=str(i+1), fill='#00FF00', font=('Arial', 12, 'bold'),
                    tags=f"box_text_{i}"
                )
    
    def on_canvas_click(self, event):
        """Handle canvas click"""
        self.start_x = event.x
        self.start_y = event.y
        self.drawing = True
    
    def on_canvas_drag(self, event):
        """Handle canvas drag"""
        if self.drawing:
            # Clear previous temporary box
            self.image_canvas.delete("temp_box")
            
            # Draw temporary box
            self.image_canvas.create_rectangle(
                self.start_x, self.start_y, event.x, event.y,
                outline='#FF0000', width=2, tags="temp_box"
            )
    
    def on_canvas_release(self, event):
        """Handle canvas release"""
        if self.drawing:
            self.drawing = False
            
            # Clear temporary box
            self.image_canvas.delete("temp_box")
            
            # Convert canvas coordinates to image coordinates
            img_x1 = int(self.start_x / self.zoom + self.offset_x)
            img_y1 = int(self.start_y / self.zoom + self.offset_y)
            img_x2 = int(event.x / self.zoom + self.offset_x)
            img_y2 = int(event.y / self.zoom + self.offset_y)
            
            # Ensure valid coordinates
            x1, y1 = min(img_x1, img_x2), min(img_y1, img_y2)
            x2, y2 = max(img_x1, img_x2), max(img_y1, img_y2)
            
            # Add box if it has reasonable size
            if abs(x2 - x1) > 10 and abs(y2 - y1) > 10:
                self.boxes.append((x1, y1, x2 - x1, y2 - y1))
                self.display_image()
    
    def on_canvas_scroll(self, event):
        """Handle canvas scroll for zooming"""
        if event.delta > 0 or event.num == 4:  # Zoom in
            self.zoom *= 1.1
        else:  # Zoom out
            self.zoom /= 1.1
            
        self.zoom = max(0.5, min(self.zoom, 5.0))
        self.display_image()
    
    def zoom_in(self):
        """Zoom in"""
        self.zoom *= 1.2
        self.zoom = min(self.zoom, 5.0)
        self.display_image()
    
    def zoom_out(self):
        """Zoom out"""
        self.zoom /= 1.2
        self.zoom = max(self.zoom, 0.5)
        self.display_image()
    
    def reset_view(self):
        """Reset zoom and pan"""
        self.zoom = 1.0
        self.offset_x = 0
        self.offset_y = 0
        self.display_image()
    
    def clear_boxes(self):
        """Clear all bounding boxes"""
        self.boxes.clear()
        self.display_image()
    
    def on_key_press(self, event):
        """Handle keyboard shortcuts"""
        if event.keysym == 'n':
            self.next_image()
        elif event.keysym == 'p':
            self.previous_image()
        elif event.keysym == 'r':
            self.reset_view()
        elif event.keysym == 'c':
            self.clear_boxes()
        elif event.keysym == 's':
            self.save_current_symbol()
    
    def save_current_symbol(self):
        """Save the currently selected symbol"""
        if not self.boxes:
            messagebox.showwarning("Warning", "No bounding boxes to save!")
            return
            
        # Get selected category
        selection = self.category_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a category first!")
            return
            
        # Get the actual category index
        search_text = self.search_var.get().lower()
        filtered_categories = [cat for cat in self.GARDINER_CATEGORIES if search_text in cat.lower()]
        if selection[0] >= len(filtered_categories):
            messagebox.showwarning("Warning", "Invalid category selection!")
            return
            
        selected_category = filtered_categories[selection[0]]
        category_code = selected_category.split(".")[0].strip()
        
        # Save all boxes
        saved_count = 0
        for i, (x, y, w, h) in enumerate(self.boxes):
            # Extract symbol
            symbol_crop = self.current_image[y:y+h, x:x+w]
            
            # Resize to standard size
            symbol_img = Image.fromarray(symbol_crop)
            symbol_img = symbol_img.resize(self.SAVE_SIZE, Image.Resampling.LANCZOS)
            
            # Save
            filename = f"{os.path.splitext(self.image_files[self.current_image_index])[0]}_symbol_{i:03d}.png"
            save_path = os.path.join(self.OUTPUT_DIR, category_code, filename)
            symbol_img.save(save_path)
            saved_count += 1
        
        messagebox.showinfo("Success", f"Saved {saved_count} symbol(s) to category '{selected_category}'")
        self.clear_boxes()
    
    def next_image(self):
        """Go to next image"""
        if self.current_image_index < len(self.image_files) - 1:
            self.current_image_index += 1
            self.load_current_image()
        else:
            messagebox.showinfo("Info", "This is the last image!")
    
    def previous_image(self):
        """Go to previous image"""
        if self.current_image_index > 0:
            self.current_image_index -= 1
            self.load_current_image()
        else:
            messagebox.showinfo("Info", "This is the first image!")
    
    def open_output_folder(self):
        """Open the output folder in file explorer"""
        if os.path.exists(self.OUTPUT_DIR):
            os.startfile(self.OUTPUT_DIR)
        else:
            messagebox.showwarning("Warning", "Output directory does not exist!")

def main():
    root = tk.Tk()
    app = HieroglyphAnnotatorGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
