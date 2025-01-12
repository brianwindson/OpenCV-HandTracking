import os
import sys

import PySimpleGUI
import cv2
import mediapipe as mp
import time
import matplotlib.pyplot as plt
import csv
import time

cap = cv2.VideoCapture(1)
mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils
pTime = 0
cTime = 0
aux = 0


class HandCap:

    def __init__(self):
        pass

    def capturar(frameSize, janela, arquivo, eventos):
        i = 1
        tempodecaptura = time.time() + 5  # agora + tempo em segundos

        while cap.isOpened():
            success, img = cap.read()
            imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            results = hands.process(imgRGB)
            print(results.multi_hand_landmarks)

            if results.multi_hand_landmarks:

                for handLms in results.multi_hand_landmarks:

                    for id, lm in enumerate(handLms.landmark):
                        h, w, c = img.shape
                        cx, cy = int(lm.x * w), int(lm.y * h)
                        print(id, cx, cy)
                        if id == 8:
                            cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
                            coordenadax = str(cx)
                            coordenaday = str(cy)
                            iteracao = str(i)
                            i = i + 1
                            linhaescrita = iteracao + ';' + coordenadax + ';' + coordenaday + '\n'
                            arquivo.write(linhaescrita)

                mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)
            if time.time() > tempodecaptura:
                cap.release()
                break
            cTime = time.time()
            # fps = 1 / (cTime - pTime)
            pTime = cTime

            # redimensiona a camera
            ret, frameOrig = cap.read()
            frame = cv2.resize(frameOrig, frameSize)

            # atualiza a imagem recebida na janela

            imgbytes = cv2.imencode(".png", img)[1].tobytes()
            janela["cam"].update(data=imgbytes)

    def plotagraf(auxarq):
        x = []
        y = []

        with open(auxarq, "r") as csvfile:
            plots= csv.reader(csvfile, delimiter=';')
            for row in plots:
                x.append(int(row[1]))
                y.append(int(row[2]))

        plt.plot(x, y, marker='o')

        plt.title('Resultado da captura:')

        plt.xlabel('x')
        plt.ylabel('y')

        plt.show()
