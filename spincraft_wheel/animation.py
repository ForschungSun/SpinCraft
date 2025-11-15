import random
import time
from typing import Callable, Optional

from .model import WheelModel
from .renderer import WheelRenderer


class WheelAnimator:
    def __init__(
        self,
        tk_root,
        model: WheelModel,
        renderer: WheelRenderer,
        on_finish: Optional[Callable[[str], None]] = None,
    ):
        self.root = tk_root
        self.model = model
        self.renderer = renderer
        self.on_finish = on_finish

        self.current_angle: float = 0.0
        self._start_angle: float = 0.0
        self._target_angle: float = 0.0
        self._start_time: float = 0.0
        self._duration: float = 0.0
        self._spinning: bool = False

    def start_spin(self):
        if self._spinning:
            return

        base_angle = random.random() * 360.0  # uniform in [0, 360)
        turns = 10

        self._start_angle = self.current_angle
        self._target_angle = self.current_angle + turns * 360.0 + base_angle
        self._duration = 10.0  # seconds
        self._start_time = time.perf_counter()
        self._spinning = True

        self._animate_step()

    def _animate_step(self):
        if not self._spinning:
            return

        now = time.perf_counter()
        t = (now - self._start_time) / self._duration
        if t >= 1.0:
            t = 1.0

        # ease-out cubic
        p = 1.0 - (1.0 - t) ** 1.8
        self.current_angle = self._start_angle + (self._target_angle - self._start_angle) * p

        self.renderer.draw(self.current_angle)

        if t < 1.0:
            self.root.after(16, self._animate_step)
        else:
            self._spinning = False
            self._on_spin_end()

    def _on_spin_end(self):
        effective_angle = self.current_angle % 360.0
        pointer_angle = (-effective_angle) % 360.0
        label = self.model.get_sector_for_angle(pointer_angle)
        if self.on_finish is not None:
            self.on_finish(label)
