"""Manual 2D Haar DWT/IDWT implementation for digital image processing."""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib
import numpy as np
from PIL import Image

matplotlib.use("Agg")
import matplotlib.pyplot as plt


IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".bmp", ".tiff", ".webp"}


def rgb_to_grey(image: np.ndarray) -> np.ndarray:
    """Return a uint8 greyscale image using standard luminance weights."""
    if image.ndim == 2:
        return image.astype(np.uint8)
    return (0.299 * image[..., 0] + 0.587 * image[..., 1] + 0.114 * image[..., 2]).astype(np.uint8)


def pad_to_even(image: np.ndarray) -> tuple[np.ndarray, tuple[int, int]]:
    """Edge-pad odd image dimensions and retain the original shape."""
    shape = image.shape
    return np.pad(image, ((0, shape[0] % 2), (0, shape[1] % 2)), mode="edge"), shape


def dwt2d_haar(image: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, tuple[int, int]]:
    """Perform one orthonormal 2D Haar decomposition: LL, LH, HL, HH."""
    image, original_shape = pad_to_even(image.astype(np.float64))
    scale = np.sqrt(2.0)
    low_rows = (image[:, 0::2] + image[:, 1::2]) / scale
    high_rows = (image[:, 0::2] - image[:, 1::2]) / scale
    ll = (low_rows[0::2] + low_rows[1::2]) / scale
    lh = (low_rows[0::2] - low_rows[1::2]) / scale
    hl = (high_rows[0::2] + high_rows[1::2]) / scale
    hh = (high_rows[0::2] - high_rows[1::2]) / scale
    return ll, lh, hl, hh, original_shape


def idwt2d_haar(
    ll: np.ndarray, lh: np.ndarray, hl: np.ndarray, hh: np.ndarray, original_shape: tuple[int, int] | None = None
) -> np.ndarray:
    """Reconstruct an image from one orthonormal 2D Haar decomposition."""
    scale = np.sqrt(2.0)
    low_rows = np.empty((ll.shape[0] * 2, ll.shape[1]), dtype=float)
    high_rows = np.empty_like(low_rows)
    low_rows[0::2], low_rows[1::2] = (ll + lh) / scale, (ll - lh) / scale
    high_rows[0::2], high_rows[1::2] = (hl + hh) / scale, (hl - hh) / scale
    image = np.empty((low_rows.shape[0], low_rows.shape[1] * 2), dtype=float)
    image[:, 0::2], image[:, 1::2] = (low_rows + high_rows) / scale, (low_rows - high_rows) / scale
    return image if original_shape is None else image[: original_shape[0], : original_shape[1]]


def normalize_approximation(subband: np.ndarray) -> np.ndarray:
    return np.clip(subband / 2, 0, 255).astype(np.uint8)


def normalize_detail(subband: np.ndarray) -> np.ndarray:
    magnitude = np.abs(subband)
    maximum = magnitude.max()
    return np.zeros_like(magnitude, dtype=np.uint8) if maximum == 0 else (magnitude / maximum * 255).astype(np.uint8)


def mosaic(ll: np.ndarray, lh: np.ndarray, hl: np.ndarray, hh: np.ndarray, border: int = 2) -> np.ndarray:
    """Create the conventional LL/HL/LH/HH DWT mosaic."""
    left = np.vstack((normalize_approximation(ll), np.full((border, ll.shape[1]), 128, np.uint8), normalize_detail(lh)))
    right = np.vstack((normalize_detail(hl), np.full((border, hl.shape[1]), 128, np.uint8), normalize_detail(hh)))
    return np.hstack((left, np.full((left.shape[0], border), 128, np.uint8), right))


def level_two_mosaic(image: np.ndarray) -> tuple[np.ndarray, dict[str, tuple[np.ndarray, ...]]]:
    """Decompose LL once more and place its mosaic in the first-level LL area."""
    ll1, lh1, hl1, hh1, shape1 = dwt2d_haar(image)
    ll2, lh2, hl2, hh2, shape2 = dwt2d_haar(ll1)
    nested = mosaic(ll2, lh2, hl2, hh2)
    target = hl1.shape
    nested = np.pad(nested, ((0, max(0, target[0] - nested.shape[0])), (0, max(0, target[1] - nested.shape[1]))), mode="edge")
    nested = nested[: target[0], : target[1]]
    left = np.vstack((nested, np.full((2, target[1]), 128, np.uint8), normalize_detail(lh1)))
    right = np.vstack((normalize_detail(hl1), np.full((2, target[1]), 128, np.uint8), normalize_detail(hh1)))
    grid = np.hstack((left, np.full((left.shape[0], 2), 128, np.uint8), right))
    return grid, {"level1": (ll1, lh1, hl1, hh1, shape1), "level2": (ll2, lh2, hl2, hh2, shape2)}


