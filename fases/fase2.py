import pygame
import random
from cenario.rua import Rua
from personagens.Personagem import Personagem2Modificado
from cenario.obstaculos import Obstaculo
from cenario.carro import Carro
from cenario.coletaveis import Pilula


def executar(tela, menu=None):
    config = {
        "velocidade": 5,
        "intervalo_obstaculos": 1000,
        "cor_fundo": (142, 165, 219),
        "intervalo_pilula": 7000
    }
    TEMPO_FASE = 2 * 60
    tempo_inicio = pygame.time.get_ticks()
    pontos_ja_adicionados = False
    game_over = False
    pontuacao = 0  # Variável para armazenar os pontos

    # Inicializa objetos
    rua = Rua(800, 600)
    personagem = Personagem2Modificado(400, 300)
    carro = None
    pilulas = []
    pilula_timer = 0

    # Grupos de sprites
    grupo_personagens = pygame.sprite.Group(personagem)
    grupo_obstaculos = pygame.sprite.Group()

    clock = pygame.time.Clock()
    running = True
    obstaculo_timer = 0

    while running:
        delta_time = clock.get_time()
        
        if not game_over:
            # Lógica do jogo
            tempo_restante = max(0, TEMPO_FASE - (pygame.time.get_ticks() - tempo_inicio) // 1000)
            
            # Verifica se completou a fase
            if tempo_restante <= 0 and not pontos_ja_adicionados and menu:
                pontuacao_total = pontuacao + 50  # 50 pontos por completar a fase
                menu.adicionar_pontos(pontuacao_total)
                pontos_ja_adicionados = True
                return True
            
            # Eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return True
                    if event.key == pygame.K_r and game_over:
                        return executar(tela, menu)

            # Atualizações
            teclas = pygame.key.get_pressed()
            rua.atualizar(config["velocidade"])
            grupo_personagens.update(teclas)
            grupo_obstaculos.update()

            # Gera obstáculos
            obstaculo_timer += delta_time
            if obstaculo_timer > config["intervalo_obstaculos"]:
                lado = 'esquerda' if random.random() < 0.5 else 'direita'
                x = random.randint(50, 250) if lado == 'esquerda' else random.randint(550, 750)
                obstaculo = Obstaculo(random.choice(['poste', 'buraco', 'lixo']), x, -100, rua)
                grupo_obstaculos.add(obstaculo)
                obstaculo_timer = 0

            # Gera pílulas
            pilula_timer += delta_time
            if pilula_timer > config["intervalo_pilula"]:
                pilulas.append(Pilula(random.randint(50, 750), -100))
                pilula_timer = 0

            # Atualiza pílulas e verifica colisões
            for pilula in pilulas[:]:
                pilula.atualizar()
                if pilula.pos_Y > 600:
                    pilulas.remove(pilula)
                elif personagem.rect.colliderect(pilula.rect):
                    personagem.aplicar_efeito_pilula()
                    pontuacao += 60  # Adiciona 60 pontos por pílula coletada
                    pilulas.remove(pilula)

            # Sistema do carro
            if rua.visible and carro is None:
                carro = Carro(100, rua.y_pos + 20, config["velocidade"])
            if carro:
                carro.atualizar()
                if carro.pos_X + carro.largura < 0 or not rua.visible:
                    carro = None
                elif personagem.rect.colliderect(pygame.Rect(carro.pos_X, carro.pos_Y, carro.largura, carro.altura)):
                    game_over = True

            # Verifica colisões com obstáculos
            for obstaculo in grupo_obstaculos:
                if personagem.rect.colliderect(obstaculo.rect):
                    if obstaculo.tipo == 'buraco':
                        game_over = True
                    else:
                        personagem.velocidade = 2
                        personagem.lento_timer = pygame.time.get_ticks()

            # Desenho
            tela.fill(config["cor_fundo"])
            rua.desenhar(tela)
            grupo_obstaculos.draw(tela)
            grupo_personagens.draw(tela)
            if carro: carro.desenhar(tela)
            for pilula in pilulas: pilula.desenhar(tela)

            # UI - Informações na tela
            fonte = pygame.font.SysFont("Arial", 24)
            tela.blit(fonte.render(f"Tempo: {tempo_restante}s", True, (0, 0, 0)), (20, 20))
            tela.blit(fonte.render(f"Pontos: {pontuacao}", True, (0, 0, 0)), (20, 50))  # Mostra pontos
            
            if personagem.controles_invertidos:
                t_efeito = max(0, (personagem.efeito_timer - pygame.time.get_ticks()) // 1000)
                tela.blit(fonte.render(f"Efeito: {t_efeito}s", True, (255, 255, 0)), (20, 80))

        else:
            # Tela de Game Over
            for event in pygame.event.get():
                if event.type == pygame.QUIT: running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r: return executar(tela, menu)
                    if event.key == pygame.K_ESCAPE: return True

            tela.fill((0, 0, 0))
            fonte = pygame.font.SysFont("Arial", 40)
            tela.blit(fonte.render("GAME OVER - Pressione R para reiniciar", True, (255, 0, 0)), (100, 300))
            # Mostra pontuação final no game over
            fonte_pontos = pygame.font.SysFont("Arial", 36)
            tela.blit(fonte_pontos.render(f"Pontuação final: {pontuacao}", True, (255, 255, 255)), (250, 350))

        pygame.display.flip()
        clock.tick(60)
    
    return False