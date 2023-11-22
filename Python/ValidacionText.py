import re
class Validacion:
    def LimpiarTexto(cadena):
        patente = re.compile(r"^[a-zA-Z]{3}\d{3}$|^[a-zA-Z]{2}\d{3}[a-zA-Z]{2}$")
        if patente.fullmatch(cadena):
            return 1
        else:
            return 0
    def LimpiarTextoReco(cadena):
        caracteres_especiales = re.compile(r"[^a-zA-Z0-9]")
        cadena = caracteres_especiales.sub("", cadena)
        if len(cadena) not in [6, 7]:
            return ""
        return cadena


