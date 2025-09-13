import time
from services.mapping_emotions import color_for_emotion

class EmotionService:
    def __init__(self, label="default"):
        self._label = label
        self._color = color_for_emotion(self._label)
        self._t0 = time.ticks_ms()

    def to_dict(self):
        return{
            "label": self._label,
            "color": self._color,
            "age_ms": time.ticks_diff(self._t0, time.ticks_ms()),
        }

    def set_emotion(self, label):
        self._label = label
        self._color = color_for_emotion(self._label)
        self._t0 = time.ticks_ms()
        return self.to_dict()

    def get_color(self):
        return self._color

    def label(self):
        return self._label