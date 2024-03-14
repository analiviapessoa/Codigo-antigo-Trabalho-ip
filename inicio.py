import pygame 
from pygame.locals import *
from sys import exit 
from random import randint

pygame.init()

marrom = (150,75,0)
largura = 400
altura = 500
font = pygame.font.SysFont('freesansbold.ttf', 16, True, False ) #fonte, tamamnho do texto, negrito, itálico
timer = pygame.time.Clock() #para ajustar a velocidade
tela = pygame.display.set_mode((largura, altura)) 
pygame.display.set_caption('doodle') #nome que fica em cima da janela

background = pygame.image.load('ceu_2.jpeg') #download do cenário
background = pygame.transform.scale(background,(largura,altura))

player = pygame.image.load('sapinha.webp') #download do jogador
player = pygame.transform.scale(player,(70,60) )
 
#coordenadas do jogador
player_x = 170
player_y = 400

plataforma = [[175,480,70,10],[85,370,70,10], [265, 370, 70, 10], [175, 260, 70, 10],[85, 150, 70, 10], [265, 150, 70, 10], [175, 30, 70, 10]]
pulo = False
y_change = 0
x_change = 0
player_speed = 3

posicao_cenario_y = 0
velocidade_cenario = .8

#checar colisões com os blocos
def check_collisions(rect_list, j) :
    global player_x, player_y, y_change
    for d in range(len(rect_list)) :
        if rect_list[d].colliderect([player_x + 10, player_y + 60, 35, 5]) and pulo == False and y_change > 0 :
            j = True
    return j

#update player posição do y em cada loop
def update_player(y_pos) :
    global pulo, y_change
    altura_pulo = 10
    gravidade = 0.3
    if pulo :
        y_change = - altura_pulo
        pulo = False
    y_pos += y_change
    y_change += gravidade
    return y_pos

#controlar o movimento das plataformas enquanto o personagem sobe
def update_plataforma(lista_plataforma, y_pos, change) :
    if y_pos < 250 and y_change < 0 :
        for m in range(len(lista_plataforma)) :
            lista_plataforma[m][1] -= change 
    else :
        pass
    for item in range(len(lista_plataforma)) :
        if lista_plataforma[item][1] > 500 :
            lista_plataforma[item] = [randint(10, 320), randint(-50, -10) , 70, 10]
    return lista_plataforma


while True :
    timer.tick(120) #velocidade 
    tela.fill((255,255,255)) #completar a tela com a cor branca


    posicao_cenario_y += velocidade_cenario     

    tela.blit(background,(0, posicao_cenario_y))
    tela.blit(background, (0, posicao_cenario_y - altura))


    if (posicao_cenario_y >= altura) :
        posicao_cenario_y = 0


    tela.blit(player, (player_x, player_y))
    blocks = []


    for c in range(len(plataforma)) :
        block = pygame.draw.rect(tela, marrom, plataforma[c], 0, 3)
        blocks.append(block)

    for event in pygame.event.get() : # a tela do jogo fechará quando o botão de X for clicado
        if event.type == QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == K_a :
                x_change = - player_speed
            if event.key == K_d :
                x_change = player_speed

        if event.type == pygame.KEYUP :
            if event.key == K_a :
                x_change = 0
            if event.key == K_d :
                x_change = 0

    pulo = check_collisions(blocks, pulo)      
    player_x += x_change
    player_y = update_player(player_y)
    plataforma = update_plataforma(plataforma, player_y, y_change) 
   
   
    pygame.display.update()   
    
