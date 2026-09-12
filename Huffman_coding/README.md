# Manual Huffman Coding for Images

A first-principles Digital Image Processing implementation of Huffman source coding. It derives symbol probabilities from a greyscale image, builds an optimal binary tree using a min-heap, encodes/decodes the pixels, and verifies lossless reconstruction.

## Features

- Manual Huffman tree, prefix-code generation, encoding, and decoding
- Shannon entropy, average code length, coding efficiency, compression ratio, and theoretical space savings
- Tkinter desktop interface with result previews
- No compression or image-processing libraries beyond NumPy/Pillow

## Setup and run

```powershell
cd Huffman_coding
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python huffman_gui.py
```

Choose an image, select **Encode with Huffman**, and view the five saved outputs. Command-line usage is also available:

```powershell
python huffman_coding.py path\to\image.jpg
```

## Example output

| Greyscale source | Losslessly decoded image |
| --- | --- |
| ![Greyscale source](Output/huffman_original_grey.png) | ![Decoded image](Output/huffman_decoded.png) |

| Bit-length spatial map | Codeword-length distribution |
| --- | --- |
| ![Bit-length map](Output/huffman_bit_length_map.png) | ![Codeword distribution](Output/huffman_length_distribution.png) |

### Compression metrics

![Huffman coding metrics](Output/huffman_metrics_summary.png)

## Project layout

```text
Huffman_coding/
|-- huffman_coding.py
|-- huffman_gui.py
|-- Input_images/
|-- Output/
|-- requirements.txt
`-- README.md
```
