"""Gestión y validación de clientes."""
import re
from entidades import Entidad
from excepciones import DatoInvalidoError

class Cliente(Entidad):
    def __init__(self, identificacion, nombre, correo, telefono):
        super().__init__(identificacion)
        self.nombre = self._validar_texto(nombre, "nombre")
        self.correo = self._validar_correo(correo)
        self.telefono = self._validar_telefono(telefono)

    @staticmethod
    def _validar_texto(valor, campo):
        if not isinstance(valor, str) or not valor.strip():
            raise DatoInvalidoError(f"El {campo} es obligatorio.")
        return valor.strip()

    @staticmethod
    def _validar_correo(correo):
        if not isinstance(correo, str) or not re.fullmatch(
            r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", correo.strip()
        ):
            raise DatoInvalidoError("El correo electrónico no tiene un formato válido.")
        return correo.strip().lower()

    @staticmethod
    def _validar_telefono(telefono):
        limpio = re.sub(r"\D", "", str(telefono))
        if len(limpio) < 7 or len(limpio) > 15:
            raise DatoInvalidoError("El teléfono debe contener entre 7 y 15 dígitos.")
        return limpio

    def describir(self):
        return f"Cliente {self.nombre} | ID: {self.identificador} | Correo: {self.correo}"

    def __str__(self):
        return self.describir()
