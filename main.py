import pygame
import random

# Inicializa o Pygame
pygame.init()

# =========================
# CONFIGURAÇÕES DA JANELA
# =========================

LARGURA = 960
ALTURA = 540
FPS = 60

tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Space Defender")

relogio = pygame.time.Clock()

# Fontes
fonte = pygame.font.Font(None, 36)
fonte_grande = pygame.font.Font(None, 80)
fonte_media = pygame.font.Font(None, 42)

# =========================
# CARREGAMENTO DO CENÁRIO
# =========================

background0 = pygame.image.load(
    "assets/images/Level3Bg0.png"
).convert_alpha()

background1 = pygame.image.load(
    "assets/images/Level3Bg1.png"
).convert_alpha()

background2 = pygame.image.load(
    "assets/images/Level3Bg2.png"
).convert_alpha()

background3 = pygame.image.load(
    "assets/images/Level3Bg3.png"
).convert_alpha()

background4 = pygame.image.load(
    "assets/images/Level3Bg4.png"
).convert_alpha()

# Redimensiona as camadas
background0 = pygame.transform.scale(background0, (LARGURA, ALTURA))
background1 = pygame.transform.scale(background1, (LARGURA, ALTURA))
background2 = pygame.transform.scale(background2, (LARGURA, ALTURA))
background3 = pygame.transform.scale(background3, (LARGURA, ALTURA))
background4 = pygame.transform.scale(background4, (LARGURA, ALTURA))

# =========================
# JOGADOR
# =========================

JOGADOR_LARGURA = 60
JOGADOR_ALTURA = 40

jogador_x = 100
jogador_y = ALTURA // 2

velocidade_jogador = 5

vidas = 3

# =========================
# TIROS
# =========================

TIRO_LARGURA = 20
TIRO_ALTURA = 6

velocidade_tiro = 10

tiros = []

# =========================
# INIMIGO
# =========================

imagem_inimigo = pygame.image.load(
    "assets/images/Enemy3.png"
).convert_alpha()

INIMIGO_LARGURA = 100
INIMIGO_ALTURA = 60

imagem_inimigo = pygame.transform.scale(
    imagem_inimigo,
    (INIMIGO_LARGURA, INIMIGO_ALTURA)
)

inimigo_x = 700

inimigo_y = random.randint(
    0,
    ALTURA - INIMIGO_ALTURA
)

velocidade_inimigo = 3

# =========================
# PONTUAÇÃO
# =========================

pontos = 0

# Ao destruir 10 inimigos, o jogador vence
META_VITORIA = 10

# =========================
# ESTADO DO JOGO
# =========================

jogo_terminado = False
vitoria = False

# =========================
# LOOP PRINCIPAL
# =========================

executando = True

