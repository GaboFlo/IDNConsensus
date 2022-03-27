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
            First dimension length should be the number of robots.
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

    si_to_uni_dyn, _ = create_si_to_uni_mapping(
        projection_distance=0.01, angular_velocity_limit=np.pi/2
    )

    for step in range(n_steps):

        callbacklist.on_step_begin(step, logs)

        if verbose > 0:
            print("-" * 30 + f"\n\tStep {step+1}/{n_steps}:")

        # Get robots wanted behavior
        wanted_velocity = controller(poses)

        # Update dynamics of agents
        unicycle_dynamics = si_to_uni_dyn(wanted_velocity, poses)

        vx = np.cos(poses[:, 2]) * unicycle_dynamics[:, 0]
        vy = np.sin(poses[:, 2]) * unicycle_dynamics[:, 0]
        dw = unicycle_dynamics[:, 1]

        if verbose > 1:
            print(f"Wanted velocity:\n{wanted_velocity}")
            print(f"Unicycle dynamics:\n{unicycle_dynamics}")
            print(f"Actual velocity:\n{np.stack((vx, vy, dw), axis=-1)}")

        poses[:, 0] += step_time * vx
        poses[:, 1] += step_time * vy
        poses[:, 2] += step_time * dw

        # Ensure angles are wrapped
        poses[:, 2] = np.arctan2(np.sin(poses[:, 2]), np.cos(poses[:, 2]))

        logs.update({"poses": poses})

        # Save history
        history.append(copy(poses))

        if verbose > 0:
            print(f"Poses:\n{poses}")

        callbacklist.on_step_end(step, logs)

    callbacklist.on_sim_end(logs)

    return history


def create_si_to_uni_mapping(projection_distance=0.1, angular_velocity_limit=np.pi):
    """Creates two functions for mapping from single integrator dynamics to
    unicycle dynamics and unicycle states to single integrator states.

    This mapping is done by placing a virtual control "point" in front of
    the unicycle.
    projection_distance: How far ahead to place the point
    angular_velocity_limit: The maximum angular velocity that can be provided
    -> (function, function)
    """

    def si_to_uni_dyn(dxi, poses):
        """Takes single-integrator velocities and transforms them to unicycle
        control inputs.
        dxi: 2xN numpy array of single-integrator control inputs
        poses: 3xN numpy array of unicycle poses
        -> 2xN numpy array of unicycle control inputs
        """

        N, _ = np.shape(dxi)

        cs = np.cos(poses[:, 2])
        ss = np.sin(poses[:, 2])

        dxu = np.zeros((N, 2))
        dxu[:, 0] = cs * dxi[:, 0] + ss * dxi[:, 1]
        dxu[:, 1] = (1 / projection_distance) * (-ss * dxi[:, 0] + cs * dxi[:, 1])

        # Impose angular velocity cap.
        dxu[dxu[:, 1] > angular_velocity_limit, 1] = angular_velocity_limit
        dxu[dxu[:, 1] < -angular_velocity_limit, 1] = -angular_velocity_limit

        return dxu

    def uni_to_si_states(poses):
        """Takes unicycle states and returns single-integrator states
        poses: 3xN numpy array of unicycle states
        -> 2xN numpy array of single-integrator states
        """

        _, N = np.shape(poses)

        si_states = np.zeros((2, N))
        si_states[:, 0] = poses[:, 0] + projection_distance * np.cos(poses[:, 2])
        si_states[:, 1] = poses[:, 1] + projection_distance * np.sin(poses[:, 2])

        return si_states

    return si_to_uni_dyn, uni_to_si_states
