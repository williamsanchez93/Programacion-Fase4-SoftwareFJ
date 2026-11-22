# Sistema Integral de Gestión de Clientes, Servicios y Reservas — Software FJ

**Universidad Nacional Abierta y a Distancia (UNAD)**  
**Escuela de Ciencias Básicas, Tecnología e Ingeniería (ECBTI)**  
**Curso:** Programación (213023) — Fase 4: Componente Práctico (Prácticas Simuladas)  
**Estudiante:** William Sánchez  
**Repositorio:** https://github.com/williamsanchez93/Programacion-Fase4-SoftwareFJ

---

## 📌 Descripción e Introducción del Proyecto

Este repositorio contiene la implementación individual completa del **Sistema Integral de Gestión de Clientes, Servicios y Reservas** para la empresa **Software FJ**, desarrollado en Python bajo el paradigma de **Programación Orientada a Objetos (POO)** y un esquema de **manejo avanzado de excepciones** con registro automático de eventos (*logging*).

Con base en las orientaciones académicas del curso para el desarrollo del componente práctico, esta solución fue construida de manera **individual y autónoma**, abordando la totalidad de las especificaciones requeridas en el **Anexo 3** (Módulos 1 al 5), garantizando la estabilidad del software mediante simulaciones de uso real y control de errores sin depender de motores de bases de datos.

---

## 🛠️ Características Principales y Arquitectura de Software

El proyecto se encuentra modularizado en 5 archivos principales interconectados bajo estándares de código limpio y control de versiones:

1. **`modulo_excepciones.py` (Módulo 1 — Base de Excepciones y Logging)**:
   - Jerarquía de excepciones personalizadas herederas de `SoftwareFJException` (`ClienteInvalidoError`, `ServicioNoDisponibleError`, `ReservaInvalidaError`, `ParametroInvalidoError`).
   - Configuración centralizada de `logging` en el archivo `software_fj.log` para el almacenamiento de eventos e incidencias con marcas de tiempo.

2. **`modulo_cliente.py` (Módulo 2 — Gestión de Clientes)**:
   - Aplicación de encapsulación estricta con atributos privados (`__cedula`, `__nombre`, `__correo`, `__telefono`).
   - Validaciones strictly implementadas mediante decoradores `@property` y `@setter` para formato numérico de documento/teléfono, formato de correo con expresiones regulares (*Regex*) y nombramiento formal.

3. **`modulo_servicio.py` (Módulo 3 — Jerarquía de Servicios POO)**:
   - Clase abstracta `Servicio` con métodos abstractos para el cálculo de costo y descripción.
   - Subclases polimórficas: `ServicioSala` (cálculo por horas, aforo y recargo audiovisual), `ServicioEquipo` (alquiler en días y garantía) y `ServicioAsesoria` (multiplicadores según nivel del consultor).

4. **`modulo_reserva.py` (Módulo 4 — Gestión de Reservas)**:
   - Integración de objetos `Cliente` y `Servicio` con estados de reserva (`PENDIENTE`, `CONFIRMADA`, `PROCESADA`, `CANCELADA`).
   - Control explícito del flujo mediante estructuras `try/except/else/finally` para operaciones de confirmación, pago y cancelación.

5. **`modulo_main.py` (Módulo 5 — Script de 10 Simulaciones)**:
   - Ejecución secuencial de **10 operaciones completas** alternando casos de éxito con intentos inválidos que fuerzan la captura de excepciones, demostrando que la aplicación nunca colapsa.

---

## 💻 Instrucciones de Ejecución

1. **Clonar el repositorio**:
   ```bash
   git clone https://github.com/williamsanchez93/Programacion-Fase4-SoftwareFJ
   cd Programacion-Fase4-SoftwareFJ
   ```

2. **Ejecutar la simulación principal**:
   ```bash
   python modulo_main.py
   ```

3. **Verificar el archivo de log**:
   Al ejecutar el programa, se generará o actualizará automáticamente el archivo `software_fj.log` en el directorio raíz.

---

## 📜 Licencia y Marco Académico
Desarrollado para la evaluación de la Fase 4 del curso de Programación (213023) — UNAD 2026.
