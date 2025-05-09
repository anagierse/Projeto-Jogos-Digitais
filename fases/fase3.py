import pygame
import random
from cenario.rua import Rua
from personagens.Personagem import Personagem1
from cenario.obstaculos import Obstaculo

def executar(tela):
    config = {
        "velocidade": 7,
        "intervalo_obstaculos": 800,
        "cor_fundo": (219, 142, 165)
    }
    
    rua = Rua(800, 600)
    personagem = Personagem1(400, 300)
    grupo_personagens = pygame.sprite.Group(personagem)
    grupo_obstaculos = pygame.sprite.Group()
    
    clock = pygame.time.Clock()
    obstaculo_timer = 0
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return True

        obstaculo_timer += clock.get_time()
        if obstaculo_timer > config["intervalo_obstaculos"]:  
            tipo = random.choice(['poste', 'buraco', 'lixo', 'carro'])
            
            # Spawn apenas nas laterais
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

        tela.fill(config["cor_fundo"])
        rua.desenhar(tela)
        grupo_obstaculos.draw(tela)
        grupo_personagens.draw(tela)
        
        pygame.display.flip()
        clock.tick(60)