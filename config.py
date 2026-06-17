import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
SRC_DIR = BASE_DIR / "src"
OUTPUT_DIR = BASE_DIR / "output"
LOG_DIR = OUTPUT_DIR / "logs"
MODELS_DIR = BASE_DIR / "models"

OUTPUT_DIR.mkdir(exist_ok=True)
LOG_DIR.mkdir(exist_ok=True)
MODELS_DIR.mkdir(exist_ok=True)

CAPTURE_MODE = "screen"
SCREEN_MONITOR = 1
YOLO_MODEL = "yolov8n.pt"
CONFIDENCE_THRESHOLD = 0.5
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
SHOW_BOUNDING_BOX = True
SHOW_AIMING_CROSSHAIR = True
SHOW_ANGLES = True
SHOW_FPS = True

COLOR_DETECTION = (0, 255, 0)
COLOR_AIMING = (0, 0, 255)
COLOR_TEXT = (255, 255, 255)

LOG_FILE = LOG_DIR / "aiming_log.txt"
RECOIL_COMPENSATION = True
