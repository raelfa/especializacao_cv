#Import das bibliotecas
import cv2
import numpy as np

#Ao fazer cv2.VideoCapture(0), o programa acessará a webcam 
cap_webcam = cv2.VideoCapture(0)
#Leitura do vídeo de fundo
cap_praia = cv2.VideoCapture('data/praia.mp4')

#Recebendo os valores de tamanho do vídeo da webcam para redimensionar o fundo
width1 = int(cap_webcam.get(cv2.CAP_PROP_FRAME_WIDTH))
height1 = int(cap_webcam.get(cv2.CAP_PROP_FRAME_HEIGHT))

#Início do loop dp vídeo
while True:
    #Recebe os frames da webcam e do vídeo 
    ret_webcam, frame_webcam = cap_webcam.read()
    ret_praia, frame_praia = cap_praia.read()

    #Se o vídeo da webcam parar, a janela será fechada
    if not ret_webcam:
        break
    #Reinicia o vídeo da praia para este estar em loop
    if not ret_praia:
        # Reiniciar o vídeo da praia para o início
        cap_praia.set(cv2.CAP_PROP_POS_FRAMES, 0)
        ret_praia, frame_praia = cap_praia.read()

    #Redimensiona o fundo
    frame_praia = cv2.resize(frame_praia, (width1, height1))

    #Define os limites de verde
    lower_green = np.array([0, 110, 0], dtype=np.uint8)
    upper_green = np.array([100, 255, 100], dtype=np.uint8)

    # Espelha horizontalmente a imagem da webcam
    frame_webcam = cv2.flip(frame_webcam, 1)

    #Cria uma máscara em que gera 1 para os pixels dentro do limite e 0 para os de fora
    mask = cv2.inRange(frame_webcam, lower_green, upper_green)

    #Aplica a máscara no fundo
    praia_background = cv2.bitwise_and(frame_praia, frame_praia, mask=mask)

    #Inverte a máscara para aplicação na webcam
    mask_inv = np.invert(mask)

    #Aplica a máscara invertida no frame da webcam
    webcam_foreground = cv2.bitwise_and(
        frame_webcam, frame_webcam, mask=mask_inv)

    #O resultado será o somatório da webcam e do fundo com suas máscaras aplicadas.
    result = cv2.addWeighted(praia_background, 1, webcam_foreground, 1, 0)

    #Mostra o vídeo e fecha a janela quando clicar no 'q'
    cv2.imshow('Resultado', result)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

#Libera o vídeo e destrói a janela.
cap_webcam.release()
cap_praia.release()

cv2.destroyAllWindows()
