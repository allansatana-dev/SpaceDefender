import random
import pygame

from settings import (
    LARGURA,
    ALTURA,
    INIMIGO_LARGURA,
    INIMIGO_ALTURA,
    VELOCIDADE_INIMIGO,
    TIRO_INIMIGO_LARGURA,
    TIRO_INIMIGO_ALTURA,
    CAMINHO_INIMIGO
)

from projectile import EnemyProjectile


# =========================
# INIMIGO
# =========================

class Enemy:

    def __init__(self):

        # =========================
        # IMAGEM
        # =========================

        self.image = pygame.image.load(
            CAMINHO_INIMIGO
        ).convert_alpha()

        self.image = pygame.transform.scale(
            self.image,
            (INIMIGO_LARGURA, INIMIGO_ALTURA)
        )

        # =========================
        # POSIÇÃO
        # =========================

        self.rect = pygame.Rect(
            700,
            random.randint(
                0,
                ALTURA - INIMIGO_ALTURA
            ),
            INIMIGO_LARGURA,
            INIMIGO_ALTURA
        )

        # =========================
        # VELOCIDADE
        # =========================

        self.speed = VELOCIDADE_INIMIGO

    # =========================
    # MOVIMENTAÇÃO
    # =========================

    def update(self):

        self.rect.x -= self.speed

    # =========================
    # DESENHAR
    # =========================

    def draw(self, screen):

        screen.blit(
            self.image,
            self.rect
        )

    # =========================
    # ATIRAR
    # =========================

    def shoot(self):

        x = self.rect.x

        y = (
            self.rect.centery
            - TIRO_INIMIGO_ALTURA // 2
        )

        return EnemyProjectile(
            x,
            y
        )

    # =========================
    # VERIFICAR SE SAIU DA TELA
    # =========================

    def saiu_da_tela(self):

        return self.rect.right <= 0

    # =========================
    # REPOSICIONAR
    # =========================

    def respawn(self):

        self.rect.x = LARGURA

        self.rect.y = random.randint(
            0,
            ALTURA - INIMIGO_ALTURA
        )

    # =========================
    # REINICIAR
    # =========================

    def reset(self):

        self.rect.x = 700

        self.rect.y = random.randint(
            0,
            ALTURA - INIMIGO_ALTURA
        )