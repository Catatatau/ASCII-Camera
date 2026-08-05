import numpy as np
import cv2

class AsciiConverter:
    def __init__(self, config=None):
        self.ramps = [
            " .:-=+*#%@",                           # Clássica 10
            " ░▒▓█",                                # Blocos Unicode
            " .'`^\",:;Il!i><~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$", # Detalhada
            " ▂▃▄▅▆▇█",                             # Blocos Verticais
            "PIXEL_ART"                             # Flag para modo Half-Block
        ]
        
        self.ramp_index = config.ramp_index if config else 0
        self.set_ramp(self.ramp_index)

    def is_pixel_art_mode(self):
        return self.ramp == "PIXEL_ART"

    def set_ramp(self, index: int):
        self.ramp_index = index % len(self.ramps)
        self.ramp = self.ramps[self.ramp_index]
        if not self.is_pixel_art_mode():
            self.num_chars = len(self.ramp)
            self.ramp_arr = np.array(list(self.ramp))

    def cycle_ramp(self) -> int:
        self.set_ramp(self.ramp_index + 1)
        return self.ramp_index

    def convert(self, frame: np.ndarray, use_color: bool = False, canvas: np.ndarray = None) -> str:
        h, w = frame.shape[:2]
        
        # Extração das matrizes de canais para cor e canvas
        b, g, r = frame[:, :, 0], frame[:, :, 1], frame[:, :, 2]
        if canvas is not None:
            cb, cg, cr = canvas[:, :, 0], canvas[:, :, 1], canvas[:, :, 2]
        else:
            cb = cg = cr = None

        lines = []

        # -------------------------------------------------------------
        # MODO PIXEL ART (HALF-BLOCK) - Dobro de resolução vertical!
        # -------------------------------------------------------------
        if self.is_pixel_art_mode():
            # Itera de 2 em 2 linhas (upper pixel = fg, lower pixel = bg)
            for y in range(0, h - 1, 2):
                row_str = []
                for x in range(w):
                    ru, gu, bu = r[y, x], g[y, x], b[y, x]
                    rd, gd, bd = r[y+1, x], g[y+1, x], b[y+1, x]
                    
                    # Sobrescrita do Canvas se houver tinta
                    if canvas is not None:
                        if cr[y, x] > 0 or cg[y, x] > 0 or cb[y, x] > 0:
                            ru, gu, bu = cr[y, x], cg[y, x], cb[y, x]
                        if cr[y+1, x] > 0 or cg[y+1, x] > 0 or cb[y+1, x] > 0:
                            rd, gd, bd = cr[y+1, x], cg[y+1, x], cb[y+1, x]
                    
                    if not use_color:
                        # Grayscale fallback
                        lu = int(0.299*ru + 0.587*gu + 0.114*bu)
                        ld = int(0.299*rd + 0.587*gd + 0.114*bd)
                        ru, gu, bu = lu, lu, lu
                        rd, gd, bd = ld, ld, ld

                    # ▀ (Upper half block)
                    row_str.append(f"\033[38;2;{ru};{gu};{bu}m\033[48;2;{rd};{gd};{bd}m▀")
                
                # Reseta o fundo e a cor para as quebras de linha
                lines.append("".join(row_str) + "\033[0m")
            return "\n".join(lines)

        # -------------------------------------------------------------
        # MODO TEXTO ASCII CLÁSSICO
        # -------------------------------------------------------------
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        indices = (gray.astype(np.uint16) * (self.num_chars - 1)) // 255
        chars = self.ramp_arr[indices]
        
        for y in range(h):
            row_str = []
            for x in range(w):
                # O desenho do Canvas sempre substitui o caractere por Bloco Sólido (█)
                if canvas is not None and (cr[y,x] > 0 or cg[y,x] > 0 or cb[y,x] > 0):
                    rv, gv, bv = cr[y,x], cg[y,x], cb[y,x]
                    if use_color:
                        row_str.append(f"\033[38;2;{rv};{gv};{bv}m█")
                    else:
                        row_str.append("█")
                else:
                    c = chars[y, x]
                    if c == ' ':
                        row_str.append(' ')
                    else:
                        if use_color:
                            rv, gv, bv = r[y, x], g[y, x], b[y, x]
                            row_str.append(f"\033[38;2;{rv};{gv};{bv}m{c}")
                        else:
                            row_str.append(c)
            
            lines.append("".join(row_str) + "\033[0m")
            
        return "\n".join(lines)
