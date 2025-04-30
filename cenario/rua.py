import pygame
import random

class Rua:
    def __init__(self, tela_largura=800, tela_altura=600):
        self.imagem_original = pygame.image.load('cenario/imagens/rua.png').convert_alpha()
        
        self.largura = tela_largura
        self.altura = 100
        self.imagem = pygame.transform.scale(self.imagem_original, (self.largura, self.altura))

        self.y_pos = -self.altura
        self.velocidade = 0
        self.visible = False
        self.tempo_proximo_appear = random.randint(5, 10) * 1000  
        self.tempo_ultimo_appear = pygame.time.get_ticks()
    
    def atualizar(self, velocidade_base):
        tempo_atual = pygame.time.get_ticks()
        
        if not self.visible:
            if tempo_atual - self.tempo_ultimo_appear >= self.tempo_proximo_appear:
                self.visible = True
                self.y_pos = -self.altura
                self.velocidade = velocidade_base
                self.tempo_ultimo_appear = tempo_atual
        else:
            self.y_pos += self.velocidade
            
            if self.y_pos > 600:
                self.visible = False
                self.tempo_proximo_appear = random.randint(5, 10) * 1000
                self.tempo_ultimo_appear = tempo_atual

    def desenhar(self, tela):
        if self.visible:
            tela.blit(self.imagem, (0, self.y_pos))
            pos_y_rua = self.rua.y_pos
            pos_y_carro = pos_y_rua + (self.rua.altura // 2) - (self.altura // 2) + self.y_offset
            tela.blit(self.imagem, (self.x, pos_y_carro))
