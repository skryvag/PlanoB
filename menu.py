import pygame
from utils import render_font, Screen
from constants import MEDIUM_FONT, SCREEN_NAMES, MENU_CONSTANTS
from string import ascii_lowercase


class Button():
    '''
    Define um botão que pode estar ativo ou inativo.
    As imagens variam dependendo do estado em que o botão está.
    '''

    def __init__(self, text, position):
        '''
        Inicializa o texto do botão, posição, caixa (que irá
        ser o pano de fundo do botão), e qual o estado do botão
        está em (não ativo no início)

        Args:
            text (string): texto que aparece no botão
            position (list): posição do botão na tela
        '''
        self.text = render_font(text, font=MEDIUM_FONT)
        self.position = position

        # retângulo de pygame que aparece como fundo do botão
        self.box = pygame.Surface([200, 40])
        self.box.fill([255, 255, 255])

        self.active = False

    def toggle_active(self):
        '''Inverte o atributo ativo (bool) e atribui a cor correta'''
        self.active = not self.active

        if self.active:
            self.box.fill([150, 150, 150])
        else:
            self.box.fill([255, 255, 255])

    def render(self, display):
        '''Exibe texto e fundo de botões com uma margem de 5px entre eles'''
        display.blit(self.box, (self.position[0] - 5, self.position[1] - 5))
        display.blit(self.text, self.position)


class Menu(Screen):
    '''
    Define a tela do menu principal. Herda os métodos de tela de um
    classe mãe. Cada quadro desta tela é gerado pela execução 
    a função render_frame uma vez. Todos os outros métodos lidam com a entrada 
    processamento, exceto o construtor.
    '''

    def __init__(self, name=''):
        '''
        Salva o atributo de imagem ninja, adiciona todos os botões a uma lista 
        e inicializa o primeiro botão como ativo.

        Args:
            name (string): nome do jogador, opcional.
        '''
        super().__init__(name)

        self.ninja_image = MENU_CONSTANTS['NINJA_IMAGE'].convert_alpha()

        self.buttons = []
        self.buttons.append(Button(text='PLAY [EASY]', position=[10, 180]))
        self.buttons.append(Button(text='PLAY [HARD]', position=[10, 240]))
        self.buttons.append(Button(text='REGRAS', position=[10, 300]))
        self.buttons.append(Button(text='HIGH SCORES', position=[10, 360]))

        self.active_button = 0
        self.buttons[self.active_button].toggle_active()

    def process_arrow_pressed(self, key):
        '''
        Quando o usuário pressiona a seta para cima ou para baixo, o botão ativo muda.
        A função desativa o botão antigo, e ativa o novo.
        '''
        if key == pygame.K_UP and self.active_button > 0:
            self.buttons[self.active_button].toggle_active()
            self.active_button -= 1  # Mudanças ativas para o botão abaixo
            self.buttons[self.active_button].toggle_active()

        if key == pygame.K_DOWN and self.active_button < len(self.buttons) - 1:
            self.buttons[self.active_button].toggle_active()
            self.active_button += 1  # Mudanças ativas para o botão acima
            self.buttons[self.active_button].toggle_active()

    def process_navigation_action(self, key):
        '''
        Quando o usuário pressiona para voltar, é definido um redirecionamento que 
        será usado pelo código principal para mudar as telas, e
        o menu deixa de funcionar.
        '''
        if key == pygame.K_RETURN:
            next_screen = SCREEN_NAMES[self.active_button + 1]

            if len(self.name) < 1 and next_screen in ['hard_game', 'easy_game']:
                return

            self.set_next_screen(next_screen)
            self.stop_running()

    def process_typing_name(self, key):
        '''Muda o atributo do nome quando uma letra ou a tecla de backspace é pressionada.'''
        if key == pygame.K_BACKSPACE:
            self.name = self.name[:-1]

        if len(self.name) > 10:
            return

        key_name = pygame.key.name(key)

        if key_name in ascii_lowercase:
            self.name += key_name.upper()

    def render_frame(self):
        '''Apresenta um quadro do menu em uma tela de jogos de pygame'''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.stop_running()

            if event.type == pygame.KEYDOWN:
                self.process_arrow_pressed(event.key)
                self.process_typing_name(event.key)
                self.process_navigation_action(event.key)

        self.screen.fill([255, 184, 122])

        self.screen.blit(MENU_CONSTANTS['TITLE'], [10, 10])
        self.screen.blit(MENU_CONSTANTS['NAME'], [10, 80])
        self.screen.blit(MENU_CONSTANTS['NAME_BOX'], [220, 70])

        self.screen.blit(MEDIUM_FONT.render(
            self.name, True, [0, 0, 0]), [225, 80])

        self.screen.blit(MENU_CONSTANTS['WARNING'], [210, 115])
        self.screen.blit(self.ninja_image, [290, 202])

        for button in self.buttons:
            button.render(self.screen)

        pygame.display.update()
