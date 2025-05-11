import pygame
import os
from menu.ranking.ranking import Ranking
from quiz.quiz import executar_quiz


class Menu:
    def __init__(self, tela):
        self.tela = tela
        pygame.font.init()
        self.fonte = pygame.font.SysFont("Comic Sans MS", 40)
        self.fonte_pequena = pygame.font.SysFont("Comic Sans MS", 25)
        self.opcoes_principal = ["Jogar", "Sobre o Jogo", "Ranking", "Quiz", "Sair"]
        self.opcoes_fases = ["Fase 1", "Fase 2", "Fase 3", "Voltar"]
        self.estado = "principal"
        self.selecionado = 0
        self.botoes = []
        
        # Carrega imagem de fundo
        caminho_fundo = os.path.join("menu", "imagens", "fundomenu.png")
        if os.path.exists(caminho_fundo):
            self.imagem_fundo = pygame.image.load(caminho_fundo).convert()
            self.imagem_fundo = pygame.transform.scale(self.imagem_fundo, tela.get_size())
        else:
            self.imagem_fundo = pygame.Surface(tela.get_size())
            self.imagem_fundo.fill((0, 0, 0))
        
        # Registra novo jogador
        self.jogador = self.registrar_novo_jogador()

    def executar(self):
        clock = pygame.time.Clock()
        while True:
            self.criar_botoes()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "Sair"

                if event.type == pygame.MOUSEMOTION:
                    self.navegar_mouse(event.pos)

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    escolha = self.processar_clique(event.pos)
                    if escolha == "Ranking":
                        ranking = Ranking(self.tela)
                        ranking.executar()
                    elif escolha == "Jogar":
                        self.estado = "fases"
                    elif escolha == "Sobre o Jogo":
                        self.estado = "sobre"
                    elif escolha == "Quiz":
                        executar_quiz() 
                    elif escolha == "Voltar":
                        self.estado = "principal"
                    elif escolha == "Sair":
                        return "Sair"
                    elif escolha in ["Fase 1", "Fase 2", "Fase 3"]:
                        return escolha

            self.desenhar()
            pygame.display.flip()
            clock.tick(30)

    def processar_clique(self, pos):
        for texto, rect, opcao in self.botoes:
            if rect.collidepoint(pos):
                return opcao
        return None

    def criar_botoes(self):
        largura, altura = self.tela.get_size()
        self.botoes = []

        if self.estado == "sobre":
            return

        opcoes = self.opcoes_fases if self.estado == "fases" else self.opcoes_principal

        for i, opcao in enumerate(opcoes):
            texto = self.fonte.render(opcao, True, (255, 255, 255))
            rect = texto.get_rect(center=(largura // 2, altura // 2 - 145 + i * 60))
            self.botoes.append((texto, rect, opcao))

    def navegar_mouse(self, pos):
        if self.estado == "sobre":
            return

        for i, (texto, rect, opcao) in enumerate(self.botoes):
            if rect.collidepoint(pos):
                self.selecionado = i

    def desenhar(self):
        self.tela.blit(self.imagem_fundo, (0, 0))

        if self.estado == "sobre":
            texto_titulo = self.fonte.render("Sobre o Jogo", True, (255, 255, 0))
            rect_titulo = texto_titulo.get_rect(center=(400, 100))
            self.tela.blit(texto_titulo, rect_titulo)

            linhas_info = [
                "Colocar aqui sobre o jogo",
                "ESC para voltar ao menu",
                "",
                "Clique para voltar"
            ]

            for i, linha in enumerate(linhas_info):
                texto = self.fonte_pequena.render(linha, True, (255, 255, 255))
                rect = texto.get_rect(center=(400, 200 + i * 40))
                self.tela.blit(texto, rect)
        else:
            for i, (texto, rect, opcao) in enumerate(self.botoes):
                cor = (255, 255, 255) if i != self.selecionado else (255, 255, 0)
                texto = self.fonte.render(opcao, True, cor)
                self.tela.blit(texto, rect)
    def registrar_novo_jogador(self):
        nome = ""
        registrado = False

        while not registrado:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    return ""
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_RETURN and nome:
                        # Salva o nome do jogador
                        with open("menu/jogador.txt", "w") as arquivo:
                            arquivo.write(nome)
                        
                        # Adiciona ao ranking com 0 pontos
                        with open("menu/ranking/ranking.txt", "a") as arquivo_ranking:
                            arquivo_ranking.write(f"\n{nome},0")
                        
                        registrado = True
                    elif evento.key == pygame.K_BACKSPACE:
                        nome = nome[:-1]
                    else:
                        nome += evento.unicode

            # Renderização da tela de registro
            self.tela.fill((0, 0, 0))
            texto_instrucao = self.fonte.render("Digite seu nome e pressione ENTER:", True, (255, 255, 255))
            texto_nome = self.fonte.render(nome, True, (255, 255, 255))
            self.tela.blit(texto_instrucao, (50, 250))
            self.tela.blit(texto_nome, (50, 300))
            pygame.display.flip()

        return nome
    
    def adicionar_pontos(self, pontos):
        """Adiciona pontos ao jogador atual no arquivo ranking.txt"""
        try:
            with open("menu/ranking/ranking.txt", "r+", encoding="utf-8") as f:
                linhas = f.readlines()
                encontrado = False
                
                for i, linha in enumerate(linhas):
                    if linha.startswith(f"{self.jogador},"):
                        partes = linha.split(",")
                        linhas[i] = f"{partes[0]},{int(partes[1]) + pontos}\n"
                        encontrado = True
                        break
                
                if not encontrado:
                    linhas.append(f"{self.jogador},{pontos}\n")
                
                f.seek(0)
                f.writelines(linhas)
        except FileNotFoundError:
            with open("menu/ranking/ranking.txt", "w", encoding="utf-8") as f:
                f.write(f"{self.jogador},{pontos}\n")