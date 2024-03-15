import pygame 
from pygame.locals import *
from sys import exit 
from random import randint

pygame.init()
#biblioteca para facilita o código e não ter que escrever valores todas as vezes 
marrom = (150,75,0)
largura = 400  
altura = 500
fps = 100 #frames por segundo 
font = pygame.font.SysFont('freesansbold.ttf', 16, True, False ) #fonte, tamamnho do texto, negrito, itálico
timer = pygame.time.Clock() #para ajustar a velocidade
tela = pygame.display.set_mode((largura, altura)) #criar tela
pygame.display.set_caption('doodle') #nome que fica em cima da janela (pesar em um nome pro jogo )

background = pygame.image.load('ceu_2.jpeg') #download do cenário
background = pygame.transform.scale(background,(largura,altura)) #definir tamanho do background

player = pygame.image.load('saponormal.png') #download do jogador
player = pygame.transform.scale(player,(120,100) ) #alterar o tamanho do personagem 
player_x = 170 #coordenada x de início da sapa
player_y = 400 #coordenada y de início da sapa

plataforma = [[175,480,70,10],[85,370,70,10], [265, 370, 70, 10], [175, 260, 70, 10],[85, 150, 70, 10], [265, 150, 70, 10], [175, 30, 70, 10]]#cada valor é um vértice das plataformas
pulo = False #a sapa não vai pular a menos que esteja na posição da plataforma
y_change = 0
x_change = 0
player_speed = 3

posicao_cenario_y = 0 #variável para fazer o cenário subir 
velocidade_cenario = .8 #velocidade que o cenário passa 

#checar colisões com os blocos
def check_collisions(rect_list, j, fps) : #rect_list são os blocos que foram gerados 
    global player_x, player_y, y_change #posição (x,y) da sapinha e a mudança de posição 
    for d in range(len(rect_list)) :
        if rect_list[d].colliderect([player_x + 40, player_y + 55, 35, 25]) and pulo == False and y_change > 4 : #colocando a função de colidir 
            j = True
            fps += 0.05 #fazer o frame aumentar aos poucos (acelerar o jogo)
    return j, fps

#update player posição do y em cada loop
def update_player(y_pos) :
    global pulo, y_change
    altura_pulo = 10
    gravidade = 0.3

    if pulo :
        y_change = -altura_pulo #o canto superior esquedo da tela tem coordenada (0,0), então ao diminuir o y a sapinha se aproxima do 0, o que faz ela pular
        pulo = False #faz com que após pular, a sapa só pule de novo quando colidir outra vez com a plataforma

    y_pos += y_change
    y_change += gravidade #faz a altura diminuir a cada pulo 
    return y_pos

#controlar o movimento das plataformas enquanto o personagem sobe
def update_plataforma(lista_plataforma, y_pos, change) :
    if y_pos < 250 and y_change < 0 : # faz com que a tela acompanhe a sapa
        for m in range(len(lista_plataforma)) :
            lista_plataforma[m][1] -= change
    else : 
        pass
    for item in range(len(lista_plataforma)) : #para quando a plataforma sair da tela
        if lista_plataforma[item][1] > 500 :
            lista_plataforma[item] = [randint(10, 320), randint(-50, -10) , 70, 10]  #faz com que a plataforma seja atualizada por um "random" com um range definido para não surgir muito longe da anterior 
    return lista_plataforma

while True :
    timer.tick(fps) #velocidade(quantidade de frames/fps)
    tela.fill((255,255,255)) #completar a tela com a cor branca (acho que não precisa dessa linha porque já tem um background)

    posicao_cenario_y += velocidade_cenario #velocidade que o backgound sobe

    tela.blit(background,(0, posicao_cenario_y)) #gerar o background
    tela.blit(background, (0, posicao_cenario_y - altura)) #gerar continuidade da tela ()

    if (posicao_cenario_y >= altura) :
        posicao_cenario_y = 0

    tela.blit(player, (player_x, player_y)) #gerar a sapinha
    blocks = []#lista das plataformas geradas

    for c in range(len(plataforma)) : #vai ficar percorrendo a lista de plataformas e desenhando
        block = pygame.draw.rect(tela, marrom, plataforma[c], 0, 3) #gerar a imagem da plataforma 
        blocks.append(block) #adicionar cada plataforma a uma lista para adicionar o efeito de 'colisão' a elas

    for event in pygame.event.get() : #adicionando as funções as teclas
        if event.type == QUIT: #a tela do jogo fechará quando o botão de X for clicado
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN: #quando o botão esta precionado 
            if event.key == K_a : 
                x_change = - player_speed #para esqueda
            if event.key == K_d :
                x_change = player_speed #para direita

        if event.type == pygame.KEYUP : #quando não estiver precionado 
            if event.key == K_a : 
                x_change = 0 #sem mudanças
            if event.key == K_d : 
                x_change = 0 #sem mudanças 

    pulo,fps = check_collisions(blocks, pulo, fps) 
    player_x += x_change
    player_y = update_player(player_y) 
    plataforma = update_plataforma(plataforma, player_y, y_change) 

    pygame.display.update()
