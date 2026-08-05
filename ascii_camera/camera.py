import cv2
import numpy as np
import threading
import queue
import time

class Camera:
    def __init__(self, camera_id=0):
        """
        Inicializa a câmera com OpenCV e inicia uma thread separada para captura contínua.
        """
        self.cap = cv2.VideoCapture(camera_id)
        if not self.cap.isOpened():
            raise RuntimeError(f"Falha ao abrir a câmera de ID {camera_id}")
        
        # Fila com tamanho 1 para manter sempre apenas o frame mais atualizado
        self.q = queue.Queue(maxsize=1)
        self.running = True
        
        # Inicia a thread
        self.thread = threading.Thread(target=self._capture_loop, daemon=True)
        self.thread.start()

    def _capture_loop(self):
        """Loop infinito da thread secundária responsável pela leitura USB da câmera."""
        while self.running:
            ret, frame = self.cap.read()
            if not ret:
                time.sleep(0.01)
                continue
            
            # Espelha o frame horizontalmente, agora nativamente colorido (BGR)
            flipped = cv2.flip(frame, 1)
            
            # Tenta limpar a fila se estiver cheia (descarta o frame velho)
            try:
                self.q.get_nowait()
            except queue.Empty:
                pass
            
            # Coloca o frame novo
            try:
                self.q.put_nowait(flipped)
            except queue.Full:
                pass

    def get_frame(self) -> np.ndarray | None:
        """
        Pega o último frame capturado de forma rápida e não bloqueante.
        """
        try:
            return self.q.get(timeout=0.01)
        except queue.Empty:
            return None

    def release(self):
        """Libera a thread e os recursos."""
        self.running = False
        if self.thread.is_alive():
            self.thread.join(timeout=1.0)
        if self.cap.isOpened():
            self.cap.release()
