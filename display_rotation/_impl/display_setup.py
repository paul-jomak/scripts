from __future__ import annotations

import win32api

from .display import Display


def get_displays() -> list[Display]:
    displays = [Display(hMonitor) for hMonitor, _, _ in win32api.EnumDisplayMonitors()]
    return displays
