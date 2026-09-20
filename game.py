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

        self.fonte = pygame.font.Font(None, 36)
        self.fonte_grande = pygame.font.Font(None, 80)
        self.fonte_media = pygame.font.Font(None, 42)
        self.fonte_pequena = pygame.font.Font(None, 30)

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

            self.draw_game_over()

        elif self.estado == VITORIA:

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

        # Tiros do jogador
        for tiro in self.player_projectiles:

            tiro.draw(
                self.screen
            )

        # Inimigo
        self.enemy.draw(
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
            (LARGURA - 140, 20)
        )

    # =========================
    # MENU
    # =========================

    def draw_menu(self):

        camada_escura = pygame.Surface(
            (LARGURA, ALTURA),
            pygame.SRCALPHA
        )

        camada_escura.fill(
            (0, 0, 0, 150)
        )

        self.screen.blit(
            camada_escura,
            (0, 0)
        )

        self.desenhar_texto_centralizado(
            "SPACE DEFENDER",
            self.fonte_grande,
            (255, 255, 255),
            75
        )

        self.desenhar_texto_centralizado(
            "Destrua 10 inimigos para vencer!",
            self.fonte,
            (255, 255, 0),
            135
        )

        self.desenhar_texto_centralizado(
            "CONTROLES",
            self.fonte_media,
            (0, 255, 255),
            195
        )

        self.desenhar_texto_centralizado(
            "W / SETA CIMA  -  Mover para cima",
            self.fonte_pequena,
            (255, 255, 255),
            240
        )

        self.desenhar_texto_centralizado(
            "S / SETA BAIXO  -  Mover para baixo",
            self.fonte_pequena,
            (255, 255, 255),
            275
        )

        self.desenhar_texto_centralizado(
            "A / SETA ESQUERDA  -  Mover para esquerda",
            self.fonte_pequena,
            (255, 255, 255),
            310
        )

        self.desenhar_texto_centralizado(
            "D / SETA DIREITA  -  Mover para direita",
            self.fonte_pequena,
            (255, 255, 255),
            345
        )

        self.desenhar_texto_centralizado(
            "ESPACO  -  Atirar",
            self.fonte_pequena,
            (255, 255, 255),
            380
        )

        self.desenhar_texto_centralizado(
            "ENTER - INICIAR",
            self.fonte_media,
            (0, 255, 0),
            445
        )

        self.desenhar_texto_centralizado(
            "ESC - SAIR",
            self.fonte_pequena,
            (255, 255, 255),
            490
        )

    # =========================
    # GAME OVER
    # =========================

    def draw_game_over(self):

        camada_escura = pygame.Surface(
            (LARGURA, ALTURA),
            pygame.SRCALPHA
        )

        camada_escura.fill(
            (0, 0, 0, 190)
        )

        self.screen.blit(
            camada_escura,
            (0, 0)
        )

        self.desenhar_texto_centralizado(
            "GAME OVER",
            self.fonte_grande,
            (255, 0, 0),
            220
        )

        self.desenhar_texto_centralizado(
            f"Pontuacao: {self.pontos}/{META_VITORIA}",
            self.fonte_media,
            (255, 255, 255),
            290
        )

        self.desenhar_texto_centralizado(
            "ENTER - Jogar novamente",
            self.fonte,
            (0, 255, 0),
            360
        )

        self.desenhar_texto_centralizado(
            "ESC - Voltar ao menu",
            self.fonte_pequena,
            (255, 255, 255),
            410
        )

    # =========================
    # VITÓRIA
    # =========================

    def draw_victory(self):

        camada_escura = pygame.Surface(
            (LARGURA, ALTURA),
            pygame.SRCALPHA
        )

        camada_escura.fill(
            (0, 0, 0, 190)
        )

        self.screen.blit(
            camada_escura,
            (0, 0)
        )

        self.desenhar_texto_centralizado(
            "VOCE VENCEU!",
            self.fonte_grande,
            (0, 255, 0),
            220
        )

        self.desenhar_texto_centralizado(
            f"Voce destruiu {self.pontos} inimigos!",
            self.fonte_media,
            (255, 255, 255),
            290
        )

        self.desenhar_texto_centralizado(
            "ENTER - Jogar novamente",
            self.fonte,
            (0, 255, 0),
            360
        )

        self.desenhar_texto_centralizado(
            "ESC - Voltar ao menu",
            self.fonte_pequena,
            (255, 255, 255),
            410
        )

    # =========================
    # CENTRALIZAR TEXTO
    # =========================

    def desenhar_texto_centralizado(
        self,
        texto,
        fonte_usada,
        cor,
        y
    ):

        superficie = fonte_usada.render(
            texto,
            True,
            cor
        )

        retangulo = superficie.get_rect(
            center=(LARGURA // 2, y)
        )

        self.screen.blit(
            superficie,
            retangulo
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