# -*- coding: utf-8 -*-
"""
Created on Tue Jan 27 11:36:43 2026

@author: metra
"""
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re

def parsear_fecha_texto(texto):
    """ Busca cualquier fecha en formato DD/MM/YYYY o DD Mes YYYY """
    texto = texto.lower()
    meses = {
        "ene": "01", "jan": "01", "enero": "01", "feb": "02", "febrero": "02",
        "mar": "03", "marzo": "03", "abr": "04", "abril": "04", "may": "05", "mayo": "05",
        "jun": "06", "junio": "06", "jul": "07", "julio": "07", "ago": "08", "agosto": "08",
        "sep": "09", "septiembre": "09", "oct": "10", "octubre": "10",
        "nov": "11", "noviembre": "11", "dic": "12", "diciembre": "12"
    }
    
    # Intentamos sacar el año (2025 o 2026)
    anio = "2025"
    if "2026" in texto: anio = "2026"
    
    # Intentamos sacar el mes
    mes = "01"
    for nombre, numero in meses.items():
        if nombre in texto:
            mes = numero
            break
            
    # Intentamos sacar el día (número de 1 o 2 cifras)
    # Buscamos números que NO sean el año ni la hora (ej: 20:00)
    numeros = re.findall(r'\b\d{1,2}\b', texto)
    dia = "01"
    for n in numeros:
        if int(n) < 32: # Es un día válido
            dia = n.zfill(2)
            break

    return f"{anio}-{mes}-{dia}"

def obtener_primer_concierto(artista):
    print(f"Buscando eventos de: {artista}")

    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    # Trucos anti-bot básicos
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        # 1. BÚSQUEDA 
        driver.get(f"https://www.ticketmaster.es/search?keyword={artista}")
        
        # Aceptar Cookies (Espera corta)
        try:
            boton = WebDriverWait(driver, 4).until(EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler")))
            boton.click()
        except:
            pass

        print("Cargando resultados...")
        time.sleep(5) # Espera  para  React cargue la lista

        # 2. ESTRATEGIA 
        # En vez de buscar una clase, buscamos elementos visuales que contengan texto
        # Buscamos bloques que tengan algo de texto
        posibles_eventos = driver.find_elements(By.XPATH, "//div[contains(@class, 'event')] | //li | //div[contains(@data-testid, 'event')]")
        
        # Si la estrategia anterior falla, cogemos enlaces generales
        if len(posibles_eventos) < 3:
             posibles_eventos = driver.find_elements(By.TAG_NAME, "a")

        print(f" Analizando {len(posibles_eventos)} elementos candidatos...")

        for elemento in posibles_eventos:
            try:
                texto = elemento.text
                # Limpieza rápida
                texto = texto.replace("\n", " ").strip()
                
                # FILTROS PARA SABER SI ES UN CONCIERTO REAL:
                # 1. Tiene que mencionar al artista (o parte del nombre)
                # 2. Tiene que tener un mes (ene, feb, mar...)
                # 3. Tiene que tener texto suficiente
                
                if len(texto) > 20 and any(m in texto.lower() for m in ["ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"]):
                    
                    # Si menciona "entradas" o el nombre del artista, vamos bien
                    if artista.lower() in texto.lower() or "entradas" in texto.lower():
                        
                        # Sacamos fecha
                        fecha = parsear_fecha_texto(texto)
                        
                        # Sacamos ciudad (Buscamos ciudades clave en el texto)
                        ciudades_comunes = ["Madrid", "Barcelona", "Valencia", "Sevilla", "Bilbao", "Málaga", "Zaragoza"]
                        ciudad_encontrada = "España (Ver Web)" # Default
                        
                        for c in ciudades_comunes:
                            if c in texto:
                                ciudad_encontrada = c
                                break
                        
                        # Si no encuentra ciudad común, intenta coger la última palabra antes de una coma (simple)
                        if ciudad_encontrada == "España (Ver Web)" and "," in texto:
                            ciudad_encontrada = texto.split(",")[-1].strip().split()[0]

                        # PRECIO FALSO (Para que el Excel no quede vacío)
                        precio = "Consultar"

                        print("¡EVENTO ENCONTRADO!")
                        print(f"Texto detectado: {texto[:40]}...")
                        print(f"Ciudad: {ciudad_encontrada}")
                        print(f"Fecha:  {fecha}")
                        
                        return ciudad_encontrada, fecha

            except:
                continue # Si un elemento da error, pasamos al siguiente

        print("No encontré ningún evento con fecha clara en la lista.")
        return None, None

    except Exception as e:
        print(f"Error Selenium: {e}")
        return None, None
    finally:
        driver.quit() 
        pass
