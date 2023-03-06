from __future__ import annotations
from dataclasses import dataclass, replace


@dataclass
class BasePortal:
    x: int
    y: int
    animation_index: int

    def _replace(self, **kwargs):
        return replace(self, **kwargs)


@dataclass
class GreenPortal:
    x: int
    y: int
    animation_index: int
    out_portal: PurplePortal

    def _replace(self, **kwargs):
        return replace(self, **kwargs)


@dataclass
class PurplePortal:
    x: int
    y: int
    animation_index: int
    out_portal: GreenPortal

    def _replace(self, **kwargs):
        return replace(self, **kwargs)