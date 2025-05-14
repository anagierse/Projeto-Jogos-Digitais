import pygame
import os

class Ranking:
    def __init__(self, tela):
        self.tela = tela
        pygame.font.init()
        # Fontes 
        self.fonte_titulo = pygame.font.SysFont("Comic Sans MS", 60, bold=True)
        self.fonte_itens = pygame.font.SysFont("Comic Sans MS", 32)
        
        # Fundo transparente
        self.fundo_transparente = pygame.Surface((600, 400), pygame.SRCALPHA)
        pygame.draw.rect(self.fundo_transparente, (20, 25, 90, 180), 
                         self.fundo_transparente.get_rect(), border_radius=10)
        
        self.caminho = os.path.join("menu", "ranking", "ranking.txt")
        self.ranking_data = self.carregar_ranking()

    def carregar_ranking(self):
        try:
            with open(self.caminho, "r", encoding="utf-8") as f:
                linhas = [linha.strip().split(",") for linha in f if linha.strip()]
                dados = [(nome, int(pontos)) for nome, pontos in linhas]
                dados.sort(key=lambda x: x[1], reverse=True)
                return dados[:5] 
        except (FileNotFoundError, ValueError):
            return []

    def adicionar_pontuacao(self, nome_jogador, pontos):
        """Adiciona uma nova pontuação ao ranking"""
        self.ranking_data.append((nome_jogador, pontos))
        # Ordena do maior para o menor
        self.ranking_data.sort(key=lambda x: x[1], reverse=True)
        # Mantém apenas as top 5 pontuações
        self.ranking_data = self.ranking_data[:5]
        
        # Salva no arquivo
        with open(self.caminho, "w", encoding="utf-8") as f:
            for nome, pts in self.ranking_data:
                f.write(f"{nome},{pts}\n")

    def executar(self):
        clock = pygame.time.Clock()
        rodando = True
        
        while rodando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    return True
                if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                    rodando = False
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    rodando = False

            # Desenha o fundo do menu por trás
            self.tela.blit(pygame.image.load(os.path.join("menu", "imagens", "fundomenu.png")).convert(), (0, 0))
            
            # Design de fundo azul transparente
            self.tela.blit(self.fundo_transparente, (100, 100))
            
            titulo = self.fonte_titulo.render("RANKING", True, (255, 255, 0))
            self.tela.blit(titulo, (400 - titulo.get_width()//2, 120))
            
            for i, (nome, pontos) in enumerate(self.ranking_data[:5]):
                y = 200 + i * 40        
                posicao = self.fonte_itens.render(f"{i+1}º", True, (255, 255, 255))
                jogador = self.fonte_itens.render(nome, True, (255, 255, 255))
                pontuacao = self.fonte_itens.render(str(pontos), True, (255, 255, 0))
                
                self.tela.blit(posicao, (150, y))
                self.tela.blit(jogador, (250, y))
                self.tela.blit(pontuacao, (500, y))

            pygame.display.flip()
            clock.tick(60)
        
        return False
