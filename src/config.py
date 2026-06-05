import os
import sys

# --- Janela / loop ---------------------------------------------------------
LARGURA, ALTURA = 800, 600
FPS = 60
TITULO = "Tux Shooter - Trabalho Engenharia de software 5249927"

# --- Regras do jogo --------------------------------------------------------
META_BUGS = 30           # bugs a destruir para vencer
VIDAS_INICIAIS = 3       # vidas do jogador
VOLUME_SONS = 0.5        # volume dos efeitos (0.0 a 1.0); 0.5 = 50%

# --- Estados do jogo (game states) -----------------------------------------
MENU = "MENU"
JOGANDO = "JOGANDO"
PAUSADO = "PAUSADO"
VITORIA = "VITORIA"
DERROTA = "DERROTA"

# --- Cores (R, G, B) -------------------------------------------------------
PRETO = (0, 0, 0)
BRANCO = (245, 245, 245)
CINZA = (160, 160, 170)
LARANJA = (255, 165, 0)
LARANJA_ESC = (210, 120, 0)
AMARELO = (255, 220, 70)
VERMELHO = (220, 60, 60)
VERMELHO_ESC = (150, 30, 30)
VERDE = (90, 210, 110)
VERDE_ESC = (40, 120, 60)
AZUL_CLARO = (120, 230, 255)
AZUL_FUNDO = (12, 16, 34)
AZUL_FUNDO2 = (22, 28, 56)

# --- Caminhos (sempre relativos ao projeto / ao executavel) ----------------
# Quando empacotado com PyInstaller, os assets ficam ao lado do .exe.
# Rodando pelo codigo, sobe um nivel (de src/ para a raiz do projeto).
if getattr(sys, "frozen", False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PASTA_IMAGENS = os.path.join(BASE_DIR, "assets", "imagens")
PASTA_SONS = os.path.join(BASE_DIR, "assets", "sons")
