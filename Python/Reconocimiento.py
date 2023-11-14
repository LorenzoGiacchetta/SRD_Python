import cv2
import numpy as np
import pytesseract
from RecorteImg import Recorte
import base64
from flask import *
from config import config
from ValidacionText import Validacion
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'

class Reconocimiento:
    def obtenerPlaca(self, img):
        Recortador = Recorte
        Recorteimg = Recortador.RecorteEsclado(Recortador,img)
        gray = cv2.cvtColor(Recorteimg, cv2.COLOR_BGR2GRAY)
        (canny,image) = self.PintarImagen(Recorteimg)
        cnts = self.Contornos(canny, Recorteimg)
        cv2.drawContours(gray, cnts, -1, (0, 255, 0), 2)
        #cv2.waitKey(0)
        return self.PorcionReconocimiento(self,cnts, Recorteimg)

    def PintarImagen(image, gausP =(3, 3), cannyP = [100, 200], iterations=20):
        # Estblece la procion de reconocimiento
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.blur(gray, gausP)
        binary = cv2.threshold(gray, 170, 255, cv2.THRESH_BINARY)[1]
        #cv2.imshow("binario", binary)
        #cv2.waitKey(0)
        canny = cv2.Canny(binary, cannyP[0], cannyP[1])
        kernel=cv2.getStructuringElement(cv2.MORPH_RECT,(10,8))
        closed1 = cv2.morphologyEx(canny,cv2.MORPH_CLOSE,kernel)
        blur = cv2.blur(closed1, (20, 7))
        binary2 = cv2.threshold(blur, 130, 255, cv2.THRESH_BINARY )[1]
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 3))
        closed2 = cv2.morphologyEx(binary2, cv2.MORPH_OPEN, kernel)

        blur2= cv2.blur(closed2, (15, 20))
        binary3 = cv2.threshold(blur2, 130, 255, cv2.THRESH_BINARY)[1]
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        closed3= cv2.morphologyEx(binary3, cv2.MORPH_CLOSE, kernel, iterations=4)


        return closed3,image

    def Contornos(canny, image):
        cnts,_ = cv2.findContours(canny, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        return cnts
        # CALCULA EL AREA DE ESA PORCION DONDE SE ENCUENTRA LA PATENTE
    def PorcionReconocimiento (self, cnts, image,min_w=10, max_w=1100, min_h=10, max_h=520, ratio=3.6):
        placas = ''
        val = Validacion
        for c in cnts:
            area = cv2.contourArea(c)
            x, y, w, h = cv2.boundingRect(c)
            epsilon = 0.07 * cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, epsilon, True)
            aspect_ratio = float(w) / h
            placa = image[y:y + h, x:x + w]
            #cv2.imshow("roi", placa)
            #cv2.waitKey(0)
            # RECONOCEMOS EL AREA Y LAS ARISTAS DE LA IMAGEN
            if 2.4 <= aspect_ratio <= 5.7:
                aux = self.lecDigitos(placa)
                if val.LimpiarTexto(aux) == True:
                    return aux
                else:
                    return ""
    def lecDigitos(image, psm=7,):
        # EXTRAE EL TEXTO Y LO MUESTRA POR CONSOLA
        # NORMALIZACION DE CARACTERES
        alphanumeric = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        options = "-c tessedit_char_whitelist={}".format(alphanumeric)
        options += " --psm {}".format(psm)
        grayTexto= cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        BinaryTexto = cv2.threshold(grayTexto, 160, 255, cv2.THRESH_BINARY)[1]
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 1 ))
        OpenText = cv2.morphologyEx(BinaryTexto, cv2.MORPH_OPEN, kernel, iterations=1)
        val = Validacion
        try:
            text = pytesseract.image_to_string(OpenText, config=options)
            return val.LimpiarTextoReco(text)
        except Exception:
            return "Error al intentar reconocer"
