#Importando as bibliotecas
import cv2
import numpy as np

#Leitura dos vídeos a serem utilizados
cap_webcam = cv2.VideoCapture('data/webcam.mp4')
cap_praia = cv2.VideoCapture('data/praia.mp4')

#Início do loop do video para leitura frame a frame
while True:
    #Salva cada frame dos vídeos e se um deles chegar ao final, fecha a janela
    ret_webcam, frame_webcam = cap_webcam.read()
    ret_praia, frame_praia = cap_praia.read()

    if not ret_webcam or not ret_praia:
        break
        
    #Limite de verde a ser aplicado o Keying
    lower_green = np.array([0,110,0], dtype = np.uint8)
    upper_green = np.array([100,255,100], dtype = np.uint8)

    #Cria uma máscara com 1s dentro do limite selecionado e 0 do lado de fora
    mask = cv2.inRange(frame_webcam, lower_green, upper_green)

    #Aplica a máscara no fundo
    praia_background = cv2.bitwise_and(frame_praia, frame_praia, mask = mask)

    #Inverte a máscara para aplicação no vídeo com fundo verde
    mask_inv = np.invert(mask)

    #Aplica a máscara inversa no vídeo com fundo verde
    webcam_foreground = cv2.bitwise_and(frame_webcam, frame_webcam, mask = mask_inv)

    #O vídeo final será o somatorio bit a bit dos vídeos com suas máscaras aplicadas
    result = cv2.addWeighted(praia_background, 1, webcam_foreground, 1, 0)

    #Exibe o vídeo e fecha a janela caso seja apertada a tecla 'q'
    cv2.imshow('Resultado', result)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


#Libera o vídeo e destrói as janelas
cap_webcam.release()
cap_praia.release()

cv2.destroyAllWindows()
