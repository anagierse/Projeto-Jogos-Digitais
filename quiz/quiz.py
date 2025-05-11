import pygame
import sys
import os

def executar_quiz():
    # Inicializa o pygame
    pygame.init()

    # Configurações da tela
    LARGURA, ALTURA = 800, 600
    tela = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("Quiz - Jornada da Vida")

    # Cores
    BRANCO = (255, 255, 255)
    PRETO = (0, 0, 0)
    VERDE = (0, 255, 0)
    VERMELHO = (255, 0, 0)
    AZUL = (0, 0, 255)
    CINZA = (200, 200, 200)

    # Caminho relativo para a imagem de fundo
    caminho_fundo = os.path.join('quiz', 'imgs', 'quiz.png')

    # Carrega a imagem de fundo
    try:
        fundo = pygame.image.load(caminho_fundo)
        fundo = pygame.transform.scale(fundo, (LARGURA, ALTURA))
    except:
        fundo = None
        print(f"Erro ao carregar imagem de fundo: {caminho_fundo}")

    # Fonte
    fonte = pygame.font.SysFont("Arial", 24)
    fonte_titulo = pygame.font.SysFont("Arial", 32, bold=True)

    # Perguntas e respostas
    perguntas = [
        {
            "pergunta": "1. O que o 'homem do saco' representa no jogo?",
            "opcoes": [
                "A) Um chefe final da fase",
                "B) Um obstáculo aleatório sem significado",
                "C) O perigo de falar com estranhos",
                "D) Um personagem engraçado"
            ],
            "correta": 2,
            "explicacao": "O 'homem do saco' representa o perigo de falar com estranhos, uma lição importante na infância."
        },
        {
            "pergunta": "2. Por que coletar doces é importante na fase da infância?",
            "opcoes": [
                "A) Eles são só decorativos",
                "B) Aumentam o tamanho do personagem",
                "C) Representam recompensas e afeto na infância",
                "D) Fazem o personagem correr mais rápido"
            ],
            "correta": 2,
            "explicacao": "Os doces representam as recompensas e o afeto que são importantes no desenvolvimento infantil."
        },
        {
            "pergunta": "3. O que acontece quando o personagem encosta em drogas na fase da adolescência?",
            "opcoes": [
                "A) Ele ganha poderes especiais",
                "B) Ele perde o controle, refletindo os efeitos negativos",
                "C) Nada muda",
                "D) Ele pula para a fase adulta"
            ],
            "correta": 1,
            "explicacao": "O personagem perde o controle, mostrando os efeitos negativos das drogas na adolescência."
        },
        {
            "pergunta": "4. Por que o jogador perde ao ser pego por um agiota?",
            "opcoes": [
                "A) Porque é parte do final secreto",
                "B) Para desbloquear uma nova fase",
                "C) Para mostrar os perigos das dívidas e apostas",
                "D) Porque o jogo tem um bug"
            ],
            "correta": 2,
            "explicacao": "Mostra os perigos reais de se envolver com dívidas e agiotas na vida adulta."
        },
        {
            "pergunta": "5. O que as máquinas de apostas fazem com o personagem?",
            "opcoes": [
                "A) Aumentam o dinheiro",
                "B) Reduzem o dinheiro, mostrando os riscos do vício",
                "C) Mudam a trilha sonora",
                "D) Fazem o personagem parar de se mover"
            ],
            "correta": 1,
            "explicacao": "As máquinas reduzem o dinheiro, ilustrando os riscos do vício em jogos de azar."
        },
        {
            "pergunta": "6. O que as fases do jogo representam?",
            "opcoes": [
                "A) Uma corrida maluca entre personagens",
                "B) Três estilos diferentes de jogabilidade",
                "C) Etapas da vida com desafios reais e sociais",
                "D) Um mundo fictício com inimigos e bônus aleatórios"
            ],
            "correta": 2,
            "explicacao": "As fases representam as diferentes etapas da vida, cada uma com seus desafios sociais reais."
        }
    ]

    # Variáveis
    pergunta_atual = 0
    resposta_selecionada = None
    feedback = ""
    acertos = 0
    mostrar_explicacao = False

    def desenhar_quiz():
        nonlocal pergunta_atual, resposta_selecionada, feedback, acertos, mostrar_explicacao
        if fundo:
            tela.blit(fundo, (0, 0))
        else:
            tela.fill(BRANCO)

        pergunta_texto = fonte.render(perguntas[pergunta_atual]["pergunta"], True, PRETO)
        tela.blit(pergunta_texto, (50, 100))

        for i, opcao in enumerate(perguntas[pergunta_atual]["opcoes"]):
            cor = AZUL if i == resposta_selecionada else PRETO
            opcao_texto = fonte.render(opcao, True, cor)
            tela.blit(opcao_texto, (50, 150 + i * 40))

            if feedback and i == perguntas[pergunta_atual]["correta"]:
                pygame.draw.rect(tela, VERDE, (30, 145 + i * 40, 750, 30), 2)

        if feedback:
            cor_feedback = VERDE if feedback == "Correto!" else VERMELHO
            feedback_texto = fonte.render(feedback, True, cor_feedback)
            tela.blit(feedback_texto, (50, 400))

            if mostrar_explicacao:
                explicacao_texto = fonte.render(perguntas[pergunta_atual]["explicacao"], True, PRETO)
                tela.blit(explicacao_texto, (50, 430))

            pygame.draw.rect(tela, CINZA, (300, 500, 200, 50))
            proximo_texto = fonte.render("Próxima Pergunta", True, PRETO)
            tela.blit(proximo_texto, (320, 515))

        progresso_texto = fonte.render(f"Pergunta {pergunta_atual + 1} de {len(perguntas)}", True, PRETO)
        tela.blit(progresso_texto, (600, 50))

        acertos_texto = fonte.render(f"Acertos: {acertos}/{len(perguntas)}", True, PRETO)
        tela.blit(acertos_texto, (600, 80))

    # Loop principal do quiz
    rodando = True
    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()

                if not feedback:
                    for i in range(4):
                        if 50 <= x <= 750 and 150 + i * 40 <= y <= 180 + i * 40:
                            resposta_selecionada = i

                if feedback and 300 <= x <= 500 and 500 <= y <= 550:
                    if pergunta_atual < len(perguntas) - 1:
                        pergunta_atual += 1
                        resposta_selecionada = None
                        feedback = ""
                        mostrar_explicacao = False
                    else:
                        tela.fill(BRANCO)
                        resultado_texto = fonte_titulo.render(f"Quiz Concluído! Você acertou {acertos} de {len(perguntas)}", True, PRETO)
                        tela.blit(resultado_texto, (100, 300))
                        pygame.display.flip()
                        pygame.time.wait(3000)
                        rodando = False

            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_RETURN and resposta_selecionada is not None and not feedback:
                if resposta_selecionada == perguntas[pergunta_atual]["correta"]:
                    feedback = "Correto!"
                    acertos += 1
                else:
                    feedback = "Incorreto!"
                mostrar_explicacao = True

        desenhar_quiz()
        pygame.display.flip()
