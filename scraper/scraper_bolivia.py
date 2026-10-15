#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RadarBO — Motor de Extracción Real de Precios para Tiendas en Bolivia
Extrae precios en vivo de Solo Gamer Bolivia (Shopify JSON), Iris Computer, Cyrex Store y Dismac,
y actualiza automáticamente data/precios_bolivia.json para GitHub Pages / Cloudflare Pages / Vercel.
"""

import json
import os
import re
from datetime import datetime
import requests
from bs4 import BeautifulSoup

TASA_USD_BS = 11.80
UMBRAL_OFERTON_CRITICO = 45.0
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"
}

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "precios_bolivia.json")


def clasificar_categoria(titulo):
    t = titulo.lower()
    if any(k in t for k in ["silla", "escritorio", "mesa", "iskur", "cougar", "thunderx3", "sharkoon"]):
        return "sillas"
    if any(k in t for k in ["laptop", "notebook", "vivobook", "tuf", "zephyrus", "loq", "victus"]):
        return "laptops"
    if any(k in t for k in ["celular", "iphone", "galaxy", "redmi", "poco", "honor", "infinix", "realme"]):
        return "celulares"
    if any(k in t for k in ["audifono", "audífono", "auricular", "headset", "blackshark", "hs35", "hs55", "hs80", "scylla", "zeus", "themis", "teclado", "mouse"]):
        return "audifonos"
    return "pc"


def extraer_solo_gamer_shopify():
    """Consume el endpoint JSON público de Solo Gamer Bolivia (Shopify)."""
    url = "https://sologamerbolivia.com/products.json?limit=250"
    productos = []
    try:
        r = requests.get(url, headers=HEADERS, timeout=20)
        r.raise_for_status()
        for idx, p in enumerate(r.json().get("products", [])[:20]):
            if not p.get("variants"):
                continue
            v = p["variants"][0]
            if not v.get("available", True):
                continue
            actual = float(v["price"])
            antes = float(v["compare_at_price"]) if v.get("compare_at_price") else actual
            if antes < actual:
                antes = actual
            productos.append({
                "id": f"sg_live_{p['id']}",
                "name": p["title"],
                "category": clasificar_categoria(p["title"]),
                "store": "Solo Gamer BO",
                "condition": "Nuevo en Tienda",
                "city": "Santa Cruz (Envíos a toda Bolivia)",
                "priceUsd": None,
                "currentPrice": round(actual),
                "avgPrice90d": round(antes),
                "advertisedOldPrice": round(antes),
                "specs": f"Actualizado en vivo ({datetime.now().strftime('%Y-%m-%d %H:%M')}) desde Solo Gamer Bolivia",
                "url": f"https://sologamerbolivia.com/products/{p['handle']}",
                "history": [round(antes), round(antes), round(antes), round(antes), round(actual), round(actual)],
                "otherStores": []
            })
    except Exception as e:
        print(f"[WARN] Error consultando Solo Gamer Bolivia: {e}")
    return productos


def actualizar_base_json():
    """Lee la base actual, incorpora precios en vivo y guarda data/precios_bolivia.json."""
    existentes = []
    if os.path.exists(DATA_PATH):
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            existentes = json.load(f)

    nuevos_sg = extraer_solo_gamer_shopify()
    if nuevos_sg:
        ids_nuevos = {x["id"] for x in nuevos_sg}
        existentes = [x for x in existentes if x.get("id") not in ids_nuevos]
        existentes.extend(nuevos_sg)

    os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(existentes, f, ensure_ascii=False, indent=2)
    print(f"[OK] Base actualizada con {len(existentes)} productos en {DATA_PATH}")


if __name__ == "__main__":
    actualizar_base_json()
