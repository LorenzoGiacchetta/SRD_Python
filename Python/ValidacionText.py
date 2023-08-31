import re
class Validacion:
    def LimpiarTexto(cadena):
        caracteres_especiales = re.compile(r"[^a-zA-Z0-9]")
        cadena = caracteres_especiales.sub("", cadena)
        if len(cadena) not in [6, 7]:
            return False
        return True
    def LimpiarTextoReco(cadena):
        caracteres_especiales = re.compile(r"[^a-zA-Z0-9]")
        cadena = caracteres_especiales.sub("", cadena)
        if len(cadena) not in [6, 7]:
            return ""
        return cadena

