import pygame
import sys

def calcular_tamanho_proporcional(imagem_path, nova_altura):
    imagem = pygame.image.load(imagem_path).convert_alpha()
    largura_original, altura_original = imagem.get_size()
    proporcao = nova_altura / altura_original
    nova_largura = int(largura_original * proporcao)
    return (nova_largura, nova_altura)

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
            self.rect.x = max(0, min(self.rect.x, 800 - self.rect.width))
            self.rect.y = max(0, min(self.rect.y, 600 - self.rect.height))



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
        caminho = 'personagens/imagens/personagemcriança.png'
        tamanho = calcular_tamanho_proporcional(caminho, 105)
        super().__init__(caminho, x, y, teclas_controle, tamanho)

class Personagem2(PersonagemBase):
    def __init__(self, x, y):
        teclas_controle = {
            "esquerda": [pygame.K_a, pygame.K_LEFT],
            "direita": [pygame.K_d, pygame.K_RIGHT],
            "cima": [pygame.K_w, pygame.K_UP],
            "baixo": [pygame.K_s, pygame.K_DOWN]
        }
        caminho = 'personagens/imagens/personagemadolescente.png'
        tamanho = calcular_tamanho_proporcional(caminho, 120)
        super().__init__(caminho, x, y, teclas_controle, tamanho)
        
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
        self.rect.x = max(0, min(self.rect.x, 800 - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, 600 - self.rect.height))
            
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
        caminho = 'personagens/imagens/personagemadulto.png'
        tamanho = calcular_tamanho_proporcional(caminho, 130)
        super().__init__(caminho, x, y, teclas_controle, tamanho)

class Vilao(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        caminho = 'personagens/imagens/homemdosaco.png'
        tamanho = calcular_tamanho_proporcional(caminho, 120)
        self.image = pygame.image.load(caminho).convert_alpha()
        self.image = pygame.transform.scale(self.image, tamanho)
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

        self.rect.x = max(0, min(self.rect.x, 800 - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, 600 - self.rect.height))

    def desenhar(self, display):
        display.blit(self.image, self.rect.topleft)

            
class Vilao2(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        caminho = 'personagens/imagens/agiota.png'
        tamanho = calcular_tamanho_proporcional(caminho, 140)
        self.image = pygame.image.load(caminho).convert_alpha()
        self.image = pygame.transform.scale(self.image, tamanho)
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
        self.rect.x = max(0, min(self.rect.x, 800 - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, 600 - self.rect.height))

    def desenhar(self, display):
        display.blit(self.image, self.rect.topleft)
