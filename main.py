#!/usr/bin/env python3
import cv2
import time
import logging
import math
from pynput import mouse, keyboard  # thêm keyboard nếu cần
import config
from src.detector import PersonDetector, PersonTracker, ScreenCapturer
from src.aiming_system import AimingSystem
from src.ui import UIDisplay

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

shot_count = 0
last_shot = 0

def on_click(x, y, button, pressed):
    global shot_count, last_shot
    if not pressed and button == mouse.Button.left:
        shot_count += 1
        last_shot = time.time()
        logger.info(f"Shot #{shot_count}")

def main():
    global shot_count, last_shot
    logger.info("Starting Robot AI Copilot...")
    try:
        sc = ScreenCapturer(config.SCREEN_MONITOR)
        w, h = sc.get_resolution()
        logger.info(f"Screen: {w}x{h}")
        
        det = PersonDetector(config.YOLO_MODEL, config.CONFIDENCE_THRESHOLD)
        trk = PersonTracker()
        aim = AimingSystem(w, h)
        ui = UIDisplay(w, h)
        
        # Mouse listener
        lst = mouse.Listener(on_click=on_click)
        lst.start()
        
        # Optional: Keyboard để đổi súng
        def on_press(key):
            try:
                if key.char == '1': aim.change_weapon("M416")
                elif key.char == '2': aim.change_weapon("AK47")
            except:
                pass
        kbd = keyboard.Listener(on_press=on_press)
        kbd.start()
        
        logger.info("Ready! Press Q to quit, 1/2 to change weapon")
        
        t0 = time.time()
        fc = 0
        fps = 0
        hist = []
        
        while True:
            start = time.time()
            frm = sc.capture()
            dets = det.detect(frm)
            trks = trk.update(dets)
            
            if config.SHOW_BOUNDING_BOX:
                frm = ui.draw_detections(frm, dets)
            
            # Find closest target
            closest = None
            min_d = float('inf')
            for t in trks:
                d = math.hypot(t["x"] - ui.cx, t["y"] - ui.cy)
                if d < min_d:
                    min_d, closest = d, t
            
            if closest:
                hist.append({"x": closest["x"], "y": closest["y"]})
                if len(hist) > 10:
                    hist.pop(0)
                
                pred = aim.predict(closest, hist)
                angles = aim.calc_angles(pred["x"], pred["y"])
                angles = aim.recoil(angles)
                
                if config.SHOW_ANGLES:
                    frm = ui.draw_aiming(frm, {
                        "angles": angles,
                        "target": pred,
                        "weapon": aim.weapon,
                        "shots": aim.shots
                    })
            
            if config.SHOW_AIMING_CROSSHAIR:
                frm = ui.draw_crosshair(frm)
            
            frm = ui.draw_weapon_info(frm, aim.weapon)
            
            fc += 1
            if time.time() - t0 > 1.0:
                fps = fc / (time.time() - t0)
                fc = 0
                t0 = time.time()
            
            if config.SHOW_FPS:
                frm = ui.draw_fps(frm, fps)
            
            frm = ui.draw_status(frm, f"Targets: {len(trks)} | Shots: {shot_count} | Weapon: {aim.weapon}")
            
            cv2.imshow("Robot AI Copilot", frm)
            
            # Auto fire khi click chuột
            if time.time() - last_shot < 0.15:
                aim.fire()
            
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q') or key == 27:
                break
            if key == ord('r'):
                aim.shots = 0
                hist.clear()
    
    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)
    finally:
        cv2.destroyAllWindows()
        lst.stop()
        logger.info(f"Closed. Total shots: {shot_count}")

if __name__ == "__main__":
    main()
