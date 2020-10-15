import pygame
import math
import random
import time
from constants import INTERMEDIATE_FONT, GAME_CONSTANTS
from utils import render_font


class Question:
    '''
    Define um objeto de pergunta matemática. A pergunta é aleatória e pode ser atualizada no mesmo objeto.
    '''

    def __init__(self, is_easy):
        '''
        Inicializa dois números de forma aleatória, pega uma operação,
        armazena o resultado, e armazena a cadeia de símbolos da operação.

        Args:
            is_easy (bool): se a dificuldade do jogo é fácil ou não
        '''

        self.is_easy = is_easy

        if self.is_easy:  # Se o jogo for fácil, somente as tabelas de horários são permitidas
            self.A = random.randint(0, 9)
            self.B = random.randint(1, 9)

            self.__operation = lambda a, b: (a * b, 'x')

        else:  # O jogo dificil deve ter todas as operações e números maiores
            self.A = random.randint(0, 12)
            self.B = random.randint(1, 12)

            # Seleciona aleatoriamente uma função que retornará a resposta e o símbolo de operação
            self.__operation = random.choice([
                lambda a, b: (a + b, '+'),
                lambda a, b: (a - b, '-'),
                lambda a, b: (a * b, 'x'),
                lambda a, b: (a / b, '/')
            ])

        self.answer, self.operation_symbol = self.__operation(self.A, self.B)

        self.prevent_non_exact_division()

    def prevent_non_exact_division(self):
        '''Continua escolhendo novos números se uma divisão não for exata e atualiza atributos'''
        if self.operation_symbol != '/':
            return

        while (self.A % self.B != 0):
            self.A = random.randint(0, 12)
            self.B = random.randint(1, 12)

        self.answer, _ = self.__operation(self.A, self.B)

    def new_question(self):
        '''Realiza o construtor para obter uma nova pergunta aleatória'''
        self.__init__(is_easy=self.is_easy)

    def try_answer(self, answer):
        '''
        Verifica se uma resposta está correta ou não

        Args:
            answer (int): resposta à pergunta matemática

        Retorna: booleano representando se a resposta está correta ou não
        '''
        return int(answer) == self.answer

    def get_string(self):
        '''Returns: representação em cadeia da questão matemática'''
        return f'{self.A} {self.operation_symbol} {self.B} ='


class MeditatingNinja:
    '''Define o ninja meditador que aparecerá no jogo'''

    def __init__(self):
        '''Inicializa a imagem, tamanho e posições do ninja na tela'''
        self.shape = GAME_CONSTANTS['NINJA_IMAGE']

        self.size = GAME_CONSTANTS['NINJA_SIZE']

        self.position = GAME_CONSTANTS['NINJA_POSITION']

    def render(self, display):
        '''Proporciona a ninja meditadora em uma determinada tela de pygame'''
        display.blit(self.shape, self.position)


class Shuriken:
    '''Define um shuriken que aparecerá no jogo'''

    def __init__(self, direction):
        '''
        Inicializa a direção, a imagem, o tamanho, a velocidade e a posição da embarcação, dependendo da direção

        Args:
            direção (string): direção para a qual o shuriken se moverá, deve ser: "DIREITA" ou "ESQUERDA".
        '''
        self.direction = direction

        self.shape = GAME_CONSTANTS['SHURIKEN_IMAGE']

        self.size = GAME_CONSTANTS['SHURIKEN_SIZE']

        self.speed = GAME_CONSTANTS['SHURIKEN_SPEED']

        init_position = GAME_CONSTANTS['SHURIKEN_POSITION']
        self.position = init_position[0] if direction == 'RIGHT' else init_position[1]

    def render(self, display):
        '''Apresenta o shuriken em uma determinada tela de jogos pygame'''
        display.blit(self.shape, self.position)

    def update_position(self):
        '''
        Em cada quadro, o shuriken moverá sua velocidade em pixels para sua direção.
        Acrescentar à coordenada x significa ir para a direita da tela.
        Subtrair da coordenada x significa ir para a esquerda da tela.
        '''
        if self.direction == 'RIGHT':
            self.position = self.position[0] + self.speed, self.position[1]

        if self.direction == 'LEFT':
            self.position = self.position[0] - self.speed, self.position[1]


