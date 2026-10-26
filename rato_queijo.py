# Rato em busca do queijo - Atividade Encontro 06 (UDWMJ - Pygame)
# Setas do teclado movem o rato. Ao colidir com o queijo, ele reaparece
# em um lugar aleatorio da tela e o placar aumenta.
#
# Sprites: se existirem os arquivos rato.png e queijo.png na mesma pasta,
# eles sao usados. Caso contrario, o jogo desenha os sprites com pygame.draw.

import os
import random
import sys

import pygame

LARGURA, ALTURA = 800, 600
FPS = 60
VELOCIDADE = 5

BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERDE_GRAMA = (120, 180, 90)
CINZA = (150, 150, 155)
CINZA_ESCURO = (90, 90, 95)
ROSA = (240, 160, 170)
AMARELO = (250, 200, 50)
LARANJA = (220, 160, 30)

PASTA = os.path.dirname(os.path.abspath(__file__))


def desenhar_rato():
    """Cria o sprite do rato (virado para a direita) com pygame.draw."""
    surf = pygame.Surface((70, 45), pygame.SRCALPHA)
    pygame.draw.line(surf, ROSA, (12, 28), (0, 10), 3)          # rabo
    pygame.draw.ellipse(surf, CINZA, (8, 12, 45, 28))           # corpo
    pygame.draw.circle(surf, CINZA, (52, 24), 13)               # cabeca
    pygame.draw.circle(surf, CINZA_ESCURO, (46, 10), 8)         # orelha
    pygame.draw.circle(surf, ROSA, (46, 10), 5)
    pygame.draw.polygon(surf, CINZA, [(60, 18), (70, 26), (60, 32)])  # focinho
    pygame.draw.circle(surf, PRETO, (69, 26), 3)                # nariz
    pygame.draw.circle(surf, PRETO, (56, 20), 3)                # olho
    pygame.draw.line(surf, PRETO, (62, 28), (70, 34), 1)        # bigodes
    pygame.draw.line(surf, PRETO, (62, 28), (70, 30), 1)
    return surf


def desenhar_queijo():
    """Cria o sprite do queijo com pygame.draw."""
    surf = pygame.Surface((50, 40), pygame.SRCALPHA)
    pygame.draw.polygon(surf, AMARELO, [(0, 39), (49, 39), (49, 12), (0, 30)])
    pygame.draw.polygon(surf, LARANJA, [(0, 30), (49, 12), (49, 39), (0, 39)], 2)
    for centro, raio in [((14, 33), 4), ((30, 27), 5), ((42, 34), 3), ((38, 20), 3)]:
        pygame.draw.circle(surf, LARANJA, centro, raio)
    return surf


def carregar_sprite(nome_arquivo, tamanho, funcao_desenho):
    caminho = os.path.join(PASTA, nome_arquivo)
    if os.path.exists(caminho):
        img = pygame.image.load(caminho).convert_alpha()
        return pygame.transform.smoothscale(img, tamanho)
    return funcao_desenho()


def posicao_aleatoria(rect, evitar=None):
    """Coloca o rect em um lugar aleatorio da tela, longe do rect 'evitar'."""
    while True:
        rect.x = random.randint(0, LARGURA - rect.width)
        rect.y = random.randint(40, ALTURA - rect.height)
        if evitar is None or not rect.colliderect(evitar.inflate(120, 120)):
            return


def main():
    pygame.init()
    tela = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("Rato em busca do queijo")
    relogio = pygame.time.Clock()
    fonte = pygame.font.SysFont("arial", 28, bold=True)

    rato_direita = carregar_sprite("rato.png", (70, 45), desenhar_rato)
    rato_esquerda = pygame.transform.flip(rato_direita, True, False)
    rato_img = rato_direita
    queijo_img = carregar_sprite("queijo.png", (50, 40), desenhar_queijo)

    rato_rect = rato_img.get_rect(center=(LARGURA // 2, ALTURA // 2))
    queijo_rect = queijo_img.get_rect()
    posicao_aleatoria(queijo_rect, evitar=rato_rect)

    pontos = 0

    while True:
        # 1: gerenciar os eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

        # 2: atualizar o estado do jogo
        teclas = pygame.key.get_pressed()
        velocidade = [0, 0]
        if teclas[pygame.K_LEFT]:
            velocidade[0] = -VELOCIDADE
            rato_img = rato_esquerda
        if teclas[pygame.K_RIGHT]:
            velocidade[0] = VELOCIDADE
            rato_img = rato_direita
        if teclas[pygame.K_UP]:
            velocidade[1] = -VELOCIDADE
        if teclas[pygame.K_DOWN]:
            velocidade[1] = VELOCIDADE

        rato_rect.move_ip(velocidade)
        rato_rect.clamp_ip(tela.get_rect())  # nao deixa o rato sair da tela

        if rato_rect.colliderect(queijo_rect):
            pontos += 1
            posicao_aleatoria(queijo_rect, evitar=rato_rect)

        # 3: renderizar
        tela.fill(VERDE_GRAMA)
        tela.blit(queijo_img, queijo_rect)
        tela.blit(rato_img, rato_rect)
        placar = fonte.render(f"Queijos: {pontos}", True, BRANCO)
        tela.blit(placar, (10, 8))
        pygame.display.flip()

        relogio.tick(FPS)


if __name__ == "__main__":
    main()
