# -*- coding: utf-8 -*-
"""
Created on Tue Jan 27 12:08:34 2026

@author: metra
"""


import csv 

# --- IMPORTACIÓN DE MÓDULOS ---
try:
    # 1. Traemos la función falsa de Spotify
    from spotify import obtener_artistas_favoritos
    # 2. Traemos TU función de conciertos (la que acabas de arreglar)
    from conciertos import obtener_primer_concierto
    # 3. Traemos TU función de vuelos (la de Kayak)
    from vuelos2 import obtener_precio_kayak 
except ImportError as e:
    print(f"ERROR: Falta un archivo. {e}")
    exit()

def main():
    print("\n" + "="*60)
    print("SOUNDTRIP: GENERADOR DE VIAJES MUSICALES")
    print("="*60)

    # 1. OBTENER ARTISTAS (INTEGRANTE 1)
    artistas = obtener_artistas_favoritos()
    
    # Preparamos una lista para guardar todo lo que encontremos
    agenda_viajes = []

    # 2. BUCLE PRINCIPAL (INTEGRANTE 2)
    print("\n" + "-"*60)
    print("INICIANDO BÚSQUEDA DE EVENTOS Y VUELOS")
    print("-" * 60)

    for artista in artistas:
        print(f"\n PROCESANDO: {artista.upper()}")
        
        # --- FASE A: BUSCAR CONCIERTO ---
        ciudad, fecha = obtener_primer_concierto(artista)
        
        if ciudad and fecha:
            # Si encontramos concierto, buscamos vuelo
            print(f" Concierto confirmado: {ciudad} ({fecha})")
            print(f" Buscando vuelos a {ciudad}...")
            
            # --- FASE B: BUSCAR VUELO ---
            # Llamamos a tu script de vuelos
            try:
                precio_vuelo = obtener_precio_kayak(ciudad, fecha)
            except Exception as e:
                precio_vuelo = "Error Vuelo"
                print(f"Falló la búsqueda de vuelo: {e}")

            # Guardamos el resultado en memoria
            resultado = {
                "Artista": artista,
                "Destino": ciudad,
                "Fecha": fecha,
                "Vuelo (Ida)": precio_vuelo
            }
            agenda_viajes.append(resultado)
            print(f" Precio Vuelo detectado: {precio_vuelo}")
            
        else:
            print(f" No se encontraron giras activas para {artista}.")

    # 3. RESULTADOS FINALES Y EXPORTACIÓN
    print("\n" + "="*60)
    print("RESUMEN FINAL DEL PROYECTO")
    print("="*60)
    
    # Imprimir tabla bonita en consola
    print(f"{'ARTISTA':<15} | {'DESTINO':<15} | {'FECHA':<12} | {'PRECIO VUELO':<12}")
    print("-" * 60)
    
    for viaje in agenda_viajes:
        print(f"{viaje['Artista']:<15} | {viaje['Destino']:<15} | {viaje['Fecha']:<12} | {viaje['Vuelo (Ida)']:<12}")
        
    # Guardar en un archivo CSV (que se abre con Excel)
    try:
        with open('resultados_soundtrip.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=["Artista", "Destino", "Fecha", "Vuelo (Ida)"])
            writer.writeheader()
            writer.writerows(agenda_viajes)
        print("\n Archivo 'resultados_soundtrip.csv' generado correctamente.")
    except Exception as e:
        print(f"\n No se pudo guardar el Excel: {e}")

    print("="*60)
    print(" EJECUCIÓN FINALIZADA")

if __name__ == "__main__":
    main()