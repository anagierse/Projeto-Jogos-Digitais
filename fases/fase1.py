import pygame
import random
from cenario.rua import Rua
from personagens.Personagem import Personagem1, Vilao
from cenario.obstaculos import Obstaculo
from cenario.coletaveis import Pirulito
from cenario.carro import Carro

def executar(tela, menu=None):
    config = {
        "velocidade": 3,
        "intervalo_obstaculos": 1500,
        "cor_fundo": (165, 219, 142),
        "velocidade_pirulito": 3  # Velocidade de queda do pirulito
    }
    TEMPO_FASE = 2 * 60
    tempo_inicio = pygame.time.get_ticks()
    pontos_ja_adicionados = False
    pontuacao = 0

    # Sistema de Game Over
    try:
        game_over_img = pygame.image.load("menu/imagens/gameover.png").convert_alpha()
        game_over_img = pygame.transform.scale(game_over_img, (800, 600))
    except:
        game_over_img = None
    game_over = False

    rua = Rua(800, 600)
    personagem = Personagem1(400, 300)
    vilao = Vilao(600, 400)
    carro = None
    
    # Sistema de pirulitos
    pirulitos = []  # Lista para armazenar múltiplos pirulitos
    pirulito_timer = 0
    intervalo_pirulito = 3000  # Aparece a cada 3 segundos

    grupo_personagens = pygame.sprite.Group(personagem)
    grupo_viloes = pygame.sprite.Group(vilao)
    grupo_obstaculos = pygame.sprite.Group()
    
    clock = pygame.time.Clock()
    obstaculo_timer = 0
    running = True

    while running:
        if not game_over:
            delta_time = clock.get_time()
            tempo_decorrido = (pygame.time.get_ticks() - tempo_inicio) // 1000
            tempo_restante = max(0, TEMPO_FASE - tempo_decorrido)

            if tempo_restante <= 0 and not pontos_ja_adicionados and menu:
                # Adiciona os pontos dos pirulitos + 50 pontos por completar a fase
                pontuacao_total = pontuacao + 50
                menu.adicionar_pontos(pontuacao_total)  # Agora envia a pontuação total
                pontos_ja_adicionados = True
                return True
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return True
                    if event.key == pygame.K_r and game_over:
                        return executar(tela, menu)

            obstaculo_timer += delta_time
            pirulito_timer += delta_time
            
            # Geração de obstáculos
            if obstaculo_timer > config["intervalo_obstaculos"]:
                tipo = random.choice(['poste', 'buraco', 'lixo'])
                x = random.randint(50, 750)
                obstaculo = Obstaculo(tipo, x, -100, rua)
                grupo_obstaculos.add(obstaculo)
                obstaculo_timer = 0

            # Geração de pirulitos
            if pirulito_timer > intervalo_pirulito:
                x_pos = random.randint(50, 750)
                novo_pirulito = Pirulito(x_pos, -100)
                pirulitos.append(novo_pirulito)
                pirulito_timer = 0

            # Atualização de pirulitos
            for pirulito in pirulitos[:]:  # Usamos [:] para criar uma cópia da lista
                pirulito.pos_Y += config["velocidade_pirulito"]
                pirulito.rect.y = pirulito.pos_Y
                pirulito.atualizar()
                # Verifica se saiu da tela
                if pirulito.pos_Y > 600:
                    pirulitos.remove(pirulito)
                # Verifica colisão com personagem
                elif personagem.rect.colliderect(pirulito.rect):
                    pontuacao += 60
                    pirulitos.remove(pirulito)

            teclas = pygame.key.get_pressed()
            rua.atualizar(config["velocidade"])
            grupo_personagens.update(teclas)
            grupo_obstaculos.update()
            vilao.update(personagem)

            # Verificação se saiu da tela pela parte de baixo
            if personagem.rect.bottom >= 600:
                game_over = True

            # Sistema do carro
            if rua.visible and carro is None:
                carro = Carro(100, rua.y_pos + 20, config["velocidade"])

            if carro:
                carro.atualizar()
                if carro.pos_X + carro.largura < 0 or not rua.visible:
                    carro = None
                if carro and personagem.rect.colliderect(pygame.Rect(carro.pos_X, carro.pos_Y, carro.largura, carro.altura)):
                    game_over = True

            # Verificação de colisões com obstáculos
            for obstaculo in grupo_obstaculos:
                if obstaculo.tipo == 'buraco' and personagem.rect.colliderect(obstaculo.rect):
                    game_over = True
                elif obstaculo.tipo in ['poste', 'lixo'] and personagem.rect.colliderect(obstaculo.rect):
                    personagem.velocidade = 1
                    personagem.lento_timer = pygame.time.get_ticks()

            if personagem.lento_timer and pygame.time.get_ticks() - personagem.lento_timer > 1000:
                personagem.velocidade = 3
                personagem.lento_timer = 0

            # Desenho de tudo
            tela.fill(config["cor_fundo"])
            rua.desenhar(tela)
            grupo_obstaculos.draw(tela)
            grupo_personagens.draw(tela)
            vilao.desenhar(tela)

            if carro:
                carro.desenhar(tela)

            for pirulito in pirulitos:
                pirulito.desenhar(tela)

            # Verificação de colisão com vilão
            zona_colisao = personagem.rect.inflate(-50, -50)
            if vilao.rect.colliderect(zona_colisao):
                game_over = True
            
            # Mostra informações na tela
            fonte_tempo = pygame.font.SysFont("Arial", 24)
            texto_tempo = fonte_tempo.render(f"Tempo: {tempo_restante}s", True, (0, 0, 0))
            tela.blit(texto_tempo, (20, 20))

            fonte_pontos = pygame.font.SysFont(None, 36)
            texto_pontos = fonte_pontos.render(f"Pirulitos: {pontuacao}", True, (0, 0, 0))
            tela.blit(texto_pontos, (20, 50))
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:  # Reiniciar
                        return executar(tela, menu)
                    if event.key == pygame.K_ESCAPE:  # Voltar ao menu
                        return True

            if game_over_img:
                tela.blit(game_over_img, (0, 0))
            else:
                tela.fill((0, 0, 0))
                fonte = pygame.font.SysFont("Arial", 40)
                texto = fonte.render("GAME OVER - Pressione R para reiniciar", True, (255, 0, 0))
                tela.blit(texto, (100, 300))

        pygame.display.flip()
        clock.tick(60)
    
    return False