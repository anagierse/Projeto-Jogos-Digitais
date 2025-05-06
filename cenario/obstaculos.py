import pygame
import random

class Obstaculo(pygame.sprite.Sprite):
    def __init__(self, tipo, x, y):
        super().__init__()
        self.tipo = tipo  
        self.velocidade = 3

        if tipo == 'poste':
            self.image = pygame.image.load('cenario/imagens/poste.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, (50, 100))
        elif tipo == 'buraco':
            self.image = pygame.Surface((50, 50), pygame.SRCALPHA)
            pygame.draw.circle(self.image, (50, 50, 50), (25, 25), 25)
        else:
            raise ValueError("Tipo de obstáculo inválido: use 'poste' ou 'buraco'.")

        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def update(self):
        self.rect.y += self.velocidade
        if self.rect.top > 600:
            self.kill()