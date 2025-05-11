import pygame

# Inicializar o pygame
pygame.init()

# Definir as dimensões da tela
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Quiz de Fases da Vida")

# Carregar o fundo
background = pygame.image.load(r"C:\Users\Ana Gierse\Documents\GitHub\Projeto-Jogos-Digitais\quiz\imgs\quiz.png")

# Definir as fontes
font = pygame.font.SysFont('Arial', 24)

# Perguntas e respostas
questions = [
    {
        "question": "1. O que o “homem do saco” representa no jogo?",
        "answers": [
            "A) Um chefe final da fase",
            "B) Um obstáculo aleatório sem significado",
            "C) O perigo de falar com estranhos",
            "D) Um personagem engraçado"
        ],
        "correct_answer": "C) O perigo de falar com estranhos"
    },
    {
        "question": "2. Por que coletar doces é importante na fase da infância?",
        "answers": [
            "A) Eles são só decorativos",
            "B) Aumentam o tamanho do personagem",
            "C) Representam recompensas e afeto na infância",
            "D) Fazem o personagem correr mais rápido"
        ],
        "correct_answer": "C) Representam recompensas e afeto na infância"
    },
    {
        "question": "3. O que acontece quando o personagem encosta em drogas na fase da adolescência?",
        "answers": [
            "A) Ele ganha poderes especiais",
            "B) Ele perde o controle, refletindo os efeitos negativos",
            "C) Nada muda",
            "D) Ele pula para a fase adulta"
        ],
        "correct_answer": "B) Ele perde o controle, refletindo os efeitos negativos"
    },
    {
        "question": "4. O que significa ter um bebê no jogo após não pegar a camisinha?",
        "answers": [
            "A) Um bônus de vida extra",
            "B) Um novo personagem jogável",
            "C) As consequências da falta de prevenção",
            "D) Um enfeite visual"
        ],
        "correct_answer": "C) As consequências da falta de prevenção"
    },
    {
        "question": "5. Por que o jogador perde ao ser pego por um agiota?",
        "answers": [
            "A) Porque é parte do final secreto",
            "B) Para desbloquear uma nova fase",
            "C) Para mostrar os perigos das dívidas e apostas",
            "D) Porque o jogo tem um bug"
        ],
        "correct_answer": "C) Para mostrar os perigos das dívidas e apostas"
    },
    {
        "question": "6. O que as máquinas de apostas fazem com o personagem?",
        "answers": [
            "A) Aumentam o dinheiro",
            "B) Reduzem o dinheiro, mostrando os riscos do vício",
            "C) Mudam a trilha sonora",
            "D) Fazem o personagem parar de se mover"
        ],
        "correct_answer": "B) Reduzem o dinheiro, mostrando os riscos do vício"
    },
    {
        "question": "8. O que as fases do jogo representam?",
        "answers": [
            "A) Uma corrida maluca entre personagens",
            "B) Três estilos diferentes de jogabilidade",
            "C) Etapas da vida com desafios reais e sociais",
            "D) Um mundo fictício com inimigos e bônus aleatórios"
        ],
        "correct_answer": "C) Etapas da vida com desafios reais e sociais"
    }
]

# Função para exibir perguntas e respostas
def display_quiz():
    screen.blit(background, (0, 0))

    y_offset = 50  # Inicializa a posição y para exibir as perguntas

    # Exibir as perguntas e respostas
    for i, question in enumerate(questions):
        question_text = font.render(question["question"], True, (255, 255, 255))
        screen.blit(question_text, (50, y_offset))
        y_offset += 40

        for j, answer in enumerate(question["answers"]):
            answer_text = font.render(answer, True, (255, 255, 255))
            screen.blit(answer_text, (50, y_offset))
            y_offset += 30

# Loop principal do jogo
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Exibir o quiz na tela
    display_quiz()

    # Atualizar a tela
    pygame.display.flip()

# Fechar o pygame
pygame.quit()
