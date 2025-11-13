from __future__ import annotations

from dataclasses import dataclass
from typing import List, Sequence, Tuple


@dataclass
class Sector:
    label: str
    start: float
    end: float
    weight: float


class WheelModel:
    def __init__(self, entries: Sequence[Tuple[str, float]]):
        if not entries:
            raise ValueError("entries must not be empty")
        self.set_entries(entries)

    def set_entries(self, entries: Sequence[Tuple[str, float]]):
        total_weight = sum(float(w) for _, w in entries)
        if total_weight <= 0:
            raise ValueError("total weight must be positive")

        sectors: List[Sector] = []
        current_angle = 0.0
        remaining = 360.0
        for i, (label, weight) in enumerate(entries):
            w = float(weight)
            if w <= 0:
                continue
            if i == len(entries) - 1:
                span = remaining
            else:
                span = 360.0 * w / total_weight
                remaining -= span
            start = current_angle
            end = start + span
            sectors.append(Sector(label=str(label), start=start, end=end, weight=w))
            current_angle = end

        self.sectors: List[Sector] = sectors

    def get_sector_for_angle(self, angle: float) -> str:

        if not self.sectors:
            raise RuntimeError("No sectors defined")

        a = angle % 360.0

        for s in self.sectors:
            start = s.start % 360.0
            end = s.end % 360.0
            if start <= end:
                if start <= a < end:
                    return s.label
            else:
                if a >= start or a < end:
                    return s.label

        return self.sectors[-1].label
