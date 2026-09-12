"""Manual Shannon-Fano source coding for greyscale images."""
from __future__ import annotations
import argparse
from pathlib import Path
import matplotlib
import numpy as np
from PIL import Image
matplotlib.use("Agg")
import matplotlib.pyplot as plt

def grey(image: np.ndarray) -> np.ndarray:
    return image.astype(np.uint8) if image.ndim == 2 else (0.299 * image[..., 0] + .587 * image[..., 1] + .114 * image[..., 2]).astype(np.uint8)

def codebook(probabilities: dict[int, float]) -> dict[int, str]:
    """Recursively split symbols into probability-balanced Shannon-Fano groups."""
    items, codes = sorted(probabilities.items(), key=lambda item: item[1], reverse=True), {}
    def split(group: list[tuple[int, float]], prefix: str) -> None:
        if len(group) == 1: codes[group[0][0]] = prefix or "0"; return
        total, running, index, best = sum(p for _, p in group), 0., 1, float("inf")
        for i, (_, probability) in enumerate(group[:-1], 1):
            running += probability
            if abs(total - 2 * running) < best: best, index = abs(total - 2 * running), i
        split(group[:index], prefix + "0"); split(group[index:], prefix + "1")
    split(items, "")
    return codes

def decode(stream: str, codes: dict[int, str], shape: tuple[int, int]) -> np.ndarray:
    reverse, token, result = {code: symbol for symbol, code in codes.items()}, "", []
    for bit in stream:
        token += bit
        if token in reverse: result.append(reverse[token]); token = ""
    return np.asarray(result, dtype=np.uint8).reshape(shape)

def report_figures(image: np.ndarray, codes: dict[int, str], frequencies: dict[int, int], data: dict[str, float], output: Path) -> dict[str, Path]:
    lut = np.array([len(codes.get(i, "")) for i in range(256)]); bit_map = lut[image]
    fig, ax = plt.subplots(figsize=(7, 5)); plot = ax.imshow(bit_map, cmap="plasma"); fig.colorbar(plot, ax=ax, label="Bits per pixel"); ax.set_title("Shannon-Fano codeword length map"); ax.axis("off"); fig.tight_layout(); heatmap = output / "shannon_fano_bit_length_map.png"; fig.savefig(heatmap, dpi=140); plt.close(fig)
    lengths: dict[int, float] = {}
    for symbol, count in frequencies.items(): lengths[len(codes[symbol])] = lengths.get(len(codes[symbol]), 0) + count / image.size * 100
    fig, ax = plt.subplots(figsize=(7, 4.5)); ax.bar(lengths.keys(), lengths.values()); ax.set(title="Shannon-Fano codeword length distribution", xlabel="Codeword length (bits)", ylabel="Pixel frequency (%)"); fig.tight_layout(); distribution = output / "shannon_fano_length_distribution.png"; fig.savefig(distribution, dpi=140); plt.close(fig)
    fig, ax = plt.subplots(figsize=(8, 4)); ax.axis("off"); text = "\n".join(("Shannon-Fano Coding Metrics", f"Entropy: {data['entropy']:.3f} bits/pixel", f"Average code length: {data['average']:.3f} bits/pixel", f"Coding efficiency: {data['efficiency']:.2f}%", f"Compression ratio: {data['ratio']:.2f} : 1", f"Theoretical space saved: {data['savings']:.2f}%", "Lossless reconstruction: verified")); ax.text(.5, .5, text, ha="center", va="center", fontsize=16, linespacing=1.8, bbox={"boxstyle":"round,pad=1", "facecolor":"#eaf3ff"}); fig.tight_layout(); summary = output / "shannon_fano_metrics_summary.png"; fig.savefig(summary, dpi=140); plt.close(fig)
    return {heatmap.name: heatmap, distribution.name: distribution, summary.name: summary}

def process(input_path: Path, output_dir: Path) -> tuple[dict[str, Path], dict[str, float]]:
    output_dir.mkdir(parents=True, exist_ok=True); image = grey(np.asarray(Image.open(input_path).convert("RGB")))
    counts = np.bincount(image.ravel(), minlength=256); frequencies = {i:int(n) for i,n in enumerate(counts) if n}; probabilities = {i:n/image.size for i,n in frequencies.items()}; codes = codebook(probabilities)
    stream = "".join(codes[int(value)] for value in image.ravel()); reconstructed = decode(stream, codes, image.shape); assert np.array_equal(image, reconstructed), "Lossless reconstruction failed."
    entropy = -sum(p * np.log2(p) for p in probabilities.values()); average = sum(probabilities[i] * len(codes[i]) for i in probabilities); data = {"entropy":entropy, "average":average, "efficiency":entropy / average * 100, "ratio":8 / average, "savings":(1 - len(stream)/(image.size*8))*100}
    original, decoded = output_dir / "shannon_fano_original_grey.png", output_dir / "shannon_fano_decoded.png"; Image.fromarray(image).save(original); Image.fromarray(reconstructed).save(decoded)
    saved = {original.name: original, decoded.name: decoded}; saved.update(report_figures(image, codes, frequencies, data, output_dir)); return saved, data

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Manual Shannon-Fano image coding."); parser.add_argument("input", type=Path); parser.add_argument("--output", type=Path, default=Path(__file__).resolve().parent / "Output"); args = parser.parse_args(); _, metrics = process(args.input, args.output); print(f"Lossless reconstruction verified. Compression ratio: {metrics['ratio']:.2f}:1")
