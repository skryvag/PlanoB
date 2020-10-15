import pygame
from constants import SCREEN_NAMES, GAME_CONSTANTS
from utils import Ranking, Screen
from game_utils import MeditatingNinja, Panel, ShurikenController, EnemyNinjaController, CollisionController


class Game(Screen):
    '''
    Define a tela do jogo. Herda os métodos da tela de um pai
    classe. Cada quadro desta tela é gerado pela execução do
    função render_frame uma vez.
    '''

    def __init__(self, name='', is_easy=False):
        '''
        Inicializa os atributos da classe mãe, pára a música do menu
        jogando e tocando música de jogo, instanciam todos os objetos que
        aparecerá na tela do jogo.

        Args:
            name (string): nome do jogador, opcional
            is_easy (bool): dificuldade do jogo, o padrão é difícil (is_easy=False)
        '''
        super().__init__(name)

        pygame.mixer.music.stop()
        pygame.mixer.music.load('music/game_soundtrack.wav')
        pygame.mixer.music.play(-1)

        self.gate_image = GAME_CONSTANTS['GATE_IMAGE']

        self.meditating_ninja = MeditatingNinja()

        self.panel = Panel(is_easy)

        self.shuriken_controller = ShurikenController(self.panel)

        # O tempo de reprodução entre inimigos varia com dificuldade
        spawn_interval = 5000 if is_easy else 1500
        self.enemy_ninja_controller = EnemyNinjaController(spawn_interval)

        self.collision_controller = CollisionController(
            self.meditating_ninja, self.shuriken_controller, self.enemy_ninja_controller, self.panel, self.on_game_over
        )

    def on_game_over(self):
        '''
        Salva a pontuação do usuário para o arquivo de texto de alta pontuação,
        estabelece um redirecionamento para o menu, pára a tela 
        da execução, e mudanças na música do menu
        '''
        ranking = Ranking('high_scores.txt')
        ranking.new_record(self.name, self.panel.score)

        self.set_next_screen(SCREEN_NAMES[0])

        self.stop_running()

        pygame.mixer.music.stop()
        pygame.mixer.music.load('music/music_calm.wav')
        pygame.mixer.music.play(-1)

    def render_frame(self):
        '''Renderiza um quadro do jogo em uma tela de jogos de pygame'''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.stop_running()

            if event.type == pygame.USEREVENT:
                self.enemy_ninja_controller.spawn_enemy_ninjas()

            if event.type == pygame.KEYDOWN:
                self.panel.process_keyboard(event.key)
                self.shuriken_controller.process_keyboard(event.key)

        self.screen.fill([255, 255, 255])

        self.meditating_ninja.render(self.screen)

        self.screen.blit(self.gate_image, [105, 105])

        self.panel.render(self.screen)

        self.shuriken_controller.render(self.screen)

        self.enemy_ninja_controller.render(self.screen)

        self.collision_controller.scan_for_collisions()

        pygame.display.update()


class HardGame(Game):
    '''Define a dificuldade do jogo para dificil. Os inimigos desovam mais rápido, e o jogador ganha mais pontos'''

    def __init__(self, name=''):
        super().__init__(name, is_easy=False)


class EasyGame(Game):
    '''Define a dificuldade do jogo para facil. Os inimigos desovam mais devagar, e o jogador ganha menos pontos".'''

    def __init__(self, name=''):
        super().__init__(name, is_easy=True)
