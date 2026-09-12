"""First-principles difference, LoG, and DoG edge detection using NumPy."""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
from PIL import Image


IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".bmp", ".tiff", ".webp"}


def rgb_to_grey(image: np.ndarray) -> np.ndarray:
    """Convert an RGB image array to uint8 greyscale."""
    if image.ndim == 2:
        return image.astype(np.uint8)
    return (0.299 * image[..., 0] + 0.587 * image[..., 1] + 0.114 * image[..., 2]).astype(np.uint8)


def contrast_stretch(image: np.ndarray) -> np.ndarray:
    minimum, maximum = image.min(), image.max()
    if maximum - minimum < 1e-8:
        return np.zeros_like(image, dtype=np.uint8)
    return np.clip(np.rint((image - minimum) / (maximum - minimum) * 255), 0, 255).astype(np.uint8)


def conv2d(image: np.ndarray, kernel: np.ndarray) -> np.ndarray:
    """Same-sized spatial convolution, written from the convolution definition."""
    height, width = kernel.shape
    padded = np.pad(image.astype(float), ((height // 2, height // 2), (width // 2, width // 2)), mode="edge")
    output = np.zeros(image.shape, dtype=float)
    for row in range(height):
        for column in range(width):
            output += kernel[height - 1 - row, width - 1 - column] * padded[row : row + image.shape[0], column : column + image.shape[1]]
    return output


def difference_edges(image: np.ndarray, method: str) -> np.ndarray:
    """Return the gradient magnitude of a forward, backward, or central difference."""
    source = image.astype(float)
    if method == "forward":
        padded = np.pad(source, ((0, 1), (0, 1)), mode="edge")
        gx, gy = padded[:-1, 1:] - padded[:-1, :-1], padded[1:, :-1] - padded[:-1, :-1]
    elif method == "backward":
        padded = np.pad(source, ((1, 0), (1, 0)), mode="edge")
        gx, gy = padded[1:, 1:] - padded[1:, :-1], padded[1:, 1:] - padded[:-1, 1:]
    elif method == "central":
        padded = np.pad(source, 1, mode="edge")
        gx, gy = (padded[1:-1, 2:] - padded[1:-1, :-2]) / 2, (padded[2:, 1:-1] - padded[:-2, 1:-1]) / 2
    else:
        raise ValueError(f"Unsupported difference method: {method}")
    return contrast_stretch(np.hypot(gx, gy))


def gaussian_kernel(sigma: float) -> np.ndarray:
    radius = int(np.ceil(3 * sigma))
    y, x = np.mgrid[-radius : radius + 1, -radius : radius + 1]
    kernel = np.exp(-(x * x + y * y) / (2 * sigma * sigma))
    return kernel / kernel.sum()


def log_kernel(sigma: float) -> np.ndarray:
    radius = int(np.ceil(3 * sigma))
    y, x = np.mgrid[-radius : radius + 1, -radius : radius + 1]
    squared_radius = x * x + y * y
    kernel = -(1 / (np.pi * sigma**4)) * (1 - squared_radius / (2 * sigma * sigma)) * np.exp(-squared_radius / (2 * sigma * sigma))
    return kernel - kernel.mean()


def zero_crossings(response: np.ndarray, threshold_ratio: float = 0.04) -> np.ndarray:
    """Detect sign changes across horizontal, vertical, and diagonal neighbours."""
    threshold = threshold_ratio * np.abs(response).max()
    padded = np.pad(response, 1, mode="edge")
    pairs = ((padded[1:-1, :-2], padded[1:-1, 2:]), (padded[:-2, 1:-1], padded[2:, 1:-1]), (padded[:-2, :-2], padded[2:, 2:]), (padded[:-2, 2:], padded[2:, :-2]))
    edges = np.zeros(response.shape, dtype=bool)
    for first, second in pairs:
        edges |= (first * second < 0) & (np.abs(first - second) > threshold)
    return (edges * 255).astype(np.uint8)


def second_order_edges(image: np.ndarray, operator: str) -> tuple[np.ndarray, np.ndarray]:
    """Return normalized response and zero-crossing map for LoG or DoG."""
    if operator == "log":
        response = conv2d(image, log_kernel(1.4))
    elif operator == "dog":
        response = conv2d(image, gaussian_kernel(1.0)) - conv2d(image, gaussian_kernel(1.6))
    else:
        raise ValueError(f"Unsupported second-order operator: {operator}")
    return contrast_stretch(response), zero_crossings(response)


def mosaic(images: list[np.ndarray], rows: int, columns: int, border: int = 2) -> np.ndarray:
    """Assemble same-sized greyscale images into a bordered RGB grid."""
    height, width = images[0].shape
    tiles = [np.repeat(item[..., None], 3, axis=2) for item in images]
    tiles.extend([np.zeros((height, width, 3), np.uint8)] * (rows * columns - len(tiles)))
    bands = []
    for row in range(rows):
        cells = []
        for column in range(columns):
            cells.append(tiles[row * columns + column])
            if column < columns - 1:
                cells.append(np.full((height, border, 3), 100, np.uint8))
        bands.append(np.hstack(cells))
    separator = np.full((border, bands[0].shape[1], 3), 100, np.uint8)
    return np.vstack([part for row, band in enumerate(bands) for part in (band, separator) if row < rows - 1] + [bands[-1]])


def process(input_path: Path, output_dir: Path) -> dict[str, Path]:
    """Process an image with every implemented edge detector and save PNG outputs."""
    output_dir.mkdir(parents=True, exist_ok=True)
    grey = rgb_to_grey(np.asarray(Image.open(input_path).convert("RGB")))
    forward, backward, central = (difference_edges(grey, name) for name in ("forward", "backward", "central"))
    log_response, log_edges = second_order_edges(grey, "log")
    dog_response, dog_edges = second_order_edges(grey, "dog")
    outputs = {
        "edge_input_greyscale.png": grey,
        "edge_1st_order_forward.png": forward,
        "edge_1st_order_backward.png": backward,
        "edge_1st_order_central.png": central,
        "edge_2nd_order_log_response.png": log_response,
        "edge_2nd_order_log_zerocrossing.png": log_edges,
        "edge_2nd_order_dog_response.png": dog_response,
        "edge_2nd_order_dog_zerocrossing.png": dog_edges,
        "edge_comparison_1st_order.png": mosaic([grey, forward, backward, central], 1, 4),
        "edge_comparison_2nd_order.png": mosaic([log_response, log_edges, dog_response, dog_edges], 2, 2),
        "edge_detection_master_grid.png": mosaic([grey, forward, backward, central, log_response, log_edges, dog_response, dog_edges], 2, 4),
    }
    for name, image in outputs.items():
        Image.fromarray(image).save(output_dir / name)
    return {name: output_dir / name for name in outputs}


def main() -> None:
    parser = argparse.ArgumentParser(description="Manual edge detection using NumPy.")
    parser.add_argument("input", type=Path, help="Image to process")
    parser.add_argument("--output", type=Path, default=Path(__file__).resolve().parent / "Output")
    args = parser.parse_args()
    saved = process(args.input, args.output)
    print(f"Saved {len(saved)} images to {args.output}")


if __name__ == "__main__":
    main()
