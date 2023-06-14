# Importando as  bibliotecas
import cv2
import numpy as np
import argparse

# Usa o parser para receber o caminho dos inputs e dos outputs
parser = argparse.ArgumentParser()
parser.add_argument("-i", "--path_image_1", required=True,
                    help="caminho para o video a ser aplicado o Keying")
parser.add_argument("-l", "--path_image_2", required=True,
                    help="caminho para o vídeo de fundo")
parser.add_argument("-o", "--path_image_out_1", required=True,
                    help="caminho para a saída do video sem fundo")
parser.add_argument("-u", "--path_image_out_2", required=True,
                    help="caminho para a saída do video final")
args = vars(parser.parse_args())

# Carrega os inputs
cap_webcam = cv2.VideoCapture(args["path_image_1"])
cap_praia = cv2.VideoCapture(args["path_image_2"])

# Altura e largura para o arquivo que gerará o vídeo
width = int(cap_webcam.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap_webcam.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Codec de vídeo
codec = cv2.VideoWriter_fourcc(*'mp4v')

# Um objeto video_writer para cada vídeo a ser gerado, sendo salvo no caminho especificado pelo argparse
video_writer_semfundo = cv2.VideoWriter(
    args["path_image_out_1"], codec, 30, (width, height))
video_writer_final = cv2.VideoWriter(
    args["path_image_out_2"], codec, 30, (width, height))

# Inicia o video
while True:
    # Pega o frame de cada um dos vídeos inputs e quando um deles acabar, fecha a janela
    ret_webcam, frame_webcam = cap_webcam.read()
    ret_praia, frame_praia = cap_praia.read()

    if not ret_webcam or not ret_praia:
        break

    # Define o limite de verde
    lower_green = np.array([0, 110, 0], dtype=np.uint8)
    upper_green = np.array([100, 255, 100], dtype=np.uint8)

    # Aplica a máscara sendo 1 para os pixels dentro do limite e 0 para os fora
    mask = cv2.inRange(frame_webcam, lower_green, upper_green)

    # Aplica a máscara no fundo
    praia_background = cv2.bitwise_and(frame_praia, frame_praia, mask=mask)

    # Faz a máscara inversa para aplicação na imagem a ter o fundo retirado
    mask_inv = np.invert(mask)

    # Retira o fundo da imagem com a máscara inversa
    webcam_foreground = cv2.bitwise_and(
        frame_webcam, frame_webcam, mask=mask_inv)

    # Cria o vídeo final somando os vídeos com suas máscasras aplicadas
    result = cv2.addWeighted(praia_background, 1, webcam_foreground, 1, 0)

    # Exibe o vídeo até que seja apertada a tecla 'q'
    cv2.imshow('Resultado', result)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # Escreve o frame em seus respectivos video_writers
    video_writer_semfundo.write(webcam_foreground)
    video_writer_final.write(result)

# Libera os vídeos e destrói as janelas
cap_webcam.release()
cap_praia.release()
video_writer_semfundo.release()
video_writer_final.release()

cv2.destroyAllWindows()
