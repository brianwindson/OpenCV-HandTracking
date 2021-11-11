from PySimpleGUI import PySimpleGUI as sg
import os
from Func import HandCap
import csv
import matplotlib.pyplot as plt

# DEFINICOES  DA CAMERA
camera_Width = 320  # 480 # 640 # 1024 # 1280
camera_Heigth = 240  # 320 # 480 # 780  # 960
frameSize = (camera_Width, camera_Heigth)

# Layout
sg.theme('Reddit')
key = ''

# COLUNAS DA GUI
coluna_esq = [
    [sg.Text('Usuário'), sg.Input(key='usuario', size=(45, 1))],
    [sg.Text('Idade'), sg.Input(key='idade', size=(5, 0))],
    [sg.Text('Altura'), sg.Input(key='altura', size=(5, 0))],
    [sg.Text('Peso'), sg.Input(key='peso', size=(5, 0))],
    [sg.Button('Entrar')],
]

coluna_cen = [
    [sg.Output(size=(20, 20))],
]

coluna_dir = [
    [sg.Image(filename="", key="cam")],
]

layout = [
    [sg.Column(coluna_esq),
     sg.Column(coluna_cen),
     sg.Column(coluna_dir)],

]

# Janela
janela = sg.Window('Tela de Login para inicio de leitura de Mãos', layout).finalize()
# Ler eventos
while True:
    x = []
    y = []
    eventos, valores = janela.read()
    if eventos == sg.WINDOW_CLOSED or eventos == 'Parar':
        break
    if eventos == 'Entrar' and valores['usuario'] != '':

        altura = valores['altura']
        usuario = valores['usuario']
        idade = valores['idade']
        peso = valores['peso']
        print('Bem vindo a Captura de Dados!')
        arq = "%s_%s_%s_%s_" % (usuario, idade, altura, peso)
        i = 0

        if os.path.exists(usuario):
            while os.path.exists("%s/%s%d.csv" % (usuario, arq, i)):
                i += 1
        else:
            os.mkdir(usuario)
        arquivo = open("%s/%s%d.csv" % (usuario, arq, i), "w", 1)
        auxarq = "%s/%s%d.csv" % (usuario, arq, i)  # cria string com o nome do arquivo para plottar o grafico
        # arquivo.write("interacao;x;y\n\n")
        i = 1
        HandCap.capturar(frameSize, janela, arquivo,
                         eventos)  # chama a funcao e envia parametos necessarios pra captura
        HandCap.plotagraf(auxarq)  # chama a funcao e envia parametos necessarios pra plottar o grafico
