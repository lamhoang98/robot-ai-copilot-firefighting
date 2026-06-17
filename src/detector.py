import cv2
import numpy as np
from ultralytics import YOLO
import mss
import config

class ScreenCapturer:
    def __init__(self, monitor=1):
        self.sct = mss.mss()
        self.monitor = self.sct.monitors[monitor]
    
    def capture(self):
        screenshot = self.sct.grab(self.monitor)
        frame = np.array(screenshot)
        return cv2.cvtColor(frame, cv2.COLOR_RGBA2BGR)
    
    def get_resolution(self):
        return self.monitor["width"], self.monitor["height"]

class PersonDetector:
    def __init__(self, model_name="yolov8n.pt", confidence=0.5):
        self.model = YOLO(model_name)
        self.confidence = confidence
    
    def detect(self, frame):
        results = self.model(frame, verbose=False)
        detections = []
        for result in results:
            for box in result.boxes:
                if int(box.cls[0]) == 0:
                    x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                    conf = float(box.conf[0])
                    if conf >= self.confidence:
                        x, y = int((x1 + x2) / 2), int((y1 + y2) / 2)
                        w, h = int(x2 - x1), int(y2 - y1)
                        detections.append({"x": x, "y": y, "w": w, "h": h, "conf": conf, "x1": int(x1), "y1": int(y1), "x2": int(x2), "y2": int(y2)})
        return detections

class PersonTracker:
    def __init__(self, max_age=30):
        self.tracks = {}
        self.next_id = 0
        self.max_age = max_age
    
    def update(self, detections):
        matched, unmatched_det, unmatched_trk = self._match(detections)
        for det_idx, trk_idx in matched:
            det = detections[det_idx]
            self.tracks[trk_idx].update({"x": det["x"], "y": det["y"], "w": det["w"], "h": det["h"], "age": 0})
            self.tracks[trk_idx]["detections"].append(det)
        for det_idx in unmatched_det:
            det = detections[det_idx]
            self.tracks[self.next_id] = {"id": self.next_id, "x": det["x"], "y": det["y"], "w": det["w"], "h": det["h"], "age": 0, "detections": [det]}
            self.next_id += 1
        for trk_idx in unmatched_trk:
            self.tracks[trk_idx]["age"] += 1
        self.tracks = {k: v for k, v in self.tracks.items() if v["age"] <= self.max_age}
        return list(self.tracks.values())
    
    def _match(self, detections):
        if not self.tracks or not detections:
            return [], list(range(len(detections))), list(self.tracks.keys())
        matched, unmatched_det, unmatched_trk = [], list(range(len(detections))), list(self.tracks.keys())
        iou_matrix = np.zeros((len(detections), len(self.tracks)))
        for i, det in enumerate(detections):
            for j, (_, trk) in enumerate(self.tracks.items()):
                iou_matrix[i, j] = self._iou(det, trk)
        while iou_matrix.size > 0:
            i, j = np.unravel_index(np.argmax(iou_matrix), iou_matrix.shape)
            if iou_matrix[i, j] > 0.3:
                matched.append((i, list(self.tracks.keys())[j]))
                unmatched_det.remove(i)
                unmatched_trk.remove(list(self.tracks.keys())[j])
                iou_matrix = np.delete(iou_matrix, i, axis=0)
                iou_matrix = np.delete(iou_matrix, j, axis=1)
            else:
                break
        return matched, unmatched_det, unmatched_trk
    
    @staticmethod
    def _iou(det, trk):
        x1_1, y1_1 = det["x"] - det["w"]//2, det["y"] - det["h"]//2
        x2_1, y2_1 = det["x"] + det["w"]//2, det["y"] + det["h"]//2
        x1_2, y1_2 = trk["x"] - trk["w"]//2, trk["y"] - trk["h"]//2
        x2_2, y2_2 = trk["x"] + trk["w"]//2, trk["y"] + trk["h"]//2
        inter = max(0, min(x2_1, x2_2) - max(x1_1, x1_2)) * max(0, min(y2_1, y2_2) - max(y1_1, y1_2))
        union = det["w"] * det["h"] + trk["w"] * trk["h"] - inter
        return inter / union if union > 0 else 0
