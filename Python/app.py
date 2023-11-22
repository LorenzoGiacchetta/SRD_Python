# IMPORTAMOS/INSTALAMOS LIBRERIAS PARA EL USO DEL CODIGO Y RESPECTIVOS COMANDOS

import cv2
import numpy as np
import pytesseract
import base64
from flask import *
from config import config
import Reconocimiento
import ValidacionText
import base64


# DECLARAMOS RUTA DE PYTESSERACT
#pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'

# CREAMOS LA API Y SU ENTORNO

enviroment = config['development']


def create_app(enviroment):
    app = Flask(__name__)
    app.config.from_object(enviroment)
    return app


app = create_app(enviroment)


# EJECUTAMOS EL PROGRAMA DE RECONOCIMIENTO
reco = Reconocimiento.Reconocimiento
vali = ValidacionText.Validacion


# CREAMOS UN METODO POST PARA COMUNICARNOS CON BLAZOR(APPWEB)
@app.route('/api/v1/Validacion', methods=['POST'])
def ValidacionPatente():
    TextoValidar =request.get_data().decode('utf-8')
    return str(vali.LimpiarTexto(TextoValidar))

@app.route('/api/v1/fake/', methods=['POST'])
def obtenerPlacaPostFake():
    return "nvz087"

#@app.route('/api/v1/Validacion/', methods=['POST'])
#def ValidacionPatente():
   # TextoValidar =request.get_data()
   # return vali.LimpiarTexto(TextoValidar)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")

#reco.obtenerPlaca('test')