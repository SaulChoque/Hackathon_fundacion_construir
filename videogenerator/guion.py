import os
import json
<<<<<<< HEAD
=======
from transformers import AutoModelForCausalLM, AutoTokenizer
>>>>>>> 59d6e9eee3775cc73dc8258ccfff38366b23a8b7
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

<<<<<<< HEAD
def cargar_datos_enriquecidos(path_json):
    with open(path_json, "r", encoding="utf-8") as f:
        return json.load(f)

def generar_prompt(datos, tema):
    contexto = "\n\n".join(
        f"Fuente: {item['fuente']}\nTítulo: {item['titulo']}\nContenido: {item['resumen'][:1500]}..."
        for item in datos
    )

    crisis_detectada = any("crisis" in d["resumen"].lower() for d in datos)
    locutor_intro = "crisis económica" if crisis_detectada else "transición política"

    prompt = f"""Eres un analista político experto en elecciones bolivianas. Genera un guion para un video documental de 7-10 minutos sobre:
=======

def procesar_resultados(archivo_json):
    """formato JSON con:
    - Filtro de calidad de contenido
    - Priorización de fuentes clave
    - Normalización de texto"""
    
    with open(archivo_json, 'r', encoding='utf-8') as f:
        datos = json.load(f)
    
    resultados = []
    fuentes_prioritarias = ["infobae.com", "lapatria.bo", "lostiempos.com"]
    
    for item in datos:
        # Filtros básicos
        if not item.get("resumen") or len(item["resumen"]) < 150:
            continue
            
        # Normalización
        contenido = item["resumen"]
        if "Fotografía de archivo" in contenido:
            contenido = contenido.split("Fotografía de archivo")[0]
        
        # Priorizar fuentes confiables
        prioridad = 2 if any(fp in item["url"] for fp in fuentes_prioritarias) else 1
        
        resultados.append({
            "titulo": item["titulo"],
            "fuente": item["fuente"],
            "contenido": contenido[:2000],  # Limitar tamaño
            "prioridad": prioridad,
            "fecha": item.get("resumen", "").split(" ")[0]  # Extrae fecha del resumen
        })
    
    # Ordenar por prioridad y longitud de contenido
    return sorted(
        resultados,
        key=lambda x: (-x["prioridad"], -len(x["contenido"]))
    

# ==============================
# 2. GENERADOR DE SHORTS OPTIMIZADO
# ==============================
def generar_shorts(datos, tema):
    """Genera guiones ultra-concisos para YouTube Shorts con:
    - Estructura cronometrada exacta
    - Datos específicos de tus fuentes
    - Adaptación al formato vertical"""
    
    # Preparar contexto para IA (top 3 fuentes)
    contexto = "\n\n".join(
        f"📌 {item['titulo']} ({item['fuente']}, {item.get('fecha', 's/f')}):\n"
        f"{item['contenido'][:300]}..."
        for item in datos[:3]
    )
>>>>>>> 59d6e9eee3775cc73dc8258ccfff38366b23a8b7

    prompt = f"""**Instrucciones exactas para YouTube Short (30-60 segundos):**

**Tema:** {tema}
**Formato OBLIGATORIO:**
[0:00-0:04] 🎣 HOOK: Afirmación impactante (usar números/controversia)
[0:04-0:12] 🎯 CONTEXTO: 1 frase sobre el candidato/elección
[0:12-0:30] 💡 PROPUESTAS: 2 MÁXIMO (con datos concretos)
[0:30-0:50] 🔥 IMPACTO: 1 consecuencia o dato polémico
[0:50-1:00] ❓ CTA: Pregunta para comentarios + emoji

**Fuentes disponibles (usar datos exactos):**
{contexto}

**Ejemplo real basado en fuentes:**
[Hook] "¡Doria Medina quiere ELIMINAR el SENADO! (Ahorro: $200M/año)"
[Contexto] "Candidato opositor lidera encuestas para 2025"
[Propuestas] 
1. Autonomías económicas regionales
2. Voto electrónico desde 2026
[Impacto] "Según Infobae: 68% apoya pero congreso rechaza"
[CTA] "¿Es viable este plan? 👇"

