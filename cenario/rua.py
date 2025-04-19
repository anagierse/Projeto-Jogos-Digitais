import pygame

class Rua:
    def __init__(self, tela_largura=800):
        self.imagem_original = pygame.image.load('cenario/imagens/rua.png').convert_alpha()
        
        self.largura = tela_largura
        proporcao = tela_largura / self.imagem_original.get_width()
        self.altura = int(self.imagem_original.get_height() * proporcao)
        
        self.imagem = pygame.transform.scale(self.imagem_original, (self.largura, self.altura))
        self.y = 400 

    def desenhar(self, tela):
        tela.blit(self.imagem, (0, self.y - self.altura))  