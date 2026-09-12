"""Tkinter interface for the manual Haar DWT project."""

from __future__ import annotations

import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

from PIL import Image, ImageTk

from DWT import process


OUTPUTS = (
    ("Greyscale original", "dwt_original_grey.png"),
    ("LL approximation", "dwt_LL_approximation.png"),
    ("LH horizontal detail", "dwt_LH_horizontal.png"),
    ("HL vertical detail", "dwt_HL_vertical.png"),
    ("HH diagonal detail", "dwt_HH_diagonal.png"),
    ("One-level DWT", "dwt_subbands_1level.png"),
    ("Two-level DWT", "dwt_subbands_2level.png"),
    ("IDWT reconstruction", "dwt_reconstructed.png"),
    ("Comparison overview", "dwt_comparison_overview.png"),
)
FILE_TYPES = [("Image files", "*.png *.jpg *.jpeg *.bmp *.tiff *.webp"), ("All files", "*.*")]


class DWTApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("2D Haar Discrete Wavelet Transform")
        self.geometry("1100x760")
        self.minsize(760, 560)
        self.project_dir = Path(__file__).resolve().parent
        self.selected_image: Path | None = None
        self.photos: list[ImageTk.PhotoImage] = []
        self.status = tk.StringVar(value="Choose an image to begin.")
        self._build()

    def _build(self) -> None:
        controls = ttk.Frame(self, padding=12)
        controls.pack(fill="x")
        ttk.Button(controls, text="Choose Image", command=self.choose_image).pack(side="left")
        self.process_button = ttk.Button(controls, text="Process Image", command=self.run_dwt, state="disabled")
        self.process_button.pack(side="left", padx=8)
        ttk.Label(controls, textvariable=self.status).pack(side="left", padx=8)

        container = ttk.Frame(self, padding=(12, 0, 12, 12))
        container.pack(fill="both", expand=True)
        self.canvas = tk.Canvas(container, highlightthickness=0)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=self.canvas.yview)
        self.results = ttk.Frame(self.canvas)
        self.results.bind("<Configure>", lambda _event: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.results, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def choose_image(self) -> None:
        filename = filedialog.askopenfilename(title="Select an image", filetypes=FILE_TYPES)
        if filename:
            self.selected_image = Path(filename)
            self.process_button.config(state="normal")
            self.status.set(f"Selected: {self.selected_image.name}")

    def run_dwt(self) -> None:
        if not self.selected_image:
            return
        try:
            output_dir = self.project_dir / "Output"
            mse, max_error = process(self.selected_image, output_dir)
            self.show_results(output_dir)
            self.status.set(f"Done — MSE: {mse:.2e}, maximum difference: {max_error:.2e}")
        except Exception as error:
            messagebox.showerror("DWT failed", str(error))

    def show_results(self, output_dir: Path) -> None:
        for widget in self.results.winfo_children():
            widget.destroy()
        self.photos.clear()
        files = [("Selected image", self.selected_image), *[(title, output_dir / name) for title, name in OUTPUTS]]
        for index, (title, path) in enumerate(files):
            with Image.open(path) as source:
                image = source.copy()
            image.thumbnail((420, 260))
            photo = ImageTk.PhotoImage(image)
            self.photos.append(photo)
            card = ttk.LabelFrame(self.results, text=title, padding=8)
            card.grid(row=index // 2, column=index % 2, padx=8, pady=8, sticky="nsew")
            ttk.Label(card, image=photo).pack()
        self.results.columnconfigure((0, 1), weight=1)
        self.canvas.yview_moveto(0)


if __name__ == "__main__":
    DWTApp().mainloop()
