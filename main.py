import pygame
import utils
import cv2
import mediapipe as mp
import random

cap = cv2.VideoCapture(0)

mphands = mp.solutions.hands
hands = mphands.Hands()
mpDraw = mp.solutions.drawing_utils

pygame.init()

win = pygame.display.set_mode((500, 500))
pygame.display.set_caption("GAME")

x = 100
y = 100
w = 25
h = 25
x_spawn = 200
y_spawn = 200
score = 0

run = True
while run:
    pygame.time.delay(100)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
    open_fingers = []
    success, img = cap.read()
    utils.detect_hands(img)
    positions = utils.find_position(img, hand=0, draw=True)
    index_pos = utils.index_tip_pos(positions)
    if len(positions) != 0:
        for i in [8, 12, 16, 20]:
            if positions[i][2] > positions[i - 2][2]:
                open_fingers.append(0)
            else:
                open_fingers.append(1)

    v = 3 * sum(open_fingers)

    # if collide then create new spawn indices and increment the score
    if x < x_spawn < x+25 and y < y_spawn < y+25:
        x_spawn = random.randint(0, 450)
        y_spawn = random.randint(0, 450)
        score += 1

    if index_pos is not None:
        i = index_pos[0]
        j = index_pos[1]

        if i is None:
            x = x
            y = y
        if i < 160 and x < 475:
            x += v
        if i > 480 and x > 10:
            x -= v
        if 160 < i < 480 and j < 240 and y > 10:
            y -= v
        if 160 < i < 480 and j > 240 and y < 475:
            y += v
    win.fill((0, 0, 0))
    font = pygame.font.SysFont('comicsans', 30, True)
    text = font.render("Score : " + str(score), 1, (255, 0, 0))
    win.blit(text, (380, 470))
    pygame.draw.rect(win, (0, 0, 255), (x, y, w, h))
    pygame.draw.circle(win, (0, 255, 255), (x_spawn, y_spawn), 5)
    pygame.display.update()
    img = cv2.flip(img, 1)

    cv2.line(img, (160, 0), (160, 640), (255, 0, 0), 2)
    cv2.line(img, (480, 0), (480, 640), (255, 0, 0), 2)
    cv2.line(img, (160, 240), (480, 240), (255, 0, 0), 2)

    cv2.putText(img, "UP", (340, 140), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 3)
    cv2.putText(img, "DOWN", (340, 380), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 3)
    cv2.putText(img, "LEFT", (60, 260), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 3)
    cv2.putText(img, "RIGHT", (540, 260), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 3)
    cv2.imshow("Video", img)
pygame.quit()

