import numpy as np
import pytest_check as check
from idnc.neutralization.simulation import basicsim


def test_basicsim():
    # Settings
    n_steps = 5
    gain = 0.1
    step_time = 0.1

    dummy_controller = lambda poses: (-gain * poses[:, 0], -gain * poses[:, 1])
    initial_poses = np.array([[0, 1], [1, 0], [0, 0], [-1, 0], [4.2, -3.7]])

    # Simulation
    history = basicsim(
        n_steps=n_steps,
        controller=dummy_controller,
        initial_poses=initial_poses,
        step_time=step_time,
        verbose=0,
    )

    # Expected simulation
    expected_history = [initial_poses]
    for step in range(n_steps):
        last_poses = expected_history[-1]
        expected_history.append((1 - gain * step_time) * last_poses)

    # Checks
    for step, (poses, expected) in enumerate(zip(history, expected_history)):
        check.is_true(
            np.all(np.abs(poses - expected) < 1e-6),
            f"At step {step}, expected robots positions were {expected} but got {poses}.",
        )
