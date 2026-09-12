"""Manual Huffman source coding for greyscale images."""

from __future__ import annotations

import argparse
import heapq
from pathlib import Path

import matplotlib
import numpy as np
from PIL import Image

matplotlib.use("Agg")
import matplotlib.pyplot as plt


class Node:
    """A Huffman tree node; uid makes equal-frequency ordering deterministic."""
    def __init__(self, symbol: int | None, frequency: int, left=None, right=None, uid: int = 0):
        self.symbol, self.frequency, self.left, self.right, self.uid = symbol, frequency, left, right, uid

    def __lt__(self, other: "Node") -> bool:
        return (self.frequency, self.uid) < (other.frequency, other.uid)


def rgb_to_grey(image: np.ndarray) -> np.ndarray:
    return image.astype(np.uint8) if image.ndim == 2 else (0.299 * image[..., 0] + 0.587 * image[..., 1] + 0.114 * image[..., 2]).astype(np.uint8)


def build_tree(frequencies: dict[int, int]) -> Node:
    heap = [Node(symbol, frequency, uid=index) for index, (symbol, frequency) in enumerate(frequencies.items())]
    heapq.heapify(heap)
    if len(heap) == 1:
        return Node(None, heap[0].frequency, left=heap[0], uid=1)
    uid = len(heap)
    while len(heap) > 1:
        left, right = heapq.heappop(heap), heapq.heappop(heap)
        heapq.heappush(heap, Node(None, left.frequency + right.frequency, left, right, uid))
        uid += 1
    return heap[0]


def codebook(root: Node) -> dict[int, str]:
    codes: dict[int, str] = {}
    def visit(node: Node, prefix: str) -> None:
        if node.symbol is not None:
            codes[node.symbol] = prefix or "0"
        else:
            visit(node.left, prefix + "0")
            visit(node.right, prefix + "1")
    visit(root, "")
    return codes


def decode(bitstream: str, root: Node, shape: tuple[int, int]) -> np.ndarray:
    values, node = [], root
    for bit in bitstream:
        node = node.left if bit == "0" else node.right
        if node.symbol is not None:
            values.append(node.symbol)
            node = root
    return np.asarray(values, dtype=np.uint8).reshape(shape)


def metrics(frequencies: dict[int, int], codes: dict[int, str], pixels: int) -> dict[str, float]:
    probabilities = {symbol: frequency / pixels for symbol, frequency in frequencies.items()}
    entropy = -sum(probability * np.log2(probability) for probability in probabilities.values())
    average = sum(probabilities[symbol] * len(codes[symbol]) for symbol in probabilities)
    compressed = sum(frequencies[symbol] * len(codes[symbol]) for symbol in frequencies)
    return {"entropy": entropy, "average_length": average, "efficiency": entropy / average * 100, "compression_ratio": 8 / average, "space_savings": (1 - compressed / (pixels * 8)) * 100}


def save_figures(grey: np.ndarray, codes: dict[int, str], frequencies: dict[int, int], data: dict[str, float], output: Path) -> dict[str, Path]:
    lengths = np.array([len(codes[symbol]) for symbol in range(256)])
    bit_map = lengths[grey]
    fig, ax = plt.subplots(figsize=(7, 5)); image = ax.imshow(bit_map, cmap="plasma"); fig.colorbar(image, ax=ax, label="Bits per pixel"); ax.set_title("Huffman codeword length map"); ax.axis("off"); fig.tight_layout()
    heatmap = output / "huffman_bit_length_map.png"; fig.savefig(heatmap, dpi=140); plt.close(fig)
    probability_by_length: dict[int, float] = {}
    for symbol, frequency in frequencies.items(): probability_by_length[len(codes[symbol])] = probability_by_length.get(len(codes[symbol]), 0) + frequency / grey.size
    fig, ax = plt.subplots(figsize=(7, 4.5)); ax.bar(probability_by_length.keys(), [value * 100 for value in probability_by_length.values()]); ax.set(title="Huffman codeword length distribution", xlabel="Codeword length (bits)", ylabel="Pixel frequency (%)"); fig.tight_layout()
    distribution = output / "huffman_length_distribution.png"; fig.savefig(distribution, dpi=140); plt.close(fig)
    fig, ax = plt.subplots(figsize=(8, 4)); ax.axis("off"); text = "\n".join(("Huffman Coding Metrics", f"Entropy: {data['entropy']:.3f} bits/pixel", f"Average code length: {data['average_length']:.3f} bits/pixel", f"Coding efficiency: {data['efficiency']:.2f}%", f"Compression ratio: {data['compression_ratio']:.2f} : 1", f"Theoretical space saved: {data['space_savings']:.2f}%", "Lossless reconstruction: verified")); ax.text(.5, .5, text, ha="center", va="center", fontsize=16, linespacing=1.8, bbox={"boxstyle": "round,pad=1", "facecolor": "#eaf3ff"}); fig.tight_layout()
    summary = output / "huffman_metrics_summary.png"; fig.savefig(summary, dpi=140); plt.close(fig)
    return {"huffman_bit_length_map.png": heatmap, "huffman_length_distribution.png": distribution, "huffman_metrics_summary.png": summary}


def process(input_path: Path, output_dir: Path) -> tuple[dict[str, Path], dict[str, float]]:
    """Encode, decode, verify, and save Huffman coding visual outputs."""
    output_dir.mkdir(parents=True, exist_ok=True)
    grey = rgb_to_grey(np.asarray(Image.open(input_path).convert("RGB")))
    counts = np.bincount(grey.ravel(), minlength=256)
    frequencies = {index: int(count) for index, count in enumerate(counts) if count}
    tree = build_tree(frequencies); codes = codebook(tree)
    stream = "".join(codes[int(symbol)] for symbol in grey.ravel())
    reconstructed = decode(stream, tree, grey.shape)
    assert np.array_equal(grey, reconstructed), "Lossless reconstruction failed."
    data = metrics(frequencies, codes, grey.size)
    original, decoded = output_dir / "huffman_original_grey.png", output_dir / "huffman_decoded.png"
    Image.fromarray(grey).save(original); Image.fromarray(reconstructed).save(decoded)
    saved = {"huffman_original_grey.png": original, "huffman_decoded.png": decoded}
    saved.update(save_figures(grey, codes, frequencies, data, output_dir))
    return saved, data


def main() -> None:
    parser = argparse.ArgumentParser(description="Manual Huffman coding for images.")
    parser.add_argument("input", type=Path); parser.add_argument("--output", type=Path, default=Path(__file__).resolve().parent / "Output")
    args = parser.parse_args()
    _, data = process(args.input, args.output)
    print(f"Lossless reconstruction verified. Compression ratio: {data['compression_ratio']:.2f}:1")


if __name__ == "__main__": main()
