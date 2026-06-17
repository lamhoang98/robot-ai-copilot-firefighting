import cv2
import config
from .weapon_profiles import get_weapon_profile

class UIDisplay:
    def __init__(self, w=1920, h=1080):
        self.w, self.h = w, h
        self.cx, self.cy = w // 2, h // 2
        self.font = cv2.FONT_HERSHEY_SIMPLEX
    
    def draw_detections(self, frame, dets):
        for det in dets:
            cv2.rectangle(frame, (det["x1"], det["y1"]), (det["x2"], det["y2"]), config.COLOR_DETECTION, 2)
            cv2.putText(frame, f"Person {det['conf']:.2f}", (det["x1"], det["y1"] - 10), self.font, 0.6, config.COLOR_DETECTION, 2)
        return frame
    
    def draw_crosshair(self, frame):
        s = 30
        cv2.line(frame, (self.cx - s, self.cy), (self.cx + s, self.cy), (0, 255, 0), 2)
        cv2.line(frame, (self.cx, self.cy - s), (self.cx, self.cy + s), (0, 255, 0), 2)
        cv2.circle(frame, (self.cx, self.cy), 3, (0, 255, 0), -1)
        return frame
    
    def draw_aiming(self, frame, info):
        a = info["angles"]
        t = info["target"]
        x, y = int(t["x"]), int(t["y"])
        cv2.circle(frame, (x, y), 10, config.COLOR_AIMING, 2)
        cv2.line(frame, (self.cx, self.cy), (x, y), config.COLOR_AIMING, 1)
        y_pos = 30
        for txt in [f"Yaw: {a['yaw']:+.2f}", f"Pitch: {a['pitch']:+.2f}", f"Dist: {int(a['dist'])}", f"Weapon: {info['weapon']}", f"Shots: {info['shots']}"]:
            cv2.putText(frame, txt, (10, y_pos), self.font, 0.6, config.COLOR_TEXT, 2)
            y_pos += 25
        return frame
    
    def draw_fps(self, frame, fps):
        cv2.putText(frame, f"FPS: {fps:.1f}", (self.w - 150, 30), self.font, 0.6, config.COLOR_TEXT, 2)
        return frame
    
    def draw_status(self, frame, txt):
        cv2.rectangle(frame, (0, self.h - 40), (self.w, self.h), (0, 255, 0), -1)
        cv2.putText(frame, txt, (10, self.h - 10), self.font, 0.7, (0, 0, 0), 2)
        return frame
    
    def draw_weapon_info(self, frame, weapon):
        prof = get_weapon_profile(weapon)
        if not prof:
            return frame
        y_pos = 30
        for txt in [f"Weapon: {weapon}", f"Type: {prof['type']}", f"DMG: {prof['damage']}", f"ROF: {prof['fire_rate']}"]:
            cv2.putText(frame, txt, (self.w - 250, y_pos), self.font, 0.5, (255, 200, 0), 1)
            y_pos += 25
        return frame
