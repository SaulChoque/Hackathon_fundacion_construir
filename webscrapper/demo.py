import requests
from bs4 import BeautifulSoup
from googlesearch import search
import json
import time

# Término de búsqueda
query = "Samuel Doria Medina propuesta elecciones presidenciales Bolivia 2025 periódico"

# Cabecera para evitar bloqueos
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
}

# Lista para guardar resultados
resultados = []

print(f"Buscando resultados en Google para: {query}")

# Buscar en Google (los primeros 10 resultados)
for url in search(query, num_results=10):
    try:
        print(f"Procesando: {url}")
        res = requests.get(url, headers=headers, timeout=8)
        soup = BeautifulSoup(res.text, 'html.parser')

        # Extraer título
        titulo = soup.title.string.strip() if soup.title and soup.title.string else "Sin título"

        # Extraer párrafos significativos
        parrafos = soup.find_all("p")
        texto_extraido = " ".join([p.get_text(strip=True) for p in parrafos[:5]])

        # Filtro para evitar resultados vacíos o bloqueados
        if "Just a moment" in texto_extraido or len(texto_extraido) < 100:
            print(f"⚠️ Página descartada por contenido insuficiente o bloqueo: {url}")
            continue

        # Guardar resultado con más metadatos
        resultados.append({
            "titulo": titulo,
            "url": url,
            "resumen": texto_extraido,
            "fuente": url.split("/")[2]
        })

        time.sleep(1.5)  # Respetar el rate limit

    except Exception as e:
        print(f"❌ Error al procesar {url}: {e}")

# Guardar como JSON
archivo_salida = "resultados_mejorados_Webscrapper_example.json"
with open(archivo_salida, "w", encoding="utf-8") as f:
    json.dump(resultados, f, ensure_ascii=False, indent=4)

print(f"\n✅ Resultados guardados en {archivo_salida}")
