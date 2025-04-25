import pygame
from cenario.rua import Rua
from Personagens.Personagem import Personagem

def main():
    pygame.init()
    
    tela_largura, tela_altura = 800, 600
    display = pygame.display.set_mode((tela_largura, tela_altura))
    
    cor_fundo = (165, 219, 142)
    rua = Rua(tela_largura, tela_altura)
    personagem = Personagem(tela_largura // 2, tela_altura  //2)  # Posição inicial

    clock = pygame.time.Clock()
    
    velocidade = 3  
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
        teclas = pygame.key.get_pressed()

        
        rua.atualizar(velocidade)
        personagem.mover(teclas)

        
        display.fill(cor_fundo)
        rua.desenhar(display)
        personagem.desenhar(display)

        pygame.display.flip()
        
        clock.tick(60) 
    
    pygame.quit()

if __name__ == "__main__":
    main()