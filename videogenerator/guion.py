import requests
from bs4 import BeautifulSoup
from googlesearch import search
import json
import time
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

def buscar_noticias(query, num_results=8):
    """Versión optimizada de tu scraper con:
    - Filtros mejorados
    - Extracción de contenido enriquecido
    - Compatibilidad con generación de shorts"""
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }
    
    resultados = []
    dominios_confiables = ["infobae.com", "lostiempos.com", "lapatria.bo", "eldeber.com.bo"]
    
    print(f"🔍 Buscando: '{query}'...")
    
    for url in search(query, num_results=num_results):
        try:
            # Filtro rápido
            if not any(d in url for d in dominios_confiables):
                continue
                
            print(f"\n📰 Procesando: {url}")
            res = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(res.text, 'html.parser')
            
            # Extracción inteligente
            titulo = soup.title.get_text(strip=True) if soup.title else "Sin título"
            
            # Estrategias específicas por sitio
            if "infobae.com" in url:
                contenido = " ".join([p.get_text() for p in soup.select("article p")][:8])
            elif "lostiempos.com" in url:
                contenido = " ".join([p.get_text() for p in soup.select(".detail-text p")][:5])
            else:  # Fallback genérico
                parrafos = [p.get_text(strip=True) for p in soup.find_all("p") if len(p.get_text(strip=True)) > 30]
                contenido = " ".join(parrafos[:5])
            
            if not contenido or len(contenido) < 150:
                continue
                
            resultados.append({
                "titulo": titulo,
                "url": url,
                "fuente": url.split("/")[2],
                "contenido": contenido[:2500],  # Limitamos tamaño
                "fecha": time.strftime("%Y-%m-%d")
            })
            
            time.sleep(1.2)  # Evitar bloqueos
            
        except Exception as e:
            print(f"⚠️ Error en {url}: {str(e)[:80]}...")
    
    return resultados

# =========================
# 2. GENERADOR DE SHORTS
# =========================
def generar_guion_shorts(datos, tema):
    """Genera guiones virales para YouTube Shorts (30-60 seg) con:
    - Hook impactante
    - 2-3 puntos clave
    - Llamado a la acción
    - Adaptado a tu scraper mejorado"""
    
    # Preparar contexto para IA
    contexto = "\n".join(
        f"📌 {item['titulo']} ({item['fuente']}):\n"
        f"{item['contenido'][:300]}...\n" 
        for item in datos[:4]  # Usamos las 4 mejores fuentes
    )
    
    prompt = f"""**Instrucciones exactas para YouTube Short (45-60 segundos):**

**Tema:** {tema}
**Formato obligatorio:**
[0:00-0:05] 🎣 HOOK: Frase impactante (usar números/controversia)
[0:05-0:20] 🎯 CONTEXTO: 1 oración sobre el candidato
[0:20-0:40] 💡 PROPUESTAS: 2 MÁXIMO (con datos duros si hay)
[0:40-0:55] 🔥 POLÉMICA: 1 dato controvertido
[0:55-1:00] ❓ CTA: Pregunta para comentarios

**Fuentes disponibles:**
{contexto}

**Ejemplo real:**
[Hook] "¡Doria Medina quiere ELIMINAR la reelección! ¿Estás de acuerdo?"
[Contexto] "Candidato presidencial propone 3 cambios radicales"
[Propuestas] 
1. Educación gratuita con impuesto a minería (5%)
2. Internet en zonas rurales (2026)
[Polémica] "Criticado por empresarios: 'Afectará inversiones'"
[CTA] "¿Votarías por estas ideas? ▼"

**Guion a generar (usar misma estructura):**
"""
    
    # Configuración óptima para respuestas cortas
    tokenizer = AutoTokenizer.from_pretrained("mistralai/Mistral-7B-v0.1")
    model = AutoModelForCausalLM.from_pretrained(
        "mistralai/Mistral-7B-v0.1",
        torch_dtype=torch.float16,
        device_map="auto",
        load_in_4bit=True  # Para mayor eficiencia
    )
    
    inputs = tokenizer(prompt, return_tensors="pt").to("cuda")
    outputs = model.generate(
        **inputs,
        max_new_tokens=350,
        temperature=0.75,
        top_p=0.9,
        do_sample=True
    )
    
    guion = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return guion.split("**Guion a generar:**")[-1].strip()

# ======================
# 3. EJECUCIÓN PRINCIPAL
# ======================
if __name__ == "__main__":
    # Configuración
    TEMA = "Propuestas de Samuel Doria Medina - Elecciones Bolivia 2025"
    QUERY = f"{TEMA} site:news OR site:com OR site:org -filetype:pdf"
    
    # Paso 1: Búsqueda y scraping
    print("🕵️‍♂️ Buscando noticias actualizadas...")
    datos_web = buscar_noticias(QUERY)
    
    if not datos_web:
        print("❌ No se encontraron resultados válidos")
        exit()
    
    with open("noticias_actuales.json", "w", encoding="utf-8") as f:
        json.dump(datos_web, f, ensure_ascii=False, indent=2)
    
    # Paso 2: Generar guion para Shorts
    print("\n🎬 Generando guion viral...")
    guion_final = generar_guion_shorts(datos_web, TEMA)
    
    # Guardar resultado
    with open("guion_shorts_final.txt", "w", encoding="utf-8") as f:
        f.write(f"# GUION PARA YOUTUBE SHORTS - {TEMA}\n\n")
        f.write(guion_final)
    
    print("\n✅ ¡Proceso completado!")
    print(f"- Noticias scrapeadas: noticias_actuales.json")
    print(f"- Guion para Shorts: guion_shorts_final.txt")
    print("\n💡 Ejemplo de guion generado:")
    print(guion_final[:500] + "...")
