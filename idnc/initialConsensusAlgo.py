#!/usr/bin/env python
"""
   CentraleSupelec TP3A
   Sylvain BERTRAND, 2022
   Groupe 7 - Abla Benabdallah, Mathis Federico, Florian Gaboriaud
   (all variables in SI unit)
   
   
   variables used by the functions of this script
       - nbRobots: nb of robots in the fleet (>1)    
       - robotNo: no of the current robot for which control is computed (1 .. nbRobots)
       - poses:  size (3 x nbRobots) 
                 eg. of use: for robot no 'robotNo', its pose can be obtained by: poses[:,robotNo-1]   (indexes in Python start from 0 !)
                           poses[0,robotNo-1]: x-coordinate of robot position (in m)
                           poses[1,robotNo-1]: y-coordinate of robot position (in m)
                           poses[2,robotNo-1]: orientation angle of robot (in rad)
   
"""

import math

import numpy as np

# import rospy

# ==============   "GLOBAL" VARIABLES KNOWN BY ALL THE FUNCTIONS ===================
# all variables declared here will be known by functions below
# if a variable here needs to be modified by a function, use 'global' keyword inside the function

gainConsensus = 1
virtualRobotNb = 0
# ===================================================================================

# =======================================
def consensus(robotNo: int, nbRobots: int, poses: np.ndarray):
    # =======================================
    adjacency = np.ones(nbRobots) - np.eye(nbRobots)
    poses = poses[:2, :]

    pos = np.stack([poses[:, robotNo - 1]] * nbRobots).transpose()
    diffs = pos - poses
    robotAdjacency = adjacency[robotNo - 1]

    global gainConsensus
    [vx, vy] = -gainConsensus * np.dot(diffs, robotAdjacency)

    return vx, vy


# ====================================


# ======== ! DO NOT MODIFY ! ============
def controller(robotNo, nbRobots, poses):
    # =======================================

    # UNCOMMENT THE ONE TO BE TESTED FOR EXPERIMENT
    vx, vy = consensus(robotNo, nbRobots, poses)
    return vx, vy


# ====================================

if __name__ == "__main__":
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
        value = consensus(robot, nRobots, poses=poses)
        print(f"Robot n°{robot} gave control {value} when expecting {expected}.")
        assert value == expected

    print("Test passed !")
