import cv2
import numpy as np
import pytesseract

class Recorte:
    #izquierda devuelve, derecha lo que necesita
    def RecorteEsclado(self, img):
        (hI,wI) = self.DatosImagenes(img)
        MatrizReco4 = self.DefinicionRecorte()
        (Vescaladoy,Vescaladox,hR,wR) = self.RecorteRescalado(MatrizReco4,hI,wI)
        (FilaI,FilaF,ColI,ColF) = self.RecorteRectangulo(hR,wR, MatrizReco4, Vescaladoy,Vescaladox)
        return self.RecorteImg(img,FilaI,FilaF,ColI,ColF)
    # Datos de la imagen h y w
    def DatosImagenes(img):
        hI, wI, c = img.shape
        return hI,wI
#definir matris de recorte
    @staticmethod
    def DefinicionRecorte():
    # TOMA 13 PATENETE DE 22
        MatrizReco1 = np.array([[0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0],
                            [0, 1, 1, 1, 0],
                            [0, 1, 1, 1, 0],
                            [0, 1, 1, 1, 0]])

        MatrizReco2 = np.array([[0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 1, 1, 1],
                            [0, 0, 0, 1, 1, 1]])

        MatrizReco3 = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 1, 1, 1, 1, 1, 1, 0],
                            [0, 0, 1, 1, 1, 1, 1, 1, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0]])
    # toma 19 de 22 patentes
        MatrizReco4 = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 1, 1, 1, 1, 1, 1, 1, 0, 0],
                            [0, 1, 1, 1, 1, 1, 1, 1, 0, 0],
                            [0, 1, 1, 1, 1, 1, 1, 1, 0, 0],
                            [0, 1, 1, 1, 1, 1, 1, 1, 0, 0]])

        MatrizReco5 = np.array([[0, 0, 0, 0, 0],
                            [0, 1, 1, 1, 0],
                            [0, 1, 1, 1, 0],
                            [0, 1, 1, 1, 0],
                            [0, 0, 0, 0, 0]])
        return MatrizReco4
    #ingresar la matris que queres recortar y el escalado sobre la imagen
    def RecorteRescalado(MatrizReco4,hI,wI):
        hR, wR = MatrizReco4.shape
        Vescaladox = int(wI / wR)
        Vescaladoy = int(hI / hR)
        return Vescaladoy,Vescaladox,hR,wR
#busqueda de 1 en la matriz de recorte y rescalado
    def RecorteRectangulo(hR,wR, MatrizReco4, Vescaladoy,Vescaladox):
        valoresx = []
        valoresy = []
        for i in range(hR):
            for j in range(wR):
                if (MatrizReco4[i, j] == 1):
                    valoresx.append(i)
                    valoresy.append(j)

        FilaI = valoresx[0] * Vescaladox
        FilaF = valoresx[-1] * Vescaladoy
        ColI = valoresy[0] * Vescaladox
        ColF = valoresy[-1] * Vescaladoy
        return FilaI,FilaF,ColI,ColF
    # recorte de la imagen
    def RecorteImg (img,FilaI,FilaF,ColI,ColF ):
        # imagen[fila inicial : fila final, columna inicial : columna final]
        # buscar las dimenciones de la matriz reco en la IMAGEN
        # cada cuadradito de la matriz de recorte, se escala en segun la imagen
        placa = img[FilaI:FilaF, ColI: ColF]
        return placa





