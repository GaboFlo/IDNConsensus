from idnc.simulation.rendering import RenderCallback
from idnc.simulation.simulation import basicsim


import numpy as np


def main():
    n_steps = 100
    gain = 1.0
    step_time = 0.1

    controller = lambda poses: (-gain * poses[:, 0], -gain * poses[:, 1])
    initial_poses = np.array([[0, 1], [1, 0], [0, 0], [-1, 0], [4.2, -3.7]])

    render_callback = RenderCallback()

    basicsim(
        n_steps,
        controller,
        initial_poses=initial_poses,
        step_time=step_time,
        callbacks=[render_callback],
        verbose=1,
    )


if __name__ == "__main__":
    main()
