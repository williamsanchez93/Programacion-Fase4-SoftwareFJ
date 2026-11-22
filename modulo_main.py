import sys
import logging

from modulo_excepciones import (
    SoftwareFJException,
    ClienteInvalidoError,
    ServicioNoDisponibleError,
    ReservaInvalidaError,
    ParametroInvalidoError,
    logger
)
from modulo_cliente import Cliente
from modulo_servicio import ServicioSala, ServicioEquipo, ServicioAsesoria
from modulo_reserva import Reserva


def ejecutar_simulaciones():
    """
    Ejecuta 10 operaciones secuenciales combinando registros exitosos y
    capturas controladas de excepciones sin interrumpir la ejecución del programa.
    """
    print("="*66)
    print("     SISTEMA INTEGRAL DE GESTION DE CLIENTES, SERVICIOS Y RESERVAS")
    print("                       SOFTWARE FJ - UNAD FASE 4                  ")
    print("="*66)
    print("Inicio del Script de Simulaciones (10 Operaciones Controladas)")
    print("="*66 + "\n")

    logger.info("=== INICIANDO SIMULACION COMPLETA ===")

    # -------------------------------------------------------------------------
    # OPERACIÓN 1: Registro Exitoso de Cliente 1 y Servicio de Sala (VÁLIDO)
    # -------------------------------------------------------------------------
    print("1. OPERACION [VALIDA]: Registro de Cliente 1 y Sala")
    try:
        cliente1 = Cliente("1012345678", "William Sanchez", "william.sanchez@ejemplo.com", "3001234567")
        sala1 = ServicioSala("SAL-10", "Auditorio Central Fj", 70000.0, 120, incluye_audiovisuales=True)
        reserva1 = Reserva("RES-101", cliente1, sala1, "2026-12-15", 6.0)
        print(f"  OK: {cliente1}")
        print(f"  OK: {sala1.obtener_descripcion()} | Total: ${sala1.calcular_costo(6.0):,.2f}\n")
    except SoftwareFJException as e:
        print(f"  ERROR INESPERADO: {e}\n")

    # -------------------------------------------------------------------------
    # OPERACIÓN 2: Confirmación y Procesamiento de Pago Reserva RES-101 (VÁLIDO)
    # -------------------------------------------------------------------------
    print("2. OPERACION [VALIDA]: Confirmacion y Pago Reserva RES-101\n")
    try:
        reserva1.confirmar_reserva()
        print()
        reserva1.procesar_pago(reserva1.costo_total)
        print()
    except SoftwareFJException as e:
        print(f"  ERROR: {e}\n")

    # -------------------------------------------------------------------------
    # OPERACIÓN 3: Intento de Registro con Cédula Alfanumérica (INVÁLIDO)
    # -------------------------------------------------------------------------
    print("3. OPERACION [INVALIDA]: Intento Cedula Alfanumerica")
    try:
        c_err1 = Cliente("10123ABC", "Pedro Gomez", "pedro@correo.com", "3001112233")
    except ClienteInvalidoError as e:
        print(f"  OK Excepcion capturada: {e}\n")

    # -------------------------------------------------------------------------
    # OPERACIÓN 4: Intento de Registro con Correo sin Dominio (INVÁLIDO)
    # -------------------------------------------------------------------------
    print("4. OPERACION [INVALIDA]: Intento Correo Erroneo")
    try:
        c_err2 = Cliente("1098765432", "Maria Rodriguez", "maria_sin_arroba", "3159876543")
    except ClienteInvalidoError as e:
        print(f"  OK Excepcion capturada: {e}\n")

    # -------------------------------------------------------------------------
    # OPERACIÓN 5: Registro de Cliente 2 y Alquiler de Equipo (VÁLIDO)
    # -------------------------------------------------------------------------
    print("5. OPERACION [VALIDA]: Registro Cliente 2 y Alquiler Equipo")
    try:
        cliente2 = Cliente("987654321", "Maria Rodriguez", "maria.rodriguez@ejemplo.com", "3159876543")
        equipo1 = ServicioEquipo("EQ-20", "Equipo Portatil", 150000.0, es_alta_gama=True)
        print(f"  OK: {cliente2}")
        print(f"  OK: {equipo1.obtener_descripcion()} | Total Alquiler: ${equipo1.calcular_costo(5, con_seguro=True):,.2f}\n")
    except SoftwareFJException as e:
        print(f"  ERROR INESPERADO: {e}\n")

    # -------------------------------------------------------------------------
    # OPERACIÓN 6: Intento de Alquilar Sala con Horas Excedidas (>24 hrs) (INVÁLIDO)
    # -------------------------------------------------------------------------
    print("6. OPERACION [INVALIDA]: Sala con Horas Excedidas (30 hrs)")
    try:
        sala_err = ServicioSala("SAL-99", "Sala Excesiva", 50000.0, 50)
        sala_err.calcular_costo(30.0)
    except ServicioNoDisponibleError as e:
        print(f"  OK Excepcion capturada: {e}\n")

    # -------------------------------------------------------------------------
    # OPERACIÓN 7: Intento de Crear Asesoría con Nivel Inexistente (INVÁLIDO)
    # -------------------------------------------------------------------------
    print("7. OPERACION [INVALIDA]: Asesoria con Nivel No Permitido")
    try:
        ase_err = ServicioAsesoria("ASE-99", "Asesoria Basica", 50000.0, nivel_consultor="BASIC")
    except ServicioNoDisponibleError as e:
        print(f"  OK Excepcion capturada: {e}\n")

    # -------------------------------------------------------------------------
    # OPERACIÓN 8: Creación y Cancelación Exitosa de Reserva RES-102 (VÁLIDO)
    # -------------------------------------------------------------------------
    print("8. OPERACION [VALIDA]: Creacion y Cancelacion Reserva RES-102\n")
    try:
        reserva2 = Reserva("RES-102", cliente2, equipo1, "2026-12-20", 5.0)
        reserva2.cancelar_reserva(motivo="Cliente solicita reprogramacion")
        print()
    except SoftwareFJException as e:
        print(f"  ERROR INESPERADO: {e}\n")

    # -------------------------------------------------------------------------
    # OPERACIÓN 9: Intento de Pago para Reserva PENDIENTE sin Confirmar (INVÁLIDO)
    # -------------------------------------------------------------------------
    print("9. OPERACION [INVALIDA]: Pago de Reserva No Confirmada\n")
    try:
        reserva3 = Reserva("RES-103", cliente2, equipo1, "2026-12-22", 3.0)
        reserva3.procesar_pago(reserva3.costo_total)
    except ReservaInvalidaError as e:
        print(f"  OK Excepcion capturada: {e}\n")

    # -------------------------------------------------------------------------
    # OPERACIÓN 10: Registro Cliente 3, Asesoría Master y Flujo Completo (VÁLIDO)
    # -------------------------------------------------------------------------
    print("10. OPERACION [VALIDA]: Registro Cliente 3, Asesoria Master y Pago RES-104")
    try:
        cliente3 = Cliente("1045678910", "Carlos Perez", "carlos.perez@ejemplo.com", "3187654321")
        asesoria1 = ServicioAsesoria("ASE-30", "Asesoria Avanzada", 120000.0, nivel_consultor="MASTER")
        reserva4 = Reserva("RES-104", cliente3, asesoria1, "2026-12-28", 5.0)
        print(f"  OK: {cliente3}")
        print(f"  OK: {asesoria1.obtener_descripcion()} | Total: ${asesoria1.calcular_costo(5.0):,.2f}\n")
        
        reserva4.confirmar_reserva()
        print()
        reserva4.procesar_pago(reserva4.costo_total)
        print()

        print("  --- RESUMEN FINAL RESERVA 104 ---")
        print(reserva4.resumen())
        print()
    except SoftwareFJException as e:
        print(f"  ERROR INESPERADO: {e}\n")

    logger.info("=== SIMULACION FINALIZADA CON EXITO ===")
    print("="*66)
    print(" SIMULACION FINALIZADA CON EXITO. 10 operaciones ejecutadas.")
    print(" Logs guardados en 'software_fj.log'.")
    print("="*66)


if __name__ == "__main__":
    ejecutar_simulaciones()