class EnemyNinja:
    '''Define um ninja inimigo que aparecerá no jogo'''

    def __init__(self, side):
        '''
        Inicializa o lado do ninja (de onde ele vem na tela), forma
        (imagens que variam dependendo do lado), tamanho, velocidade, posição (varia
        dependendo do lado).

        Args:
            lado (string): lado de onde os ninjas inimigos vêm, deve ser: "DIREITO" ou "ESQUERDA": lado de onde vêm os ninjas inimigos.
        '''
        self.side = side

        if side == 'RIGHT':
            self.shape = GAME_CONSTANTS['ENEMY_NINJA_IMAGE'][0].convert_alpha()
        else:
            self.shape = GAME_CONSTANTS['ENEMY_NINJA_IMAGE'][1].convert_alpha()

        self.size = GAME_CONSTANTS['ENEMY_NINJA_SIZE']

        self.speed = GAME_CONSTANTS['ENEMY_NINJA_SPEED']

        init_position = GAME_CONSTANTS['ENEMY_NINJA_POSITION']
        self.position = init_position[0] if side == 'RIGHT' else init_position[1]

    def render(self, display):
        '''Fornece um ninjas inimigo em uma determinada exibição de pygame'''
        display.blit(self.shape, self.position)

    def update_position(self):
        '''
        Em cada quadro, o ninja inimigo moverá sua velocidade em pixels em direção 
        o centro da tela.
        Adicionar à coordenada x significa ir para a direção correta.
        Subtrair da coordenada x significa ir para a direção esquerda.
        '''
        if self.side == 'RIGHT':
            self.position = self.position[0] - self.speed, self.position[1]

        if self.side == 'LEFT':
            self.position = self.position[0] + self.speed, self.position[1]


class Panel:
    '''
    Define o painel mostrado na parte superior da tela do jogo.
    Ele trata principalmente da exibição de informações para o usuário.
    '''

    def __init__(self, is_easy):
        '''
        Inicializa todos os atributos que serão mostrados na tela:
        pergunta matemática, pontuação do jogador, contagem shuriken.
        '''
        self.is_easy = is_easy

        self.math_question = Question(is_easy)

        self.math_question_text = render_font(
            self.math_question.get_string(), font=INTERMEDIATE_FONT
        )

        self.keyboard_input = ''

        self.keyboard_input_text = render_font(
            self.keyboard_input, font=INTERMEDIATE_FONT
        )

        self.text_box = pygame.Surface([100, 40])
        self.text_box.fill([200, 200, 200])

        self.score = 75

        self.score_text = render_font(
            f'Ninja IQ: {self.score}', font=INTERMEDIATE_FONT
        )

        self.shuriken_count = 0

        self.shuriken_count_text = render_font(
            str(self.shuriken_count), font=INTERMEDIATE_FONT
        )

    def render(self, display):
        '''Apresenta o painel inteiro em um determinado display'''
        self.render_math_question(display)
        self.render_score(display)
        self.render_shuriken_count(display)

    def render_math_question(self, display):
        '''Apresenta a pergunta matemática em uma determinada tela'''
        display.blit(self.math_question_text, [10, 10])
        display.blit(self.text_box, [10, 40])
        display.blit(self.keyboard_input_text, [13, 43])

    def render_score(self, display):
        '''Apresenta a pontuação em uma determinada tela'''
        display.blit(self.score_text, [225, 20])

    def render_shuriken_count(self, display):
        '''Fornece a contagem embaralhada em uma determinada tela'''
        display.blit(GAME_CONSTANTS['PANEL_SHURIKEN_IMAGE'], [470, 15])
        display.blit(self.shuriken_count_text, [510, 20])

    def add_score(self):
        '''Atualiza a pontuação do jogador, dependendo da dificuldade do jogo'''
        if self.is_easy:
            self.score += 5
        else:
            self.score += 10

        self.score_text = render_font(
            f'Ninja IQ: {self.score}', font=INTERMEDIATE_FONT
        )

    def spend_shuriken(self):
        '''Atualiza a contagem shuriken quando o jogador joga um shuriken'''
        self.shuriken_count -= 1

        self.shuriken_count_text = render_font(
            str(self.shuriken_count), font=INTERMEDIATE_FONT
        )

    def process_keyboard(self, key):
        '''Entrada de teclado processada (resposta de digitação do jogador)'''
        key_pressed = pygame.key.name(key)

        if key_pressed in '0123456789':
            self.keyboard_input += key_pressed

        else:
            if key == pygame.K_MINUS:
                self.keyboard_input += '-' if len(
                    self.keyboard_input) == 0 else ''

            if key == pygame.K_RETURN:
                if len(self.keyboard_input) <= 0 or self.keyboard_input == '-':
                    return

                if self.math_question.try_answer(self.keyboard_input):
                    self.shuriken_count += 1
                    self.math_question.new_question()

                self.keyboard_input = ''

            if key == pygame.K_BACKSPACE:
                self.keyboard_input = self.keyboard_input[:-1]

        self.math_question_text = render_font(
            self.math_question.get_string(), font=INTERMEDIATE_FONT
        )
        self.keyboard_input_text = render_font(
            self.keyboard_input, font=INTERMEDIATE_FONT
        )
        self.shuriken_count_text = render_font(
            str(self.shuriken_count), font=INTERMEDIATE_FONT
        )


