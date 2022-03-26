"""Callback abstract classes"""

import time
from typing import List


class Callback:

    """An object to call functions while in a simulation.
    You can define the custom functions `on_{position}` where position can be in {'sim', 'step'}.
    """

    def __init__(self):
        self.params = {}

    def set_params(self, params):
        """Sets sim parameters"""
        self.params = params

    def on_step_begin(self, step: int, logs: dict = None):
        """Triggers on each step beginning
        Args:
            step: current step.
            logs: current logs.
        """

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

    def on_sim_end(self, logs: dict = None):
        """Triggers on each simulation end
        Args:
            logs: current logs.
        """


class CallbackList(Callback):
    """An wrapper to use a list of :class:`Callback`.
    Call all concerned callbacks while in simulation.
    """

    def __init__(self, callbacks: List[Callback] = None):
        super().__init__()
        self.callbacks = callbacks if callbacks is not None else []

    def set_params(self, params):
        self.params = params
        for callback in self.callbacks:
            callback.set_params(params)

    def _call_key_hook(self, key, hook, value=None, logs: dict = None):
        """Helper func for {step|sim}_{begin|end} methods."""

        if len(self.callbacks) == 0:
            return

        hook_name = f"on_{key}_{hook}"
        t_begin_name = f"t_{key}_begin"
        dt_name = f"dt_{key}"

        if hook == "begin":
            setattr(self, t_begin_name, time.time())

        if hook == "end":
            t_begin = getattr(self, t_begin_name)
            elapsed_time = time.time() - t_begin
            setattr(self, dt_name, elapsed_time)
            if logs is not None:
                logs.update({dt_name: elapsed_time})

        for callback in self.callbacks:
            step_hook = getattr(callback, hook_name)
            if logs is not None:
                if value is None:
                    step_hook(logs)
                else:
                    step_hook(value, logs)

    def on_step_begin(self, step, logs=None):
        self._call_key_hook("step", "begin", step, logs)

    def on_step_end(self, step, logs=None):
        self._call_key_hook("step", "end", step, logs)

    def on_sim_begin(self, logs=None):
        self._call_key_hook("sim", "begin", logs=logs)

    def on_sim_end(self, logs=None):
        self._call_key_hook("sim", "end", logs=logs)
