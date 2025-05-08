import pygame

class Ranking:
    def __init__(self, tela):
        self.tela = tela
        self.fonte_titulo = pygame.font.Font("menu/fontes/ChauPhilomeneOne-Regular.ttf", 100)
        self.fonte_itens = pygame.font.Font("menu/fontes/ChauPhilomeneOne-Regular.ttf", 36)
        self.cor_azul = (20, 25, 90)  
        self.rect_azul = pygame.Rect(0, 0, 650, 450)
        self.rect_azul.center = self.tela.get_rect().center
        self.voltar_botao = pygame.Rect(350, 520, 100, 50)
        self.ranking_data = self.carregar_ranking()

    def carregar_ranking(self):
        try:
            with open("menu/ranking.txt", "r") as arquivo:
                conteudo = arquivo.read().strip()
                if not conteudo:
                    return []
                # Divide os registros por ";" e depois nome/pontuação por ","
                #Por causa que estamos guardando nome1, pontuacao; nome2, pontuacao;
                registros = [reg.strip().split(",") for reg in conteudo.split(";") if reg]
                # Converte pontuação para inteiro e ordena do maior para o menor
                registros_ordenados = sorted(registros, key=lambda x: int(x[1]), reverse=True)
                return registros_ordenados[:10]  # Mostra só o top 10
        except FileNotFoundError:
            return []

    def salvar_pontuacao(self, nome, pontuacao):
        # Adiciona a nova pontuação no início (topo) e reordena
        nova_entrada = f"{nome},{pontuacao}"
        registros_existentes = ";".join([f"{reg[0]},{reg[1]}" for reg in self.ranking_data])
        novo_conteudo = f"{nova_entrada};{registros_existentes}" if registros_existentes else nova_entrada
        
        with open("menu/ranking.txt", "w") as arquivo:
            arquivo.write(novo_conteudo)
        
        # Recarrega os dados atualizados
        self.ranking_data = self.carregar_ranking()

    def executar(self):
        fundo = pygame.image.load("menu/ranking.png").convert()
        fundo = pygame.transform.scale(fundo, (800, 600))
        
        rodando = True
        while rodando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    return False
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    if self.voltar_botao.collidepoint(evento.pos):
                        return True

            # Desenha fundo e  onde ficam os nomes retângulo azul
            self.tela.blit(fundo, (0, 0))
            superficie_azul = pygame.Surface((self.rect_azul.width, self.rect_azul.height), pygame.SRCALPHA)
            pygame.draw.rect(superficie_azul, (*self.cor_azul, 82), superficie_azul.get_rect(), border_radius=10)
            self.tela.blit(superficie_azul, self.rect_azul.topleft)
            
            # Título "RANKING"
            titulo = self.fonte_titulo.render("RANKING", True, (255, 255, 255))
            titulo_rect = titulo.get_rect(centerx=self.rect_azul.centerx, top=self.rect_azul.top + 20)
            self.tela.blit(titulo, titulo_rect)
            

            cabecalho_nome = self.fonte_itens.render("Jogador", True, (255, 255, 255))
            cabecalho_pontos = self.fonte_itens.render("Pontos", True, (255, 255, 255))
            self.tela.blit(cabecalho_nome, (self.rect_azul.left + 100, self.rect_azul.top + 100))
            self.tela.blit(cabecalho_pontos, (self.rect_azul.right - 150, self.rect_azul.top + 100))
            
            # Itens do ranking
            for i, (nome, pontos) in enumerate(self.ranking_data):
                posicao = self.fonte_itens.render(f"{i+1}º", True, (255, 255, 255))
                jogador = self.fonte_itens.render(nome, True, (255, 255, 255))
                pontuacao = self.fonte_itens.render(pontos, True, (255, 255, 255))
                
                self.tela.blit(posicao, (self.rect_azul.left + 50, self.rect_azul.top + 150 + i * 40))
                self.tela.blit(jogador, (self.rect_azul.left + 100, self.rect_azul.top + 150 + i * 40))
                self.tela.blit(pontuacao, (self.rect_azul.right - 150, self.rect_azul.top + 150 + i * 40))
            
            # Botão "Voltar"
            pygame.draw.rect(self.tela, (100, 100, 100), self.voltar_botao, border_radius=5)
            texto_voltar = self.fonte_itens.render("Voltar", True, (255, 255, 255))
            self.tela.blit(texto_voltar, (self.voltar_botao.centerx - texto_voltar.get_width()//2, 
                                          self.voltar_botao.centery - texto_voltar.get_height()//2))
            
            pygame.display.flip()
        
        return True