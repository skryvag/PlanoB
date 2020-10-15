import pygame


def render_font(text, font, color=[0, 0, 0]):
    '''
    Função que gera texto pronto para ser exibido
    na tela por pygame.

    Args:
        text (string): o texto a ser apresentado
        font (pygame.font.Font): fonte para renderizar o texto
        color (list): RGB cor do texto

    Returns:
        pygame.Surface: texto pronto para ser exibido na tela
    '''
    return font.render(text, True, color)


class Screen:
    '''
    Define uma tela. Ela define todos os métodos 
    e atributos compartilhados por todas as telas de jogo.
    '''

    def __init__(self, name=''):
        '''
        Inicializa uma janela de pygame, inicializa
        propriedade, declara next_screen, e
        armazena o nome do jogador, se houver algum.

        Args:
            name (string): nome do jogador, opcional.
        '''

        pygame.display.set_caption('The Meditating Dog')
        self.screen = pygame.display.set_mode([675, 400])

        self.run = True

        self.next_screen = None

        self.name = name

    def stop_running(self):
        '''Atributo do conjunto a falso'''
        self.run = False

    def set_next_screen(self, screen_name):
        '''Define o atributo next_screen para um determinado nome (string)'''
        self.next_screen = screen_name


class Ranking:
    '''
    Classe que define um objeto do Ranking. O objeto está conectado a um 
    arquivo de texto. Considere a linha N (onde N é estranho) como sendo o nome de 
    o jogador e a linha N + 1 a pontuação desse jogador.
    '''

    def __init__(self, path):
        '''
        Lê um determinado arquivo de texto e inicializa um mapeamento de atributos
        cada nome para cada pontuação como um dicionário. Inicializa um 
        atributo contendo uma lista ordenada de nomes, e o caminho
        ao arquivo de texto também se torna um atributo.

        Args:
            path (string): caminho para o arquivo de texto com nomes e pontuações.
        '''
        with open(path, 'r') as f:
            lines = f.read().splitlines()  # Armazena cada linha em uma matriz

        players = {}

        for i in range(0, len(lines) - 1, 2):  # Mapas de cada nome para cada pontuação
            players[lines[i]] = int(lines[i + 1])

        # Cria uma lista ordenada de nomes com base na pontuação do jogador.
        leaderboard = sorted(players, key=players.get, reverse=True)

        self.__players = players
        self.__leaderboard = leaderboard

        self.__path = path

    def update(self):
        '''Realiza a atualização de atributos do construtor com mudanças no arquivo de texto'''
        self.__init__(self.__path)

    def export_players(self):
        '''Re-escreve o arquivo de texto com os jogadores e as pontuações armazenadas no atributo do objeto'''
        with open(self.__path, 'w') as f:
            for player in self.__players.keys():
                f.write(f'{player}\n')
                f.write(f'{self.__players[player]}\n')

    def new_record(self, name, score):
        '''
        Economiza uma nova pontuação em um dicionário (__players attribute)
        e atualiza o arquivo de texto. Se o jogador já tem uma pontuação e 
        a nova não é sua maior função, a função não funciona.

        Args:
            name (string): nome do jogador
            score (int): pontuação do jogador
        '''
        if name in self.__players and self.__players[name] > score:
            return

        self.__players[name] = score

        self.export_players()

        self.update()

    def get_leaderboard(self):
        '''Returns: dicionário que mapeia nomes para pontuações'''
        return self.__leaderboard

    def get_players(self):
        '''Returns: lista de nomes de jogadores ordenados por pontuação'''
        return self.__players
