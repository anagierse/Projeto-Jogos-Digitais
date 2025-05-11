import pygame
import random
from cenario.rua import Rua
from personagens.Personagem import Personagem1
from cenario.obstaculos import Obstaculo  # Importando a classe Obstaculo

def main():
    pygame.init()
    

    tela_largura, tela_altura = 800, 600
    display = pygame.display.set_mode((tela_largura, tela_altura))
    pygame.display.set_caption("Jogo com Obstáculos")

    cor_fundo = (165, 219, 142)

    # Inicialização dos objetos
    rua = Rua(tela_largura, tela_altura)
    personagem1 = Personagem1(tela_largura // 2, tela_altura // 2)  # Posição inicial

    grupo_personagens = pygame.sprite.Group(personagem1)
    grupo_obstaculos = pygame.sprite.Group()  # Grupo de obstáculos

    clock = pygame.time.Clock()
    velocidade = 3
    running = True
    obstaculo_timer = 0  # Contador para gerar obstáculos de tempos em tempos

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        teclas = pygame.key.get_pressed()
        
        # Atualizando o movimento da rua e dos personagens
        rua.atualizar(velocidade)
        grupo_personagens.update(teclas)

        # Gerar obstáculos aleatórios a cada 1,5 segundos
        obstaculo_timer += clock.get_time()
        if obstaculo_timer > 1500:  # 1500 milissegundos = 1,5 segundos
            tipo = random.choice(['poste', 'buraco'])  # Escolhe aleatoriamente entre poste e buraco
            x = random.randint(50, tela_largura - 100)  # Posição horizontal aleatória
            obstaculo = Obstaculo(tipo, x, -100)  # A posição inicial é fora da tela
            grupo_obstaculos.add(obstaculo)  # Adiciona o obstáculo ao grupo
            obstaculo_timer = 0  # Reinicia o contador para o próximo obstáculo

        # Atualiza a posição dos obstáculos
        grupo_obstaculos.update()

        # Preenche a tela com a cor de fundo
        display.fill(cor_fundo)

        # Desenha os objetos na tela
        rua.desenhar(display)
        grupo_personagens.draw(display)
        grupo_obstaculos.draw(display)  # Desenha os obstáculos

        # Atualiza a tela
        pygame.display.flip()

        # Define a taxa de atualização (FPS)
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
