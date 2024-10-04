from flask import Flask, send_file, jsonify, request
import openai
from docx import Document
from dotenv import load_dotenv
import os
from datetime import datetime

# Cargar variables de entorno
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

# Directorio donde se guardarán los documentos generados
OUTPUT_DIR = "genai"

# Asegurarse de que la carpeta "genai" existe
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

# Simulación de los datos desde la API
def get_realistic_data(malla_curricular, silabo, rubricas, tema):
    return {
        "malla_curricular": malla_curricular,
        "silabo": silabo,
        "rubricas": rubricas,
        "tema": tema
    }

# Generar contenido con OpenAI
def generate_content(api_data):
    messages = [
        {"role": "system", "content": "Por favor, genera un contenido estructurado."},  # Mensaje del sistema opcional
        {"role": "user", "content": f"Genera brevemente una introducción sobre el tema: {api_data['tema']}."},
        {"role": "user", "content": f"Genera contenido relacionado con la malla curricular: {api_data['malla_curricular']} y el sílabo: {api_data['silabo']}."},
        {"role": "user", "content": f"Genera una conclusión basada en las rúbricas: {api_data['rubricas']}."}
    ]

    try:
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            temperature=0.7,
            max_tokens=30,
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        return str(e)

# Cargar la plantilla y reemplazar los campos
def create_document_from_template(title, introduction, content, conclusion):
    # Cargar la plantilla de Word existente
    template_path = "plantilla1.docx"
    doc = Document(template_path)

    # Reemplazar los campos en la plantilla
    for paragraph in doc.paragraphs:
        if '[titulo]' in paragraph.text:
            paragraph.text = paragraph.text.replace('[titulo]', title)
        if '[textoIntroduccion]' in paragraph.text:
            paragraph.text = paragraph.text.replace('[textoIntroduccion]', introduction)
        if '[contenido]' in paragraph.text:
            paragraph.text = paragraph.text.replace('[contenido]', content)
        if '[contenidoConclusion]' in paragraph.text:
            paragraph.text = paragraph.text.replace('[contenidoConclusion]', conclusion)
        if '[fechaActual]' in paragraph.text:
            paragraph.text = paragraph.text.replace('[fechaActual]', datetime.now().strftime("%d/%m/%Y"))

    # Guardar el documento generado en la carpeta 'genai'
    output_file = os.path.join(OUTPUT_DIR, f"{title.replace(' ', '_')}.docx")
    doc.save(output_file)
    
    return output_file

@app.route("/", methods=["GET"])
def home():
    return "La aplicación está funcionando correctamente. Usa POST /generate_word para generar un archivo Word."

@app.route('/favicon.ico')
def favicon():
    return '', 204  # Responder sin contenido

# Ruta para generar el archivo Word basado en la plantilla
@app.route("/generate_word", methods=["POST"])
def generate_word():
    try:
        # Obtener datos desde el cliente
        data = request.json
        malla_curricular = data.get('malla_curricular')
        silabo = data.get('silabo')
        rubricas = data.get('rubricas')
        tema = data.get('tema')

        # Obtener datos estructurados
        api_data = get_realistic_data(malla_curricular, silabo, rubricas, tema)

        # Generar contenido usando OpenAI
        generated_content = generate_content(api_data)

        # Dividir el contenido generado en partes
        parts = generated_content.split("\n")
        introduction = parts[0] if len(parts) > 0 else ""
        content = parts[1] if len(parts) > 1 else ""
        conclusion = parts[2] if len(parts) > 2 else ""

        # Crear el documento a partir de la plantilla
        title = api_data['tema']
        word_file = create_document_from_template(title, introduction, content, conclusion)

        # Retornar el archivo generado
        return send_file(word_file, as_attachment=True)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
