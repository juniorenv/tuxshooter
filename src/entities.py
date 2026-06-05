import math
import random

import pygame

from .config import LARGURA, ALTURA, VIDAS_INICIAIS


class Jogador:
    """Tux: move-se pela tela e atira para cima."""

    VELOCIDADE = 8
    COOLDOWN = 220          # ms entre tiros
    INVULN = 1200           # ms de invencibilidade apos levar dano

    def __init__(self, imagem):
        self.imagem = imagem
        self.rect = self.imagem.get_rect()
        self.rect.midbottom = (LARGURA // 2, ALTURA - 20)
        self.vidas = VIDAS_INICIAIS
        self.ultimo_tiro = -9999
        self.invulneravel_ate = 0

    def mover(self, teclas):
        dx = dy = 0
        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            dx -= self.VELOCIDADE
        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            dx += self.VELOCIDADE
        if teclas[pygame.K_UP] or teclas[pygame.K_w]:
            dy -= self.VELOCIDADE
        if teclas[pygame.K_DOWN] or teclas[pygame.K_s]:
            dy += self.VELOCIDADE

        self.rect.x += dx
        self.rect.y += dy

        # Mantem o Tux dentro da tela (e na metade de baixo, no eixo Y).
        self.rect.clamp_ip(pygame.Rect(0, ALTURA // 2, LARGURA, ALTURA // 2))

    def pode_atirar(self, agora):
        return agora - self.ultimo_tiro >= self.COOLDOWN

    def atirar(self, agora, imagem_bala):
        self.ultimo_tiro = agora
        return Bala(self.rect.centerx, self.rect.top, imagem_bala)

    def esta_invulneravel(self, agora):
        return agora < self.invulneravel_ate

    def levar_dano(self, agora):
        self.vidas -= 1
        self.invulneravel_ate = agora + self.INVULN

    def desenhar(self, tela, agora):
        # Pisca enquanto estiver invulneravel.
        if self.esta_invulneravel(agora) and (agora // 120) % 2 == 0:
            return
        tela.blit(self.imagem, self.rect)


class Bala:
    """Projetil disparado pelo Tux (sobe na tela)."""

    VELOCIDADE = 10

    def __init__(self, x, y, imagem):
        self.imagem = imagem
        self.rect = self.imagem.get_rect(center=(x, y))

    def atualizar(self):
        self.rect.y -= self.VELOCIDADE

    @property
    def fora_da_tela(self):
        return self.rect.bottom < 0

    def desenhar(self, tela):
        tela.blit(self.imagem, self.rect)


class Inimigo:
    """Inimigo (bug ou logo do Windows) que desce pela tela."""

    def __init__(self, imagem, velocidade):
        self.imagem = imagem
        self.rect = self.imagem.get_rect()
        self.rect.x = random.randint(0, LARGURA - self.rect.width)
        self.rect.y = -self.rect.height
        self.vy = velocidade
        self.vx = random.choice([-1, 0, 1]) * random.uniform(0.5, 1.5)

    def atualizar(self):
        self.rect.y += self.vy
        self.rect.x += int(self.vx)
        # Quica nas bordas laterais.
        if self.rect.left <= 0 or self.rect.right >= LARGURA:
            self.vx = -self.vx
            self.rect.clamp_ip(pygame.Rect(0, -1000, LARGURA, ALTURA + 2000))

    @property
    def passou(self):
        return self.rect.top > ALTURA

    def desenhar(self, tela):
        tela.blit(self.imagem, self.rect)


class Particula:
    """Faisca usada nas explosoes (efeito visual)."""

    def __init__(self, x, y, cor):
        self.x = float(x)
        self.y = float(y)
        ang = random.uniform(0, 2 * math.pi)
        vel = random.uniform(1.5, 5.0)
        self.vx = math.cos(ang) * vel
        self.vy = math.sin(ang) * vel
        self.vida = random.randint(18, 32)
        self.cor = cor

    def atualizar(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.12  # gravidade leve
        self.vida -= 1

    @property
    def morta(self):
        return self.vida <= 0

    def desenhar(self, tela):
        r = max(1, self.vida // 8)
        pygame.draw.circle(tela, self.cor, (int(self.x), int(self.y)), r)


class Estrela:
    """Estrela do fundo que rola para baixo (parallax simples)."""

    def __init__(self):
        self.x = random.randint(0, LARGURA)
        self.y = random.randint(0, ALTURA)
        self.vel = random.uniform(0.4, 1.8)
        self.tam = random.randint(1, 2)

    def atualizar(self):
        self.y += self.vel
        if self.y > ALTURA:
            self.y = 0
            self.x = random.randint(0, LARGURA)

    def desenhar(self, tela):
        brilho = 120 + int(self.vel * 60)
        brilho = min(255, brilho)
        pygame.draw.circle(tela, (brilho, brilho, brilho), (int(self.x), int(self.y)), self.tam)
