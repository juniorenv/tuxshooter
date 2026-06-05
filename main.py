import sys

import pygame

from src.config import (
    LARGURA, ALTURA, FPS, TITULO,
    MENU, JOGANDO, PAUSADO, VITORIA, DERROTA,
)
from src.assets import carregar_imagem, carregar_som, tocar
from src.entities import Estrela
from src.game import Partida
from src.ui import desenhar_menu, desenhar_fim, desenhar_pausa


def carregar_assets(audio_ok):
    """Carrega todas as imagens (obrigatorias) e sons (opcionais)."""
    return {
        "tux": carregar_imagem("tux.png", (50, 60)),
        "bug": carregar_imagem("bug.png", (42, 34)),
        "winxp": carregar_imagem("winxp.png", (40, 38)),
        "bala": carregar_imagem("bala.png", (8, 18)),
        "fundo": carregar_imagem("fundo.png", (LARGURA, ALTURA)),
        "som_tiro": carregar_som("tiro.wav", audio_ok),
        "som_explosao": carregar_som("explosao.wav", audio_ok),
        "som_dano": carregar_som("dano.wav", audio_ok),
    }


def main():
    pygame.init()

    # Audio e opcional: o jogo continua funcionando sem placa de som.
    audio_ok = True
    try:
        pygame.mixer.init()
    except pygame.error:
        audio_ok = False

    tela = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption(TITULO)
    relogio = pygame.time.Clock()

    # Fontes (fonte padrao do pygame -> sempre disponivel).
    fontes = {
        "titulo": pygame.font.Font(None, 72),
        "medio": pygame.font.Font(None, 36),
        "sub": pygame.font.Font(None, 30),
        "pequeno": pygame.font.Font(None, 28),
        "hud": pygame.font.Font(None, 30),
    }

    try:
        assets = carregar_assets(audio_ok)
    except FileNotFoundError as erro:
        pygame.quit()
        print(erro)
        sys.exit(1)

    estrelas = [Estrela() for _ in range(60)]
    estado = MENU
    partida = None

    rodando = True
    while rodando:
        dt = relogio.tick(FPS)         # ms desde o ultimo frame
        agora = pygame.time.get_ticks()

        # ---------------- Eventos ----------------
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False

            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    if estado in (MENU, VITORIA, DERROTA, PAUSADO):
                        rodando = False
                    else:  # JOGANDO -> ESC volta ao menu
                        estado = MENU

                if estado == MENU and evento.key == pygame.K_RETURN:
                    partida = Partida(assets)
                    estado = JOGANDO

                elif estado in (VITORIA, DERROTA) and evento.key == pygame.K_RETURN:
                    partida = Partida(assets)
                    estado = JOGANDO

                elif estado == JOGANDO and evento.key == pygame.K_p:
                    estado = PAUSADO
                elif estado == PAUSADO and evento.key == pygame.K_p:
                    estado = JOGANDO

        # ---------------- Atualizacao ----------------
        for e in estrelas:
            e.atualizar()

        if estado == JOGANDO and partida is not None:
            teclas = pygame.key.get_pressed()
            partida.atualizar(dt, agora, teclas)
            if partida.venceu:
                tocar(assets["som_explosao"])
                estado = VITORIA
            elif partida.perdeu:
                estado = DERROTA

        # ---------------- Desenho ----------------
        if estado == MENU:
            desenhar_menu(tela, fontes, assets, estrelas)

        elif estado in (JOGANDO, PAUSADO) and partida is not None:
            tela.blit(assets["fundo"], (0, 0))
            for e in estrelas:
                e.desenhar(tela)
            partida.desenhar(tela, fontes["hud"], agora)
            if estado == PAUSADO:
                desenhar_pausa(tela, fontes)

        elif estado == VITORIA:
            desenhar_fim(tela, fontes, assets, estrelas, True,
                         partida.bugs_destruidos if partida else 0)

        elif estado == DERROTA:
            desenhar_fim(tela, fontes, assets, estrelas, False,
                         partida.bugs_destruidos if partida else 0)

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
