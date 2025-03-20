import time
import pygame
import menu
import physicsEngine
import gameHandler
import render
from constants import *
from classes import *
import cv2  # file .mp4
import numpy as np

pygame.init()
win = pygame.display.set_mode((render.WIDTH, render.HEIGHT))
pygame.display.set_caption("F∞tball Legends") 

clock = pygame.time.Clock()

# Play intro
def play_intro_video(video_path):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error: Could not open video file {video_path}")
        return False

    intro_running = True
    while intro_running and cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            intro_running = False  # Video ended
            break
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_resized = cv2.resize(frame_rgb, (render.WIDTH, render.HEIGHT))
        frame_surface = pygame.surfarray.make_surface(np.transpose(frame_resized, (1, 0, 2)))
        win.blit(frame_surface, (0, 0))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                intro_running = False
                cap.release()
                return False 
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                intro_running = False  

        clock.tick(60) #Video 60fps 

    cap.release()
    return True  

video_path = "./assets/intro.mp4" 
if not play_intro_video(video_path):
    gameHandler.run = False  

menu.init()
render.init_images()  # Khởi tạo blue_lock_logo
gameHandler.loadStadium(gameHandler.stadium)
gameHandler.menuMatch = gameHandler.loadRecord("./assets/custom_menu_match")
render.logo = pygame.image.load("./assets/images/game_logo.png").convert_alpha() 
render.boti.append(pygame.image.load("./assets/images/easy.png").convert_alpha())
render.boti.append(pygame.image.load("./assets/images/medium.png").convert_alpha())
render.boti.append(pygame.image.load("./assets/images/hard.png").convert_alpha())

currentKeys = pygame.key.get_pressed()
mousePressed = pygame.mouse.get_pressed()

player1 = Player("Player 1", "RED", WASD, 0)
player2 = Player("Player 2", "BLUE", ARROWS, 0)

while gameHandler.run:
    clock.tick(120)
    events = pygame.event.get()
    previousKeys = currentKeys
    currentKeys = pygame.key.get_pressed()
    mouseWasPressed = mousePressed
    mousePressed = pygame.mouse.get_pressed()
    
    menu.update(previousKeys, currentKeys, mouseWasPressed, mousePressed, events, win)
    gameHandler.update(win, clock, previousKeys, currentKeys, gameHandler.stadiumWidth)
    menu.tutorial(win)
    menu.Credit(win)
    pygame.display.update()

pygame.quit()