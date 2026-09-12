import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import numpy as np
import os


class ImageArithmeticGUI:

    def __init__(self, root):

        # ================= MAIN WINDOW =================

        self.root = root
        self.root.title("Image Arithmetic Operations")
        self.root.geometry("1200x750")
        self.root.configure(bg="#f0f0f0")

        # Store uploaded image
        self.img = None
        self.gray_img = None

        # Keep references to displayed images
        self.original_color_photo = None
        self.original_gray_photo = None
        self.result_color_photo = None
        self.result_gray_photo = None

        # ================= TITLE =================

        title = tk.Label(
            root,
            text="IMAGE ARITHMETIC OPERATIONS",
            font=("Arial", 20, "bold"),
            bg="#f0f0f0"
        )

        title.pack(pady=20)

        # ================= CONTROLS =================

        control_frame = tk.Frame(
            root,
            bg="#f0f0f0"
        )

        control_frame.pack(pady=10)

        # Upload Button

        upload_button = tk.Button(
            control_frame,
            text="Upload Image",
            font=("Arial", 11, "bold"),
            width=15,
            command=self.upload_image
        )

        upload_button.grid(
            row=0,
            column=0,
            padx=15
        )

        # Operation Label

        operation_label = tk.Label(
            control_frame,
            text="Select Operation:",
            font=("Arial", 11),
            bg="#f0f0f0"
        )

        operation_label.grid(
            row=0,
            column=1,
            padx=5
        )

        # Operation Dropdown

        self.operation_var = tk.StringVar()
        self.operation_var.set("Addition")

        operation_menu = tk.OptionMenu(
            control_frame,
            self.operation_var,
            "Addition",
            "Subtraction",
            "Multiplication",
            "Division"
        )

        operation_menu.config(
            font=("Arial", 11),
            width=15
        )

        operation_menu.grid(
            row=0,
            column=2,
            padx=10
        )

        # Constant Label

        constant_label = tk.Label(
            control_frame,
            text="Constant:",
            font=("Arial", 11),
            bg="#f0f0f0"
        )

        constant_label.grid(
            row=0,
            column=3,
            padx=5
        )

        # Constant Entry

        self.constant_entry = tk.Entry(
            control_frame,
            font=("Arial", 11),
            width=10
        )

        self.constant_entry.insert(
            0,
            "10"
        )

        self.constant_entry.grid(
            row=0,
            column=4,
            padx=10
        )

        # Apply Button

        apply_button = tk.Button(
            control_frame,
            text="Apply Operation",
            font=("Arial", 11, "bold"),
            width=18,
            command=self.apply_operation
        )

        apply_button.grid(
            row=0,
            column=5,
            padx=15
        )

        # ================= IMAGE DISPLAY AREA =================

        image_frame = tk.Frame(
            root,
            bg="#f0f0f0"
        )

        image_frame.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=20
        )

        # Original Color

        self.original_color_frame = tk.LabelFrame(
            image_frame,
            text="Original Color Image",
            font=("Arial", 12, "bold"),
            bg="white"
        )

        self.original_color_frame.grid(
            row=0,
            column=0,
            padx=20,
            pady=10,
            sticky="nsew"
        )

        self.original_color_label = tk.Label(
            self.original_color_frame,
            text="No Image",
            bg="white"
        )

        self.original_color_label.pack(
            expand=True,
            fill="both",
            padx=10,
            pady=10
        )

        # Original Grayscale

        self.original_gray_frame = tk.LabelFrame(
            image_frame,
            text="Original Grayscale Image",
            font=("Arial", 12, "bold"),
            bg="white"
        )

        self.original_gray_frame.grid(
            row=0,
            column=1,
            padx=20,
            pady=10,
            sticky="nsew"
        )

        self.original_gray_label = tk.Label(
            self.original_gray_frame,
            text="No Image",
            bg="white"
        )

        self.original_gray_label.pack(
            expand=True,
            fill="both",
            padx=10,
            pady=10
        )

        # Changed Color

        self.result_color_frame = tk.LabelFrame(
            image_frame,
            text="Changed Color Image",
            font=("Arial", 12, "bold"),
            bg="white"
        )

        self.result_color_frame.grid(
            row=1,
            column=0,
            padx=20,
            pady=10,
            sticky="nsew"
        )

        self.result_color_label = tk.Label(
            self.result_color_frame,
            text="Result will appear here",
            bg="white"
        )

        self.result_color_label.pack(
            expand=True,
            fill="both",
            padx=10,
            pady=10
        )

        # Changed Grayscale

        self.result_gray_frame = tk.LabelFrame(
            image_frame,
            text="Changed Grayscale Image",
            font=("Arial", 12, "bold"),
            bg="white"
        )

        self.result_gray_frame.grid(
            row=1,
            column=1,
            padx=20,
            pady=10,
            sticky="nsew"
        )

        self.result_gray_label = tk.Label(
            self.result_gray_frame,
            text="Result will appear here",
            bg="white"
        )

        self.result_gray_label.pack(
            expand=True,
            fill="both",
            padx=10,
            pady=10
        )

        # Make grid expand properly

        image_frame.grid_rowconfigure(
            0,
            weight=1
        )

        image_frame.grid_rowconfigure(
            1,
            weight=1
        )

        image_frame.grid_columnconfigure(
            0,
            weight=1
        )

        image_frame.grid_columnconfigure(
            1,
            weight=1
        )

    # =====================================================
    # UPLOAD IMAGE
    # =====================================================

    def upload_image(self):

        file_path = filedialog.askopenfilename(
            title="Select an Image",
            filetypes=[
                (
                    "Image Files",
                    "*.jpg *.jpeg *.png *.bmp *.tif *.tiff"
                )
            ]
        )

        # User pressed Cancel

        if not file_path:
            return

        try:

            # Read image

            self.img = Image.open(
                file_path
            ).convert("RGB")

            # Convert to grayscale

            self.gray_img = self.img.convert(
                "L"
            )

            # Display original color

            self.display_image(
                self.img,
                self.original_color_label,
                "original_color_photo"
            )

            # Display original grayscale

            self.display_image(
                self.gray_img,
                self.original_gray_label,
                "original_gray_photo"
            )

            # Update titles

            filename = os.path.basename(
                file_path
            )

            self.original_color_frame.config(
                text=f"Original Color Image: {filename}"
            )

            self.original_gray_frame.config(
                text="Original Grayscale Image"
            )

            # Clear previous results

            self.result_color_label.config(
                image="",
                text="Result will appear here"
            )

            self.result_gray_label.config(
                image="",
                text="Result will appear here"
            )

            self.result_color_frame.config(
                text="Changed Color Image"
            )

            self.result_gray_frame.config(
                text="Changed Grayscale Image"
            )

        except Exception as e:

            messagebox.showerror(
                "Error",
                f"Could not open image:\n{e}"
            )

    # =====================================================
    # DISPLAY IMAGE
    # =====================================================

    def display_image(
        self,
        image,
        label,
        reference_name
    ):

        # Copy image so original is not modified

        display_image = image.copy()

        # Resize image to fit GUI

        display_image.thumbnail(
            (500, 260),
            Image.Resampling.LANCZOS
        )

        # Convert PIL image to Tkinter image

        photo = ImageTk.PhotoImage(
            display_image
        )

        # Display image

        label.config(
            image=photo,
            text=""
        )

        # Store reference

        setattr(
            self,
            reference_name,
            photo
        )

    # =====================================================
    # APPLY OPERATION
    # =====================================================

    def apply_operation(self):

        # ================= CHECK IMAGE =================

        if self.img is None:

            messagebox.showerror(
                "No Image",
                "Please upload an image first."
            )

            return

        # ================= GET CONSTANT =================

        try:

            c = float(
                self.constant_entry.get()
            )

        except ValueError:

            messagebox.showerror(
                "Invalid Constant",
                "Please enter a valid constant value."
            )

            return

        # ================= GET OPERATION =================

        operation = self.operation_var.get()

        # ================= DIVISION BY ZERO =================

        if operation == "Division" and c == 0:

            messagebox.showerror(
                "Error",
                "Division by zero is not allowed."
            )

            return

        # ================= CONVERT IMAGE TO NUMPY =================

        color_array = np.array(
            self.img,
            dtype=np.float64
        )

        gray_array = np.array(
            self.gray_img,
            dtype=np.float64
        )

        # ================= PERFORM OPERATION =================

        if operation == "Addition":

            color_result = color_array + c
            gray_result = gray_array + c

        elif operation == "Subtraction":

            color_result = color_array - c
            gray_result = gray_array - c

        elif operation == "Multiplication":

            color_result = color_array * c
            gray_result = gray_array * c

        elif operation == "Division":

            color_result = color_array / c
            gray_result = gray_array / c

        # ================= CLIP PIXEL VALUES =================

        color_result = np.clip(
            color_result,
            0,
            255
        )

        gray_result = np.clip(
            gray_result,
            0,
            255
        )

        # ================= CONVERT TO UINT8 =================

        color_result = color_result.astype(
            np.uint8
        )

        gray_result = gray_result.astype(
            np.uint8
        )

        # ================= CONVERT TO PIL =================

        color_result_image = Image.fromarray(
            color_result
        )

        gray_result_image = Image.fromarray(
            gray_result
        )

        # ================= SAVE RESULTS =================

        result_folder = os.path.join(
            os.getcwd(),
            "result"
        )

        if not os.path.exists(
            result_folder
        ):

            os.makedirs(
                result_folder
            )

        color_filename = os.path.join(
            result_folder,
            f"{operation.lower()}_color.png"
        )

        gray_filename = os.path.join(
            result_folder,
            f"{operation.lower()}_grayscale.png"
        )

        color_result_image.save(
            color_filename
        )

        gray_result_image.save(
            gray_filename
        )

        # ================= DISPLAY COLOR RESULT =================

        self.display_image(
            color_result_image,
            self.result_color_label,
            "result_color_photo"
        )

        self.result_color_frame.config(
            text=(
                f"Changed Color: {operation} "
                f"(Constant = {c})"
            )
        )

        # ================= DISPLAY GRAYSCALE RESULT =================

        self.display_image(
            gray_result_image,
            self.result_gray_label,
            "result_gray_photo"
        )

        self.result_gray_frame.config(
            text=(
                f"Changed Grayscale: {operation} "
                f"(Constant = {c})"
            )
        )

        # ================= SUCCESS MESSAGE =================

        messagebox.showinfo(
            "Success",
            "Operation completed successfully!\n\n"
            f"Results saved in:\n{result_folder}"
        )


# =========================================================
# MAIN PROGRAM
# =========================================================

if __name__ == "__main__":

    root = tk.Tk()

    app = ImageArithmeticGUI(
        root
    )

    root.mainloop()