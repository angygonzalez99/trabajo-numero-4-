# Software FJ — Fase 4, Programación (UNAD)

## Descripción
Aplicación de consola para gestionar clientes, servicios y reservas de la empresa ficticia Software FJ. El proyecto aplica programación orientada a objetos y manejo de excepciones.

## Requisitos
- Python 3.9 o superior.
- No requiere instalar paquetes externos.
- No utiliza bases de datos. Los datos se mantienen en listas durante la ejecución.
- El archivo `logs/sistema.log` almacena eventos y errores.

## Ejecución
Desde la carpeta del proyecto, ejecutar:

```bash
python main.py
```

## Estructura
- `entidades.py`: clase abstracta Entidad.
- `clientes.py`: clase Cliente y validaciones.
- `servicios.py`: clase abstracta Servicio y tres servicios concretos.
- `reservas.py`: ciclo de vida de las reservas.
- `excepciones.py`: excepciones personalizadas.
- `gestor.py`: listas en memoria y operaciones de gestión.
- `main.py`: ejecución de 14 pruebas demostrativas.
- `logs/`: archivo de eventos y errores.

## Conceptos aplicados
- Abstracción: clases abstractas `Entidad` y `Servicio`.
- Herencia: `Cliente` y los servicios especializados heredan de sus clases base.
- Encapsulación: atributos internos y propiedades.
- Polimorfismo: cada servicio implementa su propia descripción.
- Variantes de cálculo: `calcular_costo` admite descuento e impuesto mediante parámetros opcionales. Python permite este patrón para ofrecer distintas formas de invocar una operación.
- Excepciones: bloques `try/except/else/finally`, excepciones personalizadas y encadenamiento con `raise ... from error`.
- Registro: módulo `logging` para guardar eventos y errores.

## Pruebas
Al ejecutar `main.py` se simulan 14 operaciones, incluyendo registros válidos e inválidos, creación de servicios, reservas exitosas y fallidas, confirmación, cancelación y procesamiento.

## Publicación en GitHub
1. Crear un repositorio en GitHub.
2. Subir todos los archivos y carpetas del proyecto.
3. Copiar la URL del repositorio.
4. Pegar la URL en el documento académico antes de exportarlo o entregarlo.

## Nota académica
El sistema es una simulación educativa. No procesa pagos reales ni utiliza almacenamiento persistente para clientes, servicios o reservas.