<<<<<<< HEAD
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
Locutor: "En un contexto de {locutor_intro}, las elecciones bolivianas de 2025 marcarán..."
"""
    return prompt

def generar_guion(prompt, hf_token):
    print("🔄 Cargando modelo y tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained("mistralai/Mistral-7B-v0.1", use_auth_token=hf_token)
    model = AutoModelForCausalLM.from_pretrained(
        "mistralai/Mistral-7B-v0.1",
        use_auth_token=hf_token,
=======
**Guion a generar (seguid el formato):**"""
    
    # Configuración para respuestas ultra-cortas
    tokenizer = AutoTokenizer.from_pretrained("mistralai/Mistral-7B-v0.1")
    model = AutoModelForCausalLM.from_pretrained(
        "mistralai/Mistral-7B-v0.1",
>>>>>>> 59d6e9eee3775cc73dc8258ccfff38366b23a8b7
        torch_dtype=torch.float16,
        device_map="auto"
    )

    inputs = tokenizer(prompt, return_tensors="pt").to("cuda")
<<<<<<< HEAD

    outputs = model.generate(
        **inputs,
        max_new_tokens=1200,
        temperature=0.6,
=======
    outputs = model.generate(
        **inputs,
        max_new_tokens=300,  # Extremadamente conciso
        temperature=0.7,
>>>>>>> 59d6e9eee3775cc73dc8258ccfff38366b23a8b7
        top_p=0.9,
        do_sample=True,
        repetition_penalty=1.2
    )
<<<<<<< HEAD

    return tokenizer.decode(outputs[0], skip_special_tokens=True)

def guardar_guion(guion, tema):
    nombre_archivo = "guion_final.md"
    with open(nombre_archivo, "w", encoding="utf-8") as f:
        f.write(f"# Guion Video Documental: {tema}\n\n")
        f.write(guion)
    print(f"✅ Guion guardado en: {nombre_archivo}")

def main():
    tema = "propuestas electorales de Samuel Doria Medina para las elecciones presidenciales de Bolivia 2025"
    path_json = "resultados_mejorados_Webscrapper_example.json"

    if not os.path.exists(path_json):
        print("❌ Archivo JSON de entrada no encontrado.")
        return

    print("📥 Cargando datos enriquecidos...")
    datos = cargar_datos_enriquecidos(path_json)
    if not datos:
        print("❌ No se encontraron datos válidos.")
        return

    print("✍️ Generando prompt para el modelo...")
    prompt = generar_prompt(datos, tema)

    # Pega aquí tu token de Hugging Face que tiene acceso al modelo Mistral-7B
    hf_token = "coloca_tu_token_aquí"

    if not hf_token:
        print("❌ No se ha definido el token de Hugging Face.")
        return

    print("🧠 Generando guion con Mistral-7B...")
    guion = generar_guion(prompt, hf_token)

    print("💾 Guardando guion en archivo Markdown...")
    guardar_guion(guion, tema)

    print("\n📢 EXTRACTO DEL GUION:")
    print(guion[:800] + "...\n")

if __name__ == "__main__":
    main()
=======
    
    guion = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return guion.split("**Guion a generar:**")[-1].strip()

# ==============================
# 3. EJECUCIÓN PRINCIPAL
# ==============================
if __name__ == "__main__":
    # Configuración
    TEMA = "Samuel Doria Medina: Propuestas clave 2025"
    ARCHIVO_JSON = "resultados_mejorados_Webscrapper_example.json"  # Tu archivo actualizado
    
    # Paso 1: Procesar datos
    print("📊 Procesando resultados JSON...")
    datos_procesados = procesar_resultados(ARCHIVO_JSON)
    
    if not datos_procesados:
        print("❌ No hay datos válidos para generar el guion")
        exit()
    
    # Paso 2: Generar guion para Shorts
    print("🎬 Generando guion para YouTube Shorts...")
    guion = generar_shorts(datos_procesados, TEMA)
    
    # Guardar resultado
    with open("shorts_final.txt", "w", encoding="utf-8") as f:
        f.write(f"# GUION SHORT - {TEMA}\n\n")
        f.write(guion)
    
    print("\n✅ ¡Guion generado con éxito!")
    print(f"- Archivo guardado: shorts_final.txt")
    print("\n--- EXTRACTO ---")
    print(guion[:500] + "...")
>>>>>>> 59d6e9eee3775cc73dc8258ccfff38366b23a8b7
