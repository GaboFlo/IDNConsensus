import numpy as np


def from_txt_label_to_array(relativeTxtPath: str, targetWanted: int = 1) -> list:
    """
    Open txt file and return the coordinates of the potential box
    Args:
        relativeTxtPath (str): filename
        targetWanted (int, optional): index of the intruder. Defaults to 1 (DJI masterRobot). 0 for burger turtle bots

    Returns:
        list: Coordinates of the box
    """
    targetLine = {}
    with open(relativeTxtPath) as f:
        lines = f.readlines()
        for line in lines:
            line = line.split(" ")
            line = [float(i) for i in line]
            if line[0] == targetWanted:
                print(f"Intruder detected {line}")
                targetLine = {
                    "x_box_center": line[1],
                    "y_box_center": line[2],
                    "width_box": line[3],
                    "height_box": line[4],
                }
    return targetLine


if __name__ == "__main__":
    coord = from_txt_label_to_array("test_1.txt")
    print(coord)
