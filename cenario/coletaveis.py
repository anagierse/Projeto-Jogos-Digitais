import pygame

class Pirulito:
    def __init__(self, x_pos, y_pos):
        self.largura = 60  # Tamanho fixo (ajuste conforme necessário)
        self.altura = 60
        self.pos_X = x_pos  # Posição X fixa
        self.pos_Y = y_pos  # Posição Y fixa
        self.velocidade = 0  # Não se move mais

        self.imagem_original = pygame.image.load('cenario/imagens/pirulitoremo.png').convert_alpha()
        self.imagem = pygame.transform.scale(self.imagem_original, (self.largura, self.altura))
        self.rect = pygame.Rect(self.pos_X, self.pos_Y, self.largura, self.altura)

    def atualizar(self):
        # Atualiza apenas o retângulo de colisão (não se move mais)
        self.rect.x = self.pos_X
        self.rect.y = self.pos_Y

    def desenhar(self, tela):
        tela.blit(self.imagem, (self.pos_X, self.pos_Y))




class Pilula:
    def __init__(self, x_pos, y_pos):
        self.largura = 40
        self.altura = 40
        self.pos_X = x_pos
        self.pos_Y = y_pos
        self.velocidade = 2
        self.imagem_original = pygame.image.load('cenario/imagens/pilularemo.png').convert_alpha()
        self.imagem = pygame.transform.scale(self.imagem_original, (self.largura, self.altura))
        self.rect = pygame.Rect(self.pos_X, self.pos_Y, self.largura, self.altura)

    def atualizar(self):
        self.pos_Y += self.velocidade
        self.rect.y = self.pos_Y

    def desenhar(self, tela):
        tela.blit(self.imagem, (self.pos_X, self.pos_Y))



class Dinheiro:
    def __init__(self, x_pos, y_pos):
        self.largura = 60
        self.altura = 60
        self.pos_X = x_pos
        self.pos_Y = y_pos
        self.velocidade = 3
        self.imagem_original = pygame.image.load('cenario/imagens/dinheiroremo.png').convert_alpha()
        self.imagem = pygame.transform.scale(self.imagem_original, (self.largura, self.altura))
        self.rect = pygame.Rect(self.pos_X, self.pos_Y, self.largura, self.altura)

    def atualizar(self):
        self.pos_Y += self.velocidade  # Agora desce verticalmente
        self.rect.y = self.pos_Y

    def desenhar(self, tela):
        tela.blit(self.imagem, (self.pos_X, self.pos_Y))

class Maquina:
    def __init__(self, x_pos, y_pos):
        self.largura = 60
        self.altura = 60
        self.pos_X = x_pos
        self.pos_Y = y_pos
        self.velocidade = 3
        self.imagem_original = pygame.image.load('cenario/imagens/maquinaremo.png').convert_alpha()
        self.imagem = pygame.transform.scale(self.imagem_original, (self.largura, self.altura))
        self.rect = pygame.Rect(self.pos_X, self.pos_Y, self.largura, self.altura)

    def atualizar(self):
        self.pos_Y += self.velocidade  # Agora desce verticalmente
        self.rect.y = self.pos_Y

    def desenhar(self, tela):
        tela.blit(self.imagem, (self.pos_X, self.pos_Y))

