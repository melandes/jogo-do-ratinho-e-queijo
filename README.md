# Jogo do ratinho e do queijo

Atividade do Encontro 06 de UDWMJ (Desenvolvimento de Jogos Digitais com Pygame).

Você controla um rato com as setas do teclado. Quando o rato encosta no queijo, o queijo aparece em outro lugar aleatório da tela e o placar soma 1.

## Como rodar

```bash
python -m pip install -U pygame --user
python rato_queijo.py
```

No Python 3.14 o pacote `pygame` ainda não instala; use `pip install pygame-ce`, que é compatível (o código continua com `import pygame`).

## Controles

- Setas: movem o rato
- Esc: fecha o jogo

## Sprites

O jogo desenha o rato e o queijo com `pygame.draw`. Para usar imagens próprias, coloque `rato.png` e `queijo.png` na mesma pasta do script.

## Conceitos usados

O código parte dos exemplos `car.py` (imagem controlada pelo teclado) e `colision.py` (detecção de colisão) vistos em aula.

- Laço do jogo: eventos → atualizar estado → renderizar
- `pygame.key.get_pressed()` para o teclado
- `Surface.get_rect()`, `Rect.move_ip()` e `Rect.clamp_ip()` para mover o rato
- `Rect.colliderect()` para detectar a colisão com o queijo
