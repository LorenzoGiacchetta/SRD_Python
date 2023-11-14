import sys
import cv2
import os
import Reconocimiento
import pytesseract
import numpy as np

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'
reco = Reconocimiento.Reconocimiento
Input_ImagesPath="C:/Users/estudiante/PycharmProjects/E.M.A-Project/Python/img1"

files_names = os.listdir(Input_ImagesPath)
for n in files_names:
    img = cv2.imread(f".\img1\{n}")
    Text = reco.obtenerPlaca(reco ,img)
    print(Text)


