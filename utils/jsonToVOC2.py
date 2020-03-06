#!/usr/bin/env/python
# Copyright 2020 Diogo Peixoto

"""
Script to Convert boxy annotations to VOC format for YOLOv3 use.
"""

import argparse
import json
from pathlib import Path
import xml.etree.ElementTree as ET


def write_VOC_file(data, outputdir):
    """Takes in data and outputs VOC file

    :param data: dictionary with annotation data
    :param outputdir: folder to write output VOC xml files
    :return:
    """

    # dimensions are hardcoded for now.
    width = 1232
    height = 1028
    depth = 3
    # single_dir_name = "bluefox_2016-10-30-10-01-47_bag"
    for image in data:
        root = ET.Element("annotation")

        fp = Path(image["path"])
        dirname = fp.parent
        fname = Path(fp.name)
        short_img_name = str(fname)

        ET.SubElement(root, "filename").text = short_img_name
        ET.SubElement(root, "width").text = str(width)
        ET.SubElement(root, "height").text = str(height)
        ET.SubElement(root, "depth").text = str(depth)

        for obj in image["objects"]:
            obj_node = ET.SubElement(root, "object")
            ET.SubElement(obj_node, "name").text = obj["name"]

            bbox_node = ET.SubElement(obj_node, "bndbox")
            for elem, value in obj["bndbox"].items():
                ET.SubElement(bbox_node, elem).text = str(value)

        # Decompose path in folder / file name

        xml_fpath = outputdir / fname.with_suffix('.xml')
        tree = ET.ElementTree(root)
        # if str(dirname) == single_dir_name:
        tree.write(xml_fpath)


def parse_json_annotations(path, resize_factor=1):
    """Parses json annotation file to select relevant features for conversion

    :param path: string with json file
    :return: dictionary with parsed annotations
    """

    print(f"Loading json file: {path}")

    annotations = []

    with path.open() as input_handle:
        labels_dict = json.load(input_handle)

    for img_index, img in enumerate(labels_dict, start=1):
        img_dict = dict()
        img_dict["path"] = img
        img_dict["objects"] = []

        elements = labels_dict[img]

        try:
            vehicles = elements["vehicles"]

            for v_index, v_dict in enumerate(vehicles, start=1):

                obj = v_dict["AABB"]

                obj_dict = {
                    #"name": f"vehicle_{v_index}",
                    "name": "car",
                    "bndbox": {
                        "xmin": int(round(float(obj["x1"] / resize_factor))),
                        "xmax": int(round(float(obj["x2"]) / resize_factor)),
                        "ymin": int(round(float(obj["y1"]) / resize_factor)),
                        "ymax": int(round(float(obj["y2"]) / resize_factor))

                    }
                }
                img_dict["objects"].append(obj_dict)
        except KeyError:
            print(f"Could not parse image: {img}")
            continue
        else:
            annotations.append(img_dict)
        finally:
            print(f"Converting image: {img_index}/{len(labels_dict)}\r", end='')

    print(f"\nSuccessfully parsed: {len(annotations)} images")
    return annotations


def validate_path(path):
    """Returns valid path object if input path exists.

    :param path: string with path
    :return: Path
    """

    p = Path(path)

    try:
        return p.resolve(strict=True)
    except FileNotFoundError:
        raise IOError(f"Could not read path: {path}") from None


def main():
    """Main loop to convert annotations.
    """

    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('sourcefile', type=str, help='Input file with image annotations')
    ap.add_argument('outputdir', type=str, help='Folder for output annotation files')
    ap.add_argument('rs', type=float, default=1, help='resize factor for annotated images')

    args = ap.parse_args()

    ifile = validate_path(args.sourcefile)
    odir = validate_path(args.outputdir)
    resize_factor = args.rs

    print(f"Input dir is: {ifile}")
    print(f"Output dir is: {odir}")

    annotations = parse_json_annotations(ifile, resize_factor)
    write_VOC_file(annotations, odir)

if __name__ == "__main__":
    main()

