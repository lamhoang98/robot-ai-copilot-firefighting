# src/aiming_system.py
import math
import time
import config
from src.weapon_profiles import get_weapon_profile

class AimingSystem:
    def __init__(self, screen_w, screen_h):
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.cx = screen_w // 2
        self.cy = screen_h // 2
        self.weapon = "M416"  # default
        self.shots = 0
        self.last_shot_time = 0
        self.recoil_accum = {"x": 0, "y": 0}
    
    def predict(self, target, history):
        """Simple prediction + smoothing"""
        if not history:
            return target
        # Moving average
        avg_x = sum(h["x"] for h in history) / len(history)
        avg_y = sum(h["y"] for h in history) / len(history)
        return {"x": int(avg_x), "y": int(avg_y)}
    
    def calc_angles(self, tx, ty):
        """Calculate yaw/pitch to move mouse"""
        dx = tx - self.cx
        dy = ty - self.cy
        dist = math.sqrt(dx*dx + dy*dy)
        return {
            "yaw": dx,      # pixel offset
            "pitch": dy,
            "dist": dist
        }
    
    def recoil(self, angles):
        """Recoil compensation"""
        if not config.RECOIL_COMPENSATION:
            return angles
        
        prof = get_weapon_profile(self.weapon)
        if not prof or not prof.get("recoil"):
            return angles
        
        r = prof["recoil"]
        self.recoil_accum["x"] += r["h"] * 5   # scale tùy game
        self.recoil_accum["y"] += r["v"] * 8
        
        angles["yaw"] += self.recoil_accum["x"]
        angles["pitch"] += self.recoil_accum["y"]
        return angles
    
    def fire(self):
        """Simulate mouse click / fire"""
        current = time.time()
        if current - self.last_shot_time > 0.05:  # rate limit
            # Thực tế bạn cần pynput.mouse.Controller().click()
            self.shots += 1
            self.last_shot_time = current
            # Reset recoil nhẹ sau mỗi burst
            if self.shots % 5 == 0:
                self.recoil_accum["x"] *= 0.6
                self.recoil_accum["y"] *= 0.6
    
    def change_weapon(self, weapon_name):
        if weapon_name in config.WEAPON_LIST or True:  # mở rộng sau
            self.weapon = weapon_name
            self.shots = 0
            self.recoil_accum = {"x": 0, "y": 0}
