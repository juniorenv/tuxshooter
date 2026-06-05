import pygame

from .config import (
    LARGURA, ALTURA,
    BRANCO, CINZA, LARANJA, AMARELO, VERDE, VERMELHO,
)


def desenhar_texto(tela, texto, fonte, cor, x, y, centro=True):
    img = fonte.render(texto, True, cor)
    rect = img.get_rect()
    if centro:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    tela.blit(img, rect)
    return rect


def desenhar_coracao(tela, x, y, escala=1.0, cor=VERMELHO):
    """Desenha um coracao simples (duas circunferencias + triangulo)."""
    r = int(7 * escala)
    pygame.draw.circle(tela, cor, (x - r // 2, y), r // 2 + 1)
    pygame.draw.circle(tela, cor, (x + r // 2, y), r // 2 + 1)
    pygame.draw.polygon(tela, cor, [(x - r, y), (x + r, y), (x, y + r + 2)])


def desenhar_menu(tela, fontes, assets, estrelas):
    tela.blit(assets["fundo"], (0, 0))
    for e in estrelas:
        e.desenhar(tela)

    # Tux grande no topo.
    tux_grande = pygame.transform.smoothscale(assets["tux"], (110, 132))
    tela.blit(tux_grande, tux_grande.get_rect(center=(LARGURA // 2, 130)))

    desenhar_texto(tela, "TUX SHOOTER", fontes["titulo"], LARANJA, LARGURA // 2, 250)
    desenhar_texto(tela, "Defenda o Linux dos bugs!", fontes["sub"], CINZA, LARGURA // 2, 292)

    # Lista de controles.
    controles = [
        "Controles:",
        "Setas / WASD  -  Mover",
        "ESPACO        -  Atirar",
        "P             -  Pausar",
        "ESC           -  Sair",
    ]
    y = 350
    for i, linha in enumerate(controles):
        cor = AMARELO if i == 0 else BRANCO
        fonte = fontes["medio"] if i == 0 else fontes["pequeno"]
        desenhar_texto(tela, linha, fonte, cor, LARGURA // 2, y)
        y += 34

    desenhar_texto(tela, "Pressione ENTER para jogar",
                   fontes["medio"], VERDE, LARGURA // 2, ALTURA - 50)


def desenhar_fim(tela, fontes, assets, estrelas, venceu, bugs):
    tela.blit(assets["fundo"], (0, 0))
    for e in estrelas:
        e.desenhar(tela)

    if venceu:
        desenhar_texto(tela, "VITORIA!", fontes["titulo"], VERDE, LARGURA // 2, 200)
        desenhar_texto(tela, "Voce limpou o sistema dos bugs!",
                       fontes["medio"], BRANCO, LARGURA // 2, 260)
    else:
        desenhar_texto(tela, "DERROTA", fontes["titulo"], VERMELHO, LARGURA // 2, 200)
        desenhar_texto(tela, "Os bugs tomaram o sistema...",
                       fontes["medio"], BRANCO, LARGURA // 2, 260)

    desenhar_texto(tela, "Bugs destruidos: {}".format(bugs),
                   fontes["medio"], AMARELO, LARGURA // 2, 320)
    desenhar_texto(tela, "ENTER - jogar de novo      ESC - sair",
                   fontes["pequeno"], CINZA, LARGURA // 2, ALTURA - 60)


def desenhar_pausa(tela, fontes):
    # Sobreposicao semitransparente.
    overlay = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 150))
    tela.blit(overlay, (0, 0))
    desenhar_texto(tela, "PAUSADO", fontes["titulo"], BRANCO, LARGURA // 2, ALTURA // 2 - 20)
    desenhar_texto(tela, "Pressione P para continuar",
                   fontes["pequeno"], CINZA, LARGURA // 2, ALTURA // 2 + 30)
