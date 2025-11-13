import math

from .model import WheelModel
from .colors import (
    get_sector_color,
    OUTER_RING_COLOR,
    CENTER_DOT_COLOR,
    POINTER_COLOR,
    BACKGROUND_COLOR,
)


class WheelRenderer:
    def __init__(self, canvas, model: WheelModel, cx: int, cy: int, radius: int):
        self.canvas = canvas
        self.model = model
        self.cx = cx
        self.cy = cy
        self.radius = radius

        # pre-configure background
        self.canvas.configure(bg=BACKGROUND_COLOR)

    def draw(self, angle: float):
        """Draw the wheel at a given rotation angle (degrees, clockwise)."""
        self.canvas.delete("all")

        r_outer = self.radius
        r_inner = self.radius * 0.1
        r_label = self.radius * 0.65

        # outer ring
        self._draw_outer_ring(r_outer)

        # sectors
        for idx, sector in enumerate(self.model.sectors):
            span = sector.end - sector.start
            if span <= 0:
                continue

            # visible start angle in our math system
            start_vis = (sector.start + angle) % 360.0
            # convert to Tk angles: 0 at 3 o'clock CCW
            start_tk = (90.0 - start_vis) % 360.0
            extent_tk = -span  # negative: clockwise

            color = get_sector_color(idx)
            self.canvas.create_arc(
                self.cx - r_outer,
                self.cy - r_outer,
                self.cx + r_outer,
                self.cy + r_outer,
                start=start_tk,
                extent=extent_tk,
                fill=color,
                outline=BACKGROUND_COLOR,
                width=2,
            )

            # label position (use center of sector)
            center_angle = (sector.start + sector.end) / 2.0 + angle
            rad = math.radians(center_angle)
            x = self.cx + r_label * math.sin(rad)
            y = self.cy - r_label * math.cos(rad)

            self.canvas.create_text(
                x,
                y,
                text=sector.label,
                fill="#000000",
                font=("Helvetica", 14, "bold"),
            )

        # inner disk
        self.canvas.create_oval(
            self.cx - r_inner,
            self.cy - r_inner,
            self.cx + r_inner,
            self.cy + r_inner,
            fill=CENTER_DOT_COLOR,
            outline="",
        )

        # pointer (fixed at top)
        self._draw_pointer(r_outer)

    def _draw_outer_ring(self, r_outer: float):
        ring_width = 8
        self.canvas.create_oval(
            self.cx - r_outer - ring_width,
            self.cy - r_outer - ring_width,
            self.cx + r_outer + ring_width,
            self.cy + r_outer + ring_width,
            outline=OUTER_RING_COLOR,
            width=2,
        )

    def _draw_pointer(self, r_outer: float):
        pointer_height = 24
        pointer_width = 18
        top_y = self.cy - r_outer - 16
        base_y = top_y + pointer_height

        x0 = self.cx
        y0 = top_y
        x1 = self.cx - pointer_width / 2
        y1 = base_y
        x2 = self.cx + pointer_width / 2
        y2 = base_y

        self.canvas.create_polygon(
            x0,
            y0,
            x1,
            y1,
            x2,
            y2,
            fill=POINTER_COLOR,
            outline="",
        )
