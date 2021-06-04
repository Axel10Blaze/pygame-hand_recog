import cv2
import mediapipe as mp
import time

mphands = mp.solutions.hands
hands = mphands.Hands()
mpDraw = mp.solutions.drawing_utils


def detect_hands(img):
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    result = hands.process(img_rgb)
    if result.multi_hand_landmarks:
        for handlms in result.multi_hand_landmarks:
            mpDraw.draw_landmarks(img, handlms, mphands.HAND_CONNECTIONS)


def find_position(img, hand=0, draw=True):
    lmlist = []
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    result = hands.process(img_rgb)
    if result.multi_hand_landmarks:
        for handlms in result.multi_hand_landmarks:
            my_hand = result.multi_hand_landmarks[hand]

            for id, lm in enumerate(my_hand.landmark):
                if result.multi_hand_landmarks:
                    h, w, c = img.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    lmlist.append([id, cx, cy])
                    if draw:
                        cv2.circle(img, (cx, cy), 6, (255, 0, 0), cv2.FILLED)
    return lmlist


def index_tip_pos(lmlist):
    if len(lmlist) > 0:
        for id, pos in enumerate(lmlist):
            if id == 8:
                position = pos[1:3]
                return position



