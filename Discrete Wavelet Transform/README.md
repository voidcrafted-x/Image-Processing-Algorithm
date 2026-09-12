# Manual 2D Haar Discrete Wavelet Transform

A first-principles NumPy implementation of the 2D Haar Discrete Wavelet Transform (DWT) and inverse transform (IDWT). It produces one- and two-level decompositions, reconstructs the image, and verifies the reconstruction error.

## Features

- Greyscale conversion and manual LL, LH, HL, HH subband calculation (no PyWavelets or SciPy)
- Two-level decomposition of the LL approximation subband
- Exact IDWT reconstruction check using mean squared error (MSE)
- Tkinter desktop interface for selecting an image and previewing every result

## Setup

Requires Python 3.10+ and Tkinter (included with standard Python installations on Windows).

```powershell
cd "Discrete Wavelet Transform"
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## Run

Launch the desktop application:

```powershell
python DWT_GUI.py
```

Select **Choose Image**, then **Process Image**. The original image and every generated result appear in the scrollable preview. Files are saved to `Output/`.

The command-line version also remains available:

```powershell
python DWT.py --input Input_images\original.jpg
```

## Subbands

| Subband | Meaning |
| --- | --- |
| LL | Approximation (low-pass rows and columns) |
| LH | Horizontal detail |
| HL | Vertical detail |
| HH | Diagonal detail |

Odd image dimensions are edge-padded for decomposition and cropped back after reconstruction.

## Results

### Original image

![Original input](Input_images/original.jpg)

### Generated output images

| Greyscale image | LL approximation |
| --- | --- |
| ![Greyscale original](Output/dwt_original_grey.png) | ![LL approximation](Output/dwt_LL_approximation.png) |

| LH horizontal detail | HL vertical detail |
| --- | --- |
| ![LH horizontal detail](Output/dwt_LH_horizontal.png) | ![HL vertical detail](Output/dwt_HL_vertical.png) |

| HH diagonal detail | Reconstructed image |
| --- | --- |
| ![HH diagonal detail](Output/dwt_HH_diagonal.png) | ![Reconstructed image](Output/dwt_reconstructed.png) |

### DWT subband mosaics

| One-level decomposition | Two-level decomposition |
| --- | --- |
| ![One-level DWT](Output/dwt_subbands_1level.png) | ![Two-level DWT](Output/dwt_subbands_2level.png) |

### Complete comparison

![DWT comparison overview](Output/dwt_comparison_overview.png)

## Project layout

```text
Discrete Wavelet Transform/
|-- DWT.py
|-- DWT_GUI.py
|-- Input_images/original.jpg
|-- Output/
|-- requirements.txt
`-- README.md
```
