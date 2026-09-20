import pygame

from settings import (
    TIRO_LARGURA,
    TIRO_ALTURA,
    VELOCIDADE_TIRO,
    TIRO_INIMIGO_LARGURA,
    TIRO_INIMIGO_ALTURA,
    VELOCIDADE_TIRO_INIMIGO,
    CAMINHO_LASER,
    CAMINHO_TIRO_INIMIGO
)


# =========================
# PROJÉTIL DO JOGADOR
# =========================

class PlayerProjectile:

    def __init__(self, x, y):

        # Carrega a imagem do laser
        self.image = pygame.image.load(
            CAMINHO_LASER
        ).convert_alpha()

        # Rotaciona o laser para a direita
        self.image = pygame.transform.rotate(
            self.image,
            -90
        )

        # Ajusta o tamanho
        self.image = pygame.transform.scale(
            self.image,
            (TIRO_LARGURA, TIRO_ALTURA)
        )

        # Cria o retângulo usado para posição e colisão
        self.rect = pygame.Rect(
            x,
            y,
            TIRO_LARGURA,
            TIRO_ALTURA
        )

        self.speed = VELOCIDADE_TIRO

    def update(self):

        # Move o laser para a direita
        self.rect.x += self.speed

    def draw(self, screen):

        # Desenha o laser na tela
        screen.blit(
            self.image,
            self.rect
        )

    def saiu_da_tela(self, largura_tela):

        return self.rect.left >= largura_tela


# =========================
# PROJÉTIL DO INIMIGO
# =========================

class EnemyProjectile:

    def __init__(self, x, y):

        # Carrega a imagem do tiro inimigo
        self.image = pygame.image.load(
            CAMINHO_TIRO_INIMIGO
        ).convert_alpha()

        # Ajusta o tamanho
        self.image = pygame.transform.scale(
            self.image,
            (
                TIRO_INIMIGO_LARGURA,
                TIRO_INIMIGO_ALTURA
            )
        )

        # Cria o retângulo usado para posição e colisão
        self.rect = pygame.Rect(
            x,
            y,
            TIRO_INIMIGO_LARGURA,
            TIRO_INIMIGO_ALTURA
        )

        self.speed = VELOCIDADE_TIRO_INIMIGO

    def update(self):

        # Move o tiro para a esquerda
        self.rect.x -= self.speed

    def draw(self, screen):

        # Desenha o tiro na tela
        screen.blit(
            self.image,
            self.rect
        )

    def saiu_da_tela(self):

        return self.rect.right <= 0