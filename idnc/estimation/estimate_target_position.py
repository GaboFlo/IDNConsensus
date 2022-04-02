import sys


def from_txt_label_to_array(
    relativeTxtPath: str, targetWanted: int = 1, showPrint: bool = False
) -> list:
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
                targetCoord = {
                    "x_box_center": line[1],
                    "y_box_center": line[2],
                    "width_box": line[3],
                    "height_box": line[4],
                }
                if showPrint:
                    print(f"\nIntruder detected \n{targetCoord}\n")
    return targetCoord


def labels_to_relative_angles(
    coordinates: dict[str, float],
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
    leftEdgeCoord = coordinates["x_box_center"] - coordinates["width_box"] / 2
    rightEdgeCoord = coordinates["x_box_center"] + coordinates["width_box"] / 2

    """ Relative angle from the center (0.5 , 0) """
    """θ1"""
    relativeLeftAngle = (leftEdgeCoord - 0.5) * horizontalFOVDegree
    """ θ2 """
    relativeRightAngle = (rightEdgeCoord - 0.5) * horizontalFOVDegree
    if showPrint:
        print(
            f"\nIntruder detected: \nrelativeLeftAngle (θ1) : {relativeLeftAngle} \nrelativeRightAngle (θ2) : {relativeRightAngle}"
        )
    return (relativeLeftAngle, relativeRightAngle)


if __name__ == "__main__":
    """_summary_

    Raises:
        Exception: if no file name is provided with -file argument (.txt label file)
    """

    args = sys.argv[1:]
    fileName = ""
    if len(args) > 1:
        if args[0] == "-file":
            fileName = args[1]

    if fileName == "":
        raise Exception("No label file provided, use ` -file myFileName.txt `")

    print(f"\n===={fileName}=====")
    coord = from_txt_label_to_array(fileName)
    angles = labels_to_relative_angles(coord)
