import pygame
from menu.menu import Menu
from fases import fase1, fase2, fase3

def main():
    pygame.init()
    tela = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Life Snake")
    clock = pygame.time.Clock()

    # Cria uma instância do menu principal
    menu = Menu(tela)
    # Dicionário que associa o nome das fases às funções que executam cada fase
    fases = {
        "Fase 1": fase1.executar,
        "Fase 2": fase2.executar,
        "Fase 3": fase3.executar
    }

    # Loop principal do jogo — permanece no menu até o jogador sair
    while True:
        # Executa o menu e obtém a escolha do jogador (ex: "Fase 1", "Sair")
        escolha = menu.executar()
        
        # Se o jogador escolher sair, fecha o jogo corretamente
        if escolha == "Sair":
            pygame.quit()
            return
        # Se a escolha for uma das fases disponíveis    
        if escolha in fases:
            # Executa a fase correspondente, passando a tela e o menu
            resultado = fases[escolha](tela, menu)  
            # Se a fase retornar sucesso (por exemplo, o jogador venceu)
            if resultado:  
                print(f"Você ganhou 50 pontos")

if __name__ == "__main__":
    main()