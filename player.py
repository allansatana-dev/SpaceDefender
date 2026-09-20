import pygame

from settings import (
    LARGURA,
    ALTURA,
    JOGADOR_LARGURA,
    JOGADOR_ALTURA,
    VELOCIDADE_JOGADOR,
    VIDAS_INICIAIS,
    TIRO_ALTURA,
    CAMINHO_JOGADOR
)

from projectile import PlayerProjectile


# =========================
# JOGADOR
# =========================

class Player:

    def __init__(self):

        # =========================
        # IMAGEM
        # =========================

        self.image = pygame.image.load(
            CAMINHO_JOGADOR
        ).convert_alpha()

        # A imagem original aponta para cima.
        # Rotacionamos para a direita.
        self.image = pygame.transform.rotate(
            self.image,
            -90
        )

        self.image = pygame.transform.scale(
            self.image,
            (JOGADOR_LARGURA, JOGADOR_ALTURA)
        )

        # =========================
        # POSIÇÃO
        # =========================

        self.rect = pygame.Rect(
            100,
            ALTURA // 2,
            JOGADOR_LARGURA,
            JOGADOR_ALTURA
        )

        # =========================
        # ATRIBUTOS
        # =========================

        self.speed = VELOCIDADE_JOGADOR
        self.vidas = VIDAS_INICIAIS

    # =========================
    # MOVIMENTAÇÃO
    # =========================

    def update(self):

        teclas = pygame.key.get_pressed()

        if teclas[pygame.K_w] or teclas[pygame.K_UP]:
            self.rect.y -= self.speed

        if teclas[pygame.K_s] or teclas[pygame.K_DOWN]:
            self.rect.y += self.speed

        if teclas[pygame.K_a] or teclas[pygame.K_LEFT]:
            self.rect.x -= self.speed

        if teclas[pygame.K_d] or teclas[pygame.K_RIGHT]:
            self.rect.x += self.speed

        # =========================
        # LIMITES DA TELA
        # =========================

        if self.rect.left < 0:
            self.rect.left = 0

        if self.rect.right > LARGURA:
            self.rect.right = LARGURA

        if self.rect.top < 0:
            self.rect.top = 0

        if self.rect.bottom > ALTURA:
            self.rect.bottom = ALTURA

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

        x = self.rect.right

        y = (
            self.rect.centery
            - TIRO_ALTURA // 2
        )

        return PlayerProjectile(
            x,
            y
        )

    # =========================
    # PERDER VIDA
    # =========================

    def perder_vida(self):

        self.vidas -= 1

        if self.vidas < 0:
            self.vidas = 0

    # =========================
    # VERIFICAR SE ESTÁ VIVO
    # =========================

    def esta_vivo(self):

        return self.vidas > 0

    # =========================
    # REINICIAR
    # =========================

    def reset(self):

        self.rect.x = 100
        self.rect.y = ALTURA // 2

        self.vidas = VIDAS_INICIAIS