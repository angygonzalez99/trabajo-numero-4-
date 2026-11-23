"""Punto de entrada y demostración de 12 operaciones del sistema Software FJ."""
import logging
from pathlib import Path
from clientes import Cliente
from servicios import ReservaSala, AlquilerEquipo, AsesoriaEspecializada
from gestor import GestorSistema
from excepciones import ErrorSistema

def configurar_logs():
    carpeta = Path(__file__).parent / "logs"
    carpeta.mkdir(exist_ok=True)
    logging.basicConfig(
        filename=carpeta / "sistema.log",
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
        encoding="utf-8",
        force=True
    )
    logging.getLogger("SoftwareFJ").info("Inicio del sistema.")

def ejecutar_prueba(numero, descripcion, accion):
    print(f"\\nPRUEBA {numero}: {descripcion}")
    try:
        resultado = accion()
    except Exception as error:
        logging.getLogger("SoftwareFJ").exception("Prueba %s fallida: %s", numero, error)
        print(f"ERROR CONTROLADO: {error}")
        return None
    else:
        print(f"RESULTADO: {resultado}")
        return resultado
    finally:
        print("Ejecución de la prueba finalizada.")

def main():
    configurar_logs()
    gestor = GestorSistema()
    print("=" * 65)
    print(" SISTEMA INTEGRAL DE GESTIÓN - SOFTWARE FJ")
    print("=" * 65)

    ejecutar_prueba(1, "Registrar cliente válido",
        lambda: gestor.registrar_cliente(Cliente("1001", "Laura Gómez", "laura@email.com", "3001234567")))

    ejecutar_prueba(2, "Intentar registrar cliente con correo inválido",
        lambda: gestor.registrar_cliente(Cliente("1002", "Carlos Ruiz", "correo-invalido", "3101234567")))

    ejecutar_prueba(3, "Registrar segundo cliente válido",
        lambda: gestor.registrar_cliente(Cliente("1003", "Andrés Pérez", "andres@email.com", "3207654321")))

    ejecutar_prueba(4, "Crear servicio de reserva de sala",
        lambda: gestor.agregar_servicio(ReservaSala("S01", 50000, capacidad=20)))

    ejecutar_prueba(5, "Crear servicio de alquiler de equipos",
        lambda: gestor.agregar_servicio(AlquilerEquipo("S02", 18000, "Portátil")))

    ejecutar_prueba(6, "Crear servicio de asesoría especializada",
        lambda: gestor.agregar_servicio(AsesoriaEspecializada("S03", 75000, "Desarrollo de software")))

    ejecutar_prueba(7, "Intentar crear servicio con tarifa negativa",
        lambda: gestor.agregar_servicio(AlquilerEquipo("S04", -1000, "Tablet")))

    reserva_sala = ejecutar_prueba(8, "Crear reserva válida de sala",
        lambda: gestor.crear_reserva("R001", "1001", "S01", 2, personas=8))

    ejecutar_prueba(9, "Crear reserva con duración inválida",
        lambda: gestor.crear_reserva("R002", "1001", "S02", 0))

    reserva_equipo = ejecutar_prueba(10, "Crear reserva válida de equipo",
        lambda: gestor.crear_reserva("R003", "1003", "S02", 3))

    ejecutar_prueba(11, "Confirmar y procesar reserva",
        lambda: (reserva_sala.confirmar(), reserva_sala.procesar(), reserva_sala.describir())
        if reserva_sala else "No se creó la reserva.")

    ejecutar_prueba(12, "Intentar procesar una reserva que sigue pendiente",
        lambda: reserva_equipo.procesar() if reserva_equipo else "No se creó la reserva.")

    ejecutar_prueba(13, "Cancelar reserva pendiente",
        lambda: reserva_equipo.cancelar() if reserva_equipo else "No se creó la reserva.")

    ejecutar_prueba(14, "Intentar confirmar una reserva cancelada",
        lambda: reserva_equipo.confirmar() if reserva_equipo else "No se creó la reserva.")

    print("\\n" + "=" * 65)
    print(f"RESUMEN: {len(gestor.clientes)} clientes, {len(gestor.servicios)} servicios, "
          f"{len(gestor.reservas)} reservas creadas.")
    print("Los eventos y errores se encuentran en logs/sistema.log")
    print("El sistema finalizó las pruebas sin detenerse por los errores controlados.")
    logging.getLogger("SoftwareFJ").info("Fin del sistema.")

if __name__ == "__main__":
    main()
