import pygame
import os
from menu.ranking.ranking import Ranking
from quiz.quiz import executar_quiz
import textwrap


class Menu:
    def __init__(self, tela):
        self.tela = tela
        pygame.font.init()
        self.fonte = pygame.font.SysFont("Comic Sans MS", 40)
        self.fonte_pequena = pygame.font.SysFont("Comic Sans MS", 12)
         # Define opções do menu principal e submenu de fases
        self.opcoes_principal = ["Jogar", "Sobre o Jogo", "Ranking", "Quiz", "Sair"]
        self.opcoes_fases = ["Fase 1", "Fase 2", "Fase 3", "Voltar"]
        self.estado = "principal" # Estado atual do menu
        self.selecionado = 0  # Item atualmente selecionado (para destaque)
        self.botoes = []   # Lista de botões (texto, retângulo, opção)
        self.clock = pygame.time.Clock()
        
        caminho_fundo = os.path.join("menu", "imagens", "fundomenu.png")
        if os.path.exists(caminho_fundo):
            self.imagem_fundo = pygame.image.load(caminho_fundo).convert()
            self.imagem_fundo = pygame.transform.scale(self.imagem_fundo, tela.get_size())
        else:
            self.imagem_fundo = pygame.Surface(tela.get_size())
            self.imagem_fundo.fill((0, 0, 0))
        
        # Cria uma camada transparente azul
        self.fundo_transparente = pygame.Surface((750, 550), pygame.SRCALPHA)
        self.fundo_transparente.fill((0, 50, 255, 128))
        
        # Solicita o nome do jogador ao iniciar
        self.jogador = self.registrar_novo_jogador()

    def executar(self):
        while True:
            self.criar_botoes()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "Sair"

                if event.type == pygame.MOUSEMOTION:
                    self.navegar_mouse(event.pos) # Atualiza seleção com base no mouse

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

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if self.estado in ["fases", "sobre", "quiz"]:
                            self.estado = "principal"
                        elif self.estado == "principal":
                            return "Sair"

            self.desenhar()
            pygame.display.flip()
            self.clock.tick(30)

    def processar_clique(self, pos):
        for texto, rect, opcao in self.botoes:
            if rect.collidepoint(pos):
                return opcao
        return None

    def criar_botoes(self):
        largura, altura = self.tela.get_size()
        self.botoes = []

        if self.estado == "sobre":
            return  # Não cria botões se estiver na tela de "sobre"
 
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
         # Título "Sobre o Jogo"
        if self.estado == "sobre":
            texto_titulo = self.fonte.render("Sobre o Jogo", True, (255, 255, 0))
            rect_titulo = texto_titulo.get_rect(center=(self.tela.get_width() // 2, 50))
            self.tela.blit(self.fundo_transparente, (15, 40))

            texto_longo = (
                "Infância:\n"
                "Charlie Brown sempre foi uma criança alegre e curiosa, querendo explorar o mundo e as curiosidades que nele existem."
                " Todos os dias, volta para casa de sua escola sozinho, porém sua mãe sempre o avisa dos perigos que estão presentes na rua,  sequestradores,para traficá-las ou vender seus órgãos no mercado negro."
                "Todo dia, Charlie enfrenta esses perigos, para chegar em casa são e salvo.\n"
                "Adolescência:\n"
                "Após a morte de sua mãe Charlie, não soube lidar bem com o luto, estando numa idade onde as pessoas costumam começar a experimentar coisas novas, acabou entrando no mundo das drogas com colegas do ensino médio, o sentimento de poder e o fato de temporariamente esquecer de sua mãe por algum tempo é o que mais influência no contínuo vício e consumo das drogas.\n"
                "Adulta:\n"
                "Apesar de sua superação com as drogas, na fase adulta, um novo vício surgiu para suprir o vazio que sua mãe deixara, o dinheiro, mesmo tendo um trabalho que paga muito bem, rotineiramente o gasta em máquinas de apostas, e até pedir dinheiro com agiotas para poder apostar, fazendo os agiotas cobrarem sua dívida da forma que for necessário."
            )
            # Quebra o texto longo em várias linhas para caber na tela
            wrapper = textwrap.TextWrapper(width=125)
            linhas_quebradas = []
            for paragrafo in texto_longo.split("\n"):
                linhas_quebradas.extend(wrapper.wrap(paragrafo))
                linhas_quebradas.append("")

            y_pos = 100
            for linha in linhas_quebradas:
                if linha.strip() == "":
                    y_pos += 20
                else:
                    texto_renderizado = self.fonte_pequena.render(linha, True, (255, 255, 255))
                    self.tela.blit(texto_renderizado, (15, y_pos))
                    y_pos += 30

            texto_voltar = self.fonte_pequena.render(" ", True, (255, 255, 0))
            rect_voltar = texto_voltar.get_rect(center=(self.tela.get_width() // 2, self.tela.get_height() - 50))
            self.tela.blit(texto_voltar, rect_voltar)

        else:
        # Desenha botões do menu principal ou de fases
            for i, (texto, rect, opcao) in enumerate(self.botoes):
                cor = (255, 255, 255) if i != self.selecionado else (255, 255, 0)
                texto = self.fonte.render(opcao, True, cor)
                self.tela.blit(texto, rect)

    def registrar_novo_jogador(self):
        nome = ""
        registrado = False
         # Loop até o jogador inserir um nome e apertar Enter
        while not registrado:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    return ""
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_RETURN and nome:
                        # Salva nome em arquivo de jogador.txt e adiciona ao ranking.txt
                        with open("menu/jogador.txt", "w") as arquivo:
                            arquivo.write(nome)
                        with open("menu/ranking/ranking.txt", "a") as arquivo_ranking:
                            arquivo_ranking.write(f"\n{nome},0")
                        registrado = True
                    elif evento.key == pygame.K_BACKSPACE:
                        nome = nome[:-1]
                    else:
                        nome += evento.unicode
            # Interface de digitação do nome
            self.tela.fill((0, 0, 0))
            texto_instrucao = self.fonte.render("Digite seu nome e pressione ENTER:", True, (255, 255, 255))
            texto_nome = self.fonte.render(nome, True, (255, 255, 255))
            self.tela.blit(texto_instrucao, (50, 250))
            self.tela.blit(texto_nome, (50, 300))
            pygame.display.flip()

        return nome

    def adicionar_pontos(self, pontos):
        try:
            # Abre ranking e atualiza os pontos do jogador
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
            # Cria arquivo se ele não existir
            with open("menu/ranking/ranking.txt", "w", encoding="utf-8") as f:
                f.write(f"{self.jogador},{pontos}\n")
