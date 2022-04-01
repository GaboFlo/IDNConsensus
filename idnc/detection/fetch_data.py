# install latest labelbox version (3.0 or above)
# !pip3 install labelbox[data]

from typing import Dict, Any, Tuple
import os
import shutil
import requests
import ndjson

from tqdm import tqdm
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import cv2

import labelbox


def hex_to_rgb(value):
    value = value.lstrip("#")
    lv = len(value)
    return tuple(int(value[i : i + lv // 3], 16) for i in range(0, lv, lv // 3))


def visualize_bbox(image: np.ndarray, tool: Dict[str, Any]) -> np.ndarray:
    """
    Draws a bounding box on an image

    Args:
        image (np.ndarray): image to draw a bounding box onto
        tool (Dict[str,any]): Dict response from the export
    Returns:
        image with a bounding box drawn on it.
    """
    start = (int(tool["bbox"]["left"]), int(tool["bbox"]["top"]))
    end = (
        int(tool["bbox"]["left"] + tool["bbox"]["width"]),
        int(tool["bbox"]["top"] + tool["bbox"]["height"]),
    )
    return cv2.rectangle(
        image, start, end, color=hex_to_rgb(tool["color"]), thickness=2
    )


def strip_external_id_data(external_id: str) -> Tuple[int, int]:
    external_id = external_id.split("-")[0]
    cam_id = int(external_id.split("_")[1])
    scene_id = int(external_id[-1])
    return scene_id, cam_id


def labelbox_to_yolo(label, img_size):
    """Transform a labelbox label to YOLO format (class_index, xywh).

    Args:
        label: Labelbox objects.
    """
    # box
    top, left, h, w = label["bbox"].values()  # top, left, height, width
    xywh = [
        (left + w / 2) / img_size[0],
        (top + h / 2) / img_size[1],
        w / img_size[0],
        h / img_size[1],
    ]  # xywh normalized

    label_int = label["title"] == "MasterRobotDGI"
    return label_int, *xywh


def video_to_frames(
    path: str,
    annotations,
    video_title: str = "",
    split: str = "",
    dataset_path: str = None,
    visualize: bool = False,
):
    vidcap = cv2.VideoCapture(path)
    success, image = vidcap.read()
    # Note that frameNumber 1 in the annotation is frame index 0s

    if dataset_path is not None:
        images_path = os.path.join(dataset_path, "images")
        labels_path = os.path.join(dataset_path, "labels")
        if split != "":
            images_path = os.path.join(images_path, split)
            labels_path = os.path.join(labels_path, split)
        os.makedirs(images_path, exist_ok=True)
        os.makedirs(labels_path, exist_ok=True)

    frame = 1
    while success:
        image = image[:, :, ::-1]
        image_title = f"{video_title}_{frame}"
        annotation = annotations.get(frame)
        if annotation is not None:
            if dataset_path is not None:
                img_path = os.path.join(images_path, image_title) + ".jpg"
                img = Image.fromarray(image)
                img.save(img_path, quality=95, subsampling=0)
                dset_split = os.path.join(dataset_path, split)
                rel_path = os.path.relpath(img_path, start=dataset_path).replace(
                    "\\", "/"
                )
                with open(dset_split + ".txt", "a") as f:
                    f.write("./" + rel_path + "\n")

            for label in annotation["objects"]:
                if "bbox" in label:
                    if visualize:
                        image = visualize_bbox(image.astype(np.uint8), label)
                    if dataset_path is not None:
                        label_path = os.path.join(labels_path, image_title)
                        line = labelbox_to_yolo(label, tuple(img.size))
                        with open(label_path + ".txt", "a") as f:
                            f.write(("%g " * len(line)).rstrip() % line + "\n")
        if visualize:
            plt.figure(1)
            plt.imshow(image)
            plt.title(image_title)
            plt.pause(1 / 120)
            plt.clf()
        success, image = vidcap.read()
        frame += 1


def fetch_from_labelbox(api_key: str, dataset_path: str, visualize=False):
    # Create Labelbox client
    lb = labelbox.Client(api_key=api_key)
    # Get project by ID
    project = lb.get_project("cl1ax83d10obo0yd24xzxho0z")
    # Export image and text data as an annotation generator:
    labels_export = project.label_generator()
    # Export labels created in the selected date range as a json file:
    labels_export = project.export_labels(download=True)

    tmp_path = os.path.join(dataset_path, "tmp")
    os.makedirs(tmp_path, exist_ok=True)

    load_bar = tqdm(labels_export, total=len(labels_export))
    for label_export in load_bar:
        scene, cam = strip_external_id_data(label_export["External ID"])
        load_bar.set_description_str(f"Scene {scene}: cam-{cam}")

        if scene == 7:
            split = "test"
        elif scene == 4:
            split = "val"
        else:
            split = "train"

        # Get input video
        video_url = label_export["Labeled Data"]
        tmp_video_path = os.path.join(tmp_path, "video.mp4")
        with open(tmp_video_path, "wb") as file:
            file.write(requests.get(video_url).content)

        # Get annotations
        annotations_url = label_export["Label"]["frames"]
        headers = {"Authorization": f"Bearer {api_key}"}
        annotations = ndjson.loads(requests.get(annotations_url, headers=headers).text)

        annotations = {
            annotation["frameNumber"]: annotation for annotation in annotations
        }

        # Strip the labeled video into labeled images in the dataset file
        video_to_frames(
            tmp_video_path,
            annotations,
            split=split,
            dataset_path=dataset_path,
            video_title=f"{scene}_{cam}",
            visualize=visualize,
        )

    shutil.rmtree(tmp_path)


def get_key(path):
    with open(path, "r") as f:
        key = f.read()
    return key


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--key-path", type=str, default="labelbox.key", help="labelbox api key path"
    )
    parser.add_argument(
        "--visualize", action="store_true", help="to visualize data being downloaded"
    )
    parser.add_argument(
        "--clean", action="store_true", help="remove all previous loaded data"
    )
    opt = parser.parse_args()

    dataset_name = "turtlebots"
    dataset_path = os.path.join(os.path.dirname(__file__), dataset_name)

    if opt.clean:
        shutil.rmtree(dataset_path)

    fetch_from_labelbox(
        api_key=get_key(opt.key_path),
        dataset_path=dataset_path,
        visualize=opt.visualize,
    )
