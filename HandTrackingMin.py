from os import listdir
from os.path import isfile, join
from pathlib import Path

import cv2
import mediapipe as mp
import time
import numpy
import argparse
import csv

# Check whether the CSV 
# exists or not if not then create one.

cap = cv2.VideoCapture(0)

mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

pTime = 0
cTime = 0

while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
   # print(results.multi_hand_landmarks)
   
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            for id, lm in enumerate(handLms.landmark):
              #  print(id,lm)
                h, w, c = img.shape
                cx= int(lm.x*w)
                cy= int(lm.y*h)
                print('{} - {} - {}'. format (id, cx, cy))
               # if id == 0:
                cv2.circle(img, (cx, cy), 5, (255,0,255), cv2.FILLED)

#=================================
    my_file = Path("details.csv")

    if my_file.is_file():
        f=open (my_file, "w+")
        with open ('details.csv', 'a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file, delimiter=';')
                cabecalho = ['sequencia', 'pos1', 'pos2']
                writer.writerow(cabecalho)

                writer.writerow(id, cx, cy)
                #writer.writerow(data)
                #writer.writerow(["Nome", "Idade", "Sexo"])
        f.close()
        pass

    else:
        with open('details.csv', 'w', newline ='', encoding='utf-8') as file:
               writer = csv.writer(file)

               data = ((id, cx, cy))
               writer.writerow(data)

                #writer.writerow(["Nome", "Idade", "Sexo"])
                #writer.writerows([id, cx, cy])
        f.close()

#===========================================

#==================================================
        mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(img,str(int(fps)),(10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)


    cv2.imshow("image",img)
    cv2.waitKey(1)
