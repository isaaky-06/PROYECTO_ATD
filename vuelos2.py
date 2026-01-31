# -*- coding: utf-8 -*-
"""
27/1/2026

Creador:Iker Pérez del Olmo

Este programa implementa selenium para obtener el precio del vuelo más barato
a la ciudad y la fecha introducidas.
"""
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def obtener_precio_kayak(destino, fecha):
    # 1. PREPARAR URL LIMPIA DE KAYAK
    origen_code = "VLC"
    destino_code = destino.upper()[:3] 
    
    # Si la ciudad es Londres, el código genérico es LON. Si es París, PAR.
    if destino.lower() in ["londres", "london"]: destino_code = "LON"
    if destino.lower() in ["parís", "paris"]: destino_code = "PAR"
    
    print(f"Construyendo ruta para Kayak: {origen_code} -> {destino_code}")

    # URL directa: kayak.es/flights/ORIGEN-DESTINO/FECHA
    url = f"https://www.kayak.es/flights/{origen_code}-{destino_code}/{fecha}"
    
    # 2. MODO FURTIVO (STEALTH)
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    # Trucos para ocultar que es Selenium
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        driver.get(url)

        # 3. GESTIÓN DE COOKIES / ANTI-BOT
        try:
            
            time.sleep(3)
            botones = driver.find_elements(By.XPATH, "//button[contains(., 'Aceptar') or contains(., 'Accept')]")
            if botones:
                botones[0].click()
                print("Cookies aceptadas (intento automático).")
        except:
            pass

        # --- PAUSA TÁCTICA (HUMAN IN THE LOOP) ---
        WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[contains(text(), '€')] | //span[contains(text(), '€')]")))
        time.sleep(2)

        # 4. LEER EL PRECIO
        print("Buscando el precio más barato...")
        
        elementos_precio = driver.find_elements(By.XPATH, "//div[contains(@class, 'price')]//div[contains(text(), '€')]")
        
        if not elementos_precio:
            # Plan B: Buscar cualquier texto grande que tenga €
            elementos_precio = driver.find_elements(By.XPATH, "//span[contains(text(), '€')]")

        precios_nums = []
        for elem in elementos_precio:
            txt = elem.text.strip().replace('.', '').replace('€', '').strip()
            if txt.isdigit():
                valor = int(txt)
                if valor > 10: # Filtramos precios falsos o de maletas
                    precios_nums.append(valor)

        if precios_nums:
            mejor_precio = min(precios_nums)
            print(f"El vuelo más barato es: {mejor_precio} €")
            return f"{mejor_precio} €"
        else:
            print("No pude leer números. Quizás cambió el diseño.")
            return "Consultar manual"

    except Exception as e:
        print(f"Error: {e}")
        return "Error"
    finally:
        driver.quit()

   