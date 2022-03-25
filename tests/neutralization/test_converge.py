import numpy as np
import pytest_check as check
from idnc.neutralization.converge import consensus


def test_consensus():

    poses = np.array(
        [
            [1, 1, -3 * np.pi / 4],
            [1, -1, 3 * np.pi / 4],
            [-1, 1, -np.pi / 4],
            [-1, -1, np.pi / 4],
        ]
    )
    poses = poses.transpose()
    nRobots = poses.shape[1]
    gainConsensus = 1 / nRobots
    barycenter = np.mean(poses, axis=1)
    for robot in range(1, nRobots + 1):
        expected = tuple(barycenter[:2] - poses[:2, robot - 1])
        value = consensus(robot, nRobots, poses=poses, gain=gainConsensus)
        check.equal(
            value,
            expected,
            f"Robot n°{robot} gave control {value} when expecting {expected}.",
        )
