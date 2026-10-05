from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import win32api
import win32con

_ORIENTATIONS = (
    (0, win32con.DMDO_DEFAULT),
    (90, win32con.DMDO_90),
    (180, win32con.DMDO_180),
    (270, win32con.DMDO_270),
)

_DEGREE_TO_WIN32 = dict(_ORIENTATIONS)
_WIN32_TO_DEGREE = dict((win32_enum, degree) for (degree, win32_enum) in _ORIENTATIONS)

@dataclass
class Resolution:
    width: int
    height: int


class _MonitorInfoAccessor:
    def __init__(self, monitor_info: Any) -> None:
        self._monitor_info = monitor_info

    @property
    def device(self) -> str:
        return self._monitor_info["Device"]

    @property
    def is_primary(self) -> bool:
        # MONITORINFOF_PRIMARY - This is the primary display monitor.
        return self._flags == 1

    @property
    def _flags(self) -> int:
        return self._monitor_info["Flags"]


class Display:
    def __init__(self, win32_monitor: Any) -> None:
        self._wi32_monitor = win32_monitor

    @property
    def is_primary(self) -> bool:
        return self._get_info().is_primary

    @property
    def current_orientation(self) -> int:
        return _WIN32_TO_DEGREE[self._get_device_mode().DisplayOrientation]

    @property
    def resolution(self) -> Resolution:
        device_mode = self._get_device_mode()
        return Resolution(device_mode.PelsWidth, device_mode.PelsHeight)

    def rotate_to(self, degrees: int) -> None:
        if (rotation_val := _DEGREE_TO_WIN32.get(degrees)) is None:
            allowed_options = ', '.join(map(str, sorted(_DEGREE_TO_WIN32.keys())))
            raise ValueError(f"Display can only be rotated to {allowed_options} degrees.")

        device_mode = self._get_device_mode()

        if(device_mode.DisplayOrientation + rotation_val) % 2 == 1:
            device_mode.PelsWidth, device_mode.PelsHeight = device_mode.PelsHeight, device_mode.PelsWidth
        device_mode.DisplayOrientation = rotation_val

        win32api.ChangeDisplaySettingsEx(self._get_info().device, device_mode)

    def _get_info(self) -> _MonitorInfoAccessor:
        return _MonitorInfoAccessor(
            win32api.GetMonitorInfo(self._wi32_monitor),
        )

    def _get_device_mode(self):
        return win32api.EnumDisplaySettings(
            self._get_info().device,
            win32con.ENUM_CURRENT_SETTINGS,
        )
