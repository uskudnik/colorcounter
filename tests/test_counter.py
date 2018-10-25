from collections import Counter
from PIL import Image

import os
import glob

from ccounter import counter
from ccounter import utils


BASE_PATH=os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))


def reference_counter(img_path):
    img = Image.open(img_path)
    counter = Counter(img.getdata())
    ref_colors = [c for c in counter.most_common(6)]
    return ref_colors


def test_simple_imag():
    # image with olympic circles
    img_path = os.path.join(
        BASE_PATH, 'tests/fixtures/imgs/FApqk3D.jpg')

    ref_colors = reference_counter(img_path)

    with open(img_path, 'rb') as f:
        colors = counter.color_counter(f, 6)
    print([utils.rgb_to_hex(c) for c, _ in colors])
    assert ref_colors == colors


def test_multiple_images():
    img_pattern = os.path.join(
        BASE_PATH, 'tests/fixtures/imgs/*')

    imgs = glob.glob(img_pattern)
    for img_path in imgs:
        ref_colors = reference_counter(img_path)
        with open(img_path, 'rb') as f:
            colors = counter.color_counter(f, 6)
        assert ref_colors == colors
