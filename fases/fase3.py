import pygame
import random
from cenario.rua import Rua
from personagens.Personagem import Personagem3
from cenario.obstaculos import Obstaculo
from cenario.coletaveis import Dinheiro, Maquina
from cenario.carro import Carro

def executar(tela, menu=None):
    config = {
        "velocidade": 5,
        "intervalo_obstaculos": 800,
        "cor_fundo": (219, 142, 165),
        "intervalo_dinheiro": 4000,
        "intervalo_maquina": 6000,
        "velocidade_dinheiro": 3,
        "velocidade_maquina": 3,
        "perda_maquina": 15  # Alterado de 15 para 5 (agora é pontuação negativa)
    }
    
    TEMPO_FASE = 2 * 60
    tempo_inicio = pygame.time.get_ticks()
    pontos_ja_adicionados = False
    pontuacao = 0
    game_over = False

    rua = Rua(800, 600)
    personagem = Personagem3(400, 300)
    carro = None
    dinheiros = []
    maquinas = []
    dinheiro_timer = 0
    maquina_timer = 0

    grupo_personagens = pygame.sprite.Group(personagem)
    grupo_obstaculos = pygame.sprite.Group()

    clock = pygame.time.Clock()
    running = True
    obstaculo_timer = 0

    while running:
        delta_time = clock.get_time()
        tempo_decorrido = (pygame.time.get_ticks() - tempo_inicio) // 1000
        tempo_restante = max(0, TEMPO_FASE - tempo_decorrido)
        
        if not game_over:
            if tempo_restante <= 0 and not pontos_ja_adicionados and menu:
                menu.adicionar_pontos(50 + pontuacao)
                pontos_ja_adicionados = True
                return True
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    if menu:
                        menu.adicionar_pontos(pontuacao)
                    return False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if menu:
                            menu.adicionar_pontos(pontuacao)
                        return True
                    if event.key == pygame.K_r and game_over:
                        return executar(tela, menu)

            obstaculo_timer += delta_time
            dinheiro_timer += delta_time
            maquina_timer += delta_time

            if obstaculo_timer > config["intervalo_obstaculos"]:
                tipo = random.choice(['poste', 'buraco', 'lixo'])
                lado = random.choice(['esquerda', 'direita'])
                x = random.randint(50, 250) if lado == 'esquerda' else random.randint(550, 750)
                obstaculo = Obstaculo(tipo, x, -100, rua)
                
                if not any(obstaculo.rect.colliderect(o.rect) for o in grupo_obstaculos):
                    grupo_obstaculos.add(obstaculo)
                    obstaculo_timer = 0

            if dinheiro_timer > config["intervalo_dinheiro"]:
                x_pos = random.randint(50, 750)
                dinheiros.append(Dinheiro(x_pos, -100))
                dinheiro_timer = 0

            if maquina_timer > config["intervalo_maquina"]:
                x_pos = random.randint(50, 750)
                maquinas.append(Maquina(x_pos, -100))
                maquina_timer = 0

            teclas = pygame.key.get_pressed()
            rua.atualizar(config["velocidade"])
            grupo_personagens.update(teclas)
            grupo_obstaculos.update()

            if rua.visible and carro is None:
                carro = Carro(100, rua.y_pos + 20, config["velocidade"])

            if carro:
                carro.atualizar()
                if carro.pos_X + carro.largura < 0 or not rua.visible:
                    carro = None
                if carro and personagem.rect.colliderect(pygame.Rect(carro.pos_X, carro.pos_Y, carro.largura, carro.altura)):
                    if menu:
                        menu.adicionar_pontos(pontuacao)
                    game_over = True

            for dinheiro in dinheiros[:]:
                dinheiro.atualizar()
                if dinheiro.pos_Y > 600:
                    dinheiros.remove(dinheiro)
                elif personagem.rect.colliderect(dinheiro.rect):
                    pontuacao += 5  # Alterado de 60 para 5
                    dinheiros.remove(dinheiro)

            for maquina in maquinas[:]:
                maquina.atualizar()
                if maquina.pos_Y > 600:
                    maquinas.remove(maquina)
                elif personagem.rect.colliderect(maquina.rect):
                    pontuacao -= config["perda_maquina"]
                    maquinas.remove(maquina)

            for obstaculo in grupo_obstaculos:
                if personagem.rect.colliderect(obstaculo.rect):
                    if obstaculo.tipo == 'buraco':
                        if menu:
                            menu.adicionar_pontos(pontuacao)
                        game_over = True
                    else:
                        personagem.velocidade = 3
                        personagem.lento_timer = pygame.time.get_ticks()

            if personagem.lento_timer and pygame.time.get_ticks() - personagem.lento_timer > 1000:
                personagem.velocidade = 7
                personagem.lento_timer = 0

            tela.fill(config["cor_fundo"])
            rua.desenhar(tela)
            grupo_obstaculos.draw(tela)
            grupo_personagens.draw(tela)
            
            for dinheiro in dinheiros:
                dinheiro.desenhar(tela)
            for maquina in maquinas:
                maquina.desenhar(tela)
            if carro:
                carro.desenhar(tela)

            fonte = pygame.font.SysFont("Arial", 24)
            tela.blit(fonte.render(f"Tempo: {tempo_restante}s", True, (0, 0, 0)), (20, 20))
            
            cor_dinheiro = (255, 0, 0) if pontuacao < 0 else (0, 128, 0)
            tela.blit(fonte.render(f"Dinheiro: ${pontuacao}", True, cor_dinheiro), (20, 50))
            
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        return executar(tela, menu)
                    if event.key == pygame.K_ESCAPE:
                        return True

            try:
                game_over_img = pygame.image.load("menu/imagens/gameover.png").convert_alpha()
                game_over_img = pygame.transform.scale(game_over_img, (800, 600))
                tela.blit(game_over_img, (0, 0))
            except:
                tela.fill((0, 0, 0))
                fonte = pygame.font.SysFont("Arial", 40)
                tela.blit(fonte.render("GAME OVER - Pressione R para reiniciar", True, (255, 0, 0)), (100, 300))

        pygame.display.flip()
        clock.tick(60)
    
    return False