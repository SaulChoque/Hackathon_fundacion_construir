import json
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch


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

**Guion a generar (seguid el formato):**"""
    
    # Configuración para respuestas ultra-cortas
    tokenizer = AutoTokenizer.from_pretrained("mistralai/Mistral-7B-v0.1")
    model = AutoModelForCausalLM.from_pretrained(
        "mistralai/Mistral-7B-v0.1",
        torch_dtype=torch.float16,
        device_map="auto"
    )
    
    inputs = tokenizer(prompt, return_tensors="pt").to("cuda")
    outputs = model.generate(
        **inputs,
        max_new_tokens=300,  # Extremadamente conciso
        temperature=0.7,
        top_p=0.9,
        do_sample=True,
        repetition_penalty=1.2
    )
    
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
