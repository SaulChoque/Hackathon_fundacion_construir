import requests
from bs4 import BeautifulSoup
from googlesearch import search
import json

# Término de búsqueda
query = "Andronico rodriguez elecciones presidenciales Bolivia 2025 periodico"

# Cabecera para evitar bloqueos
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
}

# Lista para guardar resultados
resultados = []

# Buscar en Google (los primeros 10 resultados)
for url in search(query, num_results=10):
    try:
        res = requests.get(url, headers=headers, timeout=5)
        soup = BeautifulSoup(res.text, 'html.parser')
        
        # Extraer título de la página
        titulo = soup.title.string if soup.title else "Sin título"
        
        # Extraer primer párrafo (si existe)
        parrafos = soup.find_all('p')
        resumen = parrafos[0].get_text(strip=True) if parrafos else "No se encontró resumen"
        
        resultados.append({
            "titulo": titulo,
            "url": url,
            "resumen": resumen
        })
    except Exception as e:
        print(f"Error al acceder a {url}: {e}")

# Guardar como JSON
with open("resultados.json", "w", encoding="utf-8") as f:
    json.dump(resultados, f, ensure_ascii=False, indent=4)

print("✅ Resultados guardados en luis_arce_resultados.json")
