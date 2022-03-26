""" Module for simulations.
"""

from copy import copy
from typing import List, Tuple, Callable
import numpy as np

from idnc.simulation.callbacks import Callback, CallbackList


def basicsim(
    n_steps: int,
    controller: Callable[[np.ndarray], Tuple[np.ndarray, np.ndarray]],
    initial_poses: np.ndarray,
    step_time: float,
    callbacks: List[Callback] = None,
    verbose: int = 0,
):
    """Basic simulation used for simple theorical testing.

    Args:
        n_steps (int): Number of simulation steps.
        controller (Callable): Behavior of the robots returning their wanted velocities from all robots positions.
        initial_poses (np.ndarray): Initial poses of the robots.
            First dimention lenght should be the number of robots.
        step_time (float): Time passed each step.
        callbacks (List[Callback]): List of callbacks to apply in simulation.
        verbose (int): 0: silent, 1: print robots poses each step.
    """

    logs = {
        "n_steps": n_steps,
        "initial_poses": initial_poses,
        "step_time": step_time,
    }

    callbacklist = CallbackList(callbacks)
    callbacklist.on_sim_begin(logs)

    poses = copy(initial_poses)
    logs.update({"poses": poses})

    history = [copy(poses)]
    if verbose > 0:
        print("-" * 30 + f"\n\tInitial poses:\n{poses}")
    for step in range(n_steps):

        callbacklist.on_step_begin(step, logs)

        # Get robots behavior
        vx, vy = controller(poses)

        # Apply dynamics
        poses[:, 0] += vx * step_time
        poses[:, 1] += vy * step_time

        logs.update({"poses": poses})

        # Save history
        history.append(copy(poses))

        if verbose > 0:
            print("-" * 30 + f"\n\tStep {step+1}/{n_steps}:\nPoses:\n{poses}")

        callbacklist.on_step_end(step, logs)

    callbacklist.on_sim_end(logs)

    return history
