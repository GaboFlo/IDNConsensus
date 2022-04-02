from tabnanny import check

import numpy as np
import pytest_check as check
from idnc.estimation.estimate_target_position import (
    from_txt_label_to_array,
    labels_to_relative_angles,
)
from idnc.estimation.utils.euler_from_quaternion import euler_from_quaternion


def test_estimate_fullBox():
    coord = from_txt_label_to_array(
        "./tests/estimation/src/test_relativeAngle_fullBox.txt"
    )
    expectedCoordinates = {
        "x_boxCenter": 0.5,
        "y_boxCenter": 0.5,
        "widthBox": 1,
        "heightBox": 1,
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
    coord = from_txt_label_to_array(
        "./tests/estimation/src/test_relativeAngle_smallerBox.txt"
    )
    expectedCoordinates = {
        "x_boxCenter": 0.6,
        "y_boxCenter": 0.5,
        "widthBox": 0.2,
        "heightBox": 0.2,
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
