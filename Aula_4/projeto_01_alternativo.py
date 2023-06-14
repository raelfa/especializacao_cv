#Método alternativo para fazer Keying (não ficou tão bom quando o que usa InRange)
#importando as bibliotecas
import cv2
import numpy as np

#Definindo um limite
threshold = 13

#Carregando os vídeos e uma imagem muito semelhante ao fundo a ser retirado
video_webcam = cv2.VideoCapture('data/webcam.mp4')
video_praia = cv2.VideoCapture('data/praia.mp4')
fundo = cv2.imread('fundo_teste_2.png')

#Pegando as dimensoes do video para que o fundo genérico seja do mesmo tamanho
width1 = int(video_webcam.get(cv2.CAP_PROP_FRAME_WIDTH))
height1 = int(video_webcam.get(cv2.CAP_PROP_FRAME_HEIGHT))

#Redimensionando o fundo e convertendo para escala de cinza
fundo = cv2.resize(fundo, (width1, height1))
fundo = cv2.cvtColor(fundo, cv2.COLOR_BGR2GRAY)

#Iniciando o loop do video
while True:

    #Carregando os frames dos videos, se um dos videos acabar, a janela será fechado
    ret_webcam, frame_webcam = video_webcam.read()
    ret_praia, frame_praia = video_praia.read()

    if not ret_webcam or not ret_praia:
        break

    #Convertendo os frames dos videos para escala de cinza
    gray_webcam = cv2.cvtColor(frame_webcam, cv2.COLOR_BGR2GRAY)
    gray_praia = cv2.cvtColor(frame_praia, cv2.COLOR_BGR2GRAY)

    #Calculando a diferença absoluta entre o video e o fundo genérico. A ideia dessa abordagem é que o o fundo genérico seja muito semelhante 
    #ao fundo do video, e onde a diferença for pequena, o open_cv considerará como zero ao aplicar o threshold
    diff = cv2.absdiff(gray_webcam, fundo)

    #Aplicação do threshold. Os pixels da diferença menores que o threshold serão considerados 0 e 1 os maiores.
    _, mask = cv2.threshold(diff, threshold, 255, cv2.THRESH_BINARY)

    #Aplicação da máscara no vídeo
    webcam_foreground = cv2.bitwise_and(frame_webcam, frame_webcam, mask=mask)

    #Máscara inversa para o fundo
    mask_inv = np.invert(mask)

    #Aplicação da máscara inversa no fundo.
    praia_background = cv2.bitwise_and(frame_praia, frame_praia, mask=mask_inv)

    #Somatório dos vídeos com suas máscaras aplicadas resultarão no vídeo final com o Keying aplicado.
    result = cv2.addWeighted(praia_background, 1, webcam_foreground, 1, 0)

    #Exibe o vídeo final e se apertarem a tecla 'q', fecha a tela.
    cv2.imshow('Result', result)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

#Libera e destrói as janelas.
video_webcam.release()
video_praia.release()

cv2.destroyAllWindows()