class ShurikenController:
    ''' 
    Define um controlador para lidar com todos os shurikens que aparecem na tela.
    Ele é responsável pela renderização e processamento dos lançamentos shuriken.
    '''

    def __init__(self, panel):
        ''' 
        Inicializa uma matriz para armazenar todos os shurikens que aparecem
        na tela, e um atributo de painel para modificar o painel que
        aparece na parte superior da tela do jogo. 

        Args:
            panel (Panel): panel to be updated  '''

        self.rendered_shurikens = []

        self.panel = panel

    def render(self, display):
        '''Apresenta a cada shuriken em uma determinada tela e atualiza suas posições'''
        for shuriken in self.rendered_shurikens:
            shuriken.render(display)
            shuriken.update_position()

    def process_keyboard(self, key):
        '''Processa toques de tecla para atirar shurikens'''
        if self.panel.shuriken_count <= 0:
            return

        if key == pygame.K_LEFT:
            self.rendered_shurikens.append(Shuriken(direction='LEFT'))
            self.panel.spend_shuriken()

            pygame.mixer.Sound.play(GAME_CONSTANTS['SHURIKEN_SOUND'])

        if key == pygame.K_RIGHT:
            self.rendered_shurikens.append(Shuriken(direction='RIGHT'))
            self.panel.spend_shuriken()

            pygame.mixer.Sound.play(GAME_CONSTANTS['SHURIKEN_SOUND'])


class EnemyNinjaController:
    ''' 
    Define um controlador para lidar com todos os ninjas inimigos que aparecem na tela.
    Ele é responsável pela renderização e desova dos ninjas inimigos.
    '''

    def __init__(self, spawn_time):
        '''
        Inicializa uma matriz para armazenar todos os ninjas inimigos que aparecem em 
        tela. Um evento de pygame é definido para ser acionado entre iguais
        intervalos de tempo em milissegundos (spawn_time). Este evento 
        é tratado no circuito principal do jogo, chamando de spawn_enemy_ninjas.
        '''
        self.rendered_enemy_ninjas = []

        pygame.time.set_timer(pygame.USEREVENT, spawn_time)

    def render(self, display):
        '''Apresenta cada ninja inimigo em uma determinada tela e atualiza suas posições'''
        for enemy_ninja in self.rendered_enemy_ninjas:
            enemy_ninja.render(display)
            enemy_ninja.update_position()

    def spawn_enemy_ninjas(self):
        '''Escolha aleatoriamente um lado para o ninja e adicione-o ao conjunto.'''
        side = random.choice(['RIGHT', 'LEFT'])
        self.rendered_enemy_ninjas.append(EnemyNinja(side=side))


class CollisionController:
    '''
    Define um controlador para todas as colisões que possam acontecer no jogo.
    Dependendo de quais agentes colidiram, uma ação diferente é tomada.
    '''

    def __init__(self, meditating_ninja, shuriken_control, enemy_ninja_control, panel, gameover_action):
        '''Armazena todas as entidades do jogo para acessar suas propriedades dentro da classe'''
        self.meditating_ninja = meditating_ninja
        self.shuriken_control = shuriken_control
        self.enemy_ninja_control = enemy_ninja_control
        self.panel = panel
        self.gameover_halt = gameover_action

    def __detect_collision(self, A, B):
        '''
        Função que detecta a colisão entre dois corpos.
        Uma colisão é detectada quando a coordenada x de um corpo
        está entre os lados do outro. y-coordenadas não são
        considerado porque não há necessidade disso no jogo.

        Args: Dois corpos com uma propriedade de posição x-y (na forma de uma lista)

        Returns: bool representando a colisão dos corpos
        '''
        A_middle_x = A.position[0] + (A.size[0] // 2)

        B_front_x = B.position[0]
        B_back_x = B.position[0] + B.size[0]

        if A_middle_x >= B_front_x and A_middle_x <= B_back_x:
            return True

        return False

    def detect_gameover(self):
        '''
        Verifica se há colisões entre todos os inimigos e o ninja meditante.
        Se uma colisão tiver ocorrido, chama-se jogo sobre procedimento.
        '''
        for enemy_ninja in self.enemy_ninja_control.rendered_enemy_ninjas:
            if self.__detect_collision(enemy_ninja, self.meditating_ninja):
                self.on_gameover_detected()

    def on_gameover_detected(self):
        '''
        Pára a música do jogo e toca um efeito sonoro. Congela
        a tela e chama um procedimento para interromper a execução do jogo.
        '''
        pygame.mixer.music.stop()
        pygame.mixer.Sound.play(GAME_CONSTANTS['GONG_SOUND'])

        time.sleep(2)

        self.gameover_halt()

    def detect_player_scored(self):
        '''
        Verificações de colisões entre todos os shurikens e todos os ninjas inimigos.
        Se uma colisão tiver ocorrido, um procedimento é chamado para aumentar a pontuação.
        '''
        for shuriken in self.shuriken_control.rendered_shurikens:
            for enemy_ninja in self.enemy_ninja_control.rendered_enemy_ninjas:
                if self.__detect_collision(shuriken, enemy_ninja):
                    self.on_score(shuriken, enemy_ninja)

    def on_score(self, shuriken, enemy_ninja):
        '''Remove o ninja inimigo e o shuriken que colidiu da tela, e aumenta a pontuação'''
        self.enemy_ninja_control.rendered_enemy_ninjas.remove(enemy_ninja)
        self.shuriken_control.rendered_shurikens.remove(shuriken)
        self.panel.add_score()

    def scan_for_collisions(self):
        '''Verificações para todos os tipos de colisões'''
        self.detect_gameover()
        self.detect_player_scored()
