# src/aiming_system.py
import math
import time
import config
from src.weapon_profiles import get_weapon_profile
from pynput.mouse import Controller, Button

class AimingSystem:
    def __init__(self, screen_w: int, screen_h: int):
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.cx = screen_w // 2
        self.cy = screen_h // 2
        self.weapon = "M416"
        self.shots = 0
        self.last_shot_time = 0
        self.recoil_accum = {"x": 0.0, "y": 0.0}
        self.mouse = Controller()
        self.smoothing = config.SMOOTHING_FACTOR

    def move_mouse(self, yaw: float, pitch: float):
        move_x = int(yaw * self.smoothing)
        move_y = int(pitch * self.smoothing + config.AIM_OFFSET_Y)
        self.mouse.move(move_x, move_y)

    def predict(self, target: dict, history: list):
        if not history:
            return target
        avg_x = sum(h["x"] for h in history) / len(history)
        avg_y = sum(h["y"] for h in history) / len(history)
        return {"x": int(avg_x), "y": int(avg_y)}

    def calc_angles(self, tx: int, ty: int):
        dx = tx - self.cx
        dy = ty - self.cy
        dist = math.sqrt(dx*dx + dy*dy)
        return {"yaw": dx, "pitch": dy, "dist": dist}

    def recoil(self, angles: dict):
        if not config.RECOIL_COMPENSATION:
            return angles
        prof = get_weapon_profile(self.weapon)
        if not prof or "recoil" not in prof:
            return angles
        r = prof["recoil"]
        self.recoil_accum["x"] += r["h"] * 4.5
        self.recoil_accum["y"] += r["v"] * 7.5
        angles["yaw"] += self.recoil_accum["x"]
        angles["pitch"] += self.recoil_accum["y"]
        return angles

    def fire(self):
        current = time.time()
        if current - self.last_shot_time > 0.05:
            try:
                self.mouse.click(Button.left)
            except:
                pass
            self.shots += 1
            self.last_shot_time = current
            if self.shots % 6 == 0:
                self.recoil_accum["x"] *= 0.55
                self.recoil_accum["y"] *= 0.55

    def change_weapon(self, weapon_name: str):
        if weapon_name in config.WEAPON_LIST:
            self.weapon = weapon_name
            self.shots = 0
            self.recoil_accum = {"x": 0.0, "y": 0.0}
            print(f"🔫 Đổi súng: {weapon_name}")
