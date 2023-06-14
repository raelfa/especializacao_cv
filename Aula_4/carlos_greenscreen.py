#Importando as bibliotecas
import cv2
import numpy as np

#Carrega os videos nas variáveis
cap_webcam = cv2.VideoCapture('data/carlos_greenscreen.mov')
cap_praia = cv2.VideoCapture('data/praia.mp4')

#Salva o tamanho o arquivo webcam (carlos_greenscreen) para posteriormente redimensionar o arquivo de fundo.
width1 = int(cap_webcam.get(cv2.CAP_PROP_FRAME_WIDTH))
height1 = int(cap_webcam.get(cv2.CAP_PROP_FRAME_HEIGHT))

#Inicia o loop do video
while True:
    #Lê cada frame e um dos vídeos acabar, fechar o player
    ret_webcam, frame_webcam = cap_webcam.read()
    ret_praia, frame_praia = cap_praia.read()

    if not ret_webcam or not ret_praia:
        break

    #Redimensiona o fundo
    frame_praia = cv2.resize(frame_praia, (width1, height1))

    #Define o limites de verde
    lower_green = np.array([0, 40, 0], dtype=np.uint8)
    upper_green = np.array([170, 255, 39], dtype=np.uint8)

    #Cria uma máscara que dá o valor 1 para os valores dentro do limite e zero para os de fora
    mask = cv2.inRange(frame_webcam, lower_green, upper_green)
    # print(mask)

    #Manualmente coloca dentro da máscara os pixels que ficaram além do pano verde
    mask[0:120, 0:] = 1
    mask[120:, 0:450] = 1
    mask[120:, 750:] = 1
    # print(mask)
    mask = np.array(mask, dtype=np.uint8)

    #Aplica a máscara no background
    praia_background = cv2.bitwise_and(frame_praia, frame_praia, mask=mask)

    #Inverte a máscara para retirar o fundo verde de 'carlos_greenscreen'
    mask_inv = np.logical_not(mask).astype(np.uint8)

    #Aplicação da máscara invertida
    webcam_foreground = cv2.bitwise_and(
        frame_webcam, frame_webcam, mask=mask_inv)

    #O resultado é o somantório bia a bit do video do green screen com máscara inverse e do fundo com a máscara.
    result = cv2.addWeighted(praia_background, 1, webcam_foreground, 1, 0)

    #Exibe o vídeo
    cv2.imshow('Resultado', result)

    #Fecha o vídeo ao apertar a tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

#Liberação e destruição das janelas.
cap_webcam.release()
cap_praia.release()

cv2.destroyAllWindows()
