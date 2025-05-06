import pygame
import random
from menu.menu import Menu
from cenario.rua import Rua
from personagens.Personagem import Personagem1
from cenario.obstaculos import Obstaculo

def iniciar_jogo(display, fase):
    cor_fundo = (165, 219, 142)
    rua = Rua(800, 600)
    personagem1 = Personagem1(400, 300)
    
    grupo_personagens = pygame.sprite.Group(personagem1)
    grupo_obstaculos = pygame.sprite.Group()
    
    clock = pygame.time.Clock()
    velocidade = 3
    obstaculo_timer = 0
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return True 

   
        obstaculo_timer += clock.get_time()
        if obstaculo_timer > 1500:  
            tipo = random.choice(['poste', 'buraco'])
            x = random.randint(50, 750)
            obstaculo = Obstaculo(tipo, x, -100)
            grupo_obstaculos.add(obstaculo)
            obstaculo_timer = 0

        teclas = pygame.key.get_pressed()
        rua.atualizar(velocidade)
        grupo_personagens.update(teclas)
        grupo_obstaculos.update()

        # Renderização
        display.fill(cor_fundo)
        rua.desenhar(display)
        grupo_obstaculos.draw(display)
        grupo_personagens.draw(display)
        
        pygame.display.flip()
        clock.tick(60)

    return False

def main():
    pygame.init()
    tela = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Menu Principal")
    clock = pygame.time.Clock()

    menu = Menu(tela)

    while True:
        no_menu = True
        while no_menu:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                
                escolha = menu.navegar(event)
                if escolha in ["Fase 1", "Fase 2", "Fase 3"]:
                    no_menu = False

            menu.desenhar()
            pygame.display.flip()
            clock.tick(30)

        retornar_ao_menu = iniciar_jogo(tela, escolha)
        
        if not retornar_ao_menu:
            break  

if __name__ == "__main__":
    main()