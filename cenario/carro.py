import pygame

class carro: 
    def __init__(self, largura, y_pos):
        self.imagem_original = pygame.image.load('cenario/imagens/')
        self.largura = 50
        self.altura = 80
        self.pos_Y = y_pos
        self.pos_X = 0 - largura
        carro = pygame.Rect(pos_X, pos_Y, largura, altura)

    pygame.draw.rect(display, (0, 0, 0), carro)
