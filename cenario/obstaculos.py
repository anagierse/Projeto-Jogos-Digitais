import pygame
import random

class Obstaculo(pygame.sprite.Sprite):
    def __init__(self, tipo, x, y):
        super().__init__()
        self.tipo = tipo  
        self.velocidade = 3
        self.rua = rua  # Referência à instância da rua
        self.na_rua = False  # Flag para controle

        if tipo == 'poste':
            self.image = pygame.image.load('cenario/imagens/poste.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, (50, 100))
        elif tipo == 'buraco':
            self.image = pygame.Surface((50, 50), pygame.SRCALPHA)
            pygame.draw.circle(self.image, (50, 50, 50), (25, 25), 25)
         elif tipo == 'lixo':
            self.image = pygame.image.load('cenario/imagens/lixo.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, (50, 50))
        elif tipo == 'carro':
            self.image = pygame.image.load('cenario/imagens/carro.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, (80, 50))
        else:
            raise ValueError("Tipo de obstáculo inválido.")
            
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def update(self):
        self.rect.y += self.velocidade
        
        # Verifica se está sobrepondo a rua visível
        if self.rua.visible and self.rect.colliderect(pygame.Rect(0, self.rua.y_pos, 800, self.rua.altura)):
            self.na_rua = True
            
        # Remove se sair da tela ou estiver sobre a rua
        if self.rect.top > 600 or self.na_rua:
            self.kill()
