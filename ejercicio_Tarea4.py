from modelos import (
    Cliente, 
    ReservaSala, 
    AlquilerEquipo, 
    AsesoriaEspecializada, 
    Reserva,
    ClienteNoValidoError,
    ReservaInvalidaError
)
import logging

def ejecutar_simulacion():
    print("=== INICIANDO SIMULACIÓN DE OPERACIONES - SOFTWARE FJ ===")
    
    clientes = []
    servicios = []
    reservas = []

    # Operación 1: Registro correcto de un cliente
    print("\n--- Operación 1: Registro Exitoso de Cliente ---")
    try:
        c1 = Cliente("1098765432", "Ana María Gómez", "ana.gomez@example.com")
    except Exception as e:
        print(f"Error inesperado: {e}")
    else:
        clientes.append(c1)
        print(f"[ÉXITO] {c1.obtener_detalles()}")

    # Operación 2: Registro fallido de cliente (Correo inválido)
    print("\n--- Operación 2: Registro Fallido de Cliente (Correo Inválido) ---")
    try:
        c_fallido = Cliente("987654321", "Carlos Pérez", "carlos-sin-correo.com")
    except ClienteNoValidoError as ce:
        print(f"[CONTROLADO] Error de validación detectado: {ce}")
    except Exception as e:
        print(f"[ERROR INESPERADO] {e}")

    # Operación 3: Creación correcta de un servicio de Salas
    print("\n--- Operación 3: Creación de Servicio (Reserva de Sala) ---")
    try:
        sala = ReservaSala("SALA-01", "Sala de Juntas Principal", 150000.0, 10)
        servicios.append(sala)
        print(f"[ÉXITO] {sala.obtener_detalles()}")
    except Exception as e:
        print(f"Error al crear servicio: {e}")

    # Operación 4: Creación correcta de servicio de Alquiler de Equipos
    print("\n--- Operación 4: Creación de Servicio (Alquiler de Equipos) ---")
    try:
        equipo = AlquilerEquipo("EQ-05", "Kit de Videoconferencia 4K", 40000.0, 3)
        servicios.append(equipo)
        print(f"[ÉXITO] {equipo.obtener_detalles()} | Costo total por 3 horas: ${equipo.calcular_costo()}")
    except Exception as e:
        print(f"Error al crear servicio: {e}")

    # Operación 5: Creación de Asesoría Especializada (Senior)
    print("\n--- Operación 5: Creación de Servicio (Asesoría Especializada Senior) ---")
    try:
        asesoria = AsesoriaEspecializada("ASES-99", "Arquitectura de Software", 200000.0, "Senior")
        servicios.append(asesoria)
        print(f"[ÉXITO] {asesoria.obtener_detalles()} | Costo ajustado (Senior): ${asesoria.calcular_costo()}")
    except Exception as e:
        print(f"Error al crear servicio: {e}")

    # Operación 6: Reserva exitosa
    print("\n--- Operación 6: Creación y Confirmación de Reserva Exitosa ---")
    try:
        reserva1 = Reserva(clientes[0], servicios[0], duracion_horas=2)
        reservas.append(reserva1)
        reserva1.confirmar_reserva()
    except Exception as e:
        print(f"No se pudo completar la reserva: {e}")

    # Operación 7: Reserva fallida (Duración 0)
    print("\n--- Operación 7: Reserva Fallida (Duración Cero) ---")
    try:
        reserva_erronea = Reserva(clientes[0], servicios[1], duracion_horas=0)
        reserva_erronea.confirmar_reserva()
    except ReservaInvalidaError as rie:
        print(f"[CONTROLADO] Excepción de reserva atrapada: {rie}")
    except Exception as e:
        print(f"[ERROR INESPERADO] {e}")

    # Operación 8: Métodos sobrecargados (Descuento e Impuesto)
    print("\n--- Operación 8: Prueba de Métodos Sobrecargados (Costos con Descuento/Impuesto) ---")
    try:
        costo_final = servicios[2].calcular_costo_con_opciones(descuento=0.10, impuesto=0.19)
        print(f"[ÉXITO] Costo calculado con opciones (10% desc, 19% IVA): ${costo_final:.2f}")
    except Exception as e:
        print(f"Error en el cálculo: {e}")

    # Operación 9: Encadenamiento de excepciones
    print("\n--- Operación 9: Simulación de Encadenamiento de Excepciones ---")
    try:
        try:
            servicio_inexistente = servicios[99] 
        except IndexError as inner_error:
            raise ReservaInvalidaError("Fallo crítico: Se intentó asociar un servicio que no existe.") from inner_error
    except ReservaInvalidaError as outer_error:
        logging.error(f"Encadenamiento registrado: {outer_error} | Causa raíz: {outer_error.__cause__}")
        print(f"[CONTROLADO CON ÉXITO] Excepción encadenada atrapada: {outer_error}")
        print(f"-> Causa original: {outer_error.__cause__}")

    # Operación 10: Cancelación de reserva
    print("\n--- Operación 10: Cancelación de Reserva Existente ---")
    try:
        if reservas:
            reservas[0].cancelar_reserva()
            print(f"[ÉXITO] La reserva cambió a estado: {reservas[0].estado}")
    except Exception as e:
        print(f"Error al cancelar: {e}")

    print("\n=== SIMULACIÓN FINALIZADA. REVISA EL ARCHIVO 'sistema_fj.log' ===")

if __name__ == "__main__":
    ejecutar_simulacion()