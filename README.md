# Software FJ — Sistema Integral de Gestión de Clientes, Servicios y Reservas

**Grupo 213023_511** · Curso **Programación (213023)** · UNAD · Fase 4 – Componente práctico – Prácticas simuladas

Sistema orientado a objetos en Python, **sin base de datos**, que gestiona los clientes, los servicios
(reserva de salas, alquiler de equipos y asesorías especializadas) y las reservas de la empresa Software FJ.
Implementa abstracción, herencia, polimorfismo y encapsulación, y tiene manejo avanzado de excepciones:
cada error queda registrado en un archivo de logs y la aplicación nunca se detiene.

## Cómo ejecutarlo

Requisito: Python 3.10 o superior (no usa librerías externas).

```bash
python main.py          # Menú interactivo
python simulacion.py    # Simulación automática de 29 operaciones válidas e inválidas
```

Los eventos y errores se guardan en `logs.txt`, que se crea al ejecutar el programa.

## Estructura del proyecto y responsables

| Archivo | Contenido | Responsable |
|---|---|---|
| `excepciones.py` | Jerarquía de excepciones personalizadas (`SoftwareFJError` y sus derivadas) | Integrante 1 |
| `logger.py` | Registro de eventos en `logs.txt` y ejecución segura de operaciones | Integrante 1 |
| `base.py` | Clase abstracta `EntidadBase` (ID, fecha de creación, `describir()` y `validar()`) | Integrante 2 |
| `cliente.py` | Clase `Cliente` con atributos privados, propiedades y validaciones | Integrante 2 |
| `servicios.py` | Clase abstracta `Servicio` y sus derivadas `ReservaSala`, `AlquilerEquipo` y `AsesoriaEspecializada` | Integrante 3 |
| `reserva.py` | Clase `Reserva` (confirmar, cancelar, procesar) y `SistemaGestion` con las listas internas | Integrante 4 |
| `simulacion.py` | Simulación de 29 operaciones válidas e inválidas | Integrante 4 |
| `main.py` | Menú principal interactivo que integra todos los módulos | Integrante 5 |
| `README.md` | Documentación técnica del proyecto | Integrante 5 |

## Diagrama de clases (resumen)

```
EntidadBase (abstracta)                         SoftwareFJError
├── Cliente                                     ├── ClienteInvalidoError        (401)
├── Servicio (abstracta)                        ├── ServicioNoDisponibleError   (404)
│   ├── ReservaSala                             ├── ReservaInvalidaError        (400)
│   ├── AlquilerEquipo                          ├── CalculoInconsistenteError   (422)
│   └── AsesoriaEspecializada                   ├── DatoInvalidoError           (406)
└── Reserva ── usa ──> Cliente y Servicio       ├── ParametroFaltanteError      (412)
                                                ├── ServicioInvalidoError       (409)
SistemaGestion ── listas de ──> Cliente,        └── OperacionNoPermitidaError   (403)
                                Servicio, Reserva
```

## Requisitos del enunciado y dónde se cumplen

| Requisito | Dónde está |
|---|---|
| Clase abstracta para entidades generales | `EntidadBase` en `base.py` |
| Cliente con validaciones y datos encapsulados | `cliente.py`: atributos privados `__nombre`, `__documento`, `__correo`, `__telefono` con propiedades que validan |
| Servicio abstracto + 3 servicios especializados | `servicios.py` |
| Polimorfismo y métodos sobrescritos | Cada servicio sobrescribe `calcular_costo()`, `describir()` y `validar_parametros()` |
| Reserva con confirmación, cancelación y procesamiento | `reserva.py`: `confirmar()`, `cancelar()`, `procesar()` |
| Métodos sobrecargados | `calcular_costo(duracion, impuesto=None, descuento=None)` con parámetros opcionales y `cotizar()` con `@singledispatchmethod` (acepta número, tupla o diccionario) |
| Excepciones personalizadas | `excepciones.py` (8 clases derivadas de `SoftwareFJError`) |
| `try/except` | `SistemaGestion.registrar_cliente()` y `crear_servicio()` |
| `try/except/else` | `Reserva.confirmar()` |
| `try/except/finally` | `Reserva.cancelar()` |
| `try/except/else/finally` | `registrar_evento()`, `Reserva.procesar()` y `SistemaGestion.ejecutar()` |
| Encadenamiento (`raise ... from ...`) | Duración en letras, tipo de servicio inexistente, impuesto mal escrito, datos de cliente inválidos, fallo al escribir el log |
| Archivo de logs | `logger.py` → `logs.txt` |
| Listas internas, sin base de datos | `SistemaGestion._clientes`, `_servicios`, `_reservas` |
| Al menos 10 operaciones, válidas e inválidas | `simulacion.py` (29 operaciones) |
| El sistema no se detiene ante errores | `procesar_operacion_segura()` en el menú y `SistemaGestion.ejecutar()` en la simulación |

## Nota sobre la sobrecarga en Python

Python no permite definir dos métodos con el mismo nombre y distintos parámetros, como Java o C#.
Por eso la sobrecarga se logra de dos formas propias del lenguaje:

1. **Parámetros opcionales:** `calcular_costo(2)`, `calcular_costo(2, impuesto=0.19)`,
   `calcular_costo(2, descuento=0.1)` o `calcular_costo(2, 0.19, 0.1)`.
2. **`functools.singledispatchmethod`:** `cotizar(4)`, `cotizar((4, 0.15))` y
   `cotizar({"duracion": 4, "personas": 10})` ejecutan versiones distintas del método según el tipo del argumento.
