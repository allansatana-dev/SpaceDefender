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

# =========================
# FONTES
# =========================

fonte = pygame.font.Font(None, 36)
fonte_grande = pygame.font.Font(None, 80)
fonte_media = pygame.font.Font(None, 42)
fonte_pequena = pygame.font.Font(None, 30)

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

background0 = pygame.transform.scale(background0, (LARGURA, ALTURA))
background1 = pygame.transform.scale(background1, (LARGURA, ALTURA))
background2 = pygame.transform.scale(background2, (LARGURA, ALTURA))
background3 = pygame.transform.scale(background3, (LARGURA, ALTURA))
background4 = pygame.transform.scale(background4, (LARGURA, ALTURA))

# =========================
# JOGADOR
# =========================

# Carrega a imagem da nave
imagem_jogador = pygame.image.load(
    "assets/images/playerShip1_red.png"
).convert_alpha()

# Rotaciona a nave 90 graus para a direita
imagem_jogador = pygame.transform.rotate(
    imagem_jogador,
    -90
)

# Tamanho da nave no jogo
JOGADOR_LARGURA = 75
JOGADOR_ALTURA = 55

# Redimensiona a nave
imagem_jogador = pygame.transform.scale(
    imagem_jogador,
    (JOGADOR_LARGURA, JOGADOR_ALTURA)
)

velocidade_jogador = 5

jogador_x = 100
jogador_y = ALTURA // 2

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

velocidade_inimigo = 3

inimigo_x = 700

inimigo_y = random.randint(
    0,
    ALTURA - INIMIGO_ALTURA
)

# =========================
# PONTUAÇÃO
# =========================

pontos = 0

META_VITORIA = 10

# =========================
# ESTADOS DO JOGO
# =========================

MENU = "menu"
JOGANDO = "jogando"
GAME_OVER = "game_over"
VITORIA = "vitoria"

estado_jogo = MENU

# =========================
# FUNÇÃO PARA REINICIAR
# =========================

def reiniciar_jogo():

    global jogador_x
    global jogador_y
    global vidas
    global pontos
    global tiros
    global inimigo_x
    global inimigo_y

    jogador_x = 100
    jogador_y = ALTURA // 2

    vidas = 3
    pontos = 0

    tiros = []

    inimigo_x = 700

    inimigo_y = random.randint(
        0,
        ALTURA - INIMIGO_ALTURA
    )

# =========================
# FUNÇÃO PARA DESENHAR CENÁRIO
# =========================

def desenhar_cenario():

    tela.blit(background0, (0, 0))
    tela.blit(background1, (0, 0))
    tela.blit(background2, (0, 0))
    tela.blit(background3, (0, 0))
    tela.blit(background4, (0, 0))

# =========================
# FUNÇÃO PARA CENTRALIZAR TEXTO
# =========================

