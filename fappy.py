import pygame
import sys # system module 
import random

pygame.init()

#Game Variable
floor_x_position = 0
bg_x_position = 0
gravity = 0.20
bird_y_moment = 0 
score = 0
high_score = 0



#All function
def floor_varavaikkirathu():

    screen.blit(floor_image,(floor_x_position,450))
    screen.blit(floor_image,(floor_x_position+288,450))

def draw_bg():
    screen.blit(bg_surface,(bg_x_position,0))   # (0,0) is nothing but coordinate in x aixs(width) to y axis(lenght) \
    screen.blit(bg_surface,(bg_x_position+288,0))   # (0,0) is nothing but coordinate in x aixs(width) to y axis(lenght) \

def create_pipe():
    random_height = random.choice(pipe_height)
    bottom_pipe  = pipe_surface.get_rect(midtop=(400,random_height))
    top_pipe = pipe_surface.get_rect(midbottom=(400,random_height-100))
    return bottom_pipe,top_pipe

def move_pipe(pipes):
    for pipe in pipes:
        pipe.centerx -= 2

    return pipes

def draw_pipe(pipes):
    for pipe in pipes:
        if pipe.bottom >= 512:

            screen.blit(pipe_surface,pipe)
        else:
            filp_pipe = pygame.transform.flip(pipe_surface,False,True)
            screen.blit(filp_pipe,pipe)


def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            return False
            
        if bird_rect.top <= -100 or bird_rect.bottom >= 450:
            
            return False

    return True 
def rotate_bird(bird_surface):
    new_bird = pygame.transform.rotozoom(bird_surface,-bird_y_moment*3,1)
    return new_bird

def bird_animation():
    new_bird = bird_frame[bird_index]
    new_bird_rect = new_bird.get_rect(center=(78,bird_rect.centery))
    return new_bird,new_bird_rect

def score_display(game_state):
    if  game_state == 'main-game':
        score_surface = game_font.render(f"Score :: {str(int(score))}",True,(255,255,255))
        score_rect = score_surface.get_rect(center=(144,50))
        screen.blit(score_surface,score_rect)
    if game_state == 'game-over':
        score_surface = game_font.render(f"Score :: {str(int(score))}",True,(255,255,255))
        score_rect = score_surface.get_rect(center=(144,50))
        screen.blit(score_surface,score_rect)

        high_score_surface = game_font.render(f"High Score :: {str(int(high_score))}",True,(255,255,255))
        high_score_rect = high_score_surface.get_rect(center=(144,420))
        screen.blit(high_score_surface,high_score_rect)
screen = pygame.display.set_mode((233,512))

def update_score(score,high_score):
    if score > high_score:
        high_score = score
    return high_score
clock = pygame.time.Clock()

game_font = pygame.font.Font("assets/04B_19.TTF",20)  #/home/sharan/Desktop/code_gaming/04B_19.TTF
game_active = True
bg_surface = pygame.image.load('assets/background-day.png').convert()
floor_image = pygame.image.load('assets/base.png').convert()
# bird_surface = pygame.image.load('assets/bluebird-midflap.png').convert_alpha()
# bird_rect = bird_surface.get_rect(center=(78,256))
bird_downflap = pygame.image.load('assets/bluebird-downflap.png').convert_alpha()
bird_midflap = pygame.image.load('assets/bluebird-midflap.png').convert_alpha()
bird_upflap = pygame.image.load('assets/bluebird-upflap.png').convert_alpha()
bird_frame = [bird_downflap,bird_midflap,bird_upflap]
bird_index= 0
bird_surface = bird_frame[bird_index]
bird_rect = bird_surface.get_rect(center=(78,256))
game_over_screen = pygame.image.load('assets/gameover.png').convert_alpha()
game_over_rect = game_over_screen.get_rect(center=(120,200))
bird_flap = pygame.USEREVENT+1  # +1 is nothing but we already create a USEREVENT, So now we add +1, Ok in future when you create a other USEREVENT just to +2,+3...
pygame.time.set_timer(bird_flap,200)
pipe_surface = pygame.image.load('assets/pipe-red.png').convert()
pipe_list = []
SPWANPIPE = pygame.USEREVENT
pygame.time.set_timer(SPWANPIPE,1200) #  the second one is 1200 is mili-second 1 second =  1000 mili-second 
pipe_height = [195,200,210,220,230,240,250,260,270,280,290,300,310,320,330,340,350,360,390,400,410]
while True:
    
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit() # it will directly quit the loop
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_y_moment = 0 
                bird_y_moment = -7
            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                score = 0
                pipe_list.clear() # to clear the pipe from the list 
                bird_rect.center=(78,256)
                bird_y_moment = 0
        if event.type == SPWANPIPE:
            pipe_list.extend(create_pipe())

        if event.type == bird_flap:
            if bird_index < 2:
                bird_index += 1

            else:
                bird_index = 0
            bird_surface,bird_rect=bird_animation()
    
    if floor_x_position <= -288 and bg_x_position <= -288:
        floor_x_position = 0
        bg_x_position = 0
    
    floor_x_position -= 1
    bg_x_position -= 1
    draw_bg()
    
    if game_active:
        pipe_list = move_pipe(pipe_list)
        draw_pipe(pipe_list)
        bird_y_moment += gravity
        rotated_bird = rotate_bird(bird_surface)
        bird_rect.centery+= bird_y_moment  # centery means that the image is add in y coordinates +.20.... untill loop stop 
        screen.blit(rotated_bird,(bird_rect))   
        game_active = check_collision(pipe_list)
        score += 00.1
        score_display('main-game')   
    else:
        high_score = update_score(score,high_score)
        score_display('game-over')  
        screen.blit(game_over_screen,game_over_rect) 
    floor_varavaikkirathu()
    pygame.display.update()
    clock.tick(120)

