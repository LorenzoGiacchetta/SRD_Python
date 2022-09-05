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

    file.save('img/temp.jpg')
    file.close()

    # LEE LA IMAGEN
    image = cv2.imread('img/temp.jpg')

    # CAMBIAMOS EL COLOR DE LA IMAGEN A BLANCO Y NEGRO

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
        if len(approx) == 4 and 5000 < area < 70000:
            #print('area=', area)
            #cv2.drawContours(image, [approx], 0, (0, 255, 0), 3)
            aspect_ratio = float(w) / h
            if aspect_ratio > 1.5:
                placa = gray[y:y + h, x:x + w]

                # EXTRAE EL TEXTO Y LO MUESTRA POR CONSOLA
                text = text + pytesseract.image_to_string(placa, config='--psm 11')
                print('PLACA: ', text)
    cv2.waitKey(0)

    # DEVOLVEMOS EL TEXTO QUE EXTRAE PYTESSERACT AL METODO

    if text != "":
        return text
    else:
        return "ERROR"

# CREAMOS UN METODO POST PARA COMUNICARNOS CON BLAZOR(APPWEB)
@app.route('/api/v1/patente/', methods=['POST'])
def obtenerPlacaPost():
    #test = request.files['patente'].read()
    return jsonify(obtenerPlaca(request.files['patente']))


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")

#obtenerPlaca('test')