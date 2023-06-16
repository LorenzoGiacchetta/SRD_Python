import cv2
import numpy as np
import pytesseract
from Prueba import Recorte
import base64
from flask import *
from config import config

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'

class Reconocimiento:
    def obtenerPlaca(self, img):
        Recortador = Recorte
        Recorteimg = Recortador.RecorteEsclado(Recortador,img)
        (canny,image) = self.PintarImagen(Recorteimg)
        cnts = self.Contornos(canny, Recorteimg)
        placa = self.PorcionReconocimiento(cnts, Recorteimg)
        return self.lecDigitos(placa)

    def PintarImagen(image, gausP =(3, 3), cannyP = [100, 200], iterations=1):
        # Estblece una resolucion fija a la imagen
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        #(3,5)--> 11 de 22 patentes
        # nucleo para poder desenfocar y reducir ruido
        kernelNew = np.ones((3,5), np.float32)/15
        gray = cv2.filter2D(gray, -1,kernelNew)
        cv2.imshow("kerne", gray)
        cv2.waitKey(0)
        #gaussiana = cv2.GaussianBlur(gray, gausP, 10)
        binary = cv2.threshold(gray, 170, 255, cv2.THRESH_BINARY_INV)[1]
        cv2.imshow("binary", binary)
        cv2.waitKey(0)

        canny = cv2.Canny(binary, cannyP[0], cannyP[1])
        canny = cv2.dilate(canny, None, iterations)
        cv2.imshow("canny", canny)
        cv2.waitKey(0)

        return canny,image

    def Contornos(canny, image):
        cnts,_ = cv2.findContours(canny, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        #cv2.drawContours(image, cnts, -1, (0, 255, 0), 2)
        return  cnts;
        # CALCULA EL AREA DE ESA PORCION DONDE SE ENCUENTRA LA PATENTE
    def PorcionReconocimiento (cnts, image,min_w=80, max_w=110, min_h=25, max_h=52, ratio=2.5):

        for c in cnts:
            area = cv2.contourArea(c)
            x, y, w, h = cv2.boundingRect(c)
            epsilon = 0.07 * cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, epsilon, True)
            aspect_ratio = float(w) / h
            # RECONOCEMOS EL AREA Y LAS ARISTAS DE LA IMAGEN
            if len(approx) == 4 and 1000 < area < 10000 and (max_w > w > min_w) and (max_h > h > min_h):
                if aspect_ratio > ratio:
                    placa = image[y:y + h, x:x + w]
                    cv2.imshow("placa", placa)
                    cv2.waitKey(0)
                    return placa
    def lecDigitos(image, textAux = "", psm=7):
        # EXTRAE EL TEXTO Y LO MUESTRA POR CONSOLA
        # NORMALIZACION DE CARACTERES
        alphanumeric = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        options = "-c tessedit_char_whitelist={}".format(alphanumeric)
        options += " --psm {}".format(psm)
        #gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        #Bimg= cv2.threshold(gray, 170, 255, cv2.THRESH_BINARY_INV)[1]
        #cv2.imshow('Bimg', Bimg )
        text = textAux + pytesseract.image_to_string(image, config=options)
        return print('PLACA: ', text)
