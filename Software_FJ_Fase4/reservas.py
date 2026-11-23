"""Creación, confirmación, cancelación y procesamiento de reservas."""
from entidades import Entidad
from excepciones import ReservaInvalidaError, OperacionNoPermitidaError

class Reserva(Entidad):
    ESTADOS = ("Pendiente", "Confirmada", "Cancelada", "Procesada")

    def __init__(self, codigo, cliente, servicio, horas, personas=1):
        super().__init__(codigo)
        if cliente is None:
            raise ReservaInvalidaError("La reserva requiere un cliente.")
        if servicio is None:
            raise ReservaInvalidaError("La reserva requiere un servicio.")
        servicio.validar_parametros(horas, personas) if servicio.__class__.__name__ == "ReservaSala" else servicio.validar_parametros(horas)
        self.cliente = cliente
        self.servicio = servicio
        self.horas = horas
        self.personas = personas
        self.estado = "Pendiente"
        self.total = servicio.calcular_costo(horas)

    def confirmar(self):
        if self.estado != "Pendiente":
            raise OperacionNoPermitidaError("Solo se pueden confirmar reservas pendientes.")
        self.estado = "Confirmada"
        return self.estado

    def cancelar(self):
        if self.estado == "Procesada":
            raise OperacionNoPermitidaError("No se puede cancelar una reserva procesada.")
        if self.estado == "Cancelada":
            raise OperacionNoPermitidaError("La reserva ya está cancelada.")
        self.estado = "Cancelada"
        return self.estado

    def procesar(self):
        if self.estado != "Confirmada":
            raise OperacionNoPermitidaError("La reserva debe estar confirmada antes de procesarse.")
        self.estado = "Procesada"
        return self.estado

    def describir(self):
        return (f"Reserva {self.identificador} | Cliente: {self.cliente.nombre} | "
                f"Servicio: {self.servicio.nombre} | Horas: {self.horas} | "
                f"Total: ${self.total:,.2f} | Estado: {self.estado}")
