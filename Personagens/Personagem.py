import pygame
import sys

class Personagem:
    def __init__(self, x, y):
        self.imagem_original = pygame.image.load('personagens/imagens/personagemCriança.png')
        self.imagem = pygame.transform.scale(self.imagem_original, (150, 150))  # tamanho do personagem
        self.x = x
        self.y = y
        self.velocidade = 5  # velocidade do personagem

    def mover(self, teclas):
        if teclas[pygame.K_LEFT]:
            self.x -= self.velocidade
        if teclas[pygame.K_RIGHT]:
            self.x += self.velocidade
        if teclas[pygame.K_UP]:
            self.y -= self.velocidade
        if teclas[pygame.K_DOWN]:
            self.y += self.velocidade

    def desenhar(self, display):
        display.blit(self.imagem, (self.x, self.y))