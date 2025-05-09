import pygame
import sys

class PersonagemBase(pygame.sprite.Sprite):
    def __init__(self, imagem_path, x, y, teclas_controle, tamanho):
        super().__init__()
        self.image = pygame.image.load(imagem_path)
        self.image = pygame.transform.scale(self.image, tamanho)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.velocidade = 5
        self.teclas = teclas_controle

    def update(self, teclas_pressionadas):
        for direcao, teclas in self.teclas.items():
            if any(teclas_pressionadas[tecla] for tecla in teclas):  
                if direcao == "esquerda":
                    self.rect.x -= self.velocidade
                elif direcao == "direita":
                    self.rect.x += self.velocidade
                elif direcao == "cima":
                    self.rect.y -= self.velocidade
                elif direcao == "baixo":
                    self.rect.y += self.velocidade

        # Limites da tela
        if self.rect.left < -30:
            self.rect.left = -30
        if self.rect.right > 830:
            self.rect.right = 830
        if self.rect.top < -10:
            self.rect.top = -10
        if self.rect.bottom > 610:
            self.rect.bottom = 610

        if self.rect.bottom > 600:
            pygame.quit()
            sys.exit()

    def desenhar(self, display):
        display.blit(self.image, self.rect.topleft)

class Personagem1(PersonagemBase):
    def __init__(self, x, y):
        teclas_controle = {
            "esquerda": [pygame.K_a, pygame.K_LEFT],
            "direita": [pygame.K_d, pygame.K_RIGHT],
            "cima": [pygame.K_w, pygame.K_UP],
            "baixo": [pygame.K_s, pygame.K_DOWN]
        }
        tamanho = (110, 120)
        super().__init__('personagens/imagens/personagemcriança.png', x, y, teclas_controle, tamanho)

class Personagem2(PersonagemBase):
    def __init__(self, x, y):
        teclas_controle = {
            "esquerda": [pygame.K_a, pygame.K_LEFT],
            "direita": [pygame.K_d, pygame.K_RIGHT],
            "cima": [pygame.K_w, pygame.K_UP],
            "baixo": [pygame.K_s, pygame.K_DOWN]
        }
        tamanho = (150, 150)
        super().__init__('personagens/imagens/personagemadolescente.png', x, y, teclas_controle, tamanho)
        
class Personagem3(PersonagemBase):
    def __init__(self, x, y):
        teclas_controle = {
            "esquerda": [pygame.K_a, pygame.K_LEFT],
            "direita": [pygame.K_d, pygame.K_RIGHT],
            "cima": [pygame.K_w, pygame.K_UP],
            "baixo": [pygame.K_s, pygame.K_DOWN]
        }
        tamanho = (150, 150)
        super().__init__('personagens/imagens/personagemadulto.png', x, y, teclas_controle, tamanho)

class Vilao(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('personagens/imagens/homemdosaco.png')
        self.image = pygame.transform.scale(self.image, (120, 150))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.velocidade = 1 # velocidade do homem do saco

    def update(self, personagem):
        if personagem.rect.centerx > self.rect.centerx:
            self.rect.x += self.velocidade
        elif personagem.rect.centerx < self.rect.centerx:
            self.rect.x -= self.velocidade

        if personagem.rect.centery > self.rect.centery:
            self.rect.y += self.velocidade
        elif personagem.rect.centery < self.rect.centery:
            self.rect.y -= self.velocidade

        if self.rect.left < -30:
            self.rect.left = -30
        if self.rect.right > 830:
            self.rect.right = 830
        if self.rect.top < -10:
            self.rect.top = -10
        if self.rect.bottom > 610:
            self.rect.bottom = 610

    def desenhar(self, display):
        display.blit(self.image, self.rect.topleft)
