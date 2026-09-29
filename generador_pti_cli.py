#!/usr/bin/env python3
import sys

def calcular_voice_pick(gtin: str, lote: str, fecha: str) -> str:
    """
    Calcula el Voice Pick Code de la PTI usando el algoritmo CRC-16.
    """
    cadena = (gtin + lote + fecha).strip()
    crc = 0x0000
    
    for char in cadena:
        crc ^= ord(char)
        for _ in range(8):
            if crc & 1:
                crc = (crc >> 1) ^ 0xA001
            else:
                crc >>= 1
                
    # Convierte a base 10 y toma los últimos 4 dígitos rellenando con ceros si es necesario
    pti_str = str(crc)
    return pti_str[-4:].zfill(4)

def incrementar_consecutivo(consecutivo_str: str) -> str:
    """
    Incrementa un número en formato string manteniendo los ceros a la izquierda.
    Ejemplo: '001' -> '002'
    """
    if not consecutivo_str:
        return ""
    
    longitud = len(consecutivo_str)
    try:
        numero = int(consecutivo_str)
        siguiente_numero = numero + 1
        return str(siguiente_numero).zfill(longitud)
    except ValueError:
        return consecutivo_str

def main():
    print("="*50)
    print("      GENERADOR PTI VOICE PICK (OFFLINE)      ")
    print("="*50)
    
    try:
        gtin = input("1. GTIN (ej. 10850510002011) : ").strip()
        fecha = input("2. Fecha YYMMDD (ej. 260927) : ").strip()
        lote_base = input("3. Lote Base (ej. ABC123)    : ").strip()
        consec_inicial = input("4. Consecutivo inicial (ej. 001): ").strip()
        
        cant_str = input("5. Cantidad de etiquetas     : ").strip()
        cantidad = int(cant_str) if cant_str.isdigit() else 1

        print("\n¿Cómo deseas generar los códigos?")
        print(" [1] Generar lista completa (Tabla)")
        print(" [2] Modo paso a paso (Presionar Enter para el siguiente)")
        modo = input("\nElige una opción (1 o 2): ").strip()

        print("\n" + "="*50)

        consecutivo_actual = consec_inicial

        if modo == '1':
            # Modo Tabla
            print(f"{'LOTE COMPLETO':<25} | {'VOICE PICK'}")
            print("-" * 50)
            
            for _ in range(cantidad):
                lote_completo = lote_base + consecutivo_actual
                voice_code = calcular_voice_pick(gtin, lote_completo, fecha)
                print(f"{lote_completo:<25} | {voice_code}")
                
                consecutivo_actual = incrementar_consecutivo(consecutivo_actual)
                
            print("-" * 50)
            print(f"Se generaron {cantidad} códigos con éxito.\n")
            
        elif modo == '2':
            # Modo Paso a Paso
            for i in range(cantidad):
                lote_completo = lote_base + consecutivo_actual
                voice_code = calcular_voice_pick(gtin, lote_completo, fecha)
                
                print(f"[{i+1}/{cantidad}] Lote actual : {lote_completo}")
                print(f"        Voice Pick  : {voice_code}")
                
                if i < cantidad - 1:
                    # Espera a que el usuario presione Enter para continuar
                    input("\n...Presiona [ENTER] para generar el siguiente (o Ctrl+C para salir)")
                    print("-" * 30)
                
                consecutivo_actual = incrementar_consecutivo(consecutivo_actual)
            
            print("\n¡Secuencia finalizada!\n")
            
        else:
            print("Opción no válida. Ejecuta el script nuevamente.")

    except KeyboardInterrupt:
        print("\n\nOperación cancelada por el usuario. ¡Hasta luego!")
        sys.exit(0)
    except Exception as e:
        print(f"\nOcurrió un error: {e}")

if __name__ == "__main__":
    main()