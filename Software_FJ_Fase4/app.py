"""Aplicación gráfica Software FJ - Fase 4 UNAD.
Interfaz construida con Tkinter. Los datos viven en memoria; no usa base de datos.
"""
import tkinter as tk
from tkinter import ttk, messagebox
import logging
from pathlib import Path

from clientes import Cliente
from servicios import ReservaSala, AlquilerEquipo, AsesoriaEspecializada
from gestor import GestorSistema

ROOT = Path(__file__).parent
(ROOT / "logs").mkdir(exist_ok=True)
logging.basicConfig(
    filename=ROOT / "logs" / "sistema.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    encoding="utf-8",
    force=True
)

class SoftwareFJApp(tk.Tk):
    """Ventana principal y formularios de gestión."""

    def __init__(self):
        super().__init__()
        self.title("Software FJ | Gestión de clientes, servicios y reservas")
        self.geometry("1050x720")
        self.minsize(900, 620)
        self.configure(bg="#F3F5F8")
        self.gestor = GestorSistema()
        self._estilos()
        self._construir_interfaz()
        logging.getLogger("SoftwareFJ").info("Aplicación gráfica iniciada.")

    def _estilos(self):
        estilo = ttk.Style(self)
        try:
            estilo.theme_use("clam")
        except tk.TclError:
            pass
        estilo.configure("TNotebook", background="#F3F5F8", borderwidth=0)
        estilo.configure("TNotebook.Tab", padding=(18, 10), font=("Segoe UI", 10, "bold"))
        estilo.configure("Titulo.TLabel", font=("Segoe UI", 20, "bold"), foreground="#17365D")
        estilo.configure("Sub.TLabel", font=("Segoe UI", 10), foreground="#526174")
        estilo.configure("TButton", padding=8, font=("Segoe UI", 9, "bold"))
        estilo.configure("Treeview", rowheight=27, font=("Segoe UI", 9))
        estilo.configure("Treeview.Heading", font=("Segoe UI", 9, "bold"))

    def _construir_interfaz(self):
        encabezado = ttk.Frame(self, padding=(22, 18))
        encabezado.pack(fill="x")
        ttk.Label(encabezado, text="SOFTWARE FJ", style="Titulo.TLabel").pack(anchor="w")
        ttk.Label(encabezado, text="Sistema integral de gestión de clientes, servicios y reservas",
                  style="Sub.TLabel").pack(anchor="w", pady=(4, 0))

        self.estado = tk.StringVar(value="Sistema listo. Los datos se conservan durante esta sesión.")
        ttk.Label(self, textvariable=self.estado, relief="sunken", anchor="w", padding=7).pack(
            side="bottom", fill="x")

        self.tabs = ttk.Notebook(self)
        self.tabs.pack(fill="both", expand=True, padx=20, pady=(0, 18))
        self.tab_clientes = ttk.Frame(self.tabs, padding=16)
        self.tab_servicios = ttk.Frame(self.tabs, padding=16)
        self.tab_reservas = ttk.Frame(self.tabs, padding=16)
        self.tab_eventos = ttk.Frame(self.tabs, padding=16)
        self.tabs.add(self.tab_clientes, text="Clientes")
        self.tabs.add(self.tab_servicios, text="Servicios")
        self.tabs.add(self.tab_reservas, text="Reservas")
        self.tabs.add(self.tab_eventos, text="Resumen")

        self._crear_tab_clientes()
        self._crear_tab_servicios()
        self._crear_tab_reservas()
        self._crear_tab_eventos()

    def _campo(self, padre, texto, fila, columna, variable=None, ancho=25):
        ttk.Label(padre, text=texto).grid(row=fila, column=columna, sticky="w", padx=5, pady=5)
        entrada = ttk.Entry(padre, textvariable=variable, width=ancho)
        entrada.grid(row=fila + 1, column=columna, sticky="ew", padx=5, pady=(0, 8))
        return entrada

    def _tabla(self, padre, columnas, encabezados):
        marco = ttk.Frame(padre)
        marco.pack(fill="both", expand=True, pady=(12, 0))
        tabla = ttk.Treeview(marco, columns=columnas, show="headings")
        for col, titulo in zip(columnas, encabezados):
            tabla.heading(col, text=titulo)
            tabla.column(col, width=140, anchor="w")
        scroll = ttk.Scrollbar(marco, orient="vertical", command=tabla.yview)
        tabla.configure(yscrollcommand=scroll.set)
        tabla.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")
        return tabla

    def _crear_tab_clientes(self):
        ttk.Label(self.tab_clientes, text="Registro de clientes", style="Titulo.TLabel").pack(anchor="w")
        form = ttk.Frame(self.tab_clientes)
        form.pack(fill="x", pady=12)
        self.c_id = tk.StringVar()
        self.c_nombre = tk.StringVar()
        self.c_correo = tk.StringVar()
        self.c_telefono = tk.StringVar()
        for i, (label, var) in enumerate([
            ("Identificación", self.c_id), ("Nombre completo", self.c_nombre),
            ("Correo electrónico", self.c_correo), ("Teléfono", self.c_telefono)
        ]):
            self._campo(form, label, 0, i, var)
            form.columnconfigure(i, weight=1)
        ttk.Button(form, text="Registrar cliente", command=self.registrar_cliente).grid(
            row=2, column=0, columnspan=4, sticky="ew", padx=5, pady=5)
        self.tabla_clientes = self._tabla(self.tab_clientes,
            ("id", "nombre", "correo", "telefono"), ("Identificación", "Nombre", "Correo", "Teléfono"))

    def _crear_tab_servicios(self):
        ttk.Label(self.tab_servicios, text="Catálogo de servicios", style="Titulo.TLabel").pack(anchor="w")
        form = ttk.Frame(self.tab_servicios)
        form.pack(fill="x", pady=12)
        self.s_codigo = tk.StringVar()
        self.s_tipo = tk.StringVar(value="Sala")
        self.s_tarifa = tk.StringVar()
        self.s_detalle = tk.StringVar()
        ttk.Label(form, text="Código").grid(row=0, column=0, sticky="w", padx=5)
        ttk.Entry(form, textvariable=self.s_codigo).grid(row=1, column=0, sticky="ew", padx=5, pady=6)
        ttk.Label(form, text="Tipo de servicio").grid(row=0, column=1, sticky="w", padx=5)
        ttk.Combobox(form, textvariable=self.s_tipo, values=("Sala", "Equipo", "Asesoría"),
                     state="readonly").grid(row=1, column=1, sticky="ew", padx=5, pady=6)
        ttk.Label(form, text="Tarifa por hora (COP)").grid(row=0, column=2, sticky="w", padx=5)
        ttk.Entry(form, textvariable=self.s_tarifa).grid(row=1, column=2, sticky="ew", padx=5, pady=6)
        ttk.Label(form, text="Capacidad / equipo / especialidad").grid(row=0, column=3, sticky="w", padx=5)
        ttk.Entry(form, textvariable=self.s_detalle).grid(row=1, column=3, sticky="ew", padx=5, pady=6)
        for i in range(4):
            form.columnconfigure(i, weight=1)
        ttk.Button(form, text="Agregar servicio", command=self.agregar_servicio).grid(
            row=2, column=0, columnspan=4, sticky="ew", padx=5, pady=5)
        self.tabla_servicios = self._tabla(self.tab_servicios,
            ("codigo", "tipo", "tarifa", "detalle"), ("Código", "Servicio", "Tarifa/hora", "Detalle"))

    def _crear_tab_reservas(self):
        ttk.Label(self.tab_reservas, text="Administración de reservas", style="Titulo.TLabel").pack(anchor="w")
        form = ttk.Frame(self.tab_reservas)
        form.pack(fill="x", pady=12)
        self.r_codigo = tk.StringVar()
        self.r_cliente = tk.StringVar()
        self.r_servicio = tk.StringVar()
        self.r_horas = tk.StringVar(value="1")
        self.r_personas = tk.StringVar(value="1")
        campos = [
            ("Código reserva", self.r_codigo), ("Identificación cliente", self.r_cliente),
            ("Código servicio", self.r_servicio), ("Duración (horas)", self.r_horas),
            ("Personas (solo sala)", self.r_personas)
        ]
        for i, (label, var) in enumerate(campos):
            self._campo(form, label, 0, i, var, 19)
            form.columnconfigure(i, weight=1)
        ttk.Button(form, text="Crear reserva", command=self.crear_reserva).grid(
            row=2, column=0, columnspan=5, sticky="ew", padx=5, pady=5)

        acciones = ttk.Frame(self.tab_reservas)
        acciones.pack(fill="x", pady=5)
        ttk.Button(acciones, text="Confirmar seleccionada", command=lambda: self.cambiar_estado("confirmar")).pack(side="left", padx=4)
        ttk.Button(acciones, text="Cancelar seleccionada", command=lambda: self.cambiar_estado("cancelar")).pack(side="left", padx=4)
        ttk.Button(acciones, text="Procesar seleccionada", command=lambda: self.cambiar_estado("procesar")).pack(side="left", padx=4)
        self.tabla_reservas = self._tabla(self.tab_reservas,
            ("codigo", "cliente", "servicio", "horas", "total", "estado"),
            ("Código", "Cliente", "Servicio", "Horas", "Total COP", "Estado"))

    def _crear_tab_eventos(self):
        ttk.Label(self.tab_eventos, text="Resumen del sistema", style="Titulo.TLabel").pack(anchor="w")
        self.resumen = tk.StringVar()
        ttk.Label(self.tab_eventos, textvariable=self.resumen, style="Sub.TLabel").pack(anchor="w", pady=12)
        ttk.Button(self.tab_eventos, text="Actualizar resumen", command=self.actualizar_resumen).pack(anchor="w")
        ttk.Label(self.tab_eventos, text="Los errores y eventos se registran en logs/sistema.log.",
                  style="Sub.TLabel").pack(anchor="w", pady=10)
        ttk.Button(self.tab_eventos, text="Abrir carpeta de logs", command=self.abrir_logs).pack(anchor="w")
        self.actualizar_resumen()

    def _manejar_error(self, error):
        logging.getLogger("SoftwareFJ").exception("Operación no completada: %s", error)
        self.estado.set(f"Operación no completada: {error}")
        messagebox.showerror("No fue posible completar la operación", str(error))

    def registrar_cliente(self):
        try:
            cliente = Cliente(self.c_id.get(), self.c_nombre.get(), self.c_correo.get(), self.c_telefono.get())
            self.gestor.registrar_cliente(cliente)
            self.tabla_clientes.insert("", "end", values=(cliente.identificador, cliente.nombre, cliente.correo, cliente.telefono))
            self.estado.set(f"Cliente {cliente.nombre} registrado correctamente.")
            self._limpiar((self.c_id, self.c_nombre, self.c_correo, self.c_telefono))
            self.actualizar_resumen()
        except Exception as error:
            self._manejar_error(error)

    def agregar_servicio(self):
        try:
            codigo = self.s_codigo.get().strip()
            tarifa = float(self.s_tarifa.get())
            tipo = self.s_tipo.get()
            detalle = self.s_detalle.get().strip()
            if tipo == "Sala":
                servicio = ReservaSala(codigo, tarifa, int(detalle or "10"))
            elif tipo == "Equipo":
                servicio = AlquilerEquipo(codigo, tarifa, detalle or "Computador")
            else:
                servicio = AsesoriaEspecializada(codigo, tarifa, detalle or "Tecnología")
            self.gestor.agregar_servicio(servicio)
            self.tabla_servicios.insert("", "end", values=(codigo, servicio.nombre, f"${tarifa:,.0f}", detalle or "—"))
            self.estado.set(f"Servicio {codigo} agregado correctamente.")
            self._limpiar((self.s_codigo, self.s_tarifa, self.s_detalle))
            self.actualizar_resumen()
        except Exception as error:
            self._manejar_error(error)

    def crear_reserva(self):
        try:
            reserva = self.gestor.crear_reserva(
                self.r_codigo.get().strip(), self.r_cliente.get().strip(),
                self.r_servicio.get().strip(), float(self.r_horas.get()),
                int(self.r_personas.get() or "1")
            )
            self.tabla_reservas.insert("", "end", iid=reserva.identificador,
                values=(reserva.identificador, reserva.cliente.nombre, reserva.servicio.nombre,
                        reserva.horas, f"${reserva.total:,.0f}", reserva.estado))
            self.estado.set(f"Reserva {reserva.identificador} creada.")
            self._limpiar((self.r_codigo, self.r_cliente, self.r_servicio))
            self.actualizar_resumen()
        except Exception as error:
            self._manejar_error(error)

    def cambiar_estado(self, accion):
        seleccionado = self.tabla_reservas.selection()
        if not seleccionado:
            messagebox.showwarning("Seleccione una reserva", "Primero seleccione una reserva de la tabla.")
            return
        codigo = seleccionado[0]
        reserva = next((r for r in self.gestor.reservas if r.identificador == codigo), None)
        try:
            if accion == "confirmar":
                reserva.confirmar()
            elif accion == "cancelar":
                reserva.cancelar()
            else:
                reserva.procesar()
            valores = list(self.tabla_reservas.item(codigo, "values"))
            valores[-1] = reserva.estado
            self.tabla_reservas.item(codigo, values=valores)
            logging.getLogger("SoftwareFJ").info("Reserva %s: %s", codigo, accion)
            self.estado.set(f"Reserva {codigo}: {reserva.estado}.")
            self.actualizar_resumen()
        except Exception as error:
            self._manejar_error(error)

    def actualizar_resumen(self):
        self.resumen.set(
            f"Clientes registrados: {len(self.gestor.clientes)}    |    "
            f"Servicios disponibles: {len(self.gestor.servicios)}    |    "
            f"Reservas creadas: {len(self.gestor.reservas)}"
        )

    def abrir_logs(self):
        ruta = ROOT / "logs"
        try:
            if os.name == "nt":
                os.startfile(ruta)
            else:
                messagebox.showinfo("Carpeta de registros", str(ruta))
        except Exception as error:
            self._manejar_error(error)

    @staticmethod
    def _limpiar(variables):
        for variable in variables:
            variable.set("")

if __name__ == "__main__":
    import os
    SoftwareFJApp().mainloop()
