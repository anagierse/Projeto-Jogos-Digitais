import pygame
from menu.menu import Menu
from fases import fase1, fase2, fase3

def main():
    pygame.init()
    tela = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Meu Jogo")
    clock = pygame.time.Clock()

    menu = Menu(tela)
    fases = {
        "Fase 1": fase1.executar,
        "Fase 2": fase2.executar,
        "Fase 3": fase3.executar
    }

    while True:
        escolha = menu.executar()
        
        if escolha == "Sair":
            pygame.quit()
            return
            
        if escolha in fases:
            resultado = fases[escolha](tela, menu)  
            if resultado:  
                print(f"Você ganhou 50 pontos")

if __name__ == "__main__":
    main()