#!/usr/bin/env python3
import cv2
import time
import logging
import math
from pynput import mouse, keyboard
import config
from src.detector import PersonDetector, PersonTracker, ScreenCapturer
from src.aiming_system import AimingSystem
from src.ui import UIDisplay
from src.weapon_profiles import get_weapon_profile

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

shot_count = 0
last_shot = 0
ai_mode = True   # Chế độ AI tự động

def on_click(x, y, button, pressed):
    global shot_count, last_shot
    if not pressed and button == mouse.Button.left:
        shot_count += 1
        last_shot = time.time()

def main():
    global shot_count, last_shot, ai_mode
    logger.info("🚀 Khởi động Robot AI Copilot Firefighting...")
    
    try:
        sc = ScreenCapturer(config.SCREEN_MONITOR)
        w, h = sc.get_resolution()
        logger.info(f"📺 Độ phân giải: {w}x{h}")

        det = PersonDetector(config.YOLO_MODEL, config.CONFIDENCE_THRESHOLD)
        trk = PersonTracker()
        aim = AimingSystem(w, h)
        ui = UIDisplay(w, h)

        # Listener
        lst = mouse.Listener(on_click=on_click)
        lst.start()

        def on_press(key):
            global ai_mode
            try:
                if hasattr(key, 'char'):
                    if key.char == 'a':
                        ai_mode = not ai_mode
                        print(f"🤖 AI Mode: {'ON' if ai_mode else 'OFF'}")
                    elif key.char == '1':
                        aim.change_weapon("M416")
                    elif key.char == '2':
                        aim.change_weapon("AK47")
                    elif key.char == '3':
                        aim.change_weapon("SCAR")
                    elif key.char == '4':
                        aim.change_weapon("M249")
            except:
                pass

        kbd = keyboard.Listener(on_press=on_press)
        kbd.start()

        logger.info("✅ Sẵn sàng! Nhấn Q thoát | A bật/tắt AI | 1-4 đổi súng")

        t0 = time.time()
        fc = 0
        fps = 0
        history = []

        while True:
            start = time.time()
            frame = sc.capture()
            detections = det.detect(frame)
            tracks = trk.update(detections)

            if config.SHOW_BOUNDING_BOX:
                frame = ui.draw_detections(frame, detections)

            # Tìm target gần nhất
            closest = None
            min_dist = float('inf')
            for t in tracks:
                d = math.hypot(t["x"] - ui.cx, t["y"] - ui.cy)
                if d < min_dist:
                    min_dist = d
                    closest = t

            if closest and ai_mode:
                history.append({"x": closest["x"], "y": closest["y"]})
                if len(history) > 12:
                    history.pop(0)

                pred = aim.predict(closest, history)
                angles = aim.calc_angles(pred["x"], pred["y"])
                angles = aim.recoil(angles)

                aim.move_mouse(angles["yaw"], angles["pitch"])

                # Tự động bắn nếu target gần
                if angles["dist"] < 130:
                    aim.fire()

                if config.SHOW_ANGLES:
                    frame = ui.draw_aiming(frame, {
                        "angles": angles,
                        "target": pred,
                        "weapon": aim.weapon,
                        "shots": aim.shots
                    })

            if config.SHOW_AIMING_CROSSHAIR:
                frame = ui.draw_crosshair(frame)

            if config.SHOW_WEAPON_INFO:
                frame = ui.draw_weapon_info(frame, aim.weapon)

            # FPS
            fc += 1
            if time.time() - t0 >= 1.0:
                fps = fc / (time.time() - t0)
                fc = 0
                t0 = time.time()

            if config.SHOW_FPS:
                frame = ui.draw_fps(frame, fps)

            if config.SHOW_STATUS:
                frame = ui.draw_status(frame, f"Targets: {len(tracks)} | AI: {'ON' if ai_mode else 'OFF'} | Shots: {aim.shots}")

            cv2.imshow("Robot AI Copilot", frame)

            key = cv2.waitKey(1) & 0xFF
            if key == ord('q') or key == 27:
                break
            if key == ord('r'):
                aim.shots = 0
                history.clear()

    except Exception as e:
        logger.error(f"Lỗi: {e}", exc_info=True)
    finally:
        cv2.destroyAllWindows()
        try:
            lst.stop()
            kbd.stop()
        except:
            pass
        logger.info("Đã đóng chương trình.")

if __name__ == "__main__":
    main()
