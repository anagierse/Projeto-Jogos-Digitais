import pygame
import os

class Menu:
    def __init__(self, tela):
        self.tela = tela
        self.fonte = pygame.font.SysFont("Comic Sans MS", 40)
        self.fonte_pequena = pygame.font.SysFont("Comic Sans MS", 25)
        self.opcoes_principal = ["Jogar", "Sobre o Jogo", "Sair", "Ranking"]
        self.opcoes_fases = ["Fase 1", "Fase 2", "Fase 3", "Voltar"]
        self.estado = "principal"
        self.selecionado = 0
        self.botoes = []
        self.imagem_fundo = pygame.image.load("menu/imagens/fundomenu.png").convert()
        self.imagem_fundo = pygame.transform.scale(self.imagem_fundo, self.tela.get_size())
        self.jogador = self.registrar_novo_jogador()
        self.ranking_data = self.carregar_ranking()

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
                        with open("menu/jogador.txt", "w") as arquivo:
                            arquivo.write(nome)
                        registrado = True
                    elif evento.key == pygame.K_BACKSPACE:
                        nome = nome[:-1]
                    else:
                        nome += evento.unicode

            self.tela.fill((0, 0, 0))
            texto_instrucao = self.fonte.render("Digite seu nome e pressione ENTER:", True, (255, 255, 255))
            texto_nome = self.fonte.render(nome, True, (255, 255, 255))
            self.tela.blit(texto_instrucao, (50, 250))
            self.tela.blit(texto_nome, (50, 300))
            pygame.display.flip()

        return nome

    def carregar_ranking(self):
        try:
            with open("menu/ranking.txt", "r") as arquivo:
                linhas = arquivo.readlines()
                ranking = []
                for linha in linhas:
                    if "," in linha:
                        nome, pontos = linha.strip().split(",")
                        ranking.append((nome, int(pontos)))
                ranking.sort(key=lambda x: x[1], reverse=True)
                return ranking
        except FileNotFoundError:
            return []

    def salvar_pontuacao(self, pontos):
        if not self.jogador:
            return

        self.ranking_data.append((self.jogador, pontos))
        self.ranking_data.sort(key=lambda x: x[1], reverse=True)
        self.ranking_data = self.ranking_data[:10]

        with open("menu/ranking.txt", "w") as arquivo:
            for nome, pts in self.ranking_data:
                arquivo.write(f"{nome},{pts}\n")

    def mostrar_tela_ranking(self):
        rodando = True
        cor_azul = (20, 25, 90)
        rect_azul = pygame.Rect(100, 100, 600, 400)

        while rodando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    return False
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_ESCAPE:
                        rodando = False
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    rodando = False

            self.tela.blit(self.imagem_fundo, (0, 0))

            superficie_azul = pygame.Surface((rect_azul.width, rect_azul.height), pygame.SRCALPHA)
            pygame.draw.rect(superficie_azul, (*cor_azul, 82), superficie_azul.get_rect(), border_radius=10)
            self.tela.blit(superficie_azul, rect_azul.topleft)

            titulo = self.fonte.render("RANKING", True, (255, 255, 255))
            self.tela.blit(titulo, (rect_azul.centerx - titulo.get_width() // 2, rect_azul.top + 20))

            cabecalho_nome = self.fonte_pequena.render("Jogador", True, (255, 255, 255))
            cabecalho_pontos = self.fonte_pequena.render("Pontos", True, (255, 255, 255))
            self.tela.blit(cabecalho_nome, (rect_azul.left + 50, rect_azul.top + 80))
            self.tela.blit(cabecalho_pontos, (rect_azul.right - 150, rect_azul.top + 80))

            for i, (nome, pontos) in enumerate(self.ranking_data[:10]):
                posicao = self.fonte_pequena.render(f"{i + 1}º", True, (255, 255, 255))
                jogador = self.fonte_pequena.render(nome, True, (255, 255, 255))
                pontuacao = self.fonte_pequena.render(str(pontos), True, (255, 255, 255))
                y_pos = rect_azul.top + 120 + i * 40
                self.tela.blit(posicao, (rect_azul.left + 50, y_pos))
                self.tela.blit(jogador, (rect_azul.left + 100, y_pos))
                self.tela.blit(pontuacao, (rect_azul.right - 150, y_pos))

            texto_voltar = self.fonte_pequena.render("Clique ou pressione ESC para voltar", True, (255, 255, 255))
            self.tela.blit(texto_voltar, (rect_azul.centerx - texto_voltar.get_width() // 2, rect_azul.bottom - 40))

            pygame.display.flip()

        return True

    def executar(self):
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
                        self.mostrar_tela_ranking()
                    elif escolha == "Jogar":
                        self.estado = "fases"
                    elif escolha == "Sobre o Jogo":
                        self.estado = "sobre"
                    elif escolha == "Voltar":
                        self.estado = "principal"
                    elif escolha == "Sair":
                        return "Sair"
                    elif escolha in ["Fase 1", "Fase 2", "Fase 3"]:
                        return escolha

            self.desenhar()
            pygame.display.flip()
            pygame.time.Clock().tick(30)

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
            return None

        for i, (texto, rect, opcao) in enumerate(self.botoes):
            if rect.collidepoint(pos):
                self.selecionado = i
                return opcao
        return None

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
            if not self.botoes:
                self.criar_botoes()

            for i, (texto, rect, opcao) in enumerate(self.botoes):
                cor = (255, 255, 255) if i != self.selecionado else (255, 255, 0)
                texto = self.fonte.render(opcao, True, cor)
                self.tela.blit(texto, rect)
