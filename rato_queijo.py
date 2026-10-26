import sys, pygame
import os
import random

# Rato em busca do queijo - Atividade Encontro 06 (UDWMJ - Pygame)
# Ponto de partida: car.py (imagem + teclado + bloco caindo) e colision.py (colliderect)
# O rato pega queijos e desvia das tabuas que caem na cozinha.

FPS = 60
W_SIZE = W_WIDTH, W_HEIGHT = 800, 600
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (220, 50, 50)
GRAY = (150, 150, 155)
DARK_GRAY = (90, 90, 95)
PINK = (240, 160, 170)
YELLOW = (250, 200, 50)
ORANGE = (220, 160, 30)
WALL = (245, 230, 200)
WALL_TILE = (230, 210, 175)
FLOOR_1 = (205, 90, 75)
FLOOR_2 = (240, 235, 225)
WOOD = (150, 95, 50)
WOOD_DARK = (105, 65, 35)
SKY = (150, 200, 240)
STEEL = (190, 195, 200)
SPEED = 5
FLOOR_Y = 260 # onde termina a parede e comeca o piso
VIDAS = 3

pygame.init()

# define tamanho da janela
SCREEN = pygame.display.set_mode(W_SIZE)

# define titulo da janela
pygame.display.set_caption('Rato em busca do queijo')

clock = pygame.time.Clock()
font = pygame.font.SysFont('arial', 28, bold=True)
font_big = pygame.font.SysFont('arial', 64, bold=True)
font_nome = pygame.font.SysFont('georgia', 72, bold=True, italic=True)

PASTA = os.path.dirname(os.path.abspath(__file__))

# ---------- fundo: cozinha com o nome "melandes" ----------
fundo = pygame.Surface(W_SIZE)

# parede com azulejos
fundo.fill(WALL)
for x in range(0, W_WIDTH, 40):
   for y in range(0, FLOOR_Y, 40):
      pygame.draw.rect(fundo, WALL_TILE, (x, y, 40, 40), 1)

# janela
pygame.draw.rect(fundo, SKY, (560, 40, 180, 120))
pygame.draw.rect(fundo, WHITE, (560, 40, 180, 120), 8)
pygame.draw.line(fundo, WHITE, (650, 40), (650, 160), 6)
pygame.draw.line(fundo, WHITE, (560, 100), (740, 100), 6)
pygame.draw.circle(fundo, YELLOW, (600, 75), 18) # sol

# placa com o nome na parede
nome = font_nome.render('melandes', True, WOOD_DARK)
placa = nome.get_rect(center=(285, 100))
pygame.draw.rect(fundo, WOOD, placa.inflate(40, 20), border_radius=12)
pygame.draw.rect(fundo, WOOD_DARK, placa.inflate(40, 20), 4, border_radius=12)
fundo.blit(font_nome.render('melandes', True, WALL), placa)

# armarios e bancada
pygame.draw.rect(fundo, WOOD, (0, 170, W_WIDTH, 90))
for x in range(10, W_WIDTH, 130):
   pygame.draw.rect(fundo, WOOD_DARK, (x, 180, 115, 72), 3)
   pygame.draw.circle(fundo, STEEL, (x + 100, 216), 5) # puxador
pygame.draw.rect(fundo, STEEL, (0, 160, W_WIDTH, 12)) # tampo da bancada

# panelas penduradas
for x, r in [(32, 18), (522, 18)]:
   pygame.draw.line(fundo, DARK_GRAY, (x, 0), (x, 120 - r), 2)
   pygame.draw.circle(fundo, DARK_GRAY, (x, 120), r)
   pygame.draw.circle(fundo, STEEL, (x, 120), r - 4)

# piso xadrez
for i, x in enumerate(range(0, W_WIDTH, 50)):
   for j, y in enumerate(range(FLOOR_Y, W_HEIGHT, 50)):
      cor = FLOOR_1 if (i + j) % 2 == 0 else FLOOR_2
      pygame.draw.rect(fundo, cor, (x, y, 50, 50))

