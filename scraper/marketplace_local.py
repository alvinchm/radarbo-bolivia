#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Extractor Local Asistido para Facebook Marketplace Bolivia (La Paz / Santa Cruz / Cochabamba)
Usa tu propio perfil de navegador en VS Code para que Facebook no bloquee la sesión.
Instalación previa: pip install playwright && playwright install chromium
"""

import json
import os
import re
from playwright.sync_api import sync_playwright

BUSQUEDAS_MARKETPLACE = [
    "RTX 3060 Bolivia",
    "RTX 4060 Bolivia",
    "Ryzen 7 Bolivia",
    "Laptop Gamer RTX Bolivia",
    "Silla ergonomica Bolivia",
    "Audifonos HyperX Bolivia"
]

def capturar_marketplace():
    with sync_playwright() as p:
        # Guarda la sesión en ./fb_session para que solo inicies sesión la primera vez
        browser = p.chromium.launch_persistent_context(
            user_data_dir="./fb_session",
            headless=False
        )
        page = browser.new_page()
        page.goto("https://www.facebook.com/marketplace/")
        print("1. Si es tu primera vez, inicia sesión en Facebook en la ventana abierta.")
        input("2. Cuando veas Marketplace cargado, presiona ENTER en la terminal de VS Code...")

        resultados = []
        for q in BUSQUEDAS_MARKETPLACE:
            print(f"Buscando en Marketplace: {q}")
            page.goto(f"https://www.facebook.com/marketplace/search/?query={q}")
            page.wait_for_timeout(4000)
            enlaces = page.query_selector_all('a[href*="/marketplace/item/"]')
            for a in enlaces[:10]:
                texto = a.inner_text().replace("\n", " · ").strip()
                href = a.get_attribute("href").split("?")[0]
                if re.search(r"Bs|BOB", texto, re.IGNORECASE):
                    resultados.append({"texto": texto, "url": f"https://www.facebook.com{href}"})

        with open("../data/marketplace_capturas.json", "w", encoding="utf-8") as f:
            json.dump(resultados, f, ensure_ascii=False, indent=2)
        print(f"[OK] Se guardaron {len(resultados)} ofertas de Marketplace en data/marketplace_capturas.json")
        browser.close()

if __name__ == "__main__":
    capturar_marketplace()
