#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

@author: isaacruiz

SOUNDTRIP - Parte de Isaac Ruiz
Obtiene artistas favoritos usando Last.fm API

"""

import requests

def obtener_artistas_favoritos():
    """
    Obtiene una lista de artistas populares desde Last.fm API
    
    Application name: SoundTrip
    API key: 2b181f36c98c423cb166f7b3c3a4aede
    
    Returns:
        list: Lista de nombres de artistas
    """
    
    print("\n---- OBTENIENDO ARTISTAS DESDE LAST.FM ----")
    
    # API KEY de Last.fm
    API_KEY = "2b181f36c98c423cb166f7b3c3a4aede"
    
    
    url = "http://ws.audioscrobbler.com/2.0/"
    
    params = {
        'method': 'chart.gettopartists',  # Top artistas del momento
        'api_key': API_KEY,
        'format': 'json',
        'limit': 5  # Numero de artistas a obtener
    }
    
    try:
        # Peticion HTTP GET 
        print("Consultando Last.fm API...")
        respuesta = requests.get(url, params=params)
        
        # Verificar codigo de estado 
        if respuesta.status_code == 200:
            # La API devuelve JSON 
            datos = respuesta.json()
            
            # Extraer nombres de artistas
            artistas = []
            for artista in datos['artists']['artist']:
                nombre = artista['name']
                artistas.append(nombre)
                print(f"  - {nombre}")
            
            print(f"\nOK: {len(artistas)} artistas obtenidos\n")
            return artistas
            
        else:
            print(f"ERROR: HTTP {respuesta.status_code}")
            # Datos de backup si falla la API
            return ["Bad Bunny", "Taylor Swift", "Coldplay", "Dua Lipa", "Ed Sheeran"]
            
    except Exception as e:
        print(f"ERROR: {e}")
        # Datos de backup si falla
        print("INFO: Usando artistas de backup")
        return ["Bad Bunny", "Taylor Swift", "Coldplay", "Dua Lipa", "Ed Sheeran"]


# Prueba si ejecutas este archivo directamente
if __name__ == "__main__":
    artistas = obtener_artistas_favoritos()
    print("\nLISTA FINAL DE ARTISTAS:")
    for i, artista in enumerate(artistas, 1):
        print(f"{i}. {artista}")
