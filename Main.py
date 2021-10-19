import cv2
import mediapipe as mp
import time
from PySimpleGUI import PySimpleGUI as sg

# Layout
sg.theme('Reddit')
key = ''
layout = [
    [sg.Text('Usuário'), sg.Input(key='usuario', size=(45, 1))],
    [sg.Text('Idade'), sg.Input(key='idade', size=(5, 0))],
    [sg.Text('Senha'), sg.Input(key='senha', password_char='*', size=(45, 1))],
    [sg.Checkbox('Masculino', key='masculino'), sg.Checkbox('Feminino', key='feminino')],
    [sg.Checkbox('Salvar Login?')],
    # [sg.Slider(range=(0,255),default_value=0,orientation='h',size=(30,20),key='sliderVelocidade')],
    [sg.Button('Entrar')],
    [sg.Output(size=(30, 20))]
]

# Janela
janela = sg.Window('Tela de Login para inicio de leitura de Mãos', layout)
# Ler eventos
while True:
    eventos, valores = janela.read()
    if eventos == sg.WINDOW_CLOSED:
        break
    if eventos == 'Entrar':
        if valores['usuario'] != '':

            usuario = valores['usuario']
            idade = valores['idade']
            print('Bem vindo a Captura de Dados!')
            cap = cv2.VideoCapture(0)
            mpHands = mp.solutions.hands
            hands = mpHands.Hands()
            mpDraw = mp.solutions.drawing_utils
            pTime = 0
            cTime = 0
            arquivo = open(usuario + ".csv", "w", 1)
            # arquivo.write("interacao;x;y\n\n")
            i = 1
            while cap.isOpened():
                success, img = cap.read()
                imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                results = hands.process(imgRGB)
                print(results.multi_hand_landmarks)
                # print(results.multi_hand_landmark)
                if results.multi_hand_landmarks:
                    for handLms in results.multi_hand_landmarks:
                        for id, lm in enumerate(handLms.landmark):
                            # print(id, lm)
                            h, w, c = img.shape
                            cx, cy = int(lm.x * w), int(lm.y * h)
                            print(id, cx, cy)
                            if id == 8:
                                cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
                                coordenadax = str(cx)
                                coordenaday = str(cy)
                                iteracao = str(i)
                                # parte1= interacao+','+coordenadax+','+coordenaday+'\n'
                                # parte2=str(parte1,',',coordenaday)
                                linhaescrita = iteracao + ';' + coordenadax + ';' + coordenaday + '\n'
                                i = i + 1
                                arquivo.write(linhaescrita)

                        mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

                cTime = time.time()
                fps = 1 / (cTime - pTime)
                pTime = cTime
                # cv2.putText(img, str(int(fps)), (10, 70),cv2.FONT_HERSHEY_PLAIN,3(255, 0, 255),3 )

                cv2.imshow("image", img)
                # cv2.waitKey(1)

                if cv2.waitKey(10) & 0xFF == ord('q'):
                    # a aplicação não fecha pelo icone de X, mas apertando o q no teclado
                    # print ('Bem vindo a Captura de Dados!')
                    break

        break
        cap.release()
        cv2.destroyAllWindows()
        arquivo.close()
        print("até aqui funciona")