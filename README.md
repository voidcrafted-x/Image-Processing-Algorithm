# 🖼️ Python & Digital Image Processing Projects

A collection of Python projects developed while learning **Python programming, Digital Image Processing, Git/GitHub, Flask, OpenCV, and NumPy**.

The main project in this repository is a **web-based Digital Image Processing application** that allows users to upload images and visualize their grayscale and individual RGB channel representations.

---

## 🚀 Featured Project

### 🖼️ Digital Image Processing Web Application

A Flask-based image processing application with an interactive web interface.

Users can upload an image either by:

* 📂 Selecting it from the file manager
* 🖱️ Dragging and dropping it into the browser

The application processes the image and generates:

* 🖼️ Original image
* ⚫ Grayscale image
* 🔴 Red channel
* 🟢 Green channel
* 🔵 Blue channel

Images can also be clicked to open a **fullscreen preview**.

### Key Features

* Drag-and-drop image upload
* File manager image selection
* RGB channel extraction
* Grayscale conversion
* NumPy-based vectorized processing
* Image dimension display
* Fullscreen image preview
* Responsive web interface
* Flask backend for image processing

---

## 🧠 Image Processing

### Grayscale Conversion

The grayscale image is calculated using the standard luminance equation:

```text
Gray = 0.299R + 0.587G + 0.114B
```

The coefficients account for the different sensitivity of the human eye to red, green, and blue light.

### RGB Channel Extraction

For each pixel:

```text
Red   = [0, 0, R]
Green = [0, G, 0]
Blue  = [B, 0, 0]
```

OpenCV stores color images in **BGR format**:

```text
image[i, j] = [B, G, R]
```

---

## ⚡ Performance

The image-processing implementation uses **NumPy vectorization** instead of Python-level nested loops.

### Traditional approach

```python
for i in range(height):
    for j in range(width):
        # process one pixel
```

This requires Python to iterate over every pixel individually.

### Optimized approach

```python
b = image[:, :, 0]
g = image[:, :, 1]
r = image[:, :, 2]

gray = (
    0.299 * r +
    0.587 * g +
    0.114 * b
).astype(np.uint8)
```

NumPy performs the operations on entire arrays using optimized numerical operations, providing significantly better performance for larger images.

---

## 🛠️ Tech Stack

| Technology     | Purpose                                        |
| -------------- | ---------------------------------------------- |
| **Python**     | Core programming and image-processing logic    |
| **Flask**      | Web application backend                        |
| **OpenCV**     | Image reading and writing                      |
| **NumPy**      | Efficient numerical and image-array operations |
| **HTML**       | Web page structure                             |
| **CSS**        | User interface and responsive design           |
| **JavaScript** | Drag-and-drop and fullscreen image preview     |
| **Git**        | Version control                                |
| **GitHub**     | Source code hosting                            |

---

## 📂 Repository Structure

```text
Digital Image Processing/
│
├── README.md
├── .gitignore
├── requirements.txt
│
├── Hello_World.py
├── Tambola_Ticket_Generator.py
│
└── Image Processing Algorithm/
    │
    ├── app.py
    │
    ├── templates/
    │   └── index.html
    │
    └── static/
        └── uploads/
            └── .gitkeep
```

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/voidcrafted-x/Image-Processing-Algorithm.git
```

### 2. Navigate to the repository

```bash
cd Image-Processing-Algorithm
```

### 3. Create a virtual environment

#### Windows

```bash
python -m venv venv
```

Activate it:

```bash
venv\Scripts\activate
```

#### Linux / macOS

```bash
python3 -m venv venv
```

Activate it:

```bash
source venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Run the Image Processing Application

Navigate to the Flask application:

```bash
cd "Image Processing Algorithm"
```

Run:

```bash
python app.py
```

The Flask development server will start at:

```text
http://127.0.0.1:5000
```

Open the address in your browser.

---

## 🖥️ How It Works

```text
              User
                │
                ▼
        Upload Image
        ┌───────┴───────┐
        │               │
   File Manager    Drag & Drop
        │               │
        └───────┬───────┘
                ▼
             Flask
                │
                ▼
             OpenCV
                │
                ▼
             NumPy
                │
       ┌────────┼────────┐
       ▼        ▼        ▼
   Grayscale   Red     Green    Blue
       │        │        │        │
       └────────┴────────┴────────┘
                │
                ▼
        Results in Browser
```

---

## 📚 Other Python Programs

### 🎟️ Tambola Ticket Generator

`Tambola_Ticket_Generator.py`

A Python program that generates Tambola/Housie tickets using algorithmic logic.

### 👋 Hello World

`Hello_World.py`

A basic Python program created while learning Python fundamentals.

---

## 🔒 Git & Project Hygiene

The repository intentionally excludes:

```text
venv/
.env
__pycache__/
generated uploads
```

These files are ignored using `.gitignore` because they are environment-specific, temporary, or may contain sensitive information.

---

## 🔮 Future Improvements

Planned image-processing features include:

* 📊 Image histogram
* ⚫ Thresholding
* 🔄 Image negative
* ☀️ Brightness adjustment
* 🎚️ Contrast enhancement
* 🌫️ Gaussian filtering
* 🧹 Median filtering
* 📐 Image resizing
* 🔃 Image rotation
* ✏️ Image sharpening
* 📈 Edge detection
* 🔵 Sobel operator
* ⚡ Canny edge detection

---

## 🎯 Learning Goals

This repository is part of my learning journey toward building strong foundations in:

* Python
* Data Structures & Algorithms
* Software Development
* Digital Image Processing
* Computer Vision
* Machine Learning
* AI Engineering

---

## 👨‍💻 Author

**Nimesh**

Engineering Student | Python | AI/ML | Software Development

---

## 📄 License

This project is licensed under the **MIT License**.
