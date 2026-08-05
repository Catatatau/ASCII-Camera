import time
import sys
import msvcrt
import traceback
import os
import cv2
from camera import Camera
from ascii_converter import AsciiConverter
from renderer import Renderer
from preprocessing import Preprocessor
from config import Config
from segmentation import BackgroundRemover
from hand_tracking import HandTracker

def get_terminal_resolution():
    try:
        size = os.get_terminal_size()
        return size.columns, max(10, size.lines - 2)
    except OSError:
        return 120, 40

def main():
    config = Config()
    
    try:
        cam = Camera()
    except RuntimeError as e:
        print(f"Erro de Câmera: {e}")
        return

    converter = AsciiConverter(config)
    renderer = Renderer()
    preprocessor = Preprocessor(use_clahe=False, use_blur=True, gamma=1.2)
    bg_remover = BackgroundRemover()
    hand_tracker = HandTracker()

    os.system("") 

    last_time = time.time()
    frames = 0
    fps = 0.0
    target_width, target_height = get_terminal_resolution()

    try:
        while True:
            frame_start = time.time()
            
            if frames % 30 == 0:
                new_w, new_h = get_terminal_resolution()
                if new_w != target_width or new_h != target_height:
                    target_width, target_height = new_w, new_h
                    renderer.clear()
                    
            keys = []
            while msvcrt.kbhit():
                key = msvcrt.getch()
                if key in (b'\x00', b'\xe0'):
                    msvcrt.getch()
                    continue
                try:
                    keys.append(key.decode('utf-8').upper())
                except Exception:
                    pass
            
            if 'Q' in keys:
                break
            if 'C' in keys:
                config.ramp_index = converter.cycle_ramp()
                config.save()
            if 'X' in keys:
                config.use_color = not config.use_color
                config.save()
            if 'B' in keys:
                config.remove_bg = not config.remove_bg
                config.save()
            if 'D' in keys:
                config.draw_mode = not config.draw_mode
                config.save()
            if 'L' in keys:
                hand_tracker.clear_canvas()
            
            frame = cam.get_frame()
            if frame is None:
                time.sleep(0.001)
                continue

            try:
                processed = preprocessor.process(frame)
                canvas = None
                
                # Se o modo desenho estiver ativo, calculamos o canvas separado da imagem
                if config.draw_mode:
                    processed, canvas = hand_tracker.process(processed)

                if config.remove_bg:
                    processed = bg_remover.remove_background(processed)
                    
                # Ajuste Mágico: O modo Pixel Art (Half-Block) precisa de 2x mais linhas 
                # de imagem para preencher as mesmas linhas do console.
                img_height = target_height * 2 if converter.is_pixel_art_mode() else target_height
                    
                resized = cv2.resize(processed, (target_width, img_height))
                
                if canvas is not None:
                    canvas_resized = cv2.resize(canvas, (target_width, img_height))
                else:
                    canvas_resized = None
                    
                ascii_str = converter.convert(resized, use_color=config.use_color, canvas=canvas_resized)
            except Exception as e:
                continue
            
            frames += 1
            curr_time = time.time()
            dt = curr_time - last_time
            if dt >= 1.0:
                fps = frames / dt
                frames = 0
                last_time = curr_time
            
            # Cores UI Premium
            C_CYAN = "\033[96m"
            C_YELLOW = "\033[93m"
            C_GREEN = "\033[92m"
            C_RED = "\033[91m"
            C_RESET = "\033[0m"
            
            color_str = f"{C_GREEN}ON{C_RESET}" if config.use_color else f"{C_RED}OFF{C_RESET}"
            bg_str = f"{C_GREEN}ON{C_RESET}" if config.remove_bg else f"{C_RED}OFF{C_RESET}"
            draw_str = f"{C_GREEN}ON{C_RESET}" if config.draw_mode else f"{C_RED}OFF{C_RESET}"
            
            # Barra de Status Formatada
            status = (f"\n {C_CYAN}◆ FPS: {fps:.1f}{C_RESET}  ┃  "
                      f"{C_YELLOW}[X]{C_RESET} Cor: {color_str}  ┃  "
                      f"{C_YELLOW}[B]{C_RESET} Tela Verde: {bg_str}  ┃  "
                      f"{C_YELLOW}[D]{C_RESET} Magic Pen: {draw_str}  ┃  "
                      f"{C_YELLOW}[C]{C_RESET} Mudar Estilo  ┃  "
                      f"{C_YELLOW}[L]{C_RESET} Limpar Tela  ┃  "
                      f"{C_YELLOW}[Q]{C_RESET} Sair")
            
            # Ocultando caracteres invisíveis ANSI na contagem do ljust não é simples, 
            # então imprimiremos diretamente.
            renderer.render(ascii_str + status)
            
            elapsed = time.time() - frame_start
            time.sleep(max(0, 1.0/30.0 - elapsed))

    except KeyboardInterrupt:
        pass
    except Exception as e:
        sys.stderr.write(f"\nErro Inesperado: {e}\n")
        traceback.print_exc()
    finally:
        cam.release()
        bg_remover.close()
        hand_tracker.close()
        renderer.cleanup()
        print("\n" * (target_height + 2))
        print("Sessão encerrada.")

if __name__ == "__main__":
    main()