def comparison_figure(original: np.ndarray, level1: np.ndarray, level2: np.ndarray, reconstructed: np.ndarray, mse: float) -> Image.Image:
    fig, axes = plt.subplots(2, 2, figsize=(11, 10))
    panels = ((original, "Original (greyscale)"), (level1, "1-level DWT"), (level2, "2-level DWT"), (reconstructed, f"IDWT reconstruction\nMSE: {mse:.2e}"))
    for axis, (data, title) in zip(axes.flat, panels):
        axis.imshow(data, cmap="gray", vmin=0, vmax=255)
        axis.set_title(title)
        axis.axis("off")
    fig.suptitle("2D Haar Discrete Wavelet Transform", fontsize=16, fontweight="bold")
    fig.tight_layout()
    fig.canvas.draw()
    image = Image.fromarray(np.asarray(fig.canvas.buffer_rgba())[..., :3])
    plt.close(fig)
    return image


def find_input(path: Path | None, project_dir: Path) -> Path:
    if path:
        if not path.is_file():
            raise FileNotFoundError(f"Input image not found: {path}")
        return path
    candidates = [item for directory in (project_dir / "Input_images", project_dir / "Input") if directory.is_dir() for item in directory.iterdir() if item.suffix.lower() in IMAGE_EXTENSIONS]
    if not candidates:
        raise FileNotFoundError("Add an image to Input_images/ or supply one with --input.")
    return next((item for item in candidates if "scenar" in item.name.lower() or "tree" in item.name.lower()), candidates[0])


def process(input_path: Path, output_dir: Path) -> tuple[float, float]:
    output_dir.mkdir(parents=True, exist_ok=True)
    grey = rgb_to_grey(np.asarray(Image.open(input_path).convert("RGB")))
    ll, lh, hl, hh, shape = dwt2d_haar(grey)
    reconstructed = idwt2d_haar(ll, lh, hl, hh, shape)
    mse = float(np.mean((grey - reconstructed) ** 2))
    maximum_error = float(np.max(np.abs(grey - reconstructed)))
    assert mse < 1e-10, "Haar DWT/IDWT reconstruction failed."
    reconstructed_uint8 = np.clip(np.rint(reconstructed), 0, 255).astype(np.uint8)
    level1 = mosaic(ll, lh, hl, hh)
    level2, _ = level_two_mosaic(grey)
    images = {
        "dwt_original_grey.png": Image.fromarray(grey),
        "dwt_LL_approximation.png": Image.fromarray(normalize_approximation(ll)),
        "dwt_LH_horizontal.png": Image.fromarray(normalize_detail(lh)),
        "dwt_HL_vertical.png": Image.fromarray(normalize_detail(hl)),
        "dwt_HH_diagonal.png": Image.fromarray(normalize_detail(hh)),
        "dwt_subbands_1level.png": Image.fromarray(level1),
        "dwt_subbands_2level.png": Image.fromarray(level2),
        "dwt_reconstructed.png": Image.fromarray(reconstructed_uint8),
        "dwt_comparison_overview.png": comparison_figure(grey, level1, level2, reconstructed_uint8, mse),
    }
    for name, image in images.items():
        image.save(output_dir / name)
    return mse, maximum_error


def main() -> None:
    parser = argparse.ArgumentParser(description="Manual 2D Haar DWT and IDWT.")
    parser.add_argument("--input", type=Path, help="Path to an input image.")
    parser.add_argument("--output", type=Path, help="Directory for generated PNG files.")
    args = parser.parse_args()
    project_dir = Path(__file__).resolve().parent
    input_path = find_input(args.input, project_dir)
    output_dir = args.output or project_dir / "Output"
    mse, maximum_error = process(input_path, output_dir)
    print(f"Input: {input_path}")
    print(f"Perfect reconstruction verified. MSE: {mse:.4e}; max difference: {maximum_error:.4e}")
    print(f"Saved results to: {output_dir}")


if __name__ == "__main__":
    main()
