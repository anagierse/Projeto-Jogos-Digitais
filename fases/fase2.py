import pygame
import random
from cenario.rua import Rua
from personagens.Personagem import Personagem2, Vilao
from cenario.obstaculos import Obstaculo

def executar(tela):
    config = {
        "velocidade": 5,
        "intervalo_obstaculos": 1000,
        "cor_fundo": (142, 165, 219)
    }

    rua = Rua(800, 600)
    personagem = Personagem2(400, 300)
    vilao = Vilao(600, 400)

    grupo_personagens = pygame.sprite.Group(personagem)
    grupo_viloes = pygame.sprite.Group(vilao)
    grupo_obstaculos = pygame.sprite.Group()

    clock = pygame.time.Clock()
    obstaculo_timer = 0
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return True

        obstaculo_timer += clock.get_time()
        if obstaculo_timer > config["intervalo_obstaculos"]:
            tipo = random.choice(['poste', 'buraco', 'lixo'])
            
            # Spawn apenas nas laterais (fora da zona da rua)
            lado = random.choice(['esquerda', 'direita'])
            x = random.randint(50, 250) if lado == 'esquerda' else random.randint(550, 750)
            
            obstaculo = Obstaculo(tipo, x, -100, rua)

            # Verifica colisão com outros obstáculos
            if not any(obstaculo.rect.colliderect(o.rect) for o in grupo_obstaculos):
                grupo_obstaculos.add(obstaculo)
                obstaculo_timer = 0

        teclas = pygame.key.get_pressed()
        rua.atualizar(config["velocidade"])
        grupo_personagens.update(teclas)
        grupo_obstaculos.update()
        vilao.update(personagem)

        for obstaculo in grupo_obstaculos:
            if obstaculo.tipo == 'buraco' and personagem.rect.colliderect(obstaculo.rect):
                grupo_personagens.remove(personagem)
            elif obstaculo.tipo in ['poste', 'lixo'] and personagem.rect.colliderect(obstaculo.rect):
                personagem.velocidade = 2
                personagem.lento_timer = pygame.time.get_ticks()

        if personagem.lento_timer and pygame.time.get_ticks() - personagem.lento_timer > 1000:
            personagem.velocidade = 5
            personagem.lento_timer = 0

        tela.fill(config["cor_fundo"])
        rua.desenhar(tela)
        grupo_obstaculos.draw(tela)
        grupo_personagens.draw(tela)
        vilao.desenhar(tela)

        zona_colisao = personagem.rect.inflate(-50, -50)
        if vilao.rect.colliderect(zona_colisao):
            return False

        pygame.display.flip()
        clock.tick(60)
