from pyzbar.pyzbar import decode
from pyzbar.pyzbar import ZBarSymbol
import cv2
import numpy as np

cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret,frame = cap.read()
    if ret == True:
        d = decode(frame)
        if d:
            for barcode in d:
                x,y,w,h = barcode.rect
                cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),2)
                barcodeData = barcode.data.decode('utf-8')
                frame = cv2.putText(frame,barcodeData,(x,y-10),font,.5,(0,0,255),2,cv2.LINE_AA)
        cv2.imshow('frame',frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
