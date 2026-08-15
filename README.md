# 🖼️ Digital Image Processing

A web-based **Digital Image Processing application** built with **Python, Flask, OpenCV, NumPy, HTML, CSS, and JavaScript**.

The application allows users to upload an image using **file selection or drag-and-drop** and generates different image representations including **grayscale, red, green, and blue channels**.

---

## ✨ Features

* 📂 Upload image from File Manager
* 🖱️ Drag & Drop image upload
* 🖼️ Original image preview
* ⚫ Grayscale conversion
* 🔴 Red channel extraction
* 🟢 Green channel extraction
* 🔵 Blue channel extraction
* 🔍 Click image to open fullscreen preview
* 📐 Display image dimensions
* ⚡ Fast NumPy-based image processing
* 📱 Responsive web interface
* 🌐 Flask-based backend

---

## 🖥️ Application Preview

### Original Image

The application accepts an image through the file manager or by dragging it into the upload area.

### Processing Results

The uploaded image is processed into:

### Original

![Original](Image%20Processing%20Algorithm/results/original.jpg)

| Grayscale                                                          | Red Channel                                                            |
| ------------------------------------------------------------------ | ---------------------------------------------------------------------- |
| ![Grayscale](Image%20Processing%20Algorithm/results/grayscale.jpg) | ![Red Channel](Image%20Processing%20Algorithm/results/red_channel.jpg) |

| Green Channel                                                              | Blue Channel                                                             |
| -------------------------------------------------------------------------- | ------------------------------------------------------------------------ |
| ![Green Channel](Image%20Processing%20Algorithm/results/green_channel.jpg) | ![Blue Channel](Image%20Processing%20Algorithm/results/blue_channel.jpg) |

> Click any result image in the web application to view it in fullscreen.

---

# 🧠 Image Processing

## 1. Grayscale Conversion

The grayscale value of each pixel is calculated using the standard weighted RGB formula:

```text
Gray = 0.299R + 0.587G + 0.114B
```

The different weights account for the human eye's different sensitivity to red, green, and blue light.

---

## 2. RGB Channel Extraction

For every pixel, only one color component is preserved.

### 🔴 Red Channel

```text
Red = [0, 0, R]
```

### 🟢 Green Channel

```text
Green = [0, G, 0]
```

### 🔵 Blue Channel

```text
Blue = [B, 0, 0]
```

> **Note:** OpenCV stores color images in **BGR order**, so the channel positions are handled accordingly.

---

# ⚡ Performance Optimization

The application uses **NumPy vectorization** for faster image processing.

Instead of processing every pixel using Python nested loops:

```python
for i in range(height):
    for j in range(width):
        ...
```

the application processes entire image arrays:

```python
b = image[:, :, 0].astype(np.float32)
g = image[:, :, 1].astype(np.float32)
r = image[:, :, 2].astype(np.float32)

gray = (
    0.299 * r +
    0.587 * g +
    0.114 * b
).astype(np.uint8)
```

This significantly reduces Python-level loop overhead and improves processing speed for larger images.

---

# 🏗️ Application Architecture

```text
                    User
                     │
                     ▼
              Upload Image
             ┌───────┴───────┐
             │               │
       File Manager      Drag & Drop
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
        ┌────────────┼────────────┐
        ▼            ▼            ▼
    Grayscale       RGB       Original
                   Channels
        │
        ├── Red
        ├── Green
        └── Blue
                     │
                     ▼
              Browser Results
```

---

# 🛠️ Tech Stack

| Technology     | Purpose                            |
| -------------- | ---------------------------------- |
| **Python**     | Core programming                   |
| **Flask**      | Backend and web server             |
| **OpenCV**     | Image reading and writing          |
| **NumPy**      | Fast numerical/image processing    |
| **HTML**       | Web structure                      |
| **CSS**        | User interface                     |
| **JavaScript** | Drag & Drop and fullscreen preview |
| **Git**        | Version control                    |
| **GitHub**     | Source code hosting                |

---

# 📂 Project Structure

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
    ├── results/
    │   ├── original.jpg
    │   ├── grayscale.jpg
    │   ├── red_channel.jpg
    │   ├── green_channel.jpg
    │   └── blue_channel.jpg
    │
    ├── templates/
    │   └── index.html
    │
    └── static/
        └── uploads/
            └── .gitkeep
```

---

# ⚙️ Installation

## 1. Clone the repository

```bash
git clone https://github.com/voidcrafted-x/Image-Processing-Algorithm.git
```

## 2. Navigate to the project

```bash
cd Image-Processing-Algorithm
```

## 3. Create a virtual environment

### Windows

```bash
python -m venv venv
```

Activate:

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv
```

Activate:

```bash
source venv/bin/activate
```

## 4. Install dependencies

```bash
pip install -r requirements.txt
```

---

# ▶️ Run the Application

Navigate to the Flask application:

```bash
cd "Image Processing Algorithm"
```

Start the server:

```bash
python app.py
```

Open your browser:

```text
http://127.0.0.1:5000
```

---

# 📌 Usage

1. Open the web application.

2. Select an image from your computer **or** drag and drop an image.

3. Click **Process Image**.

4. The application generates:

   * Original
   * Grayscale
   * Red channel
   * Green channel
   * Blue channel

5. Click any result to view it in fullscreen.

---

# 📚 Additional Python Projects

This repository also contains some Python learning projects.

### 🎟️ Tambola Ticket Generator

`Tambola_Ticket_Generator.py`

Generates Tambola/Housie tickets using Python.

### 👋 Hello World

`Hello_World.py`

A basic Python program created while learning Python fundamentals.

---

# 👨‍💻 Author

**Nimesh**
