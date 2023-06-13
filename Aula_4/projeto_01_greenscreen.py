import cv2
import numpy as np

cap_webcam = cv2.VideoCapture('data/webcam.mp4')
cap_praia = cv2.VideoCapture('data/praia.mp4')

while True:
    ret_webcam, frame_webcam = cap_webcam.read()
    ret_praia, frame_praia = cap_praia.read()

    if not ret_webcam or not ret_praia:
        break
    
    lower_green = np.array([0,110,0], dtype = np.uint8)
    upper_green = np.array([100,255,100], dtype = np.uint8)

    mask = cv2.inRange(frame_webcam, lower_green, upper_green)

    praia_background = cv2.bitwise_and(frame_praia, frame_praia, mask = mask)

    mask_inv = np.invert(mask)

    webcam_foreground = cv2.bitwise_and(frame_webcam, frame_webcam, mask = mask_inv)

    result = cv2.addWeighted(praia_background, 1, webcam_foreground, 1, 0)

    cv2.imshow('Resultado', result)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    
cap_webcam.release()
cap_praia.release()

cv2.destroyAllWindows()
