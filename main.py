import pygame
from cenario.rua import Rua

pygame.init()

tela_largura, tela_altura = 800, 600
display = pygame.display.set_mode((tela_largura, tela_altura))
cor_fundo = (165, 219, 142)

rua = Rua(tela_largura)
fps = pygame.time.Clock()

loop = True
while loop:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            loop = False  
            pygame.quit()  
            quit()  
    
    display.fill(cor_fundo)
    rua.desenhar(display)
    
    pygame.display.flip()
    fps.tick(60)