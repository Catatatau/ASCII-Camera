import sys

class Renderer:
    def __init__(self):
        # Ao inicializar, escondemos o cursor para evitar flickering indesejado na tela.
        self.hide_cursor()

    def hide_cursor(self):
        sys.stdout.write("\033[?25l")
        sys.stdout.flush()

    def show_cursor(self):
        sys.stdout.write("\033[?25h")
        sys.stdout.flush()

    def clear(self):
        """
        Limpa todo o terminal e reposiciona o cursor no topo.
        Útil especialmente quando a janela sofre resize e precisamos remover artefatos.
        """
        sys.stdout.write("\033[2J\033[H")
        sys.stdout.flush()

    def render(self, ascii_str: str):
        """
        Renderiza o ASCII no terminal utilizando escape sequences
        para evitar flicker, voltando para o início (0,0) a cada frame.
        """
        sys.stdout.write("\033[H")
        sys.stdout.write(ascii_str)
        sys.stdout.flush()

    def cleanup(self):
        """
        Restaura o estado do terminal para o uso normal.
        """
        self.show_cursor()
