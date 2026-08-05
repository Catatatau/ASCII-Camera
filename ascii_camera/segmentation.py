import cv2
import numpy as np
import mediapipe as mp

class BackgroundRemover:
    def __init__(self):
        self.mp_selfie = mp.solutions.selfie_segmentation
        # model_selection=0 é mais rápido para corpo/rosto padrão (geral).
        self.segmenter = self.mp_selfie.SelfieSegmentation(model_selection=0)

    def remove_background(self, frame: np.ndarray) -> np.ndarray:
        """
        Segmenta a pessoa do fundo da imagem BGR providenciada e mascara o resto como preto absoluto.
        Isso faz com que o texto resultante fique vazio na região do background.
        """
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Processa a imagem (pesado, vai afetar FPS ligeiramente)
        results = self.segmenter.process(rgb_frame)
        
        # Máscara probabilística (se > 0.5, é a pessoa)
        condition = np.stack((results.segmentation_mask,) * 3, axis=-1) > 0.5
        
        # Fundo preto (que virará espaços na conversão ASCII devido a intensidade = 0)
        bg_image = np.zeros(frame.shape, dtype=np.uint8)
        
        # Onde a condição for verdadeira, pega o frame. Senão, pega o bg_image preto
        output_image = np.where(condition, frame, bg_image)
        return output_image

    def close(self):
        self.segmenter.close()
