import pygame
from constants import SCREEN_NAMES, RULES_CONSTANTS
from utils import Screen


class Rules(Screen):
    '''
    Define a tela de regras. Herda os métodos de tela de um pai
    classe. Cada quadro desta tela é gerado pela execução do
    função render_frame uma vez.
    '''

    def __init__(self, name=''):
        '''
        Chama a construtora da classe mãe para herdar
        atributos de classe de tela.

        Args:
            name (string): nome do jogador, opcional
        '''
        super().__init__(name)

    def render_frame(self):
        '''Apresenta um quadro da tela de regras em uma tela de jogos de pygame'''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.stop_running()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    self.set_next_screen(SCREEN_NAMES[0])
                    self.stop_running()

        self.screen.fill([255, 184, 122])

        self.screen.blit(RULES_CONSTANTS['TITLE'], [10, 10])

        self.screen.blit(RULES_CONSTANTS['SUBTITLE'], [10, 50])

        self.screen.blit(RULES_CONSTANTS['RULE_1'], [10, 85])
        self.screen.blit(RULES_CONSTANTS['RULE_2'], [10, 110])
        self.screen.blit(RULES_CONSTANTS['RULE_3'], [10, 135])
        self.screen.blit(RULES_CONSTANTS['RULE_4'], [10, 160])
        self.screen.blit(RULES_CONSTANTS['RULE_5'], [10, 185])
        self.screen.blit(RULES_CONSTANTS['RULE_6'], [10, 210])
        self.screen.blit(RULES_CONSTANTS['RULE_7'], [10, 235])
        self.screen.blit(RULES_CONSTANTS['RULE_8'], [10, 260])
        self.screen.blit(RULES_CONSTANTS['RULE_9'], [10, 285])
        self.screen.blit(RULES_CONSTANTS['RULE_10'], [10, 310])
        self.screen.blit(RULES_CONSTANTS['RULE_11'], [10, 335])

        self.screen.blit(RULES_CONSTANTS['BACK'], [180, 370])

        pygame.display.update()