while executando:

    # =========================
    # EVENTOS
    # =========================

    for evento in pygame.event.get():

        if evento.type == pygame.QUIT:
            executando = False

        if evento.type == pygame.KEYDOWN:

            # Só permite atirar se o jogo ainda estiver acontecendo
            if evento.key == pygame.K_SPACE and not jogo_terminado:

                novo_tiro = pygame.Rect(
                    jogador_x + JOGADOR_LARGURA,
                    jogador_y + JOGADOR_ALTURA // 2 - TIRO_ALTURA // 2,
                    TIRO_LARGURA,
                    TIRO_ALTURA
                )

                tiros.append(novo_tiro)

    # =========================
    # LÓGICA DO JOGO
    # =========================

    if not jogo_terminado:

        # =========================
        # MOVIMENTAÇÃO DO JOGADOR
        # =========================

        teclas = pygame.key.get_pressed()

        if teclas[pygame.K_w] or teclas[pygame.K_UP]:
            jogador_y -= velocidade_jogador

        if teclas[pygame.K_s] or teclas[pygame.K_DOWN]:
            jogador_y += velocidade_jogador

        if teclas[pygame.K_a] or teclas[pygame.K_LEFT]:
            jogador_x -= velocidade_jogador

        if teclas[pygame.K_d] or teclas[pygame.K_RIGHT]:
            jogador_x += velocidade_jogador

        # =========================
        # LIMITES DO JOGADOR
        # =========================

        if jogador_x < 0:
            jogador_x = 0

        if jogador_x > LARGURA - JOGADOR_LARGURA:
            jogador_x = LARGURA - JOGADOR_LARGURA

        if jogador_y < 0:
            jogador_y = 0

        if jogador_y > ALTURA - JOGADOR_ALTURA:
            jogador_y = ALTURA - JOGADOR_ALTURA

        # Retângulo usado para detectar colisões
        jogador_rect = pygame.Rect(
            jogador_x,
            jogador_y,
            JOGADOR_LARGURA,
            JOGADOR_ALTURA
        )

        # =========================
        # MOVIMENTAÇÃO DOS TIROS
        # =========================

        for tiro in tiros:
            tiro.x += velocidade_tiro

        # Remove tiros que saíram da tela
        tiros = [
            tiro
            for tiro in tiros
            if tiro.x < LARGURA
        ]

        # =========================
        # MOVIMENTAÇÃO DO INIMIGO
        # =========================

        inimigo_x -= velocidade_inimigo

        inimigo_rect = pygame.Rect(
            inimigo_x,
            inimigo_y,
            INIMIGO_LARGURA,
            INIMIGO_ALTURA
        )

        # =========================
        # COLISÃO: TIRO X INIMIGO
        # =========================

        for tiro in tiros[:]:

            if tiro.colliderect(inimigo_rect):

                tiros.remove(tiro)

                pontos += 1

                # Inimigo reaparece à direita
                inimigo_x = LARGURA

                # Em uma altura diferente
                inimigo_y = random.randint(
                    0,
                    ALTURA - INIMIGO_ALTURA
                )

                break

        # =========================
        # ATUALIZA RETÂNGULO INIMIGO
        # =========================

        inimigo_rect = pygame.Rect(
            inimigo_x,
            inimigo_y,
            INIMIGO_LARGURA,
            INIMIGO_ALTURA
        )

        # =========================
        # COLISÃO: JOGADOR X INIMIGO
        # =========================

        if jogador_rect.colliderect(inimigo_rect):

            vidas -= 1

            inimigo_x = LARGURA

            inimigo_y = random.randint(
                0,
                ALTURA - INIMIGO_ALTURA
            )

        # =========================
        # INIMIGO ESCAPOU
        # =========================

        if inimigo_x < -INIMIGO_LARGURA:

            vidas -= 1

            inimigo_x = LARGURA

            inimigo_y = random.randint(
                0,
                ALTURA - INIMIGO_ALTURA
            )

        # =========================
        # CONDIÇÃO DE DERROTA
        # =========================

        if vidas <= 0:

            # Impede que apareçam vidas negativas
            vidas = 0

            jogo_terminado = True
            vitoria = False

        # =========================
        # CONDIÇÃO DE VITÓRIA
        # =========================

        if pontos >= META_VITORIA:

            jogo_terminado = True
            vitoria = True

    # =========================
    # DESENHA O CENÁRIO
    # =========================

    tela.blit(background0, (0, 0))
    tela.blit(background1, (0, 0))
    tela.blit(background2, (0, 0))
    tela.blit(background3, (0, 0))
    tela.blit(background4, (0, 0))

    # =========================
    # DESENHA O JOGADOR
    # =========================

    pygame.draw.rect(
        tela,
        (0, 255, 0),
        (
            jogador_x,
            jogador_y,
            JOGADOR_LARGURA,
            JOGADOR_ALTURA
        )
    )

    # =========================
    # DESENHA OS TIROS
    # =========================

    for tiro in tiros:

        pygame.draw.rect(
            tela,
            (255, 255, 0),
            tiro
        )

    # =========================
    # DESENHA O INIMIGO
    # =========================

    if not jogo_terminado:

        tela.blit(
            imagem_inimigo,
            (inimigo_x, inimigo_y)
        )

    # =========================
    # MOSTRA PONTUAÇÃO
    # =========================

    texto_pontos = fonte.render(
        f"Pontos: {pontos}/{META_VITORIA}",
        True,
        (255, 255, 255)
    )

    tela.blit(
        texto_pontos,
        (20, 20)
    )

    # =========================
    # MOSTRA VIDAS
    # =========================

    texto_vidas = fonte.render(
        f"Vidas: {vidas}",
        True,
        (255, 255, 255)
    )

    tela.blit(
        texto_vidas,
        (LARGURA - 140, 20)
    )

    # =========================
    # TELA FINAL
    # =========================

    if jogo_terminado:

        # Cria uma camada preta transparente
        camada_escura = pygame.Surface(
            (LARGURA, ALTURA),
            pygame.SRCALPHA
        )

        camada_escura.fill(
            (0, 0, 0, 190)
        )

        tela.blit(
            camada_escura,
            (0, 0)
        )

        # -------------------------
        # VITÓRIA
        # -------------------------

        if vitoria:

            mensagem = fonte_grande.render(
                "VOCE VENCEU!",
                True,
                (0, 255, 0)
            )

        # -------------------------
        # DERROTA
        # -------------------------

        else:

            mensagem = fonte_grande.render(
                "GAME OVER",
                True,
                (255, 0, 0)
            )

        mensagem_rect = mensagem.get_rect(
            center=(
                LARGURA // 2,
                ALTURA // 2
            )
        )

        tela.blit(
            mensagem,
            mensagem_rect
        )

        # Mensagem auxiliar
        mensagem_sair = fonte_media.render(
            "Feche a janela para sair",
            True,
            (255, 255, 255)
        )

        mensagem_sair_rect = mensagem_sair.get_rect(
            center=(
                LARGURA // 2,
                ALTURA // 2 + 70
            )
        )

        tela.blit(
            mensagem_sair,
            mensagem_sair_rect
        )

    # =========================
    # ATUALIZA A TELA
    # =========================

    pygame.display.flip()

    relogio.tick(FPS)

# Encerra o Pygame
pygame.quit()