import pygame
from constants import SCREEN_NAMES
from menu import Menu
from game import HardGame, EasyGame
from rules import Rules
from high_scores import HighScores

pygame.init()

screens = dict(
    zip(SCREEN_NAMES, [Menu, EasyGame, HardGame, Rules, HighScores])
)

clock = pygame.time.Clock()


def open_window(screen, name=None):
    '''
    A função abre a tela indicada nos parâmetros e inicializa
    a tela com um nome salvo, se houver algum. Quando a tela é 
    fechado, uma nova tela é aberta se houver uma próxima_tela configurada.

    Args: 
        screen (string): nome da tela a ser aberta.
        name (string): nome do jogador, opcional.

    '''
    active_screen = screens[screen](name) if name else screens[screen]()

    while active_screen.run:
        clock.tick(60)
        active_screen.render_frame()

    try:
        open_window(active_screen.next_screen, name=active_screen.name)
    except KeyError:
        pygame.quit()


if __name__ == '__main__':
    # Carrega e toca música do menu principal
    pygame.mixer.music.load('music/music_calm.wav')
    pygame.mixer.music.play(-1)

    open_window(SCREEN_NAMES[0])  # Abre a tela zero (menu)
