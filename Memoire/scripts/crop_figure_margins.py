"""Trim near-white borders from PNG figures used in the thesis."""
from pathlib import Path

from PIL import Image, ImageChops

ROOT = Path(__file__).resolve().parents[1]
DIRS = [
    ROOT / "figures" / "eor1",
    ROOT / "figures" / "tora1",
    ROOT / "figures" / "fw1",
    ROOT / "figures" / "server1",
    ROOT / "figures" / "tests",
    ROOT / "figures" / "redundancy_tests",
    ROOT / "figures" / "port_connections",
]
SINGLE_FILES = [
    ROOT / "figures" / "device_inventory.png",
    ROOT / "figures" / "ip.png",
    ROOT / "figures" / "vlan.png",
    ROOT / "figures" / "newuse.png",
    ROOT / "figures" / "leaf_layer.png",
    ROOT / "figures" / "spine_layer.png",
    ROOT / "figures" / "network_edge.png",
    ROOT / "figures" / "cloud_connection.png",
    ROOT / "figures" / "firewall_vrrp.png",
    ROOT / "figures" / "eor_mlag.png",
    ROOT / "figures" / "sequence2.png",
]


def trim(im: Image.Image, threshold: int = 245) -> Image.Image:
    if im.mode != "RGB":
        bg = Image.new("RGB", im.size, (255, 255, 255))
        bg.paste(im, mask=im.split()[-1] if im.mode == "RGBA" else None)
        im = bg
    gray = im.convert("L")
    mask = gray.point(lambda p: 255 if p < threshold else 0)
    bbox = mask.getbbox()
    if not bbox:
        return im
    return im.crop(bbox)


def process(path: Path) -> None:
    im = Image.open(path)
    cropped = trim(im)
    if cropped.size != im.size:
        cropped.save(path, optimize=True)
        print(f"trimmed {path.name}: {im.size} -> {cropped.size}")


def main() -> None:
    for d in DIRS:
        if not d.is_dir():
            continue
        for png in d.glob("*.png"):
            process(png)
    for png in SINGLE_FILES:
        if png.is_file():
            process(png)


if __name__ == "__main__":
    main()
