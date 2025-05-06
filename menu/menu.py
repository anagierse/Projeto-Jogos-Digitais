import pygame
import sys

class Menu:
    def __init__(self, tela):
        self.tela = tela
        self.fonte = pygame.font.Font(None, 36)
        self.opcoes_principais = ["Jogar", "Sobre Nós"]
        self.opcoes_fase = ["Fase 1", "Fase 2", "Fase 3"]
        self.selecao = 0
        self.modo_fases = False

    def desenhar(self):
        self.tela.fill((0, 0, 0))

        if self.modo_fases:
            for i, opcao in enumerate(self.opcoes_fase):
                cor = (255, 0, 0) if i == self.selecao else (255, 255, 255)
                texto = self.fonte.render(opcao, True, cor)
                self.tela.blit(texto, (300, 200 + i * 40))
        else:
            for i, opcao in enumerate(self.opcoes_principais):
                cor = (255, 0, 0) if i == self.selecao else (255, 255, 255)
                texto = self.fonte.render(opcao, True, cor)
                self.tela.blit(texto, (300, 200 + i * 40))

        pygame.display.flip()

    def navegar(self, evento):
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_DOWN:
                self.selecao = (self.selecao + 1) % len(self.opcoes_principais if not self.modo_fases else self.opcoes_fase)
            elif evento.key == pygame.K_UP:
                self.selecao = (self.selecao - 1) % len(self.opcoes_principais if not self.modo_fases else self.opcoes_fase)
            elif evento.key == pygame.K_RETURN:
                if not self.modo_fases:
                    if self.selecao == 0:
                        self.modo_fases = True
                    elif self.selecao == 1:
                        print("Sobre Nós selecionado.")
                else:
                    if self.selecao == 0:
                        return "Fase 1"
                    elif self.selecao == 1:
                        return "Fase 2"
                    elif self.selecao == 2:
                        return "Fase 3"
        return None

    def mostrar_sobre_nos(self):
        print("Tela Sobre Nós")
