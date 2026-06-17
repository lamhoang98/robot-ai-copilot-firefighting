import numpy as np
import math
import config
from .weapon_profiles import get_weapon_profile

class AimingSystem:
    def __init__(self, w=1920, h=1080):
        self.w, self.h = w, h
        self.cx, self.cy = w / 2, h / 2
        self.ppd_x = w / 90
        self.ppd_y = h / 60
        self.weapon = "M416"
        self.shots = 0
    
    def calc_angles(self, tx, ty):
        ox, oy = tx - self.cx, ty - self.cy
        return {"yaw": ox / self.ppd_x, "pitch": oy / self.ppd_y, "dist": math.sqrt(ox**2 + oy**2)}
    
    def predict(self, target, history, frames=3):
        if len(history) < 2:
            return target
        vx = np.mean([history[i]["x"] - history[i-1]["x"] for i in range(1, len(history))])
        vy = np.mean([history[i]["y"] - history[i-1]["y"] for i in range(1, len(history))])
        return {"x": int(target["x"] + vx * frames), "y": int(target["y"] + vy * frames)}
    
    def recoil(self, angles):
        prof = get_weapon_profile(self.weapon)
        if not prof:
            return angles
        r = prof["recoil"]
        comp_h = r["h"] * self.shots * 50
        comp_v = r["v"] * self.shots * 50
        return {**angles, "yaw": angles["yaw"] - comp_h, "pitch": angles["pitch"] - comp_v}
    
    def fire(self):
        self.shots += 1
        if self.shots > 100:
            self.shots = 0
