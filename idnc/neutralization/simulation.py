""" Module for simulations.
"""

from copy import copy
from typing import Tuple, Callable
import numpy as np


def basicsim(
    n_steps: int,
    controller: Callable[[np.ndarray], Tuple[np.ndarray, np.ndarray]],
    initial_poses: np.ndarray,
    step_time: float,
    verbose: int = 0,
):
    """Basic simulation used for simple theorical testing.

    Args:
        n_steps (int): Number of simulation steps.
        controller (Callable): Behavior of the robots returning their wanted velocities from all robots positions.
        initial_poses (np.ndarray): Initial poses of the robots.
            First dimention lenght should be the number of robots.
        step_time (float): Time passed each step.
        verbose (int): 0: silent, 1: print robots poses each step.
    """

    poses = copy(initial_poses)
    history = [copy(poses)]
    if verbose > 0:
        print(f"Initial poses:\t{poses}")
    for step in range(n_steps):

        # Get robots behavior
        vx, vy = controller(poses)

        # Apply dynamics
        poses[:, 0] += vx * step_time
        poses[:, 1] += vy * step_time

        # Save history
        history.append(copy(poses))

        if verbose > 0:
            print(f"Step {step+1}/{n_steps}:\t{poses}")

    return history
