import cv2
import numpy as np
import argparse


#Recebe o argumento obrigatório do caminho da imagem.
parser = argparse.ArgumentParser()
parser.add_argument("-i", "--path_image", required=True, help="caminho para a imagem de entrada")
args = vars(parser.parse_args())


# Carrega o vídeo
cap = cv2.VideoCapture(args["path_image"])

# Obtém a resolução do vídeo de entrada
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))

# Obtém a taxa de quadros do vídeo de entrada
fps = cap.get(cv2.CAP_PROP_FPS)

# Define o codec e cria o objeto VideoWriter
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Use o codec 'mp4v'
out = cv2.VideoWriter('output.mp4', fourcc, fps, (frame_width, frame_height))  # Salva como .mp4


while (cap.isOpened()):
    ret, frame = cap.read()
    if ret == True:
        # Converte para cinza
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detecta as bordas
        edges = cv2.Canny(gray, 50, 150, apertureSize=3)

        # O detector de bordas Canny retorna uma imagem em tons de cinza.
        # Precisamos converter isso de volta em uma imagem BGR para salvar no vídeo.
        edges_bgr = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

        # Escreve o frame
        out.write(edges_bgr)

        # Mostra o resultado
        cv2.imshow('edges', edges)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

# Libera tudo se o trabalho estiver concluído
cap.release()
out.release()
cv2.destroyAllWindows()
