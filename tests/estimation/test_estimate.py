from tabnanny import check

import numpy as np
import pytest_check as check
from idnc.estimation.estimate_target_position import (
    from_txt_label_to_array,
    LabelBoxParams,
    labels_to_relative_angles,
)


def test_estimate_fullBox():
    coord = from_txt_label_to_array("./tests/estimation/test_fullBox.txt")
    expectedCoordinates: LabelBoxParams = {
        "x_box_center": 0.5,
        "y_box_center": 0.5,
        "width_box": 1,
        "height_box": 1,
    }
    for key in expectedCoordinates:
        check.is_true(
            np.all(np.isclose(expectedCoordinates[key], coord[key])),
            f"Recreate coordinates {coord[key]} while expecting {expectedCoordinates[key]}.",
        )

    angles = labels_to_relative_angles(expectedCoordinates)
    horizontalFOVDegree = 70.42
    expectedAngles = (-horizontalFOVDegree / 2, horizontalFOVDegree / 2)
    check.is_true(
        np.all(np.isclose(expectedAngles, angles)),
        f"Received angles {angles} instead of {expectedAngles}",
    )


def test_estimate_smallerBox():
    coord = from_txt_label_to_array("./tests/estimation/test_smallerBox.txt")
    expectedCoordinates: LabelBoxParams = {
        "x_box_center": 0.6,
        "y_box_center": 0.5,
        "width_box": 0.2,
        "height_box": 0.2,
    }
    for key in expectedCoordinates:
        check.is_true(
            np.all(np.isclose(expectedCoordinates[key], coord[key])),
            f"Recreate coordinates {coord[key]} while expecting {expectedCoordinates[key]}.",
        )

    angles = labels_to_relative_angles(expectedCoordinates)
    horizontalFOVDegree = 70.42
    expectedAngles = (0, 0.2 * horizontalFOVDegree)

    check.is_true(
        np.all(np.isclose(expectedAngles, angles)),
        f"Received angles {angles} instead of {expectedAngles}",
    )
