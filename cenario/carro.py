import pygame

class Carro:
    def __init__(self, largura, y_pos, velocidade_rua):
        self.largura = 70
        self.altura = 40
        self.pos_Y = y_pos
        self.pos_X = 800
        self.velocidade_horizontal = 8  # Velocidade para esquerda
        self.velocidade_vertical = velocidade_rua  # Velocidade da rua (para baixo)
        
        try:
            self.imagem_original = pygame.image.load('cenario/imagens/carroremo.png').convert_alpha()
            self.imagem = pygame.transform.scale(self.imagem_original, (self.largura + 10, self.altura + 10))
        except:
            self.imagem = pygame.Surface((self.largura, self.altura))
            self.imagem.fill((255, 0, 0))
            pygame.draw.rect(self.imagem, (0, 0, 0), (0, 0, self.largura, self.altura), 2)

        self.rect = pygame.Rect(self.pos_X, self.pos_Y, self.largura, self.altura)

    def atualizar(self):
        self.pos_X -= self.velocidade_horizontal  # Movimento para esquerda
        self.pos_Y += self.velocidade_vertical   # Movimento para baixo (junto com a rua)
        self.rect.x = self.pos_X
        self.rect.y = self.pos_Y

    def desenhar(self, tela):
        tela.blit(self.imagem, (self.pos_X, self.pos_Y))