def desenhar_texto_centralizado(texto, fonte_usada, cor, y):

    superficie = fonte_usada.render(
        texto,
        True,
        cor
    )

    retangulo = superficie.get_rect(
        center=(LARGURA // 2, y)
    )

    tela.blit(
        superficie,
        retangulo
    )

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

            # =========================
            # EVENTOS DO MENU
            # =========================

            if estado_jogo == MENU:

                if evento.key == pygame.K_RETURN:

                    reiniciar_jogo()
                    estado_jogo = JOGANDO

                elif evento.key == pygame.K_ESCAPE:

                    executando = False

            # =========================
            # EVENTOS DURANTE O JOGO
            # =========================

            elif estado_jogo == JOGANDO:

                if evento.key == pygame.K_SPACE:

                    # O tiro nasce na ponta da nave
                    novo_tiro = pygame.Rect(
                        jogador_x + JOGADOR_LARGURA,
                        jogador_y + JOGADOR_ALTURA // 2 - TIRO_ALTURA // 2,
                        TIRO_LARGURA,
                        TIRO_ALTURA
                    )

                    tiros.append(novo_tiro)

                elif evento.key == pygame.K_ESCAPE:

                    estado_jogo = MENU

            # =========================
            # EVENTOS DA TELA FINAL
            # =========================

            elif estado_jogo == GAME_OVER or estado_jogo == VITORIA:

                if evento.key == pygame.K_RETURN:

                    reiniciar_jogo()
                    estado_jogo = JOGANDO

                elif evento.key == pygame.K_ESCAPE:

                    estado_jogo = MENU

    # =========================
    # LÓGICA DA PARTIDA
    # =========================

    if estado_jogo == JOGANDO:

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

        # Retângulo usado para colisão
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

                inimigo_x = LARGURA

                inimigo_y = random.randint(
                    0,
                    ALTURA - INIMIGO_ALTURA
                )

                break

        # Atualiza o retângulo do inimigo
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
        # DERROTA
        # =========================

        if vidas <= 0:

            vidas = 0
            estado_jogo = GAME_OVER

        # =========================
        # VITÓRIA
        # =========================

        if pontos >= META_VITORIA:

            estado_jogo = VITORIA

    # =========================
    # DESENHA CENÁRIO
    # =========================

    desenhar_cenario()

    # =========================
    # TELA DO MENU
    # =========================

    if estado_jogo == MENU:

        camada_escura = pygame.Surface(
            (LARGURA, ALTURA),
            pygame.SRCALPHA
        )

        camada_escura.fill(
            (0, 0, 0, 150)
        )

        tela.blit(
            camada_escura,
            (0, 0)
        )

        desenhar_texto_centralizado(
            "SPACE DEFENDER",
            fonte_grande,
            (255, 255, 255),
            75
        )

        desenhar_texto_centralizado(
            "Destrua 10 inimigos para vencer!",
            fonte,
            (255, 255, 0),
            135
        )

        desenhar_texto_centralizado(
            "CONTROLES",
            fonte_media,
            (0, 255, 255),
            195
        )

        desenhar_texto_centralizado(
            "W / SETA CIMA  -  Mover para cima",
            fonte_pequena,
            (255, 255, 255),
            240
        )

        desenhar_texto_centralizado(
            "S / SETA BAIXO  -  Mover para baixo",
            fonte_pequena,
            (255, 255, 255),
            275
        )

        desenhar_texto_centralizado(
            "A / SETA ESQUERDA  -  Mover para esquerda",
            fonte_pequena,
            (255, 255, 255),
            310
        )

        desenhar_texto_centralizado(
            "D / SETA DIREITA  -  Mover para direita",
            fonte_pequena,
            (255, 255, 255),
            345
        )

        desenhar_texto_centralizado(
            "ESPACO  -  Atirar",
            fonte_pequena,
            (255, 255, 255),
            380
        )

        desenhar_texto_centralizado(
            "ENTER - INICIAR",
            fonte_media,
            (0, 255, 0),
            445
        )

        desenhar_texto_centralizado(
            "ESC - SAIR",
            fonte_pequena,
            (255, 255, 255),
            490
        )

    # =========================
    # TELA DO JOGO
    # =========================

    elif estado_jogo == JOGANDO:

        # =========================
        # DESENHA A NAVE DO JOGADOR
        # =========================

        tela.blit(
            imagem_jogador,
            (jogador_x, jogador_y)
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

        tela.blit(
            imagem_inimigo,
            (inimigo_x, inimigo_y)
        )

        # =========================
        # PONTUAÇÃO
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
        # VIDAS
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
    # GAME OVER
    # =========================

    elif estado_jogo == GAME_OVER:

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

        desenhar_texto_centralizado(
            "GAME OVER",
            fonte_grande,
            (255, 0, 0),
            220
        )

        desenhar_texto_centralizado(
            f"Pontuacao: {pontos}/{META_VITORIA}",
            fonte_media,
            (255, 255, 255),
            290
        )

        desenhar_texto_centralizado(
            "ENTER - Jogar novamente",
            fonte,
            (0, 255, 0),
            360
        )

        desenhar_texto_centralizado(
            "ESC - Voltar ao menu",
            fonte_pequena,
            (255, 255, 255),
            410
        )

    # =========================
    # VITÓRIA
    # =========================

    elif estado_jogo == VITORIA:

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

        desenhar_texto_centralizado(
            "VOCE VENCEU!",
            fonte_grande,
            (0, 255, 0),
            220
        )

        desenhar_texto_centralizado(
            f"Voce destruiu {pontos} inimigos!",
            fonte_media,
            (255, 255, 255),
            290
        )

        desenhar_texto_centralizado(
            "ENTER - Jogar novamente",
            fonte,
            (0, 255, 0),
            360
        )

        desenhar_texto_centralizado(
            "ESC - Voltar ao menu",
            fonte_pequena,
            (255, 255, 255),
            410
        )

    # =========================
    # ATUALIZA A TELA
    # =========================

    pygame.display.flip()

    relogio.tick(FPS)

# Encerra o Pygame
pygame.quit()