from idnc.simulation.rendering import RenderCallback
from idnc.simulation.simulation import basicsim


import numpy as np


def main():
    n_steps = 300
    gain = 1.0
    step_time = 0.01

    controller = lambda poses: -gain * poses[:, :2]
    initial_poses = np.array(
        [
            [0, 2, np.pi / 3],
            [2, 0, -np.pi / 6],
            [0, 0, 0],
            [-2, 0, np.pi / 4],
            [4.2, -3.7, -np.pi / 4],
        ]
    )

    render_callback = RenderCallback(fps=120)

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
