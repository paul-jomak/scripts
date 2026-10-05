from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from display_rotation import get_displays

if TYPE_CHECKING:
    from display_rotation import Display

if __name__ == "__main__":
    displays = get_displays()

    rotation_display: Optional[Display] = None
    for display in displays:
        if display.resolution.height == 3840 or display.resolution.width == 3840:
            rotation_display = display

    if not rotation_display:
        raise Exception("No display found")

    toggle = {
        0: 90,
        90: 0
    }
    rotation_display.rotate_to(
        toggle[rotation_display.current_orientation],
    )
