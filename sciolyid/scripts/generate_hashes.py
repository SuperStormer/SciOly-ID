import csv
import imghdr
import os

import imagehash
from PIL import Image


def file_type(filename):
    if os.path.isdir(filename):
        return "dir"
    if imghdr.what(filename) not in ("jpeg", "png"):
        return None
    try:
        Image.open(filename).verify()
    except:
        return None
    return "img"


def get_image_files(start_path):
    start_path = start_path[:-1] if start_path[-1] == "/" else start_path
    image_paths = []
    stack = []
    visited = []
    stack.append(start_path)
    visited.append(start_path)
    while stack:
        current = stack.pop()
        for child in os.listdir(current):
            child = current + "/" + child
            if child not in visited:
                visited.append(child)
                thing = file_type(child)
                if thing == "img":
                    image_paths.append(child)
                elif thing == "dir":
                    stack.append(child)
    return image_paths


def calculate_image_hashes(images, start_path, base_url):
    hashes = []
    for path in images:
        image_hash = imagehash.phash(Image.open(path))
        hashes.append((base_url + path.strip(start_path).strip("/"), str(image_hash)))
    return hashes


def write_hashes(start_path, base_url):
    images = get_image_files(start_path)
    hashes = calculate_image_hashes(images, start_path, base_url)
    with open("hashes.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerows(hashes)


write_hashes(".", "./")