# nome "melandes" bem grande e clarinho no piso, como marca d'agua
marca = font_big.render('melandes', True, WHITE)
marca.set_alpha(70)
fundo.blit(marca, marca.get_rect(center=(W_WIDTH // 2, 440)))

# ---------- sprites ----------
# carrega arquivo de imagem do rato (rato.png); se nao existir, desenha o rato
if os.path.exists(os.path.join(PASTA, 'rato.png')):
   rato = pygame.image.load(os.path.join(PASTA, 'rato.png')).convert_alpha()
   rato = pygame.transform.smoothscale(rato, (70, 45))
else:
   rato = pygame.Surface((70, 45), pygame.SRCALPHA)
   pygame.draw.line(rato, PINK, (12, 28), (0, 10), 3)              # rabo
   pygame.draw.ellipse(rato, GRAY, (8, 12, 45, 28))                # corpo
   pygame.draw.circle(rato, GRAY, (52, 24), 13)                    # cabeca
   pygame.draw.circle(rato, DARK_GRAY, (46, 10), 8)                # orelha
   pygame.draw.circle(rato, PINK, (46, 10), 5)
   pygame.draw.polygon(rato, GRAY, [(60, 18), (70, 26), (60, 32)]) # focinho
   pygame.draw.circle(rato, BLACK, (69, 26), 3)                    # nariz
   pygame.draw.circle(rato, BLACK, (56, 20), 3)                    # olho
   pygame.draw.line(rato, BLACK, (62, 28), (70, 34), 1)            # bigodes
   pygame.draw.line(rato, BLACK, (62, 28), (70, 30), 1)

# carrega arquivo de imagem do queijo (queijo.png); se nao existir, desenha o queijo
if os.path.exists(os.path.join(PASTA, 'queijo.png')):
   queijo = pygame.image.load(os.path.join(PASTA, 'queijo.png')).convert_alpha()
   queijo = pygame.transform.smoothscale(queijo, (50, 40))
else:
   queijo = pygame.Surface((50, 40), pygame.SRCALPHA)
   pygame.draw.polygon(queijo, YELLOW, [(0, 39), (49, 39), (49, 12), (0, 30)])
   pygame.draw.polygon(queijo, ORANGE, [(0, 30), (49, 12), (49, 39), (0, 39)], 2)
   for centro, raio in [((14, 33), 4), ((30, 27), 5), ((42, 34), 3), ((38, 20), 3)]:
      pygame.draw.circle(queijo, ORANGE, centro, raio)

# tabua de cozinha que cai (o "bloco" do car.py)
tabua = pygame.Surface((90, 16), pygame.SRCALPHA)
pygame.draw.rect(tabua, WOOD, (0, 0, 90, 16), border_radius=6)
pygame.draw.rect(tabua, WOOD_DARK, (0, 0, 90, 16), 2, border_radius=6)
pygame.draw.circle(tabua, WOOD_DARK, (80, 8), 3) # furinho do cabo

# o rato "olha" para o lado em que esta andando
rato_direita = rato
rato_esquerda = pygame.transform.flip(rato, True, False)


def novo_queijo():
   # sorteia um lugar no piso, longe do rato
   while True:
      queijo_rect.center = (random.randint(40, W_WIDTH - 40), random.randint(FLOOR_Y + 30, W_HEIGHT - 30))
      if not queijo_rect.colliderect(rato_rect.inflate(160, 160)):
         return


def nova_tabua(bloco):
   # recoloca a tabua acima da tela, em um x aleatorio
   bloco.x = random.randint(0, W_WIDTH - bloco.width)
   bloco.bottom = random.randint(-300, 0)


def reiniciar():
   global pontos, vidas, invencivel, game_over
   pontos = 0
   vidas = VIDAS
   invencivel = 0
   game_over = False
   rato_rect.center = (W_WIDTH // 2, W_HEIGHT - 80)
   novo_queijo()
   for bloco in blocos:
      nova_tabua(bloco)


# captura retangulo das imagens
rato_rect = rato.get_rect()
queijo_rect = queijo.get_rect()
blocos = [tabua.get_rect() for _ in range(4)]

reiniciar()

while True:
   SCREEN.blit(fundo, (0, 0)) # redesenha a cozinha

   # captura um evento na interface
   for event in pygame.event.get():
      if event.type == pygame.QUIT:
         pygame.quit()
         sys.exit()
      if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and game_over:
         reiniciar()

   if not game_over:
      # captura as teclas pressionadas (permite andar na diagonal)
      if pygame.key.get_focused():
         key = pygame.key.get_pressed()
         if key[pygame.K_LEFT]:
            rato_rect.move_ip(-SPEED, 0) # move o rato para a esquerda
            rato = rato_esquerda
         if key[pygame.K_RIGHT]:
            rato_rect.move_ip(SPEED, 0) # move o rato para a direita
            rato = rato_direita
         if key[pygame.K_UP]:
            rato_rect.move_ip(0, -SPEED) # move o rato para cima
         if key[pygame.K_DOWN]:
            rato_rect.move_ip(0, SPEED) # move o rato para baixo

      # nao deixa o rato sair do piso
      rato_rect.clamp_ip(pygame.Rect(0, FLOOR_Y - 20, W_WIDTH, W_HEIGHT - FLOOR_Y + 20))

      # colisao com o queijo: ele aparece em outro lugar aleatorio
      if rato_rect.colliderect(queijo_rect):
         pontos += 1
         novo_queijo()

      # tabuas caem cada vez mais rapido conforme o placar sobe
      velocidade_queda = 3 + pontos // 3
      for bloco in blocos:
         bloco.move_ip(0, velocidade_queda)
         if bloco.top > W_HEIGHT:
            nova_tabua(bloco)
         # colisao com a tabua: perde uma vida (e fica piscando um tempinho)
         if invencivel == 0 and rato_rect.colliderect(bloco):
            vidas -= 1
            invencivel = FPS * 2
            nova_tabua(bloco)
            if vidas == 0:
               game_over = True

      if invencivel > 0:
         invencivel -= 1

   SCREEN.blit(queijo, queijo_rect) # redesenha queijo na tela
   for bloco in blocos:
      SCREEN.blit(tabua, bloco) # redesenha tabuas na tela
   if invencivel % 10 < 5: # pisca quando foi atingido
      SCREEN.blit(rato, rato_rect) # redesenha rato na tela

   # placar e vidas (sobre uma faixa escura para dar leitura)
   faixa = pygame.Surface((W_WIDTH, 46), pygame.SRCALPHA)
   faixa.fill((0, 0, 0, 120))
   SCREEN.blit(faixa, (0, 0))
   SCREEN.blit(font.render(f'Queijos: {pontos}', True, WHITE), (12, 8))
   SCREEN.blit(font.render('Vidas: ' + '♥' * vidas, True, RED), (W_WIDTH - 200, 8))

   if game_over:
      escuro = pygame.Surface(W_SIZE, pygame.SRCALPHA)
      escuro.fill((0, 0, 0, 150))
      SCREEN.blit(escuro, (0, 0))
      texto = font_big.render('FIM DE JOGO', True, WHITE)
      SCREEN.blit(texto, texto.get_rect(center=(W_WIDTH // 2, W_HEIGHT // 2 - 30)))
      texto = font.render(f'{pontos} queijos  -  ESPACO para jogar de novo', True, YELLOW)
      SCREEN.blit(texto, texto.get_rect(center=(W_WIDTH // 2, W_HEIGHT // 2 + 30)))

   pygame.display.update() # atualiza a tela
   clock.tick(FPS)
