from dataclasses import fields
from tabnanny import check

import numpy as np
import pytest_check as check
from idnc.estimation.estimate_target_position import (
    LabelBoxParams,
    from_txt_label_to_LabelBoxParams,
    labels_to_relative_angles,
)
from idnc.estimation.utils.euler_from_quaternion import euler_from_quaternion


def test_estimate_fullBox():
    coord = from_txt_label_to_LabelBoxParams(
        "./tests/estimation/src/test_relativeAngle_fullBox.txt"
    )
    expectedCoordinates = LabelBoxParams(0.5, 0.5, 1.0, 1.0)

    for field in fields(expectedCoordinates):
        expectation = getattr(expectedCoordinates, field.name)
        reality = getattr(coord, field.name)
        check.is_true(
            np.all(np.isclose(expectation, reality)),
            f"Recreate coordinates {expectation} while expecting {reality}.",
        )

    angles = labels_to_relative_angles(expectedCoordinates)
    horizontalFOVDegree = 70.42
    expectedAngles = (-horizontalFOVDegree / 2, horizontalFOVDegree / 2)
    check.is_true(
        np.all(np.isclose(expectedAngles, angles)),
        f"Received angles {angles} instead of {expectedAngles}",
    )


def test_estimate_smallerBox():
    coord = from_txt_label_to_LabelBoxParams(
        "./tests/estimation/src/test_relativeAngle_smallerBox.txt"
    )
    expectedCoordinates = LabelBoxParams(0.6, 0.5, 0.2, 0.2)

    for field in fields(expectedCoordinates):
        expectation = getattr(expectedCoordinates, field.name)
        reality = getattr(coord, field.name)
        check.is_true(
            np.all(np.isclose(expectation, reality)),
            f"Recreate coordinates {expectation} while expecting {reality}.",
        )

    angles = labels_to_relative_angles(expectedCoordinates)
    horizontalFOVDegree = 70.42
    expectedAngles = (0, 0.2 * horizontalFOVDegree)

    check.is_true(
        np.all(np.isclose(expectedAngles, angles)),
        f"Received angles {angles} instead of {expectedAngles}",
    )
