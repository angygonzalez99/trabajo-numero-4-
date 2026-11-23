"""Administración en memoria de clientes, servicios y reservas."""
import logging
from excepciones import ClienteDuplicadoError, ServicioNoDisponibleError, ReservaInvalidaError
from reservas import Reserva

class GestorSistema:
    def __init__(self):
        self.clientes = []
        self.servicios = []
        self.reservas = []
        self.logger = logging.getLogger("SoftwareFJ")

    def registrar_cliente(self, cliente):
        if any(c.identificador == cliente.identificador for c in self.clientes):
            raise ClienteDuplicadoError(f"Ya existe el cliente {cliente.identificador}.")
        self.clientes.append(cliente)
        self.logger.info("Cliente registrado: %s", cliente.identificador)
        return cliente

    def agregar_servicio(self, servicio):
        if any(s.identificador == servicio.identificador for s in self.servicios):
            raise ValueError(f"Ya existe el servicio {servicio.identificador}.")
        self.servicios.append(servicio)
        self.logger.info("Servicio agregado: %s", servicio.identificador)
        return servicio

    def crear_reserva(self, codigo, identificacion_cliente, codigo_servicio, horas, personas=1):
        cliente = next((c for c in self.clientes if c.identificador == str(identificacion_cliente)), None)
        servicio = next((s for s in self.servicios if s.identificador == str(codigo_servicio)), None)
        if cliente is None:
            raise ReservaInvalidaError("No se encontró el cliente solicitado.")
        if servicio is None:
            raise ReservaInvalidaError("No se encontró el servicio solicitado.")
        if not servicio.disponible:
            raise ServicioNoDisponibleError("El servicio seleccionado no está disponible.")
        try:
            reserva = Reserva(codigo, cliente, servicio, horas, personas)
        except Exception as error:
            # Encadenamiento: se conserva la causa original para facilitar el diagnóstico.
            raise ReservaInvalidaError("No fue posible crear la reserva.") from error
        self.reservas.append(reserva)
        self.logger.info("Reserva creada: %s", codigo)
        return reserva
