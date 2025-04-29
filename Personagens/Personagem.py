import pygame
import sys

class Personagem1(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('personagens/imagens/personagemCriança.png')
        self.image = pygame.transform.scale(self.image, (150, 150))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.velocidade = 5

    def update(self, teclas):
        if teclas[pygame.K_LEFT]:
            self.rect.x -= self.velocidade
        if teclas[pygame.K_RIGHT]:
            self.rect.x += self.velocidade
        if teclas[pygame.K_UP]:
            self.rect.y -= self.velocidade
        if teclas[pygame.K_DOWN]:
            self.rect.y += self.velocidade

    def desenhar(self, display):
        display.blit(self.image, self.rect.topleft)
