import pygame
import sys
import os

def executar_quiz():
    pygame.init()
    LARGURA, ALTURA = 800, 600
    tela = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("Quiz - Jornada da Vida")

    BRANCO = (255, 255, 255)
    PRETO = (0, 0, 0)
    VERDE = (0, 255, 0)
    VERMELHO = (255, 0, 0)
    AZUL = (0, 0, 255)
    CINZA = (200, 200, 200)

    caminho_fundo = os.path.join('quiz', 'imgs', 'quiz.png')
    try:
        fundo = pygame.image.load(caminho_fundo)
        fundo = pygame.transform.scale(fundo, (LARGURA, ALTURA))
    except:
        fundo = None
        print(f"Erro ao carregar imagem de fundo: {caminho_fundo}")

    try:
        fonte = pygame.font.SysFont("Georgia", 20)
        fonte_negrito = pygame.font.SysFont("Georgia", 20, bold=True)
        fonte_titulo = pygame.font.SysFont("Georgia", 24, bold=True)
        fonte_explicacao = pygame.font.SysFont("Georgia", 18)
    except:
        fonte = pygame.font.SysFont("Arial", 20)
        fonte_negrito = pygame.font.SysFont("Arial", 20, bold=True)
        fonte_titulo = pygame.font.SysFont("Arial", 24, bold=True)
        fonte_explicacao = pygame.font.SysFont("Arial", 18)

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

    pergunta_atual = 0
    resposta_selecionada = None
    feedback = ""
    acertos = 0
    mostrar_explicacao = False

    def desenhar_quiz():
        nonlocal pergunta_atual, resposta_selecionada, feedback, acertos, mostrar_explicacao
        tela.blit(fundo, (0, 0)) if fundo else tela.fill(BRANCO)

        pygame.draw.rect(tela, CINZA, (650, 10, 130, 50), border_radius=6)
        pygame.draw.rect(tela, PRETO, (650, 10, 130, 50), 1, border_radius=6)
        tela.blit(fonte.render(f"{pergunta_atual + 1}/{len(perguntas)}", True, PRETO), (660, 18))
        tela.blit(fonte.render(f"Acertos: {acertos}", True, PRETO), (660, 38))

        pygame.draw.rect(tela, BRANCO, (30, 70, 740, 80), border_radius=6)
        pygame.draw.rect(tela, AZUL, (30, 70, 740, 80), 1, border_radius=6)

        # Pergunta
        palavras = perguntas[pergunta_atual]["pergunta"].split()
        linhas = []
        linha = ""
        for palavra in palavras:
            teste = (linha + " " + palavra).strip()
            if fonte_titulo.size(teste)[0] < 700:
                linha = teste
            else:
                linhas.append(linha)
                linha = palavra
        linhas.append(linha)
        for i, l in enumerate(linhas):
            tela.blit(fonte_titulo.render(l, True, PRETO), (50, 85 + i * 25))

        # Opções
        for i, opcao in enumerate(perguntas[pergunta_atual]["opcoes"]):
            y = 160 + i * 55
            cor_borda = AZUL if i == resposta_selecionada else PRETO
            pygame.draw.rect(tela, BRANCO, (30, y, 740, 45), border_radius=6)
            pygame.draw.rect(tela, cor_borda, (30, y, 740, 45), 1, border_radius=6)
            tela.blit(fonte.render(opcao, True, PRETO), (50, y + 12))
            if feedback and i == perguntas[pergunta_atual]["correta"]:
                pygame.draw.rect(tela, VERDE, (30, y, 740, 45), 2, border_radius=6)

        # Feedback e explicação
        if feedback:
            pygame.draw.rect(tela, BRANCO, (30, 390, 740, 90), border_radius=6)
            cor_feedback = VERDE if feedback == "Correto!" else VERMELHO
            pygame.draw.rect(tela, cor_feedback, (30, 390, 740, 90), 1, border_radius=6)
            tela.blit(fonte_negrito.render(feedback, True, cor_feedback), (50, 400))
            if mostrar_explicacao:
                explicacao = perguntas[pergunta_atual]["explicacao"]
                linha = ""
                y = 430
                for palavra in explicacao.split():
                    teste = f"{linha} {palavra}".strip()
                    if fonte_explicacao.size(teste)[0] < 700:
                        linha = teste
                    else:
                        tela.blit(fonte_explicacao.render(linha, True, PRETO), (50, y))
                        linha = palavra
                        y += 20
                tela.blit(fonte_explicacao.render(linha, True, PRETO), (50, y))

            # Botão
            pygame.draw.rect(tela, CINZA, (300, 530, 200, 35), border_radius=6)
            pygame.draw.rect(tela, PRETO, (300, 530, 200, 35), 1, border_radius=6)
            tela.blit(fonte.render("Próxima Pergunta", True, PRETO), (320, 540))

    rodando = True
    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif evento.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()

                if not feedback:
                    for i in range(4):
                        y_opcao = 160 + i * 55
                        if 30 <= x <= 770 and y_opcao <= y <= y_opcao + 45:
                            resposta_selecionada = i

                elif 300 <= x <= 500 and 530 <= y <= 565:
                    if pergunta_atual < len(perguntas) - 1:
                        pergunta_atual += 1
                        resposta_selecionada = None
                        feedback = ""
                        mostrar_explicacao = False
                    else:
                        tela.fill(BRANCO)
                        msg = f"Quiz Concluído! Você acertou {acertos} de {len(perguntas)}"
                        fim = fonte_titulo.render(msg, True, PRETO)
                        tela.blit(fim, (LARGURA // 2 - fim.get_width() // 2, ALTURA // 2 - 30))
                        pygame.display.flip()
                        pygame.time.wait(3000)
                        rodando = False

            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN and resposta_selecionada is not None and not feedback:
                    correta = perguntas[pergunta_atual]["correta"]
                    if resposta_selecionada == correta:
                        feedback = "Correto!"
                        acertos += 1
                    else:
                        feedback = "Incorreto!"
                    mostrar_explicacao = True

        desenhar_quiz()
        pygame.display.update()
