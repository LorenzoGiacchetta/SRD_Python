# IMPORTAMOS/INSTALAMOS LIBRERIAS PARA EL USO DEL CODIGO Y RESPECTIVOS COMANDOS

import cv2
import pytesseract
import base64
from flask import *
from config import config

# DECLARAMOS RUTA DE PYTESSERACT
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'

# CREAMOS LA API Y SU ENTORNO

enviroment = config['development']


def create_app(enviroment):
    app = Flask(__name__)
    app.config.from_object(enviroment)
    return app


app = create_app(enviroment)


# EJECUTAMOS EL PROGRAMA DE RECONOCIMIENTO

def obtenerPlaca(file):
    text = ""

    # CODIFICALA IMAGEN EN BASE64
    file.save('img/temp.jpg')
    # with open('img/temp.jpg', "rb") as image2string:
    #     string = base64.b64encode(image2string.read())

    # GUARDA EL CODIGO EN UN NUEVO ARCHIVO
    # with open('patAux.bin', "wb") as file:
    #     file.write(string)
    #
    # # LEE EL ARCHIVO
    # file = open('patAux.bin', 'rb')
    # byte = file.read()
    file.close()

    # DECODIFICA EL CODIGO EN BASE64 Y LO CONVIERTE EN IMAGEN NUEVAMENTE
    # decodeit = open('img/patAux.jpg', 'wb')
    # decodeit.write(base64.b64decode(byte))
    # decodeit.close()

    # LEE LA IMAGEN
    image = cv2.imread('img/temp.jpg')
    # b = cv2.imread('img/fotoN3.jpg')

    # CAMBIAMOS EL COLOR DE LA IMAGEN A BLANCO Y NEGRO
    # for i, img_nm in enumerate(image):
    #     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    #     (h, w) = gray.shape[:2]
    #     if i == 0:
    #         thr = gray
    #     else:
    #         if i == 0:
    #             thr = gray
    #         gray = cv2.resize(gray, (w * 3, h * 3))
    #         erd = cv2.erode(gray, None, iterations=1)
    #         if i == len(image) - 1:
    #             thr = cv2.threshold(erd, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    #         else:
    #             thr = cv2.threshold(erd, 255, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    #     bnt = cv2.bitwise_not(thr)

        # BUSCA LA PATENTE Y HACE UN RECORTE DE LA IMAGEN
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.blur(gray, (3, 3))
    canny = cv2.Canny(gray, 150, 200)
    canny = cv2.dilate(canny, None, iterations=1)
    cnts,_ = cv2.findContours(canny, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(image, cnts, -1, (0, 255, 0), 2)

    # CALCULA EL AREA DE ESA PORCION DONDE SE ENCUENTRA LA PATENTE
    for c in cnts:
        area = cv2.contourArea(c)
        x, y, w, h = cv2.boundingRect(c)
        epsilon = 0.07 * cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, epsilon, True)

        # RECONOCEMOS EL AREA Y LAS ARISTAS DE LA IMAGEN
        if len(approx) == 4 and 8000 < area < 70000:
            #print('area=', area)
            #cv2.drawContours(image, [approx], 0, (0, 255, 0), 3)
            aspect_ratio = float(w) / h
            if aspect_ratio > 1.5:
                placa = gray[y:y + h, x:x + w]

                # EXTRAE EL TEXTO Y LO MUESTRA POR CONSOLA
                text = text + pytesseract.image_to_string(placa, config='--psm 11')
                print('PLACA: ', text)

                # CREAMOS DOS VENTANAS UNA CON EL RECORTE DE LA PATENTE
                # Y OTRA CON EL TEXTO QUE SE EXTRAJO
                cv2.imshow('PLACA', placa)
                cv2.moveWindow('PLACA', 10, 10)

                #cv2.putText(b, "Patente:", (0, 50), 1, 2, (255, 255, 255), 3)
                #cv2.putText(b, text, (140, 50), 1, 2, (255, 255, 255), 3)

    #cv2.imshow('Placa', b)
    #cv2.moveWindow('Placa', 200, 10)
    cv2.waitKey(0)

    # DEVOLVEMOS EL TEXTO QUE EXTRAE PYTESSERACT A LA VARIABLE

    if text != "":
        return text
    else:
        return "ERROR"

    # CREAMOS UNA SIMULACION DE UN METODO POST PARA RECIBIR UNA BASE64 Y DEVOLVER EL TEXTO
    # EL METODO POST LO QUE HACE ES SOLICITAR ALGO EN ESTE CASO EL TEXTO, Y ENVIA LA FOTO CODIFICADA EN BASE 64


@app.route('/api/v1/patente/', methods=['POST'])
def obtenerPlacaPost():
    #test = request.files['patente'].read()
    return jsonify(obtenerPlaca(request.files['patente']))


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")

#obtenerPlaca('test')