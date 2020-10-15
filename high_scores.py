import pygame
from constants import MEDIUM_FONT, SCREEN_NAMES, HIGH_SCORES_CONSTANTS
from utils import render_font, Ranking, Screen


class HighScores(Screen):
    '''
    Define a tela de alta pontuação. Herda os métodos de tela de um pai
    classe. Cada quadro desta tela é gerado pela execução da função
    render_frame uma vez.
    '''

    def __init__(self, name=''):
        '''
        Inicializa os atributos da classe mãe, cria um Ranking
        objeto para lidar com o arquivo de texto de alta pontuação, e cria
        duas listas paralelas para armazenar as altas pontuações atuais.

        Args:
            name (string): nome do jogador, opcional
        '''
        super().__init__(name)

        self.ranking = Ranking('high_scores.txt')

        self.names = []
        self.scores = []

        score = self.ranking.get_players()

        for name in self.ranking.get_leaderboard()[:10]:
            self.names.append(
                render_font(name, font=MEDIUM_FONT, color=[0, 0, 255])
            )

            self.scores.append(
                render_font(str(score[name]),
                            font=MEDIUM_FONT, color=[0, 0, 255])
            )

    def render_frame(self):
        '''Apresenta um quadro da tela de alta pontuação em uma tela de jogos pygame'''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.stop_running()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    self.set_next_screen(SCREEN_NAMES[0])
                    self.stop_running()

        self.screen.fill([255, 184, 122])

        self.screen.blit(HIGH_SCORES_CONSTANTS['TITLE'], [10, 10])

        self.screen.blit(HIGH_SCORES_CONSTANTS['SUBTITLE'], [10, 50])

        for i in range(10):  # Apresenta cada pontuação alta com uma margem de 25px
            self.screen.blit(self.names[i], [180, 25 * i + 90])
            self.screen.blit(self.scores[i], [360, 25 * i + 90])

        self.screen.blit(HIGH_SCORES_CONSTANTS['BACK'], [180, 360])

        pygame.display.update()
