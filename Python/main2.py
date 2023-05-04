import cv2
import Reconocimiento
import sys
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'
reco = Reconocimiento.Reconocimiento
img = cv2.imread(sys.argv[1])
print(reco.obtenerPlaca(reco,img))
