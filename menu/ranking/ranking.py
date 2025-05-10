
# main.py
import pygame
from menu.menu import Menu
from fases import fase1, fase2, fase3

def main():
    pygame.init()
    tela = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Meu Jogo")
    clock = pygame.time.Clock()

    menu = Menu(tela)
    fases = {
        "Fase 1": fase1.executar,
        "Fase 2": fase2.executar,
        "Fase 3": fase3.executar
    }

    while True:
        escolha = menu.executar()

        if escolha == "Sair":
            pygame.quit()
            return

        if escolha == "Ranking":
            from menu.ranking.ranking import Ranking
            ranking_screen = Ranking(tela)
            ranking_screen.executar()
            continue

        if escolha in fases:
            if not fases[escolha](tela):
                break

if __name__ == "__main__":
    main()

# menu/menu.py
import pygame
import os

class Menu:
    def __init__(self, tela):
        self.tela = tela
        pygame.font.init()
        self.fonte = pygame.font.SysFont("Comic Sans MS", 40)
        self.fonte_pequena = pygame.font.SysFont("Comic Sans MS", 25)
        self.opcoes_principal = ["Jogar", "Sobre o Jogo", "Ranking", "Sair"]
        self.opcoes_fases = ["Fase 1", "Fase 2", "Fase 3", "Voltar"]
        self.estado = "principal"
        self.selecionado = 0
        self.botoes = []
        # Carrega imagem de fundo
        caminho = os.path.join(os.path.dirname(__file__), "imagens", "fundomenu.png")
        if os.path.exists(caminho):
            img = pygame.image.load(caminho)
            self.imagem_fundo = pygame.transform.scale(img, self.tela.get_size())
        else:
            self.imagem_fundo = None

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
                        return "Ranking"
                    if escolha == "Jogar":
                        self.estado = "fases"
                    elif escolha == "Sobre o Jogo":
                        self.estado = "sobre"
                    elif escolha == "Voltar":
                        self.estado = "principal"
                    elif escolha == "Sair":
                        return "Sair"
                    elif escolha in self.opcoes_fases:
                        return escolha

            self.desenhar()
            pygame.display.flip()
            clock.tick(30)

    def criar_botoes(self):
        largura, altura = self.tela.get_size()
        self.botoes = []
        if self.estado == "sobre":
            return
        opcoes = self.opcoes_fases if self.estado == "fases" else self.opcoes_principal
        self.botoes = []
        for i, opcao in enumerate(opcoes):
            rect = pygame.Rect(0, 0, 200, 50)
            rect.center = (largura // 2, altura // 2 - 100 + i * 60)
            self.botoes.append((opcao, rect))

    def processar_clique(self, pos):
        for opcao, rect in self.botoes:
            if rect.collidepoint(pos):
                return opcao
        return None

    def navegar_mouse(self, pos):
        for i, (_, rect) in enumerate(self.botoes):
            if rect.collidepoint(pos):
                self.selecionado = i

    def desenhar(self):
        if self.imagem_fundo:
            self.tela.blit(self.imagem_fundo, (0, 0))
        else:
            self.tela.fill((0,0,0))

        if self.estado == "sobre":
            titulo = self.fonte.render("Sobre o Jogo", True, (255, 255, 0))
            self.tela.blit(titulo, (50, 50))
            linhas = ["Este é um jogo de exemplo.", "Pressione Voltar para retornar ao menu."]
            for i, l in enumerate(linhas):
                t = self.fonte_pequena.render(l, True, (255, 255, 255))
                self.tela.blit(t, (50, 150 + i * 40))
        else:
            for i, (opcao, rect) in enumerate(self.botoes):
                cor = (255, 255, 0) if i == self.selecionado else (255, 255, 255)
                texto = self.fonte.render(opcao, True, cor)
                self.tela.blit(texto, texto.get_rect(center=rect.center))

# menu/ranking/ranking.py
import pygame
import os

class Ranking:
    def __init__(self, tela):
        self.tela = tela
        pygame.font.init()
        self.fonte_titulo = pygame.font.SysFont("Arial", 60, bold=True)
        self.fonte_itens = pygame.font.SysFont("Arial", 32)
        base = os.path.dirname(__file__)
        self.caminho = os.path.join(base, "ranking.txt")
        print("Caminho de ranking:", self.caminho)
        self.ranking_data = self.carregar_ranking()

    def carregar_ranking(self):
        lista = []
        try:
            with open(self.caminho, "r", encoding="utf-8") as f:
                for linha in f:
                    if "," in linha:
                        nome, pts = linha.strip().split(",", 1)
                        lista.append((nome, int(pts)))
        except FileNotFoundError:
            print("Arquivo não encontrado.")
            open(self.caminho, "w", encoding="utf-8").close()
        print("Dados carregados:", lista)
        lista.sort(key=lambda x: x[1], reverse=True)
        return lista[:10]

    def executar(self):
        clock = pygame.time.Clock()
        while True:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    return
                if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                    return

            # Desenho de fundo
            self.tela.fill((30,30,50))

            # Título
            titulo = self.fonte_titulo.render("RANKING", True, (255,255,255))
            self.tela.blit(titulo, (self.tela.get_width()//2 - titulo.get_width()//2, 50))

            # Itens
            for i, (nome, pts) in enumerate(self.ranking_data):
                y = 150 + i * 40
                txt_pos = self.fonte_itens.render(f"{i+1}º {nome}", True, (255,255,255))
                txt_pts = self.fonte_itens.render(str(pts), True, (255,255,255))
                self.tela.blit(txt_pos, (100, y))
                self.tela.blit(txt_pts, (600, y))

            pygame.display.flip()
            clock.tick(60)
