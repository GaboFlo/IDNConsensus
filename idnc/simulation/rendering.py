from copy import copy
from os import path
from time import sleep
from typing import Tuple

import numpy as np

import pyglet
from pyglet.image import Texture
from pyglet import clock

from idnc.simulation.callbacks import Callback


class RenderCallback(Callback):

    """An object to call functions while in a simulation.
    You can define the custom functions `on_{position}` where position can be in {'sim', 'step'}.
    """

    def __init__(self, fps=120):
        self.params = {}
        self.fps = 120
        self.window = pyglet.window.Window(800, 600)
        ressources_path = path.join(path.dirname(__file__), "resources")

        pyglet.resource.path = [ressources_path]
        pyglet.resource.reindex()
        self.window_title = pyglet.text.Label(
            text="Robots simulation",
            x=self.window.width // 2,
            y=self.window.height,
            anchor_x="center",
            anchor_y="top",
        )

        # Build images
        def resize_image(image: Texture, size: Tuple[int, int]):
            """Sets an image's anchor point to its center"""
            image.width = int(size[0])
            image.height = int(size[1])

        def center_image(image: Texture):
            """Sets an image's anchor point to its center"""
            image.anchor_x = image.width // 2
            image.anchor_y = image.height // 2

        self.burger_image: Texture = pyglet.resource.image("burger.png")
        resize_image(self.burger_image, size=(64, 64))
        center_image(self.burger_image)

        # Build sprites
        self.burger_sprites = []

        @self.window.event
        def on_draw():
            self.window.clear()
            self.window_title.draw()

            for burger_sprite in self.burger_sprites:
                burger_sprite.draw()

    def map_to_display(self, poses: np.ndarray, scale=(1.0, 1.0)) -> np.ndarray:
        """Map scene poses to display poses.

        Args:
            poses (np.ndarray): Scene poses.

        Returns:
            np.ndarray: Display poses.
        """
        disp_poses = copy(poses)
        disp_poses *= np.array(
            [[self.window.width / scale[0], self.window.height / scale[1]]]
        )
        disp_poses += np.array([[self.window.width // 2, self.window.height // 2]])
        return disp_poses

    def update(self, poses):
        display_poses = self.map_to_display(poses, scale=(10, 10))
        for sprite, pos in zip(self.burger_sprites, display_poses):
            sprite.position = pos

    def on_step_begin(self, step: int, logs: dict = None):
        """Triggers on each step beginning
        Args:
            step: current step.
            logs: current logs.
        """
        dt = clock.tick()
        for window in pyglet.app.windows:
            window.switch_to()
            window.dispatch_events()
            window.dispatch_event("on_draw")
            window.flip()
        poses = logs.get("poses", logs["initial_poses"])
        self.update(poses)
        sleep(max(0, 1 / self.fps - dt))

    def on_step_end(self, step: int, logs: dict = None):
        """Triggers on each step end
        Args:
            step: current step.
            logs: current logs.
        """

    def on_sim_begin(self, logs: dict = None):
        """Triggers on each simulation beginning
        Args:
            logs: current logs.
        """
        display_poses = self.map_to_display(logs["initial_poses"], scale=(10, 10))
        self.burger_sprites = [
            pyglet.sprite.Sprite(img=self.burger_image, x=pos[0], y=pos[1])
            for pos in display_poses
        ]
        # pyglet.app.run()

    def on_sim_end(self, logs: dict = None):
        """Triggers on each simulation end
        Args:
            logs: current logs.
        """
