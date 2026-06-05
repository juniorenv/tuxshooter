import os

import pygame

from .config import PASTA_IMAGENS, PASTA_SONS, VOLUME_SONS


def carregar_imagem(nome, tamanho=None):
    """Carrega assets/imagens/<nome>. Levanta erro claro se o arquivo faltar."""
    caminho = os.path.join(PASTA_IMAGENS, nome)
    if not os.path.isfile(caminho):
        raise FileNotFoundError(
            "Asset de imagem nao encontrado: {}\n"
            "Gere os assets antes de jogar:  python gerar_assets.py".format(caminho)
        )
    imagem = pygame.image.load(caminho).convert_alpha()
    if tamanho is not None:
        imagem = pygame.transform.smoothscale(imagem, tamanho)
    return imagem


def carregar_som(nome, audio_ok):
    """Carrega assets/sons/<nome>; retorna None se nao houver audio/arquivo."""
    if not audio_ok:
        return None
    caminho = os.path.join(PASTA_SONS, nome)
    if os.path.isfile(caminho):
        try:
            som = pygame.mixer.Sound(caminho)
            som.set_volume(VOLUME_SONS)
            return som
        except pygame.error:
            return None
    return None


def tocar(som):
    """Toca um som se ele existir (nunca quebra se nao houver audio)."""
    if som is not None:
        som.play()
