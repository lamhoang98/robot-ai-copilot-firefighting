# config.py
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
MODELS_DIR = BASE_DIR / "models"
OUTPUT_DIR = BASE_DIR / "output"
LOG_DIR = OUTPUT_DIR / "logs"

# Tạo thư mục
for d in [MODELS_DIR, OUTPUT_DIR, LOG_DIR]:
    d.mkdir(exist_ok=True)

# ====================== CẤU HÌNH CHUNG ======================
DEBUG = True
SCREEN_MONITOR = 1                    # 0 = màn hình chính, 1 = màn hình thứ 2
YOLO_MODEL = "yolov8n.pt"             # yolov8n.pt (nhẹ), yolov8s.pt, yolov8m.pt
CONFIDENCE_THRESHOLD = 0.45
IOU_THRESHOLD = 0.45

# Hiển thị
SHOW_BOUNDING_BOX = True
SHOW_AIMING_CROSSHAIR = True
SHOW_ANGLES = True
SHOW_FPS = True
SHOW_WEAPON_INFO = True
SHOW_STATUS = True

# Aiming & Recoil
RECOIL_COMPENSATION = True
SMOOTHING_FACTOR = 0.68               # 0.5 ~ 0.85 (càng nhỏ càng mượt)
AIM_OFFSET_Y = -25                    # Aim cao hơn một chút (đầu)

# ====================== WEAPON ======================
WEAPON_PROFILES = {
    "M416": {
        "name": "M416",
        "type": "AR",
        "damage": 41,
        "fire_rate": 6.5,
        "recoil": {"h": 1.8, "v": 2.2}
    },
    "AK47": {
        "name": "AK47",
        "type": "AR",
        "damage": 49,
        "fire_rate": 6.2,
        "recoil": {"h": 2.5, "v": 3.0}
    },
    "SCAR": {
        "name": "SCAR-L",
        "type": "AR",
        "damage": 43,
        "fire_rate": 6.4,
        "recoil": {"h": 1.6, "v": 2.0}
    },
    "M249": {
        "name": "M249",
        "type": "LMG",
        "damage": 45,
        "fire_rate": 7.5,
        "recoil": {"h": 2.8, "v": 3.5}
    }
}

WEAPON_LIST = list(WEAPON_PROFILES.keys())

# ====================== MÀU SẮC ======================
COLOR_BOX = (0, 255, 0)
COLOR_AIM = (0, 0, 255)
COLOR_TEXT = (255, 255, 255)
COLOR_STATUS = (0, 255, 255)
