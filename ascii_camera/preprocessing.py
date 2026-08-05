import cv2
import numpy as np

class Preprocessor:
    def __init__(self, use_clahe=False, use_blur=False, gamma=1.0):
        self.use_clahe = use_clahe
        self.use_blur = use_blur
        self.gamma = gamma
        
        self.clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8)) if use_clahe else None
        
        if self.gamma != 1.0:
            inv_gamma = 1.0 / self.gamma
            table = np.array([((i / 255.0) ** inv_gamma) * 255 for i in np.arange(0, 256)]).astype("uint8")
            self.gamma_table = table
        else:
            self.gamma_table = None

    def process(self, frame: np.ndarray) -> np.ndarray:
        """
        Aplica os filtros configurados num frame BGR.
        """
        if self.use_blur:
            frame = cv2.GaussianBlur(frame, (3, 3), 0)
        
        if self.use_clahe and self.clahe is not None:
            # Em cores, aplicamos o CLAHE no canal L (Luminosity) do modelo de cores LAB
            lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
            l, a, b = cv2.split(lab)
            cl = self.clahe.apply(l)
            limg = cv2.merge((cl, a, b))
            frame = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)
            
        if self.gamma_table is not None:
            frame = cv2.LUT(frame, self.gamma_table)
            
        return frame
