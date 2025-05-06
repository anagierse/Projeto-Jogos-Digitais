import pygame
import random
from cenario.rua import Rua
from personagens.Personagem import Personagem1
from cenario.obstaculos import Obstaculo

def main():
    pygame.init()
    
    tela_largura, tela_altura = 800, 600
    display = pygame.display.set_mode((tela_largura, tela_altura))
    pygame.display.set_caption("Jogo de Corrida")

    cor_fundo = (165, 219,142) 
    rua = Rua(tela_largura)
    personagem = Personagem1(tela_largura // 2, tela_altura // 2)

    grupo_personagens = pygame.sprite.Group(personagem)
    grupo_obstaculos = pygame.sprite.Group()

    clock = pygame.time.Clock()
    velocidade = 3
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        teclas = pygame.key.get_pressed()
        
        # Atualizações
        rua.atualizar(velocidade)
        grupo_personagens.update(teclas)
        grupo_obstaculos.update()

        if random.random() < 0.02:  
            tipo = random.choice(['poste', 'buraco'])
            x = random.randint(50, tela_largura - 50)
            obstaculo = Obstaculo(tipo, x, -50)
            grupo_obstaculos.add(obstaculo)

        
        display.fill(cor_fundo)
        rua.desenhar(display)
        grupo_obstaculos.draw(display)
        grupo_personagens.draw(display)
        
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()