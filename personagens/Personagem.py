import pygame
import sys

class PersonagemBase(pygame.sprite.Sprite):
    def __init__(self, imagem_path, x, y, teclas_controle, tamanho):
        super().__init__()
        self.image = pygame.image.load(imagem_path)
        self.image = pygame.transform.scale(self.image, tamanho)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.velocidade = 6
        self.teclas = teclas_controle
        self.lento_timer = 0

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
        self.velocidade = 5
        self.lento_timer = 0

    def update(self, teclas_pressionadas):
        # Implementação original do update
        movimento = {
            "esquerda": any(teclas_pressionadas[tecla] for tecla in self.teclas_controle["esquerda"]),
            "direita": any(teclas_pressionadas[tecla] for tecla in self.teclas_controle["direita"]),
            "cima": any(teclas_pressionadas[tecla] for tecla in self.teclas_controle["cima"]),
            "baixo": any(teclas_pressionadas[tecla] for tecla in self.teclas_controle["baixo"])
        }

        if movimento["esquerda"]:
            self.rect.x -= self.velocidade
        if movimento["direita"]:
            self.rect.x += self.velocidade
        if movimento["cima"]:
            self.rect.y -= self.velocidade
        if movimento["baixo"]:
            self.rect.y += self.velocidade

        self.rect.x = max(0, min(self.rect.x, 800 - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, 600 - self.rect.height))

class Personagem2Modificado(Personagem2):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.velocidade_padrao = 5
        self.velocidade = self.velocidade_padrao
        self.controles_invertidos = False
        self.efeito_timer = 0
        self.duracao_efeito = 5000  # 5 segundos de efeito

    def update(self, teclas_pressionadas):
        # Verifica se o efeito acabou
        if self.controles_invertidos and pygame.time.get_ticks() > self.efeito_timer:
            self.controles_invertidos = False
            self.velocidade = self.velocidade_padrao

        # Mapeamento das teclas (invertidas ou normais)
        esquerda = (teclas_pressionadas[pygame.K_DOWN] or teclas_pressionadas[pygame.K_s]) if self.controles_invertidos else (teclas_pressionadas[pygame.K_LEFT] or teclas_pressionadas[pygame.K_a])
        direita = (teclas_pressionadas[pygame.K_UP] or teclas_pressionadas[pygame.K_w]) if self.controles_invertidos else (teclas_pressionadas[pygame.K_RIGHT] or teclas_pressionadas[pygame.K_d])
        cima = (teclas_pressionadas[pygame.K_RIGHT] or teclas_pressionadas[pygame.K_d]) if self.controles_invertidos else (teclas_pressionadas[pygame.K_UP] or teclas_pressionadas[pygame.K_w])
        baixo = (teclas_pressionadas[pygame.K_LEFT] or teclas_pressionadas[pygame.K_a]) if self.controles_invertidos else (teclas_pressionadas[pygame.K_DOWN] or teclas_pressionadas[pygame.K_s])

        # Movimentação
        if esquerda:
            self.rect.x -= self.velocidade
        if direita:
            self.rect.x += self.velocidade
        if cima:
            self.rect.y -= self.velocidade
        if baixo:
            self.rect.y += self.velocidade

        # Mantém dentro da tela
        if self.rect.left < -30:
            self.rect.left = -30
        if self.rect.right > 830:
            self.rect.right = 830
        if self.rect.top < -10:
            self.rect.top = -10
        if self.rect.bottom > 610:
            self.rect.bottom = 610
            
    def aplicar_efeito_pilula(self):
        self.velocidade += 2  # Aumenta a velocidade
        self.controles_invertidos = True
        self.efeito_timer = pygame.time.get_ticks() + self.duracao_efeito

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
        self.velocidade = 0.6 # velocidade do homem do saco

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

            
class Vilao2(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('personagens/imagens/agiota.png')  
        self.image = pygame.transform.scale(self.image, (130, 160))  
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.velocidade = 0.6  

    def update(self, personagem_alvo):
        # Movimento em direção ao personagem alvo
        if personagem_alvo.rect.centerx > self.rect.centerx:
            self.rect.x += self.velocidade
        elif personagem_alvo.rect.centerx < self.rect.centerx:
            self.rect.x -= self.velocidade

        if personagem_alvo.rect.centery > self.rect.centery:
            self.rect.y += self.velocidade
        elif personagem_alvo.rect.centery < self.rect.centery:
            self.rect.y -= self.velocidade

        # Limites da tela
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
