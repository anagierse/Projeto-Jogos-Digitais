import pygame
import random
from cenario.rua import Rua
from personagens.Personagem import Personagem3, Vilao2
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
        "perda_maquina": 5
    }
    
    TEMPO_FASE = 2 * 5
    tempo_inicio = pygame.time.get_ticks()
    pontos_ja_adicionados = False
    pontuacao = 0
    game_over = False

    # Sistema de Game Over
    try:
        game_over_img = pygame.image.load("menu/imagens/gameover.png").convert_alpha()
        game_over_img = pygame.transform.scale(game_over_img, (800, 600))
    except:
        game_over_img = None

    # Inicialização de objetos
    rua = Rua(800, 600)
    personagem = Personagem3(400, 300)
    vilao2 = Vilao2(700, 100)
    carro = None
    dinheiros = []
    maquinas = []
    dinheiro_timer = 0
    maquina_timer = 0

    # Grupos de sprites
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
            # Verificação de término do tempo
            if tempo_restante <= 0 and not pontos_ja_adicionados and menu:
                menu.adicionar_pontos(50 + pontuacao)
                pontos_ja_adicionados = True
                return True
            
            # Tratamento de eventos
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

            # Verificação se saiu da tela
            if personagem.rect.bottom >= 600:
                game_over = True

            # Atualizações de tempo
            obstaculo_timer += delta_time
            dinheiro_timer += delta_time
            maquina_timer += delta_time

            # Geração de obstáculos
            if obstaculo_timer > config["intervalo_obstaculos"]:
                tipo = random.choice(['poste', 'buraco', 'lixo'])
                lado = random.choice(['esquerda', 'direita'])
                x = random.randint(50, 250) if lado == 'esquerda' else random.randint(550, 750)
                obstaculo = Obstaculo(tipo, x, -100, rua)
                
                if not any(obstaculo.rect.colliderect(o.rect) for o in grupo_obstaculos):
                    grupo_obstaculos.add(obstaculo)
                    obstaculo_timer = 0

            # Geração de dinheiro
            if dinheiro_timer > config["intervalo_dinheiro"]:
                x_pos = random.randint(50, 750)
                dinheiros.append(Dinheiro(x_pos, -100))
                dinheiro_timer = 0

            # Geração de máquinas
            if maquina_timer > config["intervalo_maquina"]:
                x_pos = random.randint(50, 750)
                maquinas.append(Maquina(x_pos, -100))
                maquina_timer = 0

            # Atualização de objetos
            teclas = pygame.key.get_pressed()
            rua.atualizar(config["velocidade"])
            grupo_personagens.update(teclas)
            grupo_obstaculos.update()
            vilao2.update(personagem)

            # Atualização de carro
            if rua.visible and carro is None:
                carro = Carro(100, rua.y_pos + 20, config["velocidade"])

            if carro:
                carro.atualizar()
                if carro.pos_X + carro.largura < 0 or not rua.visible:
                    carro = None
                if carro and personagem.rect.colliderect(
                    pygame.Rect(carro.pos_X, carro.pos_Y, carro.largura, carro.altura).inflate(-75, -75)):
                    game_over = True

            # Atualização de dinheiros
            for dinheiro in dinheiros[:]:
                dinheiro.atualizar()
                if dinheiro.pos_Y > 600:
                    dinheiros.remove(dinheiro)
                elif personagem.rect.colliderect(dinheiro.rect):
                    pontuacao += 5
                    dinheiros.remove(dinheiro)

            # Atualização de máquinas
            for maquina in maquinas[:]:
                maquina.atualizar()
                if maquina.pos_Y > 600:
                    maquinas.remove(maquina)
                elif personagem.rect.colliderect(maquina.rect):
                    pontuacao -= config["perda_maquina"]
                    maquinas.remove(maquina)
                    
            # Verificação de colisões com agiota        
            zona_colisao = personagem.rect.inflate(-65, -65)
            if vilao2.rect.colliderect(zona_colisao):
                game_over = True

            # Verificação de colisões com obstáculos
            for obstaculo in grupo_obstaculos:
                if personagem.rect.colliderect(obstaculo.rect):
                    if obstaculo.tipo == 'buraco':
                        game_over = True
                    else:
                        personagem.velocidade = 3
                        personagem.lento_timer = pygame.time.get_ticks()

            # Restaura velocidade
            if personagem.lento_timer and pygame.time.get_ticks() - personagem.lento_timer > 1000:
                personagem.velocidade = 7
                personagem.lento_timer = 0

            # Renderização
            tela.fill(config["cor_fundo"])
            rua.desenhar(tela)
            vilao2.desenhar(tela)
            grupo_obstaculos.draw(tela)
            grupo_personagens.draw(tela)
            
            for dinheiro in dinheiros:
                dinheiro.desenhar(tela)
            for maquina in maquinas:
                maquina.desenhar(tela)
            if carro:
                carro.desenhar(tela)

            # UI
            fonte = pygame.font.SysFont("Arial", 24)
            tela.blit(fonte.render(f"Tempo: {tempo_restante}s", True, (0, 0, 0)), (20, 20))
            
            cor_dinheiro = (255, 0, 0) if pontuacao < 0 else (0, 128, 0)
            tela.blit(fonte.render(f"Dinheiro: ${pontuacao}", True, cor_dinheiro), (20, 50))
            
        else:
            # Tela de Game Over
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        return executar(tela, menu)
                    if event.key == pygame.K_ESCAPE:
                        if menu:
                            menu.adicionar_pontos(pontuacao)
                        return True

            if game_over_img:
                tela.blit(game_over_img, (0, 0))
            else:
                tela.fill((0, 0, 0))
                fonte = pygame.font.SysFont("Arial", 40)
                tela.blit(fonte.render("GAME OVER - Pressione R para reiniciar", True, (255, 0, 0)), (100, 300))
                fonte_pontos = pygame.font.SysFont("Arial", 36)
                tela.blit(fonte_pontos.render(f"Pontuação final: {pontuacao}", True, (255, 255, 255)), (250, 350))

        pygame.display.flip()
        clock.tick(60)
    
    return False
