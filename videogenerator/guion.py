import json
import requests
from bs4 import BeautifulSoup
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

def extraer_contenido_real(url):
    """Extrae contenido completo de artículos periodísticos"""
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
        }
        res = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')
        
        # Estrategias de extracción para diferentes sitios
        if "infobae.com" in url:
            contenido = " ".join([p.get_text() for p in soup.select("article p")])
        elif "lapatria.bo" in url:
            contenido = " ".join([p.get_text() for p in soup.select(".article-content p")])
        elif "lostiempos.com" in url:
            contenido = " ".join([p.get_text() for p in soup.select(".detail-text p")])
        else:
            # Extracción genérica como fallback
            parrafos = soup.find_all('p')
            contenido = " ".join([p.get_text(strip=True) for p in parrafos if len(p.get_text(strip=True)) > 30])
        
        return contenido[:3000]  # Limitar tamaño
    except Exception as e:
        print(f"Error extrayendo {url}: {str(e)[:100]}...")
        return None

def procesar_resultados(archivo_json):
    """Enriquece los resultados con contenido real"""
    with open(archivo_json, 'r', encoding='utf-8') as f:
        datos = json.load(f)
    
    resultados_procesados = []
    for item in datos:
        if "just a moment" in item["titulo"].lower():
            continue  # Saltar captchas
            
        contenido_real = extraer_contenido_real(item["url"])
        if contenido_real:
            resultados_procesados.append({
                "titulo": item["titulo"],
                "fuente": item["url"].split('/')[2],  # Dominio
                "contenido": f"{item['resumen']}\n\n{contenido_real}" if item["resumen"] else contenido_real
            })
    
    return resultados_procesados[:5]  # Limitar a 5 mejores

def generar_guion_estructurado(datos, tema):
    """Genera un guion profesional con estructura definida"""
    # Preparar contexto para el LLM
    contexto = "\n\n".join(
        f"Fuente: {item['fuente']}\nTítulo: {item['titulo']}\nContenido: {item['contenido'][:1500]}..."
        for item in datos
    )
    
    prompt = f"""Eres un analista político experto en elecciones bolivianas. Genera un guion para un video documental de 7-10 minutos sobre:

**Tema central:** {tema}

**Fuentes investigadas:**
{contexto}

**Estructura requerida:**
1. INTRODUCCIÓN (1 min):
   - Contexto histórico de las elecciones 2025
   - Presentación del candidato
   - Mencionar fuentes consultadas

2. PROPUESTAS CLAVE (4-5 mins):
   - Económicas (máx 2 propuestas concretas con datos)
   - Políticas (reforma electoral, etc.)
   - Sociales (educación, salud)
   - Citando fuentes específicas cuando corresponda

3. ANÁLISIS (2 mins):
   - Posibles impactos de las propuestas
   - Comparación breve con otros candidatos
   - Viabilidad política

4. CONCLUSIÓN (1 min):
   - Resumen ejecutivo
   - Frase de cierre impactante

**Estilo:**
- Formal pero accesible
- Neutral (no tomar partido)
- Usar datos verificables
- Incluir al menos 3 citas textuales de las fuentes

[INICIO DEL GUION]
**Título:** "Análisis de las propuestas de Samuel Doria Medina para Bolivia 2025"

**[INTRODUCCIÓN]**
(Video: Imágenes de campaña electoral)
Locutor: "En un contexto de {"crisis económica" if any("crisis" in d["contenido"].lower() for d in datos) else "transición política"}, las elecciones bolivianas de 2025 marcarán..."
"""
    
    # Cargar modelo (versión optimizada)
    model_name = "mistralai/Mistral-7B-v0.1"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        torch_dtype=torch.float16,
        device_map="auto"
    )
    
    inputs = tokenizer(prompt, return_tensors="pt").to("cuda")
    
    outputs = model.generate(
        **inputs,
        max_new_tokens=1200,
        temperature=0.6,  # Más preciso
        top_p=0.9,
        do_sample=True,
        repetition_penalty=1.1
    )
    
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

def generar_guion_corto(datos, tema):
    """
    Genera guion para videos cortos (30-60 seg) con:
    - Hook inicial impactante
    - 3 puntos clave máximo
    - Lenguaje simple y directo
    - Llamado a la acción final
    """
    contexto = "\n".join(
        f"- {item['titulo']}: {item['contenido'][:200]}..." 
        for item in datos[:3]  # Solo 3 fuentes clave
    )

    prompt = f"""**Instrucciones para video corto de YouTube (30-60 segundos):**
Tema: {tema}
Estilo: Dinámico, rápido y objetivo (para TikTok/Shorts)
Estructura obligatoria:
1. [0:00-0:05] HOOK INICIAL: Frase impactante (ej: "¡Esta propuesta cambiará Bolivia!")
2. [0:05-0:20] CONTEXTO: 1 oración sobre el candidato y elecciones
3. [0:20-0:45] PROPUESTAS: 2-3 puntos clave (máx 10 palabras cada uno)
4. [0:45-0:55] DATO CURIOSO: 1 estadística o cita textual
5. [0:55-1:00] CTA: "¿Qué opinas? Comenta ▼"

**Fuentes disponibles:**
{contexto}

**Ejemplo de salida:**
[Hook] "¿Sabías que Doria Medina propone eliminar la reelección presidencial?"
[Contexto] "En las elecciones 2025, el candidato busca..."
[Propuestas] 
1. Reforma económica con 3 medidas clave
2. Educación gratuita hasta la universidad
[Dato] "Según La Patria: 68% apoya esta reforma"
[CTA] "¿Estás de acuerdo? ▼"

**Guion real a generar:**
"""
    
    # Modelo rápido (optimizado para respuestas breves)
    tokenizer = AutoTokenizer.from_pretrained("mistralai/Mistral-7B-v0.1")
    model = AutoModelForCausalLM.from_pretrained(
        "mistralai/Mistral-7B-v0.1",
        torch_dtype=torch.float16,
        device_map="auto",
        load_in_4bit=True  # Para mayor velocidad
    )
    
    inputs = tokenizer(prompt, return_tensors="pt").to("cuda")
    outputs = model.generate(
        **inputs,
        max_new_tokens=350,  # Texto más corto
        temperature=0.8,     # Más creativo
        do_sample=True,
        top_k=40
    )
    
    return tokenizer.decode(outputs[0], skip_special_tokens=True).split("**Guion real a generar:**")[-1]


def main():
    # Configuración
    tema = "propuestas electorales de Samuel Doria Medina para las elecciones presidenciales de Bolivia 2025"
    
    print("📊 Procesando resultados.json...")
    datos = procesar_resultados("resultados.json")
    
    if not datos:
        print("No se pudo extraer contenido válido")
        return
    
    with open("datos_enriquecidos.json", "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=2)
    
    print("🎬 Generando guion profesional...")
    guion = generar_guion_estructurado(datos, tema)
    
    # Guardar con formato
    with open("guion_final.md", "w", encoding="utf-8") as f:
        f.write(f"# Guion Video Documental: {tema}\n\n")
        f.write(guion)
    
    print("\n✅ Proceso completado:")
    print(f"- Datos enriquecidos: datos_enriquecidos.json")
    print(f"- Guion profesional: guion_final.md")
    print("\n--- EXTRACTO ---")
    print(guion[:1000] + "...")

if __name__ == "__main__":
    main()
