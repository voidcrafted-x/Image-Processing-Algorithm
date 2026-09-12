"""Tkinter user interface for manual edge detection."""

from __future__ import annotations

import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

from PIL import Image, ImageTk

from edge_detection import process


IMAGE_TYPES = [("Image files", "*.png *.jpg *.jpeg *.bmp *.tiff *.webp"), ("All files", "*.*")]


class EdgeDetectionApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Edge Detection from First Principles")
        self.geometry("1100x760")
        self.minsize(760, 560)
        self.project_dir = Path(__file__).resolve().parent
        self.selected: Path | None = None
        self.photos: list[ImageTk.PhotoImage] = []
        self.status = tk.StringVar(value="Choose an image to begin.")
        self._build_interface()

    def _build_interface(self) -> None:
        controls = ttk.Frame(self, padding=12)
        controls.pack(fill="x")
        ttk.Button(controls, text="Choose Image", command=self.choose_image).pack(side="left")
        self.run_button = ttk.Button(controls, text="Detect Edges", command=self.detect_edges, state="disabled")
        self.run_button.pack(side="left", padx=8)
        ttk.Label(controls, textvariable=self.status).pack(side="left", padx=8)
        holder = ttk.Frame(self, padding=(12, 0, 12, 12))
        holder.pack(fill="both", expand=True)
        self.canvas = tk.Canvas(holder, highlightthickness=0)
        scrollbar = ttk.Scrollbar(holder, orient="vertical", command=self.canvas.yview)
        self.gallery = ttk.Frame(self.canvas)
        self.gallery.bind("<Configure>", lambda _event: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.gallery, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def choose_image(self) -> None:
        filename = filedialog.askopenfilename(title="Select an image", filetypes=IMAGE_TYPES)
        if filename:
            self.selected = Path(filename)
            self.run_button.config(state="normal")
            self.status.set(f"Selected: {self.selected.name}")

    def detect_edges(self) -> None:
        if not self.selected:
            return
        try:
            saved = process(self.selected, self.project_dir / "Output")
            self.show_images(saved)
            self.status.set(f"Done — {len(saved)} output images saved to Output.")
        except Exception as error:
            messagebox.showerror("Edge detection failed", str(error))

    def show_images(self, saved: dict[str, Path]) -> None:
        for widget in self.gallery.winfo_children():
            widget.destroy()
        self.photos.clear()
        for index, (name, path) in enumerate(saved.items()):
            with Image.open(path) as source:
                image = source.copy()
            image.thumbnail((420, 260))
            photo = ImageTk.PhotoImage(image)
            self.photos.append(photo)
            card = ttk.LabelFrame(self.gallery, text=name.removesuffix(".png").replace("_", " ").title(), padding=8)
            card.grid(row=index // 2, column=index % 2, padx=8, pady=8, sticky="nsew")
            ttk.Label(card, image=photo).pack()
        self.gallery.columnconfigure((0, 1), weight=1)
        self.canvas.yview_moveto(0)


if __name__ == "__main__":
    EdgeDetectionApp().mainloop()
