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

import numpy as np


def consensus(robotNo: int, nbRobots: int, poses: np.ndarray, gain: float = 1.0):
    adjacency = np.ones(nbRobots) - np.eye(nbRobots)
    poses = poses[:2, :]

    pos = np.stack([poses[:, robotNo - 1]] * nbRobots).transpose()
    diffs = pos - poses
    robotAdjacency = adjacency[robotNo - 1]

    [vx, vy] = -gain * np.dot(diffs, robotAdjacency)

    return vx, vy


def controller(robotNo, nbRobots, poses):
    vx, vy = consensus(robotNo, nbRobots, poses)
    return vx, vy
