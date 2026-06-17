__version__ = "1.0.0"
__author__ = "Team AI Copilot"

from .detector import PersonDetector, ScreenCapturer, PersonTracker
from .aiming_system import AimingSystem
from .ui import UIDisplay
from .weapon_profiles import WEAPON_PROFILES

__all__ = ["PersonDetector", "ScreenCapturer", "PersonTracker", "AimingSystem", "UIDisplay", "WEAPON_PROFILES"]
