import os
import json
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

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
Locutor: "En un contexto de {locutor_intro}, las elecciones bolivianas de 2025 marcarán..."
"""
    return prompt

def generar_guion(prompt, hf_token):
    print("🔄 Cargando modelo y tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained("mistralai/Mistral-7B-v0.1", use_auth_token=hf_token)
    model = AutoModelForCausalLM.from_pretrained(
        "mistralai/Mistral-7B-v0.1",
        use_auth_token=hf_token,
        torch_dtype=torch.float16,
        device_map="auto"
    )

    inputs = tokenizer(prompt, return_tensors="pt").to("cuda")

    outputs = model.generate(
        **inputs,
        max_new_tokens=1200,
        temperature=0.6,
        top_p=0.9,
        do_sample=True,
        repetition_penalty=1.1
    )

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
