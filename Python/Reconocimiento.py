import cv2
import numpy as np
import pytesseract
import base64
from flask import *
from config import config


class Reconocimiento:
    def obtenerPlaca(self, img):
        (canny,gray) = self.PintarImagen(img)
        cnts = self.Contornos(canny, img)
        placa = self.PorcionReconocimiento(cnts, gray)
        return self.lecDigitos(placa)

    def PintarImagen(image, blurP =(3, 3), cannyP = [150, 200], iterations=1):
        cv2.imshow("Pintar",image)
        cv2.waitKey(0)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.blur(gray, blurP)
        canny = cv2.Canny(gray, cannyP[0], cannyP[1])
        canny = cv2.dilate(canny, None, iterations)
        return (canny,gray)

    def Contornos(canny, image):
        cnts,_ = cv2.findContours(canny, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(image, cnts, -1, (0, 255, 0), 2)
        return  cnts;
        # CALCULA EL AREA DE ESA PORCION DONDE SE ENCUENTRA LA PATENTE
    def PorcionReconocimiento (cnts, gray):
        for c in cnts:
            area = cv2.contourArea(c)
            x, y, w, h = cv2.boundingRect(c)
            epsilon = 0.07 * cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, epsilon, True)
            # RECONOCEMOS EL AREA Y LAS ARISTAS DE LA IMAGEN
            if len(approx) == 4 and 5000 < area < 70000:
                # print('area=', area)
                # cv2.drawContours(image, [approx], 0, (0, 255, 0), 3)
                aspect_ratio = float(w) / h
                if aspect_ratio > 1.5:
                    placa = gray[y:y + h, x:x + w]
                    return placa
    def lecDigitos(placa, textAux = ""):
        # EXTRAE EL TEXTO Y LO MUESTRA POR CONSOLA
        text = textAux + pytesseract.image_to_string(placa, config='--psm 7')
        return print('PLACA: ', text)
