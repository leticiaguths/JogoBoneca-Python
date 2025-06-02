import pygame
import sys
import random

pygame.init()

musicajogo = pygame.mixer.Sound("musicajogo.mp3")
musicajogo.set_volume(0.3)

musicapassos = pygame.mixer.Sound("passos.mp3")
musicapassos.set_volume(0.8)

musicaperdeu = pygame.mixer.Sound("musicaperdeu.mp3")
musicaperdeu.set_volume(0.3)

musicajogo.play(-1)

LARGURA, ALTURA = 800, 600
TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Desvie Rápido!")

imagem_fundo = pygame.image.load("imagem.png")
imagem_fundo = pygame.transform.scale(imagem_fundo, (LARGURA, ALTURA))

img_boneca = pygame.image.load("boneca.png")
img_boneca = pygame.transform.scale(img_boneca, (50, 50))

img_cerca = pygame.image.load("cerca.png")
img_cerca = pygame.transform.scale(img_cerca, (50, 50))

BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERMELHO = (200, 50, 50)
AZUL = (50, 150, 255)
CINZA = (100, 100, 100)
AMARELO = (255, 220, 0)

fonte_grande = pygame.font.SysFont('Arial Black', 60)
fonte_media = pygame.font.SysFont('Arial', 40)
fonte_pequena = pygame.font.SysFont('Arial', 30)

clock = pygame.time.Clock()
FPS = 60

jogador_largura = 50
jogador_altura = 50
jogador_x = LARGURA // 2
jogador_y = ALTURA - jogador_altura - 10
velocidade_jogador = 7

obstaculos = []
velocidade_obstaculo = 5
obstaculo_largura = 50
obstaculo_altura = 50
pontuacao = 0

def desenhar_texto(texto, fonte, cor, superficie, x, y, sombra=True):
    if sombra:
        sombra_obj = fonte.render(texto, True, PRETO)
        sombra_rect = sombra_obj.get_rect(center=(x + 2, y + 2))
        superficie.blit(sombra_obj, sombra_rect)
    texto_obj = fonte.render(texto, True, cor)
    texto_rect = texto_obj.get_rect(center=(x, y))
    superficie.blit(texto_obj, texto_rect)

def criar_obstaculo():
    x_pos = random.randint(0, LARGURA - obstaculo_largura)
    y_pos = -obstaculo_altura
    obstaculos.append(pygame.Rect(x_pos, y_pos, obstaculo_largura, obstaculo_altura))

def botao(texto, x, y, largura, altura, cor, acao=None):
    mouse = pygame.mouse.get_pos()
    clique = pygame.mouse.get_pressed()
    botao_rect = pygame.Rect(x, y, largura, altura)

    if botao_rect.collidepoint(mouse):
        pygame.draw.rect(TELA, cor, botao_rect, border_radius=10)
        if clique[0] and acao:
            pygame.time.delay(200)
            acao()
    else:
        pygame.draw.rect(TELA, CINZA, botao_rect, border_radius=10)

    desenhar_texto(texto, fonte_pequena, PRETO, TELA, x + largura // 2, y + altura // 2)

def mostrar_ajuda():
    ajuda_ativa = True
    while ajuda_ativa:
        TELA.blit(imagem_fundo, (0, 0))
        desenhar_texto("Ajuda", fonte_grande, AMARELO, TELA, LARGURA // 2, 100)
        desenhar_texto("Use as setas para desviar dos obstáculos.", fonte_pequena, BRANCO, TELA, LARGURA // 2, 200)
        desenhar_texto("Pressione [ESC] para voltar", fonte_pequena, BRANCO, TELA, LARGURA // 2, 300)
        pygame.display.update()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                ajuda_ativa = False

def tela_inicial():
    while True:
        TELA.blit(imagem_fundo, (0, 0))
        desenhar_texto('🌀 Desvie Rápido! 🌀', fonte_grande, AZUL, TELA, LARGURA // 2, 100)

        botao("Jogar", 300, 250, 200, 50, AZUL, acao=iniciar_jogo)
        botao("Ajuda", 300, 320, 200, 50, AMARELO, acao=mostrar_ajuda)
        botao("Sair", 300, 390, 200, 50, VERMELHO, acao=pygame.quit)

        pygame.display.update()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

def tela_game_over():
    musicaperdeu.play(-1)
    while True:
        TELA.blit(imagem_fundo, (0, 0))
        desenhar_texto('💥 Game Over 💥', fonte_grande, VERMELHO, TELA, LARGURA // 2, ALTURA // 3)
        desenhar_texto(f'Sua Pontuação: {int(pontuacao)}', fonte_media, BRANCO, TELA, LARGURA // 2, ALTURA // 2)
        desenhar_texto('Pressione [ESPAÇO] para tentar novamente', fonte_pequena, CINZA, TELA, LARGURA // 2, ALTURA // 2 + 80)
        pygame.display.update()
        musicapassos.stop()
        musicajogo.stop()
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE:
                musicaperdeu.stop()
                musicajogo.play(-1)
                return
        

def iniciar_jogo():

    musicapassos.play(-1)
    global jogador_x, pontuacao, obstaculos
    jogo_ativo = True
    jogador_x = LARGURA // 2
    pontuacao = 0
    obstaculos.clear()

    while jogo_ativo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and jogador_x > 0:
            jogador_x -= velocidade_jogador
        if keys[pygame.K_RIGHT] and jogador_x < LARGURA - jogador_largura:
            jogador_x += velocidade_jogador

        if random.randint(1, 20) == 1:
            criar_obstaculo()

        for obstaculo in obstaculos[:]:
            obstaculo.y += velocidade_obstaculo
            if obstaculo.top > ALTURA:
                obstaculos.remove(obstaculo)

        pontuacao += 0.1
        jogador_rect = pygame.Rect(jogador_x, jogador_y, jogador_largura, jogador_altura)

        for obstaculo in obstaculos:
            if jogador_rect.colliderect(obstaculo):
                jogo_ativo = False

        TELA.blit(imagem_fundo, (0, 0))
        TELA.blit(img_boneca, (jogador_x, jogador_y))
        for obstaculo in obstaculos:
            TELA.blit(img_cerca, (obstaculo.x, obstaculo.y))

        desenhar_texto(f'Pontuação: {int(pontuacao)}', fonte_pequena, BRANCO, TELA, 120, 30)
        pygame.display.update()
        clock.tick(FPS)

    tela_game_over()

tela_inicial()