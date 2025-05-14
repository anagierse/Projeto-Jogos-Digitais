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
        "intervalo_pilula": 7000,
        "limite_pilulas_para_inverter": 3,
        "bonus_velocidade_por_pilula": 1,
        "velocidade_maxima": 8
    }
    TEMPO_FASE = 2 * 60
    tempo_inicio = pygame.time.get_ticks()
    pontos_ja_adicionados = False
    game_over = False
    pontuacao = 0
    contador_pilulas = 0

    # Sistema de Game Over
    try:
        game_over_img = pygame.image.load("menu/imagens/gameover.png").convert_alpha()
        game_over_img = pygame.transform.scale(game_over_img, (800, 600))
    except:
        game_over_img = None

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
            
            if tempo_restante <= 0 and not pontos_ja_adicionados and menu:
                pontuacao_total = pontuacao + 50
                menu.adicionar_pontos(pontuacao_total)
                pontos_ja_adicionados = True
                return True
            
            # Eventos
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

            # Atualizações
            teclas = pygame.key.get_pressed()
            rua.atualizar(config["velocidade"])
            grupo_personagens.update(teclas)
            grupo_obstaculos.update()

            # Verificação se saiu da tela
            if personagem.rect.bottom >= 600:
                game_over = True

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
                    contador_pilulas += 1
                    pontuacao += 5
                    
                    # Aplica efeitos graduais
                    if contador_pilulas <= config["limite_pilulas_para_inverter"]:
                        nova_velocidade = min(
                            config["velocidade_maxima"],
                            personagem.velocidade_padrao + 
                            (contador_pilulas * config["bonus_velocidade_por_pilula"])
                        )
                        personagem.velocidade = nova_velocidade
                    else:
                        personagem.aplicar_efeito_pilula()
                        
                    pilulas.remove(pilula)

            # Sistema do carro
            if rua.visible and carro is None:
                carro = Carro(100, rua.y_pos + 20, config["velocidade"])
            if carro:
                carro.atualizar()
                if carro.pos_X + carro.largura < 0 or not rua.visible:
                    carro = None
                elif personagem.rect.colliderect(
                    pygame.Rect(carro.pos_X, carro.pos_Y, carro.largura, carro.altura).inflate(75, 75)):                    
                if menu:
                        menu.adicionar_pontos(pontuacao)
                    game_over = True

            # Verifica colisões com obstáculos
            for obstaculo in grupo_obstaculos:
                if personagem.rect.colliderect(obstaculo.rect):
                    if obstaculo.tipo == 'buraco':
                        if menu:
                            menu.adicionar_pontos(pontuacao)
                        game_over = True
                    else:
                        personagem.velocidade = max(1, personagem.velocidade_padrao - 2)
                        personagem.lento_timer = pygame.time.get_ticks() + 1000

            # Verifica se o efeito de redução de velocidade acabou
            if not personagem.controles_invertidos and personagem.lento_timer and pygame.time.get_ticks() > personagem.lento_timer:
                personagem.velocidade = personagem.velocidade_padrao + (
                    min(contador_pilulas, config["limite_pilulas_para_inverter"]) * 
                    config["bonus_velocidade_por_pilula"]
                )
                personagem.lento_timer = 0

            # Desenho
            tela.fill(config["cor_fundo"])
            rua.desenhar(tela)
            grupo_obstaculos.draw(tela)
            grupo_personagens.draw(tela)
            if carro: carro.desenhar(tela)
            for pilula in pilulas: pilula.desenhar(tela)

            # UI
            fonte = pygame.font.SysFont("Arial", 24)
            tela.blit(fonte.render(f"Tempo: {tempo_restante}s", True, (0, 0, 0)), (20, 20))
            tela.blit(fonte.render(f"Pontos: {pontuacao}", True, (0, 0, 0)), (20, 50))
            tela.blit(fonte.render(f"Pílulas: {contador_pilulas}", True, (0, 0, 0)), (20, 80))
            
            if personagem.controles_invertidos:
                t_efeito = max(0, (personagem.efeito_timer - pygame.time.get_ticks()) // 1000)
                tela.blit(fonte.render(f"Controles invertidos: {t_efeito}s", True, (255, 0, 0)), (20, 110))
            
            tela.blit(fonte.render(f"Velocidade: {personagem.velocidade}", True, (0, 0, 255)), (20, 140))

        else:
            # Tela de Game Over
            for event in pygame.event.get():
                if event.type == pygame.QUIT: running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r: return executar(tela, menu)
                    if event.key == pygame.K_ESCAPE: return True

            if game_over_img:
                tela.blit(game_over_img, (0, 0))
            else:
                tela.fill((0, 0, 0))
                fonte = pygame.font.SysFont("Arial", 40)
                tela.blit(fonte.render("GAME OVER - Pressione R para reiniciar", True, (255, 0, 0)), (100, 300))
                fonte_pontos = pygame.font.SysFont("Arial", 36)
                tela.blit(fonte_pontos.render(f"Pontuação final: {pontuacao}", True, (255, 255, 255)), (250, 350))
                tela.blit(fonte_pontos.render(f"Pílulas coletadas: {contador_pilulas}", True, (255, 255, 255)), (250, 400))

        pygame.display.flip()
        clock.tick(60)
    
    return False
