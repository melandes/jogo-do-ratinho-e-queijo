# Jogo do ratinho e do queijo

Atividade do Encontro 06 de UDWMJ (Desenvolvimento de Jogos Digitais com Pygame).

O rato anda pela cozinha da **melandes** atrás de queijos. Quando ele encosta no queijo, o queijo aparece em outro lugar aleatório e o placar soma 1. Tábuas de cozinha caem do alto: se uma acertar o rato, ele perde uma vida. Com 3 batidas é fim de jogo. As tábuas caem mais rápido conforme o placar sobe.

## Como rodar

```bash
python -m pip install -U pygame --user
python rato_queijo.py
```

No Python 3.14 o pacote `pygame` ainda não instala; use `pip install pygame-ce`, que é compatível (o código continua com `import pygame`).

## Controles

- Setas: movem o rato
- Espaço: joga de novo depois do fim de jogo

## Sprites

O jogo desenha a cozinha, o rato, o queijo e as tábuas com `pygame.draw`. Para usar imagens próprias, coloque `rato.png` e `queijo.png` na mesma pasta do script.

## Conceitos usados

O código parte dos exemplos `car.py` (imagem controlada pelo teclado e bloco caindo) e `colision.py` (detecção de colisão) vistos em aula.

- Laço do jogo: eventos → atualizar estado → renderizar
- `pygame.key.get_pressed()` para o teclado
- `Surface.get_rect()`, `Rect.move_ip()` e `Rect.clamp_ip()` para mover o rato e as tábuas
- `Rect.colliderect()` para a colisão com o queijo e com as tábuas
- `random` para reposicionar o queijo e as tábuas
