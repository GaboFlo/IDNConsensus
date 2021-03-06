import argparse
from dataclasses import dataclass
from typing import Dict


@dataclass
class LabelBoxParams:
    x_box_center: float
    y_box_center: float
    width_box: float
    height_box: float


def from_txt_label_to_array(
    relativeTxtPath: str, targetWanted: int = 1, showPrint: bool = False
):
    """
    Open txt file and return the coordinates of the potential box
    Args:
        relativeTxtPath (str): filename
        targetWanted (int, optional): index of the intruder. Defaults to 1 (DJI masterRobot). 0 for burger turtle bots

    Returns:
        list: Coordinates of the box
    """
    targetCoord = {}
    with open(relativeTxtPath) as f:
        lines = f.readlines()
        for line in lines:
            line = line.split(" ")
            line = [float(i) for i in line]
            if line[0] == targetWanted:
                targetCoord = LabelBoxParams(
                    line[1],
                    line[2],
                    line[3],
                    line[4],
                )
                if showPrint:
                    print(f"\nIntruder detected \n{targetCoord}\n")
    return targetCoord


def labels_to_relative_angles(
    coordinates: LabelBoxParams,
    horizontalFOVDegree: float = 70.42,
    showPrint: bool = False,
):
    """
    Get horizontal angles between the center of the picture and the vertical boxes of the target

    Args:
        coordinates (dict[str, float]): coordinates of the potential box [x_box_center, y_box_center, width_box, height_box])
        horizontalFOVDegree (float) : Horizontal FOV of the camera (degree)

    Returns :
        relativeLeftAngle (float): angle between the left edge of the box and the center of camera (0.5 , 0)
        relativeRightAngle (float): angle between the right edge of the box and the center of camera (0.5 , 0)

    """

    """ Coordinates of the vertical edges of the box in the global picture. """
    leftEdgeCoord = (
        getattr(coordinates, "x_box_center") - getattr(coordinates, "width_box") / 2
    )
    rightEdgeCoord = (
        getattr(coordinates, "x_box_center") + getattr(coordinates, "width_box") / 2
    )

    """ Relative angle from the center (0.5 , 0) """
    """??1"""
    relativeLeftAngle = (leftEdgeCoord - 0.5) * horizontalFOVDegree
    """ ??2 """
    relativeRightAngle = (rightEdgeCoord - 0.5) * horizontalFOVDegree
    if showPrint:
        print(
            f"\nIntruder detected: \nrelativeLeftAngle (??1) : {relativeLeftAngle} \nrelativeRightAngle (??2) : {relativeRightAngle}"
        )
    return (relativeLeftAngle, relativeRightAngle)


if __name__ == "__main__":
    """_summary_

    Raises:
        Exception: if no file name is provided with -file argument (.txt label file)
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--file",
        dest="file",
        required=True,
        type=str,
        help="Relative path of the .txt file",
    )

    arg = parser.parse_args()

    print(f"\n===={arg.file}=====")
    coord = from_txt_label_to_array(arg.file)
    angles = labels_to_relative_angles(coord)
