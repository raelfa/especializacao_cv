import cv2
import numpy as np

threshold = 13

video_webcam = cv2.VideoCapture('data/webcam.mp4')
video_praia = cv2.VideoCapture('data/praia.mp4')
fundo = cv2.imread('fundo_teste_2.png')

width1 = int(video_webcam.get(cv2.CAP_PROP_FRAME_WIDTH))
height1 = int(video_webcam.get(cv2.CAP_PROP_FRAME_HEIGHT))

fundo = cv2.resize(fundo, (width1, height1))
fundo = cv2.cvtColor(fundo, cv2.COLOR_BGR2GRAY)

while True:

    ret_webcam, frame_webcam = video_webcam.read()
    ret_praia, frame_praia = video_praia.read()

    if not ret_webcam or not ret_praia:
        break

    gray_webcam = cv2.cvtColor(frame_webcam, cv2.COLOR_BGR2GRAY)
    gray_praia = cv2.cvtColor(frame_praia, cv2.COLOR_BGR2GRAY)

    diff = cv2.absdiff(gray_webcam, fundo)

    _, mask = cv2.threshold(diff, threshold, 255, cv2.THRESH_BINARY)

    webcam_foreground = cv2.bitwise_and(frame_webcam, frame_webcam, mask=mask)

    mask_inv = np.invert(mask)

    praia_background = cv2.bitwise_and(frame_praia, frame_praia, mask=mask_inv)

    result = cv2.addWeighted(praia_background, 1, webcam_foreground, 1, 0)

    cv2.imshow('Result', result)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_webcam.release()
video_praia.release()

cv2.destroyAllWindows()
