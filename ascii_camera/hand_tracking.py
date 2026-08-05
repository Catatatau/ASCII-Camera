import cv2
import numpy as np
import mediapipe as mp

class HandTracker:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7
        )
        self.canvas = None
        self.prev_x, self.prev_y = 0, 0
        self.is_drawing = False

    def process(self, frame: np.ndarray):
        if self.canvas is None or self.canvas.shape != frame.shape:
            self.canvas = np.zeros_like(frame)

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb_frame)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                thumb_tip = hand_landmarks.landmark[4]
                index_tip = hand_landmarks.landmark[8]

                h, w, c = frame.shape
                tx, ty = int(thumb_tip.x * w), int(thumb_tip.y * h)
                ix, iy = int(index_tip.x * w), int(index_tip.y * h)

                distance = np.sqrt((tx - ix)**2 + (ty - iy)**2)
                cx, cy = (tx + ix) // 2, (ty + iy) // 2

                if distance < 40:
                    if not self.is_drawing:
                        self.is_drawing = True
                        self.prev_x, self.prev_y = cx, cy
                    else:
                        # Desenhamos uma linha mais fina no canvas original
                        # Vamos usar uma cor neon ciano (BGR: 255, 255, 0)
                        cv2.line(self.canvas, (self.prev_x, self.prev_y), (cx, cy), (255, 255, 0), 10)
                        self.prev_x, self.prev_y = cx, cy
                else:
                    self.is_drawing = False
        else:
            self.is_drawing = False

        # Na Fase 5, não mesclamos mais o canvas no frame nativamente, 
        # devolvemos o canvas separado para o ASCII converter transformá-lo num bloco sólido.
        return frame, self.canvas

    def clear_canvas(self):
        if self.canvas is not None:
            self.canvas = np.zeros_like(self.canvas)
            
    def close(self):
        self.hands.close()
