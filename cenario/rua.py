import pygame


class Rua:
    def __init__(self, tela_largura=800, tela_altura=600):
        self.imagem_original = pygame.image.load('cenario/imagens/rua.png').convert_alpha()
        
        self.largura = tela_largura
        self.altura = 100  #Se quiser afinar a rua so mexer aqui
        self.imagem = pygame.transform.scale(self.imagem_original, (self.largura, self.altura))

        self.y_pos = 0

    def atualizar(self, velocidade):
        self.y_pos += velocidade

     #aqui ele vai reiniciar sempre que a rua chegar no fim da tela, precisa mudar isso 
        if self.y_pos > 600:
            self.y_pos = -self.altura  

    def desenhar(self, tela):
        tela.blit(self.imagem, (0, self.y_pos))
