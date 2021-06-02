import pygame
import sys
import random
import os
from tkinter import Tk

startX = (Tk().winfo_screenwidth() / 2) - (576 / 2)
startY = 25
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (startX, startY)


def draw_floor():
    screen.blit(floor_surface, (floor_x_pos, 900))
    screen.blit(floor_surface, (floor_x_pos + 576, 900))


def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe_rect_temp = pipe_surface_bottom.get_rect(midtop=(700, random_pipe_pos))
    top_pipe_rect_temp = pipe_surface_top.get_rect(midbottom=(700, random_pipe_pos - 300))
    return bottom_pipe_rect_temp, top_pipe_rect_temp


def move_pipes(bottom_pipe, top_pipe):
    bottom_pipe.centerx -= 5
    top_pipe.centerx -= 5
    draw_pipes(bottom_pipe, top_pipe)


def draw_pipes(bottom_pipe, top_pipe):
    screen.blit(pipe_surface_bottom, bottom_pipe)
    screen.blit(pipe_surface_top, top_pipe)


def check_collison(bottom_pipe, top_pipe):
    if (bird_rect.colliderect(bottom_pipe)) or (bird_rect.colliderect(top_pipe)):
        hit_sound.play()
        return False
    elif (bird_rect.top <= -100) or (bird_rect.bottom >= 900):
        die_sound.play()
        return False

    return True


def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird, bird_movement * -3, 1)
    return new_bird


def bird_animation():
    new_bird = bird_frames[bird_index]
    new_bird_rect = new_bird.get_rect(center=(100, bird_rect.centery))
    return new_bird, new_bird_rect


def score_display(game_state):
    if game_state == 'main_game':
        score_surface = game_font.render(str(score), True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(288, 100))
        screen.blit(score_surface, score_rect)
    elif game_state == 'game_over':
        score_surface = game_font.render('Score : ' + str(score), True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(288, 100))
        screen.blit(score_surface, score_rect)
        high_score_surface = game_font.render('High Score : ' + str(high_score), True, (255, 255, 255))
        high_score_rect = high_score_surface.get_rect(center=(288, 850))
        screen.blit(high_score_surface, high_score_rect)


def update_highscore(score_temp, high_score_temp):
    if score_temp > high_score_temp:
        high_score_temp = score_temp

    return high_score_temp


pygame.init()
screen = pygame.display.set_mode((576, 1024))  # Ekran Boyutunun Ayarlandığı Kısım
pygame.display.set_caption('FlappyBird - Ömer Ulusoy 352621')
programIcon = pygame.image.load('flappy-bird-assets/favicon.ico')
pygame.display.set_icon(programIcon)
clock = pygame.time.Clock()
game_font = pygame.font.Font("flappy-bird-assets/font/04B_19.TTF", 40)

gravity = 0.25
bird_movement = 0
score = 0
high_score = 0
gameActive = False

bg_surface = pygame.image.load('flappy-bird-assets/sprites/background-day.png').convert()
bg_surface = pygame.transform.scale2x(bg_surface)

floor_surface = pygame.image.load('flappy-bird-assets/sprites/base.png').convert()
floor_surface = pygame.transform.scale2x(floor_surface)
floor_x_pos = 0

bird_downflap = pygame.transform.scale2x(
    pygame.image.load('flappy-bird-assets/sprites/bluebird-downflap.png').convert_alpha())
bird_midflap = pygame.transform.scale2x(
    pygame.image.load('flappy-bird-assets/sprites/bluebird-midflap.png').convert_alpha())
bird_upflap = pygame.transform.scale2x(
    pygame.image.load('flappy-bird-assets/sprites/bluebird-upflap.png').convert_alpha())
bird_frames = [bird_downflap, bird_midflap, bird_upflap]
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center=(100, 200))

BIRDFLAP = pygame.USEREVENT
pygame.time.set_timer(BIRDFLAP, 200)

pipe_surface_bottom = pygame.image.load('flappy-bird-assets/sprites/pipe-green.png').convert()
pipe_surface_bottom = pygame.transform.scale2x(pipe_surface_bottom)
pipe_surface_top = pygame.transform.flip(pipe_surface_bottom, False, True)
pipe_height = [400, 600, 800]
bottom_pipe_rect, top_pipe_rect = create_pipe()

game_over_surface = pygame.transform.scale2x(
    pygame.image.load('flappy-bird-assets/sprites/message.png').convert_alpha())
game_over_rect = game_over_surface.get_rect(center=(288, 512))

flap_sound = pygame.mixer.Sound('flappy-bird-assets/audio/wing.wav')
count_score_sound = pygame.mixer.Sound('flappy-bird-assets/audio/point.wav')
hit_sound = pygame.mixer.Sound('flappy-bird-assets/audio/hit.wav')
die_sound = pygame.mixer.Sound('flappy-bird-assets/audio/die.wav')

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Oyunu Kapatmak için
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and gameActive:
                bird_movement = 0
                bird_movement -= 12
                flap_sound.play()
            elif event.key == pygame.K_SPACE and not gameActive:
                bottom_pipe_rect, top_pipe_rect = create_pipe()
                gameActive = True
                score = 0
        if event.type == BIRDFLAP:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0
            bird_surface, bird_rect = bird_animation()
    # Skor
    if bird_rect.centerx == top_pipe_rect.centerx:
        score += 1
        count_score_sound.play()

    # Karakter ve çevre birimlerinin resimleri yükleniyor
    screen.blit(bg_surface, (0, 0))
    if gameActive:
        # Kuş
        bird_movement += gravity
        rotated_bird = rotate_bird(bird_surface)
        bird_rect.centery += int(bird_movement)
        screen.blit(rotated_bird, bird_rect)
        gameActive = check_collison(bottom_pipe_rect, top_pipe_rect)
        # Borular
        if top_pipe_rect.centerx < -50:
            bottom_pipe_rect, top_pipe_rect = create_pipe()
        else:
            move_pipes(bottom_pipe_rect, top_pipe_rect)
        score_display('main_game')
    else:
        bird_movement = 0
        bird_rect.center = (100, 200)
        rotated_bird = rotate_bird(bird_surface)
        screen.blit(rotated_bird, bird_rect)
        screen.blit(game_over_surface, game_over_rect)
        high_score = update_highscore(score, high_score)
        score_display('game_over')
    # Zemin
    floor_x_pos -= 1
    draw_floor()
    if floor_x_pos <= -576:
        floor_x_pos = 0
    pygame.display.update()
    clock.tick(120)
