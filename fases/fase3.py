import pygame
import random
from cenario.rua import Rua
from personagens.Personagem import Personagem3
from cenario.obstaculos import Obstaculo

def executar(tela, menu =None):
    config = {
        "velocidade": 7,
        "intervalo_obstaculos": 800,
        "cor_fundo": (219, 142, 165)
    }
    
    TEMPO_FASE = 2 * 60
    tempo_inicio = pygame.time.get_ticks()  # Inicializa o timer corretamente
    pontos_ja_adicionados = False

    try:
        game_over_img = pygame.image.load("menu/imagens/gameover.png").convert_alpha()
        game_over_img = pygame.transform.scale(game_over_img, (800, 600))
    except:
        game_over_img = None
    game_over = False

    rua = Rua(800, 600)
    personagem = Personagem3(400, 300)
    grupo_personagens = pygame.sprite.Group(personagem)
    grupo_obstaculos = pygame.sprite.Group()
    
    clock = pygame.time.Clock()
    obstaculo_timer = 0
    running = True

    while running:
        if not game_over:
            tempo_decorrido = (pygame.time.get_ticks() - tempo_inicio) // 1000
            tempo_restante = max(0, TEMPO_FASE - tempo_decorrido)

            if tempo_restante <= 0 and not pontos_ja_adicionados and menu:
                menu.adicionar_pontos(50)
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

            obstaculo_timer += clock.get_time()
            if obstaculo_timer > config["intervalo_obstaculos"]:  
                tipo = random.choice(['poste', 'buraco', 'lixo', 'carro'])
                
                lado = random.choice(['esquerda', 'direita'])
                x = random.randint(50, 250) if lado == 'esquerda' else random.randint(550, 750)
                
                obstaculo = Obstaculo(tipo, x, -100, rua)
                
                if not any(obstaculo.rect.colliderect(o.rect) for o in grupo_obstaculos):
                    grupo_obstaculos.add(obstaculo)
                    obstaculo_timer = 0

            teclas = pygame.key.get_pressed()
            rua.atualizar(config["velocidade"])
            grupo_personagens.update(teclas)
            grupo_obstaculos.update()

            tela.fill(config["cor_fundo"])
            rua.desenhar(tela)
            grupo_obstaculos.draw(tela)
            grupo_personagens.draw(tela)
            
            fonte_tempo = pygame.font.SysFont("Arial", 24)
            texto_tempo = fonte_tempo.render(f"Tempo: {tempo_restante}s", True, (0, 0, 0))
            tela.blit(texto_tempo, (20, 20))
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