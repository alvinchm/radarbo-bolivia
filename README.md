# RadarBO — Rastreador de Precios y Ofertones Black Friday Bolivia

Proyecto listo para abrir en **VS Code** y desplegar gratis en **GitHub Pages**, **Cloudflare Pages (`*.pages.dev`)** o **Vercel (`*.vercel.app`)**.

## Estructura del Proyecto
- `index.html`: Aplicación web optimizada con soporte para atajos de teclado (`/` para buscar), filtro Anti-Caros (Dismac), conversión en vivo con la tasa de cambio (`Bs. 11.80 / USD`) y escáner de Facebook Marketplace.
- `data/precios_bolivia.json`: Base de datos JSON que alimenta la web.
- `scraper/scraper_bolivia.py`: Script en Python que consulta precios en vivo de tiendas bolivianas.
- `scraper/marketplace_local.py`: Script local con Playwright para extraer ofertas de Facebook Marketplace Bolivia usando tu propia sesión de navegador sin riesgo de bloqueo.
- `.github/workflows/actualizar_precios.yml`: Automatización gratuita con **GitHub Actions** que ejecuta el scraper cada 6 horas en la nube.

## Cómo usarlo en VS Code (Paso a Paso)
1. Descomprime este archivo `.zip` y abre la carpeta en **VS Code**.
2. Instala la extensión **Live Server** en VS Code, haz clic derecho sobre `index.html` y elige **"Open with Live Server"**.
3. Para correr el scraper en tu terminal de VS Code:
   ```bash
   pip install -r requirements.txt
   python scraper/scraper_bolivia.py
   ```

## Cómo publicarlo en Internet Gratis (y obtener un dominio `.dev`)
- **Opción A (Gratis con subdominio `.pages.dev`):** Sube este repositorio a tu cuenta de GitHub y conéctalo en [Cloudflare Pages](https://pages.cloudflare.com/). Te dará gratis un enlace rápido terminado en `.dev` (por ejemplo, `radarbo.pages.dev`).
- **Opción B (GitHub Pages + GitHub Actions 100% Gratis):** Sube el proyecto a GitHub, entra a `Settings > Pages` y activa la publicación desde la rama `main`. El archivo `.github/workflows/actualizar_precios.yml` actualizará los precios cada 6 horas automáticamente.
- **Opción C (Dominio propio `.dev` como `radarbo.dev`):** Si quieres comprar un dominio `.dev` exclusivo, regístralo al costo (~$12 USD/año) en [Cloudflare Registrar](https://www.cloudflare.com/domains/) o [Porkbun](https://porkbun.com/products/domains) y conéctalo a tu proyecto en Cloudflare Pages o GitHub Pages.
