"""Servicios disponibles en Software FJ. No utiliza bases de datos."""
from abc import ABC, abstractmethod
from entidades import Entidad
from excepciones import DatoInvalidoError

IMPUESTO = 0.19

class Servicio(Entidad, ABC):
    def __init__(self, codigo, nombre, tarifa_hora, disponible=True):
        super().__init__(codigo)
        if not isinstance(tarifa_hora, (int, float)) or tarifa_hora <= 0:
            raise DatoInvalidoError("La tarifa por hora debe ser un número positivo.")
        self.nombre = nombre.strip() if isinstance(nombre, str) and nombre.strip() else None
        if self.nombre is None:
            raise DatoInvalidoError("El nombre del servicio es obligatorio.")
        self.tarifa_hora = float(tarifa_hora)
        self.disponible = bool(disponible)

    def validar_parametros(self, horas):
        if not isinstance(horas, (int, float)) or isinstance(horas, bool) or horas <= 0:
            raise DatoInvalidoError("La duración debe ser mayor que cero.")
        if not self.disponible:
            from excepciones import ServicioNoDisponibleError
            raise ServicioNoDisponibleError(f"El servicio '{self.nombre}' no está disponible.")

    # Variante flexible del cálculo: permite descuento e impuesto opcionales.
    # En Python se puede simular la sobrecarga mediante parámetros opcionales.
    def calcular_costo(self, horas, descuento=0, incluir_impuesto=False):
        self.validar_parametros(horas)
        if not isinstance(descuento, (int, float)) or not 0 <= descuento <= 100:
            raise DatoInvalidoError("El descuento debe estar entre 0 y 100.")
        subtotal = self.tarifa_hora * horas
        subtotal -= subtotal * (descuento / 100)
        return round(subtotal * (1 + IMPUESTO if incluir_impuesto else 1), 2)

    @abstractmethod
    def describir_servicio(self):
        raise NotImplementedError

    def describir(self):
        return self.describir_servicio()

class ReservaSala(Servicio):
    def __init__(self, codigo, tarifa_hora, capacidad=10, disponible=True):
        super().__init__(codigo, "Reserva de sala", tarifa_hora, disponible)
        if not isinstance(capacidad, int) or capacidad <= 0:
            raise DatoInvalidoError("La capacidad debe ser un entero positivo.")
        self.capacidad = capacidad

    def validar_parametros(self, horas, personas=1):
        super().validar_parametros(horas)
        if not isinstance(personas, int) or personas <= 0 or personas > self.capacidad:
            raise DatoInvalidoError(f"La cantidad de personas debe estar entre 1 y {self.capacidad}.")

    def describir_servicio(self):
        return f"{self.nombre} | Capacidad: {self.capacidad} | Tarifa/hora: ${self.tarifa_hora:,.0f}"

class AlquilerEquipo(Servicio):
    def __init__(self, codigo, tarifa_hora, tipo_equipo="Computador", disponible=True):
        super().__init__(codigo, "Alquiler de equipos", tarifa_hora, disponible)
        if not isinstance(tipo_equipo, str) or not tipo_equipo.strip():
            raise DatoInvalidoError("Debe indicar el tipo de equipo.")
        self.tipo_equipo = tipo_equipo.strip()

    def describir_servicio(self):
        return f"{self.nombre} | Equipo: {self.tipo_equipo} | Tarifa/hora: ${self.tarifa_hora:,.0f}"

class AsesoriaEspecializada(Servicio):
    def __init__(self, codigo, tarifa_hora, especialidad="Tecnología", disponible=True):
        super().__init__(codigo, "Asesoría especializada", tarifa_hora, disponible)
        if not isinstance(especialidad, str) or not especialidad.strip():
            raise DatoInvalidoError("Debe indicar la especialidad.")
        self.especialidad = especialidad.strip()

    def describir_servicio(self):
        return f"{self.nombre} | Especialidad: {self.especialidad} | Tarifa/hora: ${self.tarifa_hora:,.0f}"
