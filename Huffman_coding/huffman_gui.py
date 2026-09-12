"""Tkinter interface for manual Huffman image coding."""

from __future__ import annotations
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
from huffman_coding import process

FILE_TYPES = [("Image files", "*.png *.jpg *.jpeg *.bmp *.tiff *.webp"), ("All files", "*.*")]


class HuffmanApp(tk.Tk):
    def __init__(self):
        super().__init__(); self.title("Huffman Coding — Digital Image Processing"); self.geometry("1100x760"); self.minsize(760, 560)
        self.project = Path(__file__).resolve().parent; self.selected: Path | None = None; self.photos: list[ImageTk.PhotoImage] = []; self.status = tk.StringVar(value="Choose an image to begin.")
        controls = ttk.Frame(self, padding=12); controls.pack(fill="x")
        ttk.Button(controls, text="Choose Image", command=self.choose).pack(side="left")
        self.run = ttk.Button(controls, text="Encode with Huffman", command=self.encode, state="disabled"); self.run.pack(side="left", padx=8)
        ttk.Label(controls, textvariable=self.status).pack(side="left", padx=8)
        holder = ttk.Frame(self, padding=(12, 0, 12, 12)); holder.pack(fill="both", expand=True)
        self.canvas = tk.Canvas(holder, highlightthickness=0); scroll = ttk.Scrollbar(holder, orient="vertical", command=self.canvas.yview); self.gallery = ttk.Frame(self.canvas)
        self.gallery.bind("<Configure>", lambda _event: self.canvas.configure(scrollregion=self.canvas.bbox("all"))); self.canvas.create_window((0, 0), window=self.gallery, anchor="nw"); self.canvas.configure(yscrollcommand=scroll.set); self.canvas.pack(side="left", fill="both", expand=True); scroll.pack(side="right", fill="y")

    def choose(self):
        filename = filedialog.askopenfilename(title="Select an image", filetypes=FILE_TYPES)
        if filename: self.selected = Path(filename); self.run.config(state="normal"); self.status.set(f"Selected: {self.selected.name}")

    def encode(self):
        try:
            saved, data = process(self.selected, self.project / "Output")
            for widget in self.gallery.winfo_children(): widget.destroy()
            self.photos.clear()
            for index, (name, path) in enumerate(saved.items()):
                with Image.open(path) as source: image = source.copy()
                image.thumbnail((420, 280)); photo = ImageTk.PhotoImage(image); self.photos.append(photo)
                card = ttk.LabelFrame(self.gallery, text=name.removesuffix(".png").replace("_", " ").title(), padding=8); card.grid(row=index // 2, column=index % 2, padx=8, pady=8, sticky="nsew"); ttk.Label(card, image=photo).pack()
            self.status.set(f"Lossless reconstruction verified — compression ratio: {data['compression_ratio']:.2f}:1")
            self.canvas.yview_moveto(0)
        except Exception as error: messagebox.showerror("Huffman coding failed", str(error))


if __name__ == "__main__": HuffmanApp().mainloop()
