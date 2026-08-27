import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import numpy as np

import matplotlib
matplotlib.use("TkAgg")

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt


class HistogramEqualizationApp:

    def __init__(self, root):

        self.root = root

        # =====================================================
        # WINDOW SETTINGS
        # =====================================================

        self.root.title(
            "RGB Histogram Equalization - Digital Image Processing"
        )

        self.root.geometry("1350x850")
        self.root.minsize(1100, 700)

        self.root.configure(
            bg="#101827"
        )

        # =====================================================
        # VARIABLES
        # =====================================================

        self.original_image = None
        self.equalized_image = None
        self.file_path = None

        # =====================================================
        # COLORS
        # =====================================================

        self.bg = "#101827"
        self.sidebar = "#172033"
        self.card = "#1e293b"

        self.blue = "#2563eb"
        self.blue_hover = "#1d4ed8"

        self.green = "#16a34a"
        self.green_hover = "#15803d"

        self.purple = "#7c3aed"
        self.purple_hover = "#6d28d9"

        self.gray_button = "#475569"
        self.gray_button_hover = "#334155"

        self.white = "#ffffff"
        self.gray = "#94a3b8"
        self.border = "#334155"

        # =====================================================
        # CREATE GUI
        # =====================================================

        self.create_sidebar()
        self.create_main_area()

    # =========================================================
    # SIDEBAR
    # =========================================================

    def create_sidebar(self):

        sidebar = tk.Frame(
            self.root,
            bg=self.sidebar,
            width=270
        )

        sidebar.pack(
            side="left",
            fill="y"
        )

        sidebar.pack_propagate(False)

        # -----------------------------------------------------
        # APPLICATION TITLE
        # -----------------------------------------------------

        tk.Label(
            sidebar,
            text="IMAGE",
            font=("Segoe UI", 25, "bold"),
            fg=self.blue,
            bg=self.sidebar
        ).pack(
            anchor="w",
            padx=25,
            pady=(30, 0)
        )

        tk.Label(
            sidebar,
            text="PROCESSING STUDIO",
            font=("Segoe UI", 11, "bold"),
            fg=self.white,
            bg=self.sidebar
        ).pack(
            anchor="w",
            padx=25
        )

        tk.Label(
            sidebar,
            text="Digital Image Processing",
            font=("Segoe UI", 9),
            fg=self.gray,
            bg=self.sidebar
        ).pack(
            anchor="w",
            padx=25,
            pady=(5, 25)
        )

        # Separator
        tk.Frame(
            sidebar,
            height=1,
            bg=self.border
        ).pack(
            fill="x",
            padx=20
        )

        # -----------------------------------------------------
        # OPERATIONS TITLE
        # -----------------------------------------------------

        tk.Label(
            sidebar,
            text="OPERATIONS",
            font=("Segoe UI", 9, "bold"),
            fg=self.gray,
            bg=self.sidebar
        ).pack(
            anchor="w",
            padx=25,
            pady=(25, 10)
        )

        # -----------------------------------------------------
        # UPLOAD BUTTON
        # -----------------------------------------------------

        self.make_button(
            sidebar,
            "📁  Upload Image",
            self.upload_image,
            self.blue
        )

        # -----------------------------------------------------
        # EQUALIZATION BUTTON
        # -----------------------------------------------------

        self.make_button(
            sidebar,
            "✨  Equalize Histogram",
            self.equalize_image,
            self.green
        )

        # -----------------------------------------------------
        # SAVE RESULT BUTTON
        # -----------------------------------------------------

        self.make_button(
            sidebar,
            "💾  Save Equalized Image",
            self.save_image,
            self.gray_button
        )

        # -----------------------------------------------------
        # SAVE FULL OUTPUT BUTTON
        # -----------------------------------------------------

        self.make_button(
            sidebar,
            "🖼  Save Full Output",
            self.save_full_output,
            self.purple
        )

        # -----------------------------------------------------
        # RESET BUTTON
        # -----------------------------------------------------

        self.make_button(
            sidebar,
            "↻  Reset",
            self.reset,
            "#334155"
        )

        # -----------------------------------------------------
        # IMAGE INFORMATION
        # -----------------------------------------------------

        tk.Label(
            sidebar,
            text="IMAGE INFORMATION",
            font=("Segoe UI", 9, "bold"),
            fg=self.gray,
            bg=self.sidebar
        ).pack(
            anchor="w",
            padx=25,
            pady=(35, 10)
        )

        self.info_label = tk.Label(
            sidebar,
            text="No image selected",
            font=("Segoe UI", 9),
            fg=self.gray,
            bg=self.card,
            justify="left",
            anchor="nw",
            padx=15,
            pady=15,
            wraplength=220
        )

        self.info_label.pack(
            fill="x",
            padx=20
        )

        # -----------------------------------------------------
        # BOTTOM TEXT
        # -----------------------------------------------------

        tk.Label(
            sidebar,
            text="Histogram Equalization\n"
                 "Digital Image Processing\n"
                 "Version 1.0",
            font=("Segoe UI", 8),
            fg="#64748b",
            bg=self.sidebar,
            justify="left"
        ).pack(
            side="bottom",
            anchor="w",
            padx=25,
            pady=20
        )

    # =========================================================
    # BUTTON CREATOR
    # =========================================================

    def make_button(
        self,
        parent,
        text,
        command,
        color
    ):

        button = tk.Button(
            parent,
            text=text,
            command=command,
            font=("Segoe UI", 10, "bold"),
            bg=color,
            fg="white",
            activebackground=color,
            activeforeground="white",
            relief="flat",
            bd=0,
            cursor="hand2",
            anchor="w",
            padx=15,
            pady=12
        )

        button.pack(
            fill="x",
            padx=20,
            pady=5
        )

        return button

    # =========================================================
    # MAIN AREA
    # =========================================================

    def create_main_area(self):

        main = tk.Frame(
            self.root,
            bg=self.bg
        )

        main.pack(
            side="right",
            fill="both",
            expand=True
        )

        # -----------------------------------------------------
        # HEADER
        # -----------------------------------------------------

        header = tk.Frame(
            main,
            bg=self.bg
        )

        header.pack(
            fill="x",
            padx=30,
            pady=(25, 10)
        )

        tk.Label(
            header,
            text="Histogram Equalization",
            font=("Segoe UI", 25, "bold"),
            fg=self.white,
            bg=self.bg
        ).pack(
            anchor="w"
        )

        tk.Label(
            header,
            text="Improve RGB image contrast by redistributing channel intensities",
            font=("Segoe UI", 10),
            fg=self.gray,
            bg=self.bg
        ).pack(
            anchor="w",
            pady=(4, 0)
        )

        # -----------------------------------------------------
        # STATUS
        # -----------------------------------------------------

        self.status = tk.Label(
            main,
            text="Ready — upload an image to begin",
            font=("Segoe UI", 9),
            fg=self.gray,
            bg=self.card,
            anchor="w",
            padx=15,
            pady=8
        )

        self.status.pack(
            fill="x",
            padx=30,
            pady=(5, 10)
        )

        # -----------------------------------------------------
        # CONTENT GRID
        # -----------------------------------------------------

        grid = tk.Frame(
            main,
            bg=self.bg
        )

        grid.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=5
        )

        grid.columnconfigure(
            0,
            weight=1
        )

        grid.columnconfigure(
            1,
            weight=1
        )

        grid.rowconfigure(
            0,
            weight=1
        )

        grid.rowconfigure(
            1,
            weight=1
        )

        # =====================================================
        # ORIGINAL IMAGE
        # =====================================================

        self.original_frame = self.create_card(
            grid,
            "BEFORE HISTOGRAM EQUALIZATION",
            0,
            0
        )

        self.original_label = tk.Label(
            self.original_frame,
            text="Upload an image",
            font=("Segoe UI", 12),
            fg=self.gray,
            bg=self.card
        )

        self.original_label.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        # =====================================================
        # ORIGINAL HISTOGRAM
        # =====================================================

        self.original_hist_frame = self.create_card(
            grid,
            "ORIGINAL HISTOGRAM + CDF",
            0,
            1
        )

        # =====================================================
        # EQUALIZED IMAGE
        # =====================================================

        self.equalized_frame = self.create_card(
            grid,
            "AFTER HISTOGRAM EQUALIZATION",
            1,
            0
        )

        self.equalized_label = tk.Label(
            self.equalized_frame,
            text="Equalized image will appear here",
            font=("Segoe UI", 12),
            fg=self.gray,
            bg=self.card
        )

        self.equalized_label.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        # =====================================================
        # EQUALIZED HISTOGRAM
        # =====================================================

        self.equalized_hist_frame = self.create_card(
            grid,
            "EQUALIZED HISTOGRAM + CDF",
            1,
            1
        )

    # =========================================================
    # CREATE CARD
    # =========================================================

    def create_card(
        self,
        parent,
        title,
        row,
        column
    ):

        frame = tk.Frame(
            parent,
            bg=self.card,
            highlightbackground=self.border,
            highlightthickness=1
        )

        frame.grid(
            row=row,
            column=column,
            sticky="nsew",
            padx=6,
            pady=6
        )

        tk.Label(
            frame,
            text=title,
            font=("Segoe UI", 10, "bold"),
            fg=self.white,
            bg=self.card,
            anchor="w"
        ).pack(
            fill="x",
            padx=15,
            pady=10
        )

        tk.Frame(
            frame,
            height=1,
            bg=self.border
        ).pack(
            fill="x"
        )

        return frame

    # =========================================================
    # UPLOAD IMAGE
    # =========================================================

    def upload_image(self):

        filename = filedialog.askopenfilename(
            title="Select an Image",
            filetypes=[
                (
                    "Image Files",
                    "*.jpg *.jpeg *.png *.bmp *.tif *.tiff *.webp"
                ),
                ("JPEG Files", "*.jpg *.jpeg"),
                ("PNG Files", "*.png"),
                ("BMP Files", "*.bmp"),
                ("TIFF Files", "*.tif *.tiff"),
                ("All Files", "*.*")
            ]
        )

        if not filename:
            return

        try:

            # -------------------------------------------------
            # OPEN IMAGE
            # -------------------------------------------------

            image = Image.open(
                filename
            )

            # -------------------------------------------------
            # CONVERT TO RGB COLOR
            # -------------------------------------------------

            image = image.convert(
                "RGB"
            )

            self.original_image = image
            self.equalized_image = None
            self.file_path = filename

            # -------------------------------------------------
            # DISPLAY ORIGINAL IMAGE
            # -------------------------------------------------

            self.show_image(
                image,
                self.original_label
            )

            # -------------------------------------------------
            # IMAGE INFORMATION
            # -------------------------------------------------

            import os

            name = os.path.basename(
                filename
            )

            width, height = image.size

            self.info_label.config(
                text=(
                    f"File:\n{name}\n\n"
                    f"Dimensions:\n"
                    f"{width} × {height}\n\n"
                    f"Mode:\n"
                    f"24-bit RGB Color\n\n"
                    f"Total Pixels:\n"
                    f"{width * height:,}"
                )
            )

            # -------------------------------------------------
            # ORIGINAL HISTOGRAM
            # -------------------------------------------------

            self.plot_histogram(
                image,
                self.original_hist_frame
            )

            # -------------------------------------------------
            # CLEAR EQUALIZED AREA
            # -------------------------------------------------

            self.remove_graph(
                self.equalized_hist_frame
            )

            self.equalized_label.config(
                image="",
                text="Click\n\nEqualize Histogram",
                fg=self.gray
            )

            self.status.config(
                text="✓ Image uploaded successfully"
            )

        except Exception as e:

            messagebox.showerror(
                "Error",
                f"Could not open image.\n\n{e}"
            )

    # =========================================================
    # HISTOGRAM EQUALIZATION
    # =========================================================

    def equalize_image(
        self
    ):

        if self.original_image is None:

            messagebox.showwarning(
                "No Image",
                "Please upload an image first."
            )

            return

        try:

            self.status.config(
                text="Processing RGB histogram equalization..."
            )

            self.root.update_idletasks()

            # -------------------------------------------------
            # CONVERT RGB IMAGE TO NUMPY
            # -------------------------------------------------

            image_array = np.array(
                self.original_image.convert("RGB"),
                dtype=np.uint8
            )

            # -------------------------------------------------
            # EQUALIZE EACH RGB CHANNEL SEPARATELY
            # -------------------------------------------------

            equalized_array = np.zeros_like(
                image_array
            )

            for channel in range(3):

                channel_data = image_array[:, :, channel]

                # Histogram
                histogram = np.bincount(
                    channel_data.flatten(),
                    minlength=256
                )

                # CDF
                cdf = histogram.cumsum()

                non_zero_cdf = cdf[
                    cdf > 0
                ]

                if len(non_zero_cdf) == 0:
                    equalized_array[:, :, channel] = channel_data
                    continue

                cdf_min = non_zero_cdf[0]

                total_pixels = channel_data.size

                denominator = (
                    total_pixels - cdf_min
                )

                if denominator == 0:

                    equalized_array[:, :, channel] = channel_data

                else:

                    lookup_table = (
                        (
                            cdf - cdf_min
                        )
                        /
                        denominator
                    ) * 255

                    lookup_table = np.clip(
                        lookup_table,
                        0,
                        255
                    )

                    lookup_table = lookup_table.astype(
                        np.uint8
                    )

                    equalized_array[:, :, channel] = (
                        lookup_table[channel_data]
                    )

            # -------------------------------------------------
            # CONVERT BACK TO RGB PIL IMAGE
            # -------------------------------------------------

            self.equalized_image = Image.fromarray(
                equalized_array,
                mode="RGB"
            )

            # -------------------------------------------------
            # DISPLAY EQUALIZED IMAGE
            # -------------------------------------------------

            self.show_image(
                self.equalized_image,
                self.equalized_label
            )

            # -------------------------------------------------
            # DISPLAY EQUALIZED RGB HISTOGRAM
            # -------------------------------------------------

            self.plot_histogram(
                self.equalized_image,
                self.equalized_hist_frame
            )

            self.status.config(
                text="✓ RGB histogram equalization completed"
            )

        except Exception as e:

            messagebox.showerror(
                "Processing Error",
                f"RGB histogram equalization failed.\\n\\n{e}"
            )

            self.status.config(
                text="Processing failed"
            )

    # =========================================================
    # DISPLAY IMAGE
    # =========================================================

    def show_image(
        self,
        image,
        label
    ):

        self.root.update_idletasks()

        width = label.winfo_width()
        height = label.winfo_height()

        if width < 100:
            width = 500

        if height < 100:
            height = 300

        image_copy = image.copy()

        image_copy.thumbnail(
            (
                width - 30,
                height - 30
            ),
            Image.Resampling.LANCZOS
        )

        photo = ImageTk.PhotoImage(
            image_copy
        )

        label.config(
            image=photo,
            text=""
        )

        # Keep reference
        label.image = photo

    # =========================================================
    # PLOT HISTOGRAM
    # =========================================================

    def plot_histogram(
        self,
        image,
        parent
    ):

        # Remove previous graph
        self.remove_graph(
            parent
        )

        # -----------------------------------------------------
        # NUMPY RGB ARRAY
        # -----------------------------------------------------

        array = np.array(
            image.convert("RGB"),
            dtype=np.uint8
        )

        # -----------------------------------------------------
        # RGB HISTOGRAMS
        # -----------------------------------------------------

        red_hist = np.bincount(
            array[:, :, 0].flatten(),
            minlength=256
        )

        green_hist = np.bincount(
            array[:, :, 1].flatten(),
            minlength=256
        )

        blue_hist = np.bincount(
            array[:, :, 2].flatten(),
            minlength=256
        )

        # -----------------------------------------------------
        # RGB CDFS
        # -----------------------------------------------------

        red_cdf = red_hist.cumsum()
        green_cdf = green_hist.cumsum()
        blue_cdf = blue_hist.cumsum()

        red_cdf_scaled = (
            red_cdf / red_cdf[-1]
        ) * max(red_hist.max(), 1)

        green_cdf_scaled = (
            green_cdf / green_cdf[-1]
        ) * max(green_hist.max(), 1)

        blue_cdf_scaled = (
            blue_cdf / blue_cdf[-1]
        ) * max(blue_hist.max(), 1)

        # -----------------------------------------------------
        # MATPLOTLIB FIGURE
        # -----------------------------------------------------

        fig = Figure(
            figsize=(5, 3),
            dpi=90,
            facecolor=self.card
        )

        ax = fig.add_subplot(
            111
        )

        ax.set_facecolor(
            self.card
        )

        x = range(256)

        # RGB histograms
        ax.plot(
            x,
            red_hist,
            color="red",
            linewidth=1.5,
            label="Red"
        )

        ax.plot(
            x,
            green_hist,
            color="green",
            linewidth=1.5,
            label="Green"
        )

        ax.plot(
            x,
            blue_hist,
            color="blue",
            linewidth=1.5,
            label="Blue"
        )

        # RGB CDFs
        ax.plot(
            x,
            red_cdf_scaled,
            color="darkred",
            linewidth=1,
            linestyle="--",
            label="Red CDF"
        )

        ax.plot(
            x,
            green_cdf_scaled,
            color="darkgreen",
            linewidth=1,
            linestyle="--",
            label="Green CDF"
        )

        ax.plot(
            x,
            blue_cdf_scaled,
            color="darkblue",
            linewidth=1,
            linestyle="--",
            label="Blue CDF"
        )

        ax.set_xlim(
            0,
            255
        )

        ax.set_xlabel(
            "Intensity",
            color="#cbd5e1"
        )

        ax.set_ylabel(
            "Frequency",
            color="#cbd5e1"
        )

        ax.legend(
            fontsize=6,
            loc="upper right"
        )

        ax.grid(
            alpha=0.15,
            color="#94a3b8"
        )

        ax.tick_params(
            colors="#cbd5e1",
            labelsize=8
        )

        for spine in ax.spines.values():

            spine.set_color(
                "#475569"
            )

        fig.tight_layout()

        # -----------------------------------------------------
        # EMBED IN TKINTER
        # -----------------------------------------------------

        canvas = FigureCanvasTkAgg(
            fig,
            master=parent
        )

        canvas.draw()

        canvas.get_tk_widget().pack(
            fill="both",
            expand=True,
            padx=8,
            pady=5
        )

        parent.graph_canvas = canvas

    # =========================================================
    # REMOVE GRAPH
    # =========================================================

    def remove_graph(
        self,
        parent
    ):

        if hasattr(
            parent,
            "graph_canvas"
        ):

            try:

                parent.graph_canvas.get_tk_widget().destroy()

            except:
                pass

            parent.graph_canvas = None

    # =========================================================
    # SAVE EQUALIZED IMAGE ONLY
    # =========================================================

    def save_image(self):

        if self.equalized_image is None:

            messagebox.showwarning(
                "No Result",
                "Please equalize the image first."
            )

            return

        filename = filedialog.asksaveasfilename(
            title="Save Equalized Image",
            defaultextension=".png",
            filetypes=[
                ("PNG Image", "*.png"),
                ("JPEG Image", "*.jpg"),
                ("BMP Image", "*.bmp"),
                ("TIFF Image", "*.tiff")
            ],
            initialfile="equalized_image.png"
        )

        if not filename:
            return

        try:

            self.equalized_image.save(
                filename
            )

            self.status.config(
                text=f"✓ Equalized image saved"
            )

            messagebox.showinfo(
                "Saved",
                "Equalized image saved successfully!"
            )

        except Exception as e:

            messagebox.showerror(
                "Save Error",
                f"Could not save image.\n\n{e}"
            )

    # =========================================================
    # SAVE COMPLETE OUTPUT
    # =========================================================

    def save_full_output(self):

        # -----------------------------------------------------
        # CHECK ORIGINAL IMAGE
        # -----------------------------------------------------

        if self.original_image is None:

            messagebox.showwarning(
                "No Image",
                "Please upload an image first."
            )

            return

        # -----------------------------------------------------
        # CHECK EQUALIZED IMAGE
        # -----------------------------------------------------

        if self.equalized_image is None:

            messagebox.showwarning(
                "No Equalized Image",
                "Please click 'Equalize Histogram' first."
            )

            return

        # -----------------------------------------------------
        # SAVE DIALOG
        # -----------------------------------------------------

        filename = filedialog.asksaveasfilename(
            title="Save Complete Histogram Equalization Output",
            defaultextension=".png",
            filetypes=[
                ("PNG Image", "*.png"),
                ("JPEG Image", "*.jpg"),
                ("All Files", "*.*")
            ],
            initialfile="histogram_equalization_output.png"
        )

        if not filename:
            return

        try:

            # =================================================
            # ORIGINAL IMAGE ARRAY
            # =================================================

            original = np.array(
                self.original_image,
                dtype=np.uint8
            )

            # =================================================
            # EQUALIZED IMAGE ARRAY
            # =================================================

            equalized = np.array(
                self.equalized_image,
                dtype=np.uint8
            )

            # =================================================
            # ORIGINAL HISTOGRAM
            # =================================================

            # RGB histograms
            original_hist_r = np.bincount(
                original[:, :, 0].flatten(),
                minlength=256
            )
            original_hist_g = np.bincount(
                original[:, :, 1].flatten(),
                minlength=256
            )
            original_hist_b = np.bincount(
                original[:, :, 2].flatten(),
                minlength=256
            )

            equalized_hist_r = np.bincount(
                equalized[:, :, 0].flatten(),
                minlength=256
            )
            equalized_hist_g = np.bincount(
                equalized[:, :, 1].flatten(),
                minlength=256
            )
            equalized_hist_b = np.bincount(
                equalized[:, :, 2].flatten(),
                minlength=256
            )

            # RGB CDFs
            original_cdf_r = original_hist_r.cumsum()
            original_cdf_g = original_hist_g.cumsum()
            original_cdf_b = original_hist_b.cumsum()

            equalized_cdf_r = equalized_hist_r.cumsum()
            equalized_cdf_g = equalized_hist_g.cumsum()
            equalized_cdf_b = equalized_hist_b.cumsum()

            original_cdf_scaled_r = (
                original_cdf_r / original_cdf_r[-1]
            ) * max(original_hist_r.max(), 1)

            original_cdf_scaled_g = (
                original_cdf_g / original_cdf_g[-1]
            ) * max(original_hist_g.max(), 1)

            original_cdf_scaled_b = (
                original_cdf_b / original_cdf_b[-1]
            ) * max(original_hist_b.max(), 1)

            equalized_cdf_scaled_r = (
                equalized_cdf_r / equalized_cdf_r[-1]
            ) * max(equalized_hist_r.max(), 1)

            equalized_cdf_scaled_g = (
                equalized_cdf_g / equalized_cdf_g[-1]
            ) * max(equalized_hist_g.max(), 1)

            equalized_cdf_scaled_b = (
                equalized_cdf_b / equalized_cdf_b[-1]
            ) * max(equalized_hist_b.max(), 1)

            # =================================================
            # CREATE FIGURE
            # =================================================

            fig = Figure(
                figsize=(14, 9),
                dpi=150,
                facecolor="white"
            )

            # =================================================
            # TOP LEFT - ORIGINAL IMAGE
            # =================================================

            ax1 = fig.add_subplot(
                2,
                2,
                1
            )

            ax1.imshow(
                original
            )

            ax1.set_title(
                "Before Histogram Equalization",
                fontsize=14,
                fontweight="bold"
            )

            ax1.axis(
                "off"
            )

            # =================================================
            # TOP RIGHT - ORIGINAL HISTOGRAM
            # =================================================

            ax2 = fig.add_subplot(
                2,
                2,
                2
            )

            ax2.plot(
                range(256),
                original_hist_r,
                color="red",
                linewidth=1.5,
                label="Red"
            )

            ax2.plot(
                range(256),
                original_hist_g,
                color="green",
                linewidth=1.5,
                label="Green"
            )

            ax2.plot(
                range(256),
                original_hist_b,
                color="blue",
                linewidth=1.5,
                label="Blue"
            )

            ax2.plot(
                range(256),
                original_cdf_scaled_r,
                color="darkred",
                linewidth=1,
                linestyle="--"
            )

            ax2.plot(
                range(256),
                original_cdf_scaled_g,
                color="darkgreen",
                linewidth=1,
                linestyle="--"
            )

            ax2.plot(
                range(256),
                original_cdf_scaled_b,
                color="darkblue",
                linewidth=1,
                linestyle="--"
            )

            ax2.legend(fontsize=6)

            ax2.set_title(
                "Corresponding Histogram and Cumulative Histogram",
                fontsize=11,
                fontweight="bold"
            )

            ax2.set_xlabel(
                "Intensity"
            )

            ax2.set_ylabel(
                "Frequency"
            )

            ax2.set_xlim(
                0,
                255
            )

            ax2.grid(
                alpha=0.20
            )

            # =================================================
            # BOTTOM LEFT - EQUALIZED IMAGE
            # =================================================

            ax3 = fig.add_subplot(
                2,
                2,
                3
            )

            ax3.imshow(
                equalized
            )

            ax3.set_title(
                "After Histogram Equalization",
                fontsize=14,
                fontweight="bold"
            )

            ax3.axis(
                "off"
            )

            # =================================================
            # BOTTOM RIGHT - EQUALIZED HISTOGRAM
            # =================================================

            ax4 = fig.add_subplot(
                2,
                2,
                4
            )

            ax4.plot(
                range(256),
                equalized_hist_r,
                color="red",
                linewidth=1.5,
                label="Red"
            )

            ax4.plot(
                range(256),
                equalized_hist_g,
                color="green",
                linewidth=1.5,
                label="Green"
            )

            ax4.plot(
                range(256),
                equalized_hist_b,
                color="blue",
                linewidth=1.5,
                label="Blue"
            )

            ax4.plot(
                range(256),
                equalized_cdf_scaled_r,
                color="darkred",
                linewidth=1,
                linestyle="--"
            )

            ax4.plot(
                range(256),
                equalized_cdf_scaled_g,
                color="darkgreen",
                linewidth=1,
                linestyle="--"
            )

            ax4.plot(
                range(256),
                equalized_cdf_scaled_b,
                color="darkblue",
                linewidth=1,
                linestyle="--"
            )

            ax4.legend(fontsize=6)

            ax4.set_title(
                "Corresponding Histogram and Cumulative Histogram",
                fontsize=11,
                fontweight="bold"
            )

            ax4.set_xlabel(
                "Intensity"
            )

            ax4.set_ylabel(
                "Frequency"
            )

            ax4.set_xlim(
                0,
                255
            )

            ax4.grid(
                alpha=0.20
            )

            # =================================================
            # MAIN TITLE
            # =================================================

            fig.suptitle(
                "RGB Histogram Equalization - Digital Image Processing",
                fontsize=18,
                fontweight="bold"
            )

            # =================================================
            # LAYOUT
            # =================================================

            fig.tight_layout(
                rect=[
                    0,
                    0,
                    1,
                    0.95
                ]
            )

            # =================================================
            # SAVE
            # =================================================

            fig.savefig(
                filename,
                dpi=150,
                bbox_inches="tight",
                facecolor="white"
            )

            # Close Matplotlib figure
            plt.close(
                fig
            )

            # =================================================
            # SUCCESS
            # =================================================

            self.status.config(
                text="✓ Complete output saved successfully"
            )

            messagebox.showinfo(
                "Output Saved",
                "Complete output saved successfully!\n\n"
                "The file contains:\n\n"
                "1. Original Image\n"
                "2. Original Histogram + CDF\n"
                "3. Equalized Image\n"
                "4. Equalized Histogram + CDF"
            )

        except Exception as e:

            messagebox.showerror(
                "Save Error",
                "Could not save complete output.\n\n"
                + str(e)
            )

    # =========================================================
    # RESET
    # =========================================================

    def reset(self):

        self.original_image = None
        self.equalized_image = None
        self.file_path = None

        # Original image
        self.original_label.config(
            image="",
            text="Upload an image",
            fg=self.gray
        )

        # Equalized image
        self.equalized_label.config(
            image="",
            text="Equalized image will appear here",
            fg=self.gray
        )

        # Information
        self.info_label.config(
            text="No image selected"
        )

        # Remove graphs
        self.remove_graph(
            self.original_hist_frame
        )

        self.remove_graph(
            self.equalized_hist_frame
        )

        self.status.config(
            text="Ready — upload an image to begin"
        )


# =============================================================
# MAIN PROGRAM
# =============================================================

if __name__ == "__main__":

    root = tk.Tk()

    app = HistogramEqualizationApp(
        root
    )

    root.mainloop()
