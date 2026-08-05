import json
import os

CONFIG_FILE = "config.json"

class Config:
    def __init__(self):
        self.ramp_index = 0
        self.use_color = False
        self.remove_bg = False
        self.draw_mode = False
        self.load()

    def load(self):
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.ramp_index = data.get("ramp_index", 0)
                    self.use_color = data.get("use_color", False)
                    self.remove_bg = data.get("remove_bg", False)
                    self.draw_mode = data.get("draw_mode", False)
            except Exception:
                pass

    def save(self):
        try:
            with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                json.dump({
                    "ramp_index": self.ramp_index,
                    "use_color": self.use_color,
                    "remove_bg": self.remove_bg,
                    "draw_mode": self.draw_mode
                }, f, indent=4)
        except Exception:
            pass
