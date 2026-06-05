import random

import pygame

from .config import META_BUGS, BRANCO, CINZA, VERDE, VERMELHO, AMARELO, LARGURA
from .entities import Jogador, Inimigo, Particula
from .assets import tocar
from .ui import desenhar_texto, desenhar_coracao


class Partida:
    """Encapsula uma partida; criar uma nova instancia reinicia o jogo."""

    def __init__(self, assets):
        self.assets = assets
        self.jogador = Jogador(assets["tux"])
        self.balas = []
        self.inimigos = []
        self.particulas = []
        self.bugs_destruidos = 0
        self.tempo_spawn = 0
        self.intervalo_spawn = 1100  # ms; diminui conforme o jogo avanca

    @property
    def venceu(self):
        return self.bugs_destruidos >= META_BUGS

    @property
    def perdeu(self):
        return self.jogador.vidas <= 0

    def explodir(self, x, y, cor):
        for _ in range(14):
            self.particulas.append(Particula(x, y, cor))

    def atualizar(self, dt, agora, teclas):
        # --- Jogador ---
        self.jogador.mover(teclas)
        if teclas[pygame.K_SPACE] and self.jogador.pode_atirar(agora):
            self.balas.append(self.jogador.atirar(agora, self.assets["bala"]))
            tocar(self.assets["som_tiro"])

        # --- Spawn de inimigos (mais rapido conforme o progresso) ---
        self.tempo_spawn += dt
        self.intervalo_spawn = max(360, 1100 - self.bugs_destruidos * 22)
        if self.tempo_spawn >= self.intervalo_spawn:
            self.tempo_spawn = 0
            velocidade = min(2.0 + self.bugs_destruidos * 0.08, 6.0)
            # Inimigo aleatorio: ora um "bug", ora o logo do Windows.
            imagem = random.choice([self.assets["bug"], self.assets["winxp"]])
            self.inimigos.append(Inimigo(imagem, velocidade))

        # --- Balas ---
        for bala in self.balas:
            bala.atualizar()
        self.balas = [b for b in self.balas if not b.fora_da_tela]

        # --- Inimigos ---
        for inimigo in self.inimigos:
            inimigo.atualizar()

        # --- Colisoes bala x inimigo ---
        balas_vivas = []
        for bala in self.balas:
            atingiu = False
            for inimigo in self.inimigos:
                if inimigo.rect.colliderect(bala.rect):
                    atingiu = True
                    self.inimigos.remove(inimigo)
                    self.bugs_destruidos += 1
                    self.explodir(inimigo.rect.centerx, inimigo.rect.centery, VERMELHO)
                    tocar(self.assets["som_explosao"])
                    break
            if not atingiu:
                balas_vivas.append(bala)
        self.balas = balas_vivas

        # --- Inimigos que colidem com o Tux ou escapam pela base ---
        restantes = []
        for inimigo in self.inimigos:
            if not self.jogador.esta_invulneravel(agora) and inimigo.rect.colliderect(self.jogador.rect):
                self.jogador.levar_dano(agora)
                self.explodir(inimigo.rect.centerx, inimigo.rect.centery, AMARELO)
                tocar(self.assets["som_dano"])
                continue  # inimigo e removido na colisao
            if inimigo.passou:
                self.jogador.levar_dano(agora)
                tocar(self.assets["som_dano"])
                continue
            restantes.append(inimigo)
        self.inimigos = restantes

        # --- Particulas ---
        for p in self.particulas:
            p.atualizar()
        self.particulas = [p for p in self.particulas if not p.morta]

    def desenhar(self, tela, fonte_hud, agora):
        for inimigo in self.inimigos:
            inimigo.desenhar(tela)
        for bala in self.balas:
            bala.desenhar(tela)
        for p in self.particulas:
            p.desenhar(tela)
        self.jogador.desenhar(tela, agora)
        self.desenhar_hud(tela, fonte_hud)

    def desenhar_hud(self, tela, fonte):
        # Progresso (bugs destruidos / meta).
        desenhar_texto(tela, "Bugs: {}/{}".format(self.bugs_destruidos, META_BUGS),
                       fonte, BRANCO, 16, 12, centro=False)
        # Barra de progresso.
        largura_barra = 200
        prog = self.bugs_destruidos / META_BUGS
        pygame.draw.rect(tela, CINZA, (16, 40, largura_barra, 12), 1)
        pygame.draw.rect(tela, VERDE, (16, 40, int(largura_barra * min(1.0, prog)), 12))

        # Vidas (coracoes no canto direito).
        for i in range(self.jogador.vidas):
            desenhar_coracao(tela, LARGURA - 24 - i * 28, 22, escala=1.4)
