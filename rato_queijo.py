import sys, pygame
import os
import random

# Rato em busca do queijo - Atividade Encontro 06 (UDWMJ - Pygame)
# Ponto de partida: car.py (imagem + teclado) e colision.py (colliderect)

FPS = 60
W_SIZE = W_WIDTH, W_HEIGHT = 640, 480
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (120, 180, 90)
GRAY = (150, 150, 155)
DARK_GRAY = (90, 90, 95)
PINK = (240, 160, 170)
YELLOW = (250, 200, 50)
ORANGE = (220, 160, 30)
W_BGCOLOR = GREEN
SPEED = 5

pygame.init()

# define tamanho da janela
SCREEN = pygame.display.set_mode(W_SIZE)

# define titulo da janela
pygame.display.set_caption('Rato em busca do queijo')

clock = pygame.time.Clock()
font = pygame.font.SysFont('arial', 28, bold=True)

PASTA = os.path.dirname(os.path.abspath(__file__))

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

# o rato "olha" para o lado em que esta andando
rato_direita = rato
rato_esquerda = pygame.transform.flip(rato, True, False)

# captura retangulo das imagens
rato_rect = rato.get_rect()
queijo_rect = queijo.get_rect()

# altera atributo 'center' das imagens
rato_rect.center = (W_WIDTH // 2, W_HEIGHT // 2)
queijo_rect.center = (random.randint(40, W_WIDTH - 40), random.randint(60, W_HEIGHT - 40))

pontos = 0
while True:
   SCREEN.fill(W_BGCOLOR) # (re)colore fundo

   # captura um evento na interface
   for event in pygame.event.get():
      if event.type == pygame.QUIT:
         pygame.quit()
         sys.exit()

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

   # nao deixa o rato sair da tela
   rato_rect.clamp_ip(SCREEN.get_rect())

   # colisao: o queijo aparece em outro lugar aleatorio da tela
   if rato_rect.colliderect(queijo_rect):
      pontos += 1
      while queijo_rect.colliderect(rato_rect.inflate(120, 120)):
         x = random.randint(40, W_WIDTH - 40)
         y = random.randint(60, W_HEIGHT - 40)
         queijo_rect.center = (x, y) # altera atributo 'center' do queijo

   SCREEN.blit(queijo, queijo_rect) # redesenha queijo na tela
   SCREEN.blit(rato, rato_rect) # redesenha rato na tela
   SCREEN.blit(font.render(f'Queijos: {pontos}', True, WHITE), (10, 8)) # placar
   pygame.display.update() # atualiza a tela
   clock.tick(FPS)
