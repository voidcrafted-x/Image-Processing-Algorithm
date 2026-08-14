from flask import Flask, render_template, request, send_from_directory
import cv2
import numpy as np
import os
import uuid

app = Flask(__name__)

# --------------------------------------------------
# Upload Folder
# --------------------------------------------------

UPLOAD_FOLDER = os.path.join(
    app.root_path,
    "static",
    "uploads"
)

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# --------------------------------------------------
# Image Processing
# --------------------------------------------------

def process_image(image_path):

    # Read image
    image = cv2.imread(image_path)

    if image is None:
        return None

    # Get dimensions
    height, width = image.shape[:2]

    # --------------------------------------------------
    # FAST PIXEL PROCESSING USING NUMPY
    # --------------------------------------------------

    # OpenCV -> BGR
    b = image[:, :, 0].astype(np.float32)
    g = image[:, :, 1].astype(np.float32)
    r = image[:, :, 2].astype(np.float32)

    # Grayscale algorithm
    gray = (
        0.299 * r +
        0.587 * g +
        0.114 * b
    ).astype(np.uint8)

    # Red channel
    red = np.zeros_like(image)
    red[:, :, 2] = image[:, :, 2]

    # Green channel
    green = np.zeros_like(image)
    green[:, :, 1] = image[:, :, 1]

    # Blue channel
    blue = np.zeros_like(image)
    blue[:, :, 0] = image[:, :, 0]

    # --------------------------------------------------
    # Generate unique filenames
    # --------------------------------------------------

    uid = str(uuid.uuid4())

    original_name = uid + "_original.jpg"
    gray_name = uid + "_gray.jpg"
    red_name = uid + "_red.jpg"
    green_name = uid + "_green.jpg"
    blue_name = uid + "_blue.jpg"

    # --------------------------------------------------
    # Save images
    # --------------------------------------------------

    cv2.imwrite(
        os.path.join(UPLOAD_FOLDER, original_name),
        image
    )

    cv2.imwrite(
        os.path.join(UPLOAD_FOLDER, gray_name),
        gray
    )

    cv2.imwrite(
        os.path.join(UPLOAD_FOLDER, red_name),
        red
    )

    cv2.imwrite(
        os.path.join(UPLOAD_FOLDER, green_name),
        green
    )

    cv2.imwrite(
        os.path.join(UPLOAD_FOLDER, blue_name),
        blue
    )

    return {
        "original": original_name,
        "gray": gray_name,
        "red": red_name,
        "green": green_name,
        "blue": blue_name,
        "width": width,
        "height": height
    }


# --------------------------------------------------
# Home
# --------------------------------------------------

@app.route("/")
def home():

    return render_template(
        "index.html",
        results=None
    )


# --------------------------------------------------
# Process Image
# --------------------------------------------------

@app.route("/process", methods=["POST"])
def process():

    if "image" not in request.files:

        return render_template(
            "index.html",
            error="No image selected.",
            results=None
        )

    file = request.files["image"]

    if file.filename == "":

        return render_template(
            "index.html",
            error="Please select an image.",
            results=None
        )

    # Unique filename
    uid = str(uuid.uuid4())

    # Keep original extension
    extension = os.path.splitext(
        file.filename
    )[1]

    upload_name = uid + "_input" + extension

    image_path = os.path.join(
        UPLOAD_FOLDER,
        upload_name
    )

    # Save uploaded image
    file.save(image_path)

    # Process image
    results = process_image(image_path)

    if results is None:

        return render_template(
            "index.html",
            error="Invalid image.",
            results=None
        )

    return render_template(
        "index.html",
        results=results
    )


# --------------------------------------------------
# Serve Images
# --------------------------------------------------

@app.route("/image/<filename>")
def serve_image(filename):

    return send_from_directory(
        UPLOAD_FOLDER,
        filename
    )


# --------------------------------------------------
# Run Flask
# --------------------------------------------------

if __name__ == "__main__":

    app.run(
        debug=True
    )