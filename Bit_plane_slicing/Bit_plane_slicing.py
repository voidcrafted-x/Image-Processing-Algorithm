import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import numpy as np
import os


class BitPlaneSlicingApp:

    def __init__(self, root):

        self.root = root

        # =====================================================
        # WINDOW
        # =====================================================

        self.root.title(
            "Bit-Plane Slicing | Digital Image Processing"
        )

        self.root.geometry("1400x850")
        self.root.minsize(1150, 700)

        self.root.configure(
            bg="#0f172a"
        )

        # =====================================================
        # VARIABLES
        # =====================================================

        self.image = None
        self.current_plane = None
        self.file_path = None

        # =====================================================
        # COLORS
        # =====================================================

        self.bg = "#0f172a"
        self.sidebar = "#111827"
        self.card = "#1e293b"
        self.card2 = "#243244"

        self.blue = "#2563eb"
        self.blue_hover = "#1d4ed8"

        self.green = "#16a34a"
        self.green_hover = "#15803d"

        self.orange = "#f59e0b"
        self.orange_hover = "#d97706"

        self.purple = "#7c3aed"
        self.purple_hover = "#6d28d9"

        self.red = "#dc2626"

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
            width=280
        )

        sidebar.pack(
            side="left",
            fill="y"
        )

        sidebar.pack_propagate(False)

        # -----------------------------------------------------
        # LOGO / TITLE
        # -----------------------------------------------------

        tk.Label(
            sidebar,
            text="IMAGE",
            font=("Segoe UI", 27, "bold"),
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
        # OPERATIONS
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

        # Upload
        self.create_button(
            sidebar,
            "📁  Upload Image",
            self.upload_image,
            self.blue
        )

        # Show selected plane
        self.create_button(
            sidebar,
            "🔍  Show Selected Plane",
            self.show_selected_plane,
            self.green
        )

        # All planes
        self.create_button(
            sidebar,
            "▦  Show All Bit Planes",
            self.show_all_planes,
            self.purple
        )

        # Save selected
        self.create_button(
            sidebar,
            "💾  Save Selected Plane",
            self.save_plane,
            self.orange
        )

        # Save all
        self.create_button(
            sidebar,
            "🖼  Save Full Output",
            self.save_full_output,
            "#0891b2"
        )

        # Reset
        self.create_button(
            sidebar,
            "↻  Reset",
            self.reset,
            "#334155"
        )

        # -----------------------------------------------------
        # BIT PLANE SELECTOR
        # -----------------------------------------------------

        tk.Label(
            sidebar,
            text="BIT PLANE",
            font=("Segoe UI", 9, "bold"),
            fg=self.gray,
            bg=self.sidebar
        ).pack(
            anchor="w",
            padx=25,
            pady=(30, 8)
        )

        plane_frame = tk.Frame(
            sidebar,
            bg=self.card
        )

        plane_frame.pack(
            fill="x",
            padx=20
        )

        tk.Label(
            plane_frame,
            text="Select plane:",
            font=("Segoe UI", 10),
            fg=self.white,
            bg=self.card
        ).pack(
            side="left",
            padx=12,
            pady=12
        )

        self.plane_var = tk.IntVar(
            value=7
        )

        self.plane_menu = tk.OptionMenu(
            plane_frame,
            self.plane_var,
            *range(8),
            command=self.show_selected_plane
        )

        self.plane_menu.config(
            font=("Segoe UI", 10, "bold"),
            bg="#334155",
            fg="white",
            activebackground="#475569",
            activeforeground="white",
            highlightthickness=0,
            width=5
        )

        self.plane_menu["menu"].config(
            bg="#1e293b",
            fg="white",
            activebackground=self.blue,
            activeforeground="white"
        )

        self.plane_menu.pack(
            side="right",
            padx=10,
            pady=7
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
            pady=(30, 10)
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
            wraplength=235
        )

        self.info_label.pack(
            fill="x",
            padx=20
        )

        # -----------------------------------------------------
        # BOTTOM
        # -----------------------------------------------------

        tk.Label(
            sidebar,
            text="Bit-Plane Slicing\n"
                 "Digital Image Processing\n"
                 "Version 2.0",
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
    # CREATE BUTTON
    # =========================================================

    def create_button(
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
            pady=11
        )

        button.pack(
            fill="x",
            padx=20,
            pady=4
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
            pady=(25, 5)
        )

        tk.Label(
            header,
            text="Bit-Plane Slicing",
            font=("Segoe UI", 27, "bold"),
            fg=self.white,
            bg=self.bg
        ).pack(
            anchor="w"
        )

        tk.Label(
            header,
            text="Decompose an 8-bit grayscale image into individual binary bit planes",
            font=("Segoe UI", 10),
            fg=self.gray,
            bg=self.bg
        ).pack(
            anchor="w",
            pady=(5, 0)
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
            pady=9
        )

        self.status.pack(
            fill="x",
            padx=30,
            pady=15
        )

        # -----------------------------------------------------
        # DISPLAY AREA
        # -----------------------------------------------------

        display_frame = tk.Frame(
            main,
            bg=self.bg
        )

        display_frame.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=5
        )

        display_frame.columnconfigure(
            0,
            weight=1
        )

        display_frame.columnconfigure(
            1,
            weight=1
        )

        display_frame.rowconfigure(
            0,
            weight=1
        )

        # =====================================================
        # ORIGINAL IMAGE CARD
        # =====================================================

        original_card = self.create_card(
            display_frame,
            "ORIGINAL IMAGE",
            0,
            0
        )

        self.original_label = tk.Label(
            original_card,
            text="📁\n\nUpload an image",
            font=("Segoe UI", 15),
            fg=self.gray,
            bg=self.card,
            cursor="hand2"
        )

        self.original_label.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        # Click original image
        self.original_label.bind(
            "<Button-1>",
            self.open_original_fullscreen
        )

        # =====================================================
        # BIT PLANE CARD
        # =====================================================

        plane_card = self.create_card(
            display_frame,
            "SELECTED BIT PLANE",
            0,
            1
        )

        self.plane_title = tk.Label(
            plane_card,
            text="Bit Plane 7",
            font=("Segoe UI", 13, "bold"),
            fg=self.blue,
            bg=self.card
        )

        self.plane_title.pack(
            pady=(8, 0)
        )

        self.plane_label = tk.Label(
            plane_card,
            text="Select an image",
            font=("Segoe UI", 15),
            fg=self.gray,
            bg=self.card,
            cursor="hand2"
        )

        self.plane_label.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        # Click plane image
        self.plane_label.bind(
            "<Button-1>",
            self.open_plane_fullscreen
        )

        # -----------------------------------------------------
        # HINT
        # -----------------------------------------------------

        tk.Label(
            main,
            text="💡 Tip: Click either image to open it in a larger full-size viewer",
            font=("Segoe UI", 9),
            fg=self.gray,
            bg=self.bg
        ).pack(
            pady=(3, 8)
        )

    # =========================================================
    # CARD
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
            padx=7,
            pady=7
        )

        tk.Label(
            frame,
            text=title,
            font=("Segoe UI", 11, "bold"),
            fg=self.white,
            bg=self.card
        ).pack(
            anchor="w",
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

        file_path = filedialog.askopenfilename(
            title="Select an Image",
            filetypes=[
                (
                    "Image Files",
                    "*.jpg *.jpeg *.png *.bmp *.tif *.tiff *.webp"
                ),
                ("JPEG Files", "*.jpg *.jpeg"),
                ("PNG Files", "*.png"),
                ("Bitmap Files", "*.bmp"),
                ("TIFF Files", "*.tif *.tiff"),
                ("All Files", "*.*")
            ]
        )

        if not file_path:
            return

        try:

            # Open and convert to grayscale
            self.image = Image.open(
                file_path
            ).convert("L")

            self.file_path = file_path

            # Reset current plane
            self.current_plane = None

            # Display original
            self.display_main_image(
                self.image,
                self.original_label
            )

            # Information
            filename = os.path.basename(
                file_path
            )

            width, height = self.image.size

            self.info_label.config(
                text=(
                    f"File:\n{filename}\n\n"
                    f"Dimensions:\n"
                    f"{width} × {height}\n\n"
                    f"Mode:\n"
                    f"8-bit Grayscale\n\n"
                    f"Total Pixels:\n"
                    f"{width * height:,}"
                )
            )

            self.status.config(
                text=f"✓ Loaded: {filename}"
            )

            # Automatically show MSB
            self.plane_var.set(7)
            self.show_selected_plane(7)

        except Exception as e:

            messagebox.showerror(
                "Error",
                f"Could not open image:\n\n{e}"
            )

    # =========================================================
    # GET BIT PLANE
    # =========================================================

    def get_bit_plane(
        self,
        plane_number
    ):

        if self.image is None:
            return None

        image_array = np.array(
            self.image,
            dtype=np.uint8
        )

        # Extract bit
        bit_plane = (
            image_array >> plane_number
        ) & 1

        # Convert 0/1 to 0/255
        bit_plane = (
            bit_plane * 255
        )

        return Image.fromarray(
            bit_plane.astype(np.uint8),
            mode="L"
        )

    # =========================================================
    # SHOW SELECTED PLANE
    # =========================================================

    def show_selected_plane(
        self,
        plane=None
    ):

        if self.image is None:

            messagebox.showwarning(
                "No Image",
                "Please upload an image first."
            )

            return

        if plane is None:
            plane = self.plane_var.get()
        else:
            plane = int(plane)
            self.plane_var.set(plane)

        self.current_plane = self.get_bit_plane(
            plane
        )

        self.plane_title.config(
            text=f"Bit Plane {plane}"
        )

        self.display_main_image(
            self.current_plane,
            self.plane_label
        )

        self.status.config(
            text=f"✓ Displaying Bit Plane {plane}"
        )

    # =========================================================
    # DISPLAY MAIN IMAGE
    # =========================================================

    def display_main_image(
        self,
        image,
        label
    ):

        self.root.update_idletasks()

        width = label.winfo_width()
        height = label.winfo_height()

        if width < 200:
            width = 520

        if height < 200:
            height = 500

        # Leave room around image
        max_width = width - 30
        max_height = height - 30

        image_copy = image.copy()

        image_copy.thumbnail(
            (
                max_width,
                max_height
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

        # Prevent garbage collection
        label.image = photo

    # =========================================================
    # OPEN ORIGINAL FULL SIZE
    # =========================================================

    def open_original_fullscreen(
        self,
        event=None
    ):

        if self.image is None:

            return

        self.open_full_image(
            self.image,
            "Original Image"
        )

    # =========================================================
    # OPEN PLANE FULL SIZE
    # =========================================================

    def open_plane_fullscreen(
        self,
        event=None
    ):

        if self.current_plane is None:

            return

        plane = self.plane_var.get()

        self.open_full_image(
            self.current_plane,
            f"Bit Plane {plane}"
        )

    # =========================================================
    # FULL IMAGE VIEWER
    # =========================================================

    def open_full_image(
        self,
        image,
        title
    ):

        window = tk.Toplevel(
            self.root
        )

        window.title(
            f"{title} - Full Size"
        )

        window.geometry(
            "1200x850"
        )

        window.configure(
            bg="#0f172a"
        )

        window.minsize(
            700,
            500
        )

        # -----------------------------------------------------
        # HEADER
        # -----------------------------------------------------

        header = tk.Frame(
            window,
            bg="#111827"
        )

        header.pack(
            fill="x"
        )

        tk.Label(
            header,
            text=title,
            font=("Segoe UI", 18, "bold"),
            fg="white",
            bg="#111827"
        ).pack(
            side="left",
            padx=20,
            pady=15
        )

        tk.Label(
            header,
            text=f"{image.width} × {image.height}",
            font=("Segoe UI", 10),
            fg=self.gray,
            bg="#111827"
        ).pack(
            side="right",
            padx=20
        )

        # -----------------------------------------------------
        # IMAGE AREA
        # -----------------------------------------------------

        container = tk.Frame(
            window,
            bg="#0f172a"
        )

        container.pack(
            fill="both",
            expand=True
        )

        image_label = tk.Label(
            container,
            bg="#0f172a"
        )

        image_label.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

        # -----------------------------------------------------
        # FUNCTION TO RESIZE IMAGE WITH WINDOW
        # -----------------------------------------------------

        def update_image(event=None):

            width = container.winfo_width()
            height = container.winfo_height()

            if width < 100:
                return

            if height < 100:
                return

            copy = image.copy()

            copy.thumbnail(
                (
                    width - 40,
                    height - 40
                ),
                Image.Resampling.LANCZOS
            )

            photo = ImageTk.PhotoImage(
                copy
            )

            image_label.config(
                image=photo
            )

            image_label.image = photo

        # Update whenever window changes size
        container.bind(
            "<Configure>",
            update_image
        )

        # Initial update
        window.after(
            100,
            update_image
        )

        # -----------------------------------------------------
        # CLOSE BUTTON
        # -----------------------------------------------------

        tk.Button(
            window,
            text="Close",
            command=window.destroy,
            font=("Segoe UI", 10, "bold"),
            bg=self.blue,
            fg="white",
            activebackground=self.blue_hover,
            activeforeground="white",
            relief="flat",
            bd=0,
            padx=30,
            pady=10,
            cursor="hand2"
        ).pack(
            pady=(0, 15)
        )

    # =========================================================
    # SHOW ALL PLANES
    # =========================================================

    def show_all_planes(self):

        if self.image is None:

            messagebox.showwarning(
                "No Image",
                "Please upload an image first."
            )

            return

        # -----------------------------------------------------
        # WINDOW
        # -----------------------------------------------------

        all_window = tk.Toplevel(
            self.root
        )

        all_window.title(
            "All Bit Planes"
        )

        all_window.geometry(
            "1250x850"
        )

        all_window.minsize(
            900,
            650
        )

        all_window.configure(
            bg=self.bg
        )

        # -----------------------------------------------------
        # HEADER
        # -----------------------------------------------------

        header = tk.Frame(
            all_window,
            bg="#111827"
        )

        header.pack(
            fill="x"
        )

        tk.Label(
            header,
            text="All Bit Planes",
            font=("Segoe UI", 22, "bold"),
            fg="white",
            bg="#111827"
        ).pack(
            side="left",
            padx=25,
            pady=15
        )

        tk.Label(
            header,
            text="Bit 7 = MSB     •     Bit 0 = LSB",
            font=("Segoe UI", 10),
            fg=self.gray,
            bg="#111827"
        ).pack(
            side="right",
            padx=25
        )

        # -----------------------------------------------------
        # SCROLLABLE CANVAS
        # -----------------------------------------------------

        canvas = tk.Canvas(
            all_window,
            bg=self.bg,
            highlightthickness=0
        )

        scrollbar = tk.Scrollbar(
            all_window,
            orient="vertical",
            command=canvas.yview
        )

        canvas.configure(
            yscrollcommand=scrollbar.set
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        canvas.pack(
            side="left",
            fill="both",
            expand=True
        )

        grid_frame = tk.Frame(
            canvas,
            bg=self.bg
        )

        canvas_window = canvas.create_window(
            (0, 0),
            window=grid_frame,
            anchor="nw"
        )

        # -----------------------------------------------------
        # STORE REFERENCES
        # -----------------------------------------------------

        all_window.image_refs = []

        # -----------------------------------------------------
        # CREATE 8 PLANES
        # -----------------------------------------------------

        for plane in range(8):

            card = tk.Frame(
                grid_frame,
                bg=self.card,
                highlightbackground=self.border,
                highlightthickness=1
            )

            row = plane // 4
            column = plane % 4

            card.grid(
                row=row,
                column=column,
                padx=10,
                pady=10,
                sticky="nsew"
            )

            # Title
            tk.Label(
                card,
                text=f"BIT PLANE {plane}",
                font=("Segoe UI", 12, "bold"),
                fg=self.white,
                bg=self.card
            ).pack(
                pady=8
            )

            # Plane image
            plane_img = self.get_bit_plane(
                plane
            )

            # Larger preview
            preview = self.resize_keep_ratio(
                plane_img,
                (260, 260)
            )

            photo = ImageTk.PhotoImage(
                preview
            )

            image_label = tk.Label(
                card,
                image=photo,
                bg=self.card,
                cursor="hand2"
            )

            image_label.pack(
                padx=10,
                pady=5
            )

            all_window.image_refs.append(
                photo
            )

            # Click to full size
            image_label.bind(
                "<Button-1>",
                lambda event,
                img=plane_img,
                p=plane:
                self.open_full_image(
                    img,
                    f"Bit Plane {p}"
                )
            )

            # Bit information
            bit_type = (
                "MSB"
                if plane == 7
                else
                "LSB"
                if plane == 0
                else
                ""
            )

            tk.Label(
                card,
                text=bit_type,
                font=("Segoe UI", 9, "bold"),
                fg=self.orange,
                bg=self.card
            ).pack(
                pady=(0, 8)
            )

        # Configure grid
        for i in range(4):

            grid_frame.columnconfigure(
                i,
                weight=1
            )

        # Update scroll region
        def update_scroll(event=None):

            canvas.configure(
                scrollregion=canvas.bbox("all")
            )

        grid_frame.bind(
            "<Configure>",
            update_scroll
        )

        # Make canvas window width follow canvas
        def resize_canvas(event):

            canvas.itemconfig(
                canvas_window,
                width=event.width
            )

        canvas.bind(
            "<Configure>",
            resize_canvas
        )

    # =========================================================
    # SAVE SELECTED PLANE
    # =========================================================

    def save_plane(self):

        if self.current_plane is None:

            messagebox.showwarning(
                "No Bit Plane",
                "Please select a bit plane first."
            )

            return

        plane = self.plane_var.get()

        file_path = filedialog.asksaveasfilename(
            title="Save Bit Plane",
            defaultextension=".png",
            filetypes=[
                ("PNG Image", "*.png"),
                ("JPEG Image", "*.jpg"),
                ("Bitmap Image", "*.bmp"),
                ("All Files", "*.*")
            ],
            initialfile=f"bit_plane_{plane}.png"
        )

        if not file_path:
            return

        try:

            self.current_plane.save(
                file_path
            )

            self.status.config(
                text=f"✓ Saved Bit Plane {plane}"
            )

            messagebox.showinfo(
                "Saved",
                f"Bit Plane {plane} saved successfully!"
            )

        except Exception as e:

            messagebox.showerror(
                "Save Error",
                f"Could not save image:\n\n{e}"
            )

    # =========================================================
    # SAVE FULL OUTPUT
    # =========================================================

    def save_full_output(self):

        if self.image is None:

            messagebox.showwarning(
                "No Image",
                "Please upload an image first."
            )

            return

        file_path = filedialog.asksaveasfilename(
            title="Save Complete Bit-Plane Output",
            defaultextension=".png",
            filetypes=[
                ("PNG Image", "*.png"),
                ("JPEG Image", "*.jpg"),
                ("All Files", "*.*")
            ],
            initialfile="bit_plane_slicing_output.png"
        )

        if not file_path:
            return

        try:

            # =================================================
            # CREATE OUTPUT IMAGE
            #
            # Layout:
            #
            # ┌───────────────────┬───────────────────┐
            # │ Original Image    │ Bit Plane 7       │
            # ├───────────────────┼───────────────────┤
            # │ Bit Plane 6       │ Bit Plane 5       │
            # ├───────────────────┼───────────────────┤
            # │ Bit Plane 4       │ Bit Plane 3       │
            # ├───────────────────┼───────────────────┤
            # │ Bit Plane 2       │ Bit Plane 1       │
            # ├───────────────────┼───────────────────┤
            # │ Bit Plane 0       │                   │
            # └───────────────────┴───────────────────┘
            #
            # =================================================

            images = []

            # Original
            images.append(
                (
                    "Original Image",
                    self.image
                )
            )

            # Planes 7 -> 0
            for plane in range(7, -1, -1):

                images.append(
                    (
                        f"Bit Plane {plane}",
                        self.get_bit_plane(plane)
                    )
                )

            # =================================================
            # OUTPUT SIZE
            # =================================================

            cell_width = 500
            cell_height = 400

            rows = 5
            columns = 2

            title_height = 80

            output_width = (
                columns * cell_width
            )

            output_height = (
                title_height +
                rows * cell_height
            )

            # =================================================
            # CREATE WHITE CANVAS
            # =================================================

            output = Image.new(
                "RGB",
                (
                    output_width,
                    output_height
                ),
                "white"
            )

            # =================================================
            # DRAW
            # =================================================

            from PIL import ImageDraw, ImageFont

            draw = ImageDraw.Draw(
                output
            )

            # Try to use a nice font
            try:

                title_font = ImageFont.truetype(
                    "arial.ttf",
                    28
                )

                label_font = ImageFont.truetype(
                    "arial.ttf",
                    22
                )

            except:

                title_font = ImageFont.load_default()
                label_font = ImageFont.load_default()

            # Main title
            title = "BIT-PLANE SLICING"

            bbox = draw.textbbox(
                (0, 0),
                title,
                font=title_font
            )

            title_x = (
                output_width -
                (bbox[2] - bbox[0])
            ) // 2

            draw.text(
                (
                    title_x,
                    20
                ),
                title,
                fill="black",
                font=title_font
            )

            # =================================================
            # PLACE IMAGES
            # =================================================

            for index, (name, img) in enumerate(images):

                row = index // columns
                column = index % columns

                x = (
                    column *
                    cell_width
                )

                y = (
                    title_height +
                    row *
                    cell_height
                )

                # Border
                draw.rectangle(
                    (
                        x,
                        y,
                        x + cell_width - 1,
                        y + cell_height - 1
                    ),
                    outline="#555555",
                    width=3
                )

                # Label
                bbox = draw.textbbox(
                    (0, 0),
                    name,
                    font=label_font
                )

                text_width = (
                    bbox[2] - bbox[0]
                )

                text_x = (
                    x +
                    (
                        cell_width -
                        text_width
                    ) // 2
                )

                draw.text(
                    (
                        text_x,
                        y + 15
                    ),
                    name,
                    fill="black",
                    font=label_font
                )

                # -------------------------------------------------
                # IMAGE
                # -------------------------------------------------

                img_copy = img.convert(
                    "L"
                )

                img_copy.thumbnail(
                    (
                        cell_width - 40,
                        cell_height - 80
                    ),
                    Image.Resampling.LANCZOS
                )

                # Center image
                image_x = (
                    x +
                    (
                        cell_width -
                        img_copy.width
                    ) // 2
                )

                image_y = (
                    y +
                    60 +
                    (
                        (
                            cell_height - 80
                        ) -
                        img_copy.height
                    ) // 2
                )

                output.paste(
                    img_copy.convert("RGB"),
                    (
                        image_x,
                        image_y
                    )
                )

            # =================================================
            # SAVE
            # =================================================

            output.save(
                file_path,
                quality=95
            )

            self.status.config(
                text="✓ Complete bit-plane output saved"
            )

            messagebox.showinfo(
                "Output Saved",
                "Complete output saved successfully!\n\n"
                "The output contains:\n\n"
                "• Original Image\n"
                "• Bit Plane 7\n"
                "• Bit Plane 6\n"
                "• Bit Plane 5\n"
                "• Bit Plane 4\n"
                "• Bit Plane 3\n"
                "• Bit Plane 2\n"
                "• Bit Plane 1\n"
                "• Bit Plane 0"
            )

        except Exception as e:

            messagebox.showerror(
                "Save Error",
                f"Could not save complete output:\n\n{e}"
            )

    # =========================================================
    # RESIZE IMAGE
    # =========================================================

    def resize_keep_ratio(
        self,
        image,
        max_size
    ):

        copy = image.copy()

        copy.thumbnail(
            max_size,
            Image.Resampling.LANCZOS
        )

        return copy

    # =========================================================
    # RESET
    # =========================================================

    def reset(self):

        self.image = None
        self.current_plane = None
        self.file_path = None

        self.original_label.config(
            image="",
            text="📁\n\nUpload an image"
        )

        self.plane_label.config(
            image="",
            text="Select an image"
        )

        self.plane_title.config(
            text="Bit Plane 7"
        )

        self.info_label.config(
            text="No image selected"
        )

        self.status.config(
            text="Ready — upload an image to begin"
        )

        self.plane_var.set(
            7
        )


# =============================================================
# MAIN
# =============================================================

if __name__ == "__main__":

    root = tk.Tk()

    app = BitPlaneSlicingApp(
        root
    )

    root.mainloop()
