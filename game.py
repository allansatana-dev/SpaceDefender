import random
import pygame

from settings import (
    LARGURA,
    ALTURA,
    FPS,
    TITULO_JOGO,
    META_VITORIA,
    MENU,
    JOGANDO,
    GAME_OVER,
    VITORIA,
    INTERVALO_TIRO_MIN,
    INTERVALO_TIRO_MAX,
    CAMINHO_BACKGROUND_0,
    CAMINHO_BACKGROUND_1,
    CAMINHO_BACKGROUND_2,
    CAMINHO_BACKGROUND_3,
    CAMINHO_BACKGROUND_4,
    CAMINHO_MUSICA
)

from player import Player
from enemy import Enemy


class Game:

    def __init__(self):

        # =========================
        # INICIALIZAÇÃO DO PYGAME
        # =========================

        pygame.init()

        self.screen = pygame.display.set_mode(
            (LARGURA, ALTURA)
        )

        pygame.display.set_caption(
            TITULO_JOGO
        )

        self.clock = pygame.time.Clock()

        self.running = True

        # =========================
        # FONTES
        # =========================

        self.fonte = pygame.font.Font(
            None,
            36
        )

        self.fonte_grande = pygame.font.Font(
            None,
            80
        )

        self.fonte_media = pygame.font.Font(
            None,
            42
        )

        self.fonte_pequena = pygame.font.Font(
            None,
            30
        )

        # =========================
        # BACKGROUNDS
        # =========================

        self.backgrounds = [
            self.carregar_background(CAMINHO_BACKGROUND_0),
            self.carregar_background(CAMINHO_BACKGROUND_1),
            self.carregar_background(CAMINHO_BACKGROUND_2),
            self.carregar_background(CAMINHO_BACKGROUND_3),
            self.carregar_background(CAMINHO_BACKGROUND_4)
        ]

        # =========================
        # MÚSICA
        # =========================

        pygame.mixer.music.load(
            CAMINHO_MUSICA
        )

        pygame.mixer.music.set_volume(0.4)

        pygame.mixer.music.play(-1)

        # =========================
        # OBJETOS DO JOGO
        # =========================

        self.player = Player()

        self.enemy = Enemy()

        # =========================
        # PROJÉTEIS
        # =========================

        self.player_projectiles = []

        self.enemy_projectiles = []

        # =========================
        # PONTUAÇÃO
        # =========================

        self.pontos = 0

        # =========================
        # ESTADO DO JOGO
        # =========================

        self.estado = MENU

        # =========================
        # CONTROLE DO TIRO INIMIGO
        # =========================

        self.ultimo_tiro_inimigo = pygame.time.get_ticks()

        self.proximo_intervalo_tiro = random.randint(
            INTERVALO_TIRO_MIN,
            INTERVALO_TIRO_MAX
        )

    # =========================
    # CARREGAR BACKGROUND
    # =========================

    def carregar_background(self, caminho):

        imagem = pygame.image.load(
            caminho
        ).convert_alpha()

        return pygame.transform.scale(
            imagem,
            (LARGURA, ALTURA)
        )

    # =========================
    # LOOP PRINCIPAL
    # =========================

    def run(self):

        while self.running:

            self.handle_events()

            self.update()

            self.draw()

            pygame.display.flip()

            self.clock.tick(FPS)

        pygame.quit()

    # =========================
    # EVENTOS
    # =========================

    def handle_events(self):

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:

                # =========================
                # MENU
                # =========================

                if self.estado == MENU:

                    if event.key == pygame.K_RETURN:
                        self.reset_game()
                        self.estado = JOGANDO

                    elif event.key == pygame.K_ESCAPE:
                        self.running = False

                # =========================
                # JOGANDO
                # =========================

                elif self.estado == JOGANDO:

                    if event.key == pygame.K_SPACE:

                        novo_tiro = self.player.shoot()

                        self.player_projectiles.append(
                            novo_tiro
                        )

                    elif event.key == pygame.K_ESCAPE:

                        self.estado = MENU

                # =========================
                # GAME OVER / VITÓRIA
                # =========================

                elif self.estado in (
                    GAME_OVER,
                    VITORIA
                ):

                    if event.key == pygame.K_RETURN:

                        self.reset_game()

                        self.estado = JOGANDO

                    elif event.key == pygame.K_ESCAPE:

                        self.estado = MENU

    # =========================
    # ATUALIZAÇÃO
    # =========================

    def update(self):

        if self.estado != JOGANDO:
            return

        # =========================
        # JOGADOR
        # =========================

        self.player.update()

        # =========================
        # INIMIGO
        # =========================

        self.enemy.update()

        # =========================
        # TIROS DO JOGADOR
        # =========================

        for tiro in self.player_projectiles[:]:

            tiro.update()

            if tiro.saiu_da_tela(LARGURA):

                self.player_projectiles.remove(
                    tiro
                )

        # =========================
        # TIROS DO INIMIGO
        # =========================

        for tiro in self.enemy_projectiles[:]:

            tiro.update()

            if tiro.saiu_da_tela():

                self.enemy_projectiles.remove(
                    tiro
                )

        # =========================
        # INIMIGO ATIRA
        # =========================

        self.enemy_shoot()

        # =========================
        # COLISÕES
        # =========================

        self.check_collisions()

        # =========================
        # INIMIGO SAIU DA TELA
        # =========================

        if self.enemy.saiu_da_tela():

            self.player.perder_vida()

            self.enemy.respawn()

        # =========================
        # GAME OVER
        # =========================

        if not self.player.esta_vivo():

            self.estado = GAME_OVER

        # =========================
        # VITÓRIA
        # =========================

        elif self.pontos >= META_VITORIA:

            self.estado = VITORIA

    # =========================
    # TIRO DO INIMIGO
    # =========================

    def enemy_shoot(self):

        tempo_atual = pygame.time.get_ticks()

        tempo_decorrido = (
            tempo_atual
            - self.ultimo_tiro_inimigo
        )

        if tempo_decorrido >= self.proximo_intervalo_tiro:

            novo_tiro = self.enemy.shoot()

            self.enemy_projectiles.append(
                novo_tiro
            )

            self.ultimo_tiro_inimigo = tempo_atual

            self.proximo_intervalo_tiro = random.randint(
                INTERVALO_TIRO_MIN,
                INTERVALO_TIRO_MAX
            )

    # =========================
    # COLISÕES
    # =========================

    def check_collisions(self):

        # =========================
        # TIRO DO JOGADOR X INIMIGO
        # =========================

        for tiro in self.player_projectiles[:]:

            if tiro.rect.colliderect(
                self.enemy.rect
            ):

                if tiro in self.player_projectiles:

                    self.player_projectiles.remove(
                        tiro
                    )

                self.pontos += 1

                self.enemy.respawn()

                break

        # =========================
        # TIRO INIMIGO X JOGADOR
        # =========================

        for tiro in self.enemy_projectiles[:]:

            if tiro.rect.colliderect(
                self.player.rect
            ):

                if tiro in self.enemy_projectiles:

                    self.enemy_projectiles.remove(
                        tiro
                    )

                self.player.perder_vida()

                break

        # =========================
        # INIMIGO X JOGADOR
        # =========================

        if self.enemy.rect.colliderect(
            self.player.rect
        ):

            self.player.perder_vida()

            self.enemy.respawn()

    # =========================
    # DESENHAR
    # =========================

    def draw(self):

        self.draw_background()

        if self.estado == MENU:

            self.draw_menu()

        elif self.estado == JOGANDO:

            self.draw_game()

        elif self.estado == GAME_OVER:

            self.draw_game()

            self.draw_game_over()

        elif self.estado == VITORIA:

            self.draw_game()

            self.draw_victory()

    # =========================
    # BACKGROUND
    # =========================

    def draw_background(self):

        for background in self.backgrounds:

            self.screen.blit(
                background,
                (0, 0)
            )

    # =========================
    # JOGO
    # =========================

    def draw_game(self):

        # Jogador
        self.player.draw(
            self.screen
        )

        # Inimigo
        self.enemy.draw(
            self.screen
        )

        # Tiros do jogador
        for tiro in self.player_projectiles:

            tiro.draw(
                self.screen
            )

        # Tiros do inimigo
        for tiro in self.enemy_projectiles:

            tiro.draw(
                self.screen
            )

        # HUD
        self.draw_hud()

    # =========================
    # HUD
    # =========================

    def draw_hud(self):

        texto_pontos = self.fonte.render(
            f"Pontos: {self.pontos}/{META_VITORIA}",
            True,
            (255, 255, 255)
        )

        texto_vidas = self.fonte.render(
            f"Vidas: {self.player.vidas}",
            True,
            (255, 255, 255)
        )

        self.screen.blit(
            texto_pontos,
            (20, 20)
        )

        self.screen.blit(
            texto_vidas,
            (
                LARGURA
                - texto_vidas.get_width()
                - 20,
                20
            )
        )

    # =========================
    # MENU
    # =========================

    def draw_menu(self):

        overlay = pygame.Surface(
            (LARGURA, ALTURA),
            pygame.SRCALPHA
        )

        overlay.fill(
            (0, 0, 0, 150)
        )

        self.screen.blit(
            overlay,
            (0, 0)
        )

        titulo = self.fonte_grande.render(
            "SPACE DEFENDER",
            True,
            (255, 255, 255)
        )

        objetivo = self.fonte_media.render(
            "Destrua 10 inimigos para vencer!",
            True,
            (255, 255, 255)
        )

        controles = [
            "CONTROLES",
            "W / SETA CIMA - Mover para cima",
            "S / SETA BAIXO - Mover para baixo",
            "A / SETA ESQUERDA - Mover para esquerda",
            "D / SETA DIREITA - Mover para direita",
            "ESPACO - Atirar",
            "ENTER - INICIAR",
            "ESC - SAIR"
        ]

        self.centralizar_texto(
            titulo,
            60
        )

        self.centralizar_texto(
            objetivo,
            140
        )

        y = 220

        for texto in controles:

            superficie = self.fonte_pequena.render(
                texto,
                True,
                (255, 255, 255)
            )

            self.centralizar_texto(
                superficie,
                y
            )

            y += 35

    # =========================
    # GAME OVER
    # =========================

    def draw_game_over(self):

        overlay = pygame.Surface(
            (LARGURA, ALTURA),
            pygame.SRCALPHA
        )

        overlay.fill(
            (0, 0, 0, 180)
        )

        self.screen.blit(
            overlay,
            (0, 0)
        )

        titulo = self.fonte_grande.render(
            "GAME OVER",
            True,
            (255, 255, 255)
        )

        reiniciar = self.fonte_media.render(
            "ENTER - Jogar novamente",
            True,
            (255, 255, 255)
        )

        menu = self.fonte_media.render(
            "ESC - Voltar ao menu",
            True,
            (255, 255, 255)
        )

        self.centralizar_texto(
            titulo,
            170
        )

        self.centralizar_texto(
            reiniciar,
            280
        )

        self.centralizar_texto(
            menu,
            330
        )

    # =========================
    # VITÓRIA
    # =========================

    def draw_victory(self):

        overlay = pygame.Surface(
            (LARGURA, ALTURA),
            pygame.SRCALPHA
        )

        overlay.fill(
            (0, 0, 0, 180)
        )

        self.screen.blit(
            overlay,
            (0, 0)
        )

        titulo = self.fonte_grande.render(
            "VOCÊ VENCEU!",
            True,
            (255, 255, 255)
        )

        reiniciar = self.fonte_media.render(
            "ENTER - Jogar novamente",
            True,
            (255, 255, 255)
        )

        menu = self.fonte_media.render(
            "ESC - Voltar ao menu",
            True,
            (255, 255, 255)
        )

        self.centralizar_texto(
            titulo,
            170
        )

        self.centralizar_texto(
            reiniciar,
            280
        )

        self.centralizar_texto(
            menu,
            330
        )

    # =========================
    # CENTRALIZAR TEXTO
    # =========================

    def centralizar_texto(
        self,
        superficie,
        y
    ):

        x = (
            LARGURA
            - superficie.get_width()
        ) // 2

        self.screen.blit(
            superficie,
            (x, y)
        )

    # =========================
    # REINICIAR JOGO
    # =========================

    def reset_game(self):

        self.player.reset()

        self.enemy.reset()

        self.player_projectiles.clear()

        self.enemy_projectiles.clear()

        self.pontos = 0

        self.ultimo_tiro_inimigo = pygame.time.get_ticks()

        self.proximo_intervalo_tiro = random.randint(
            INTERVALO_TIRO_MIN,
            INTERVALO_TIRO_MAX
        )