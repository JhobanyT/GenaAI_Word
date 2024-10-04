# Proyecto de Generación de Presentaciones y Documentos

Este proyecto permite la creación automática de presentaciones en **Word** utilizando **Flask** y varias bibliotecas de Python.

## Requisitos previos

## Instalación

Sigue los siguientes pasos para configurar y ejecutar el proyecto en tu entorno local:

2. **Crear un entorno virtual y activalo**
- virtualenv -p python3 env_tesis
- env_tesis\Scripts\activate

3. **Instalar las dependencias**
Instala las dependencias necesarias ejecutando los siguientes comandos:

- pip install Flask
- pip install Flask-Limiter
- pip install openai
- pip install python-pptx
- pip install python-dotenv
- pip install python-docx

Verificar las dependencias instaladas

- pip list

3. **Tener Postman y Sigue los siguiente pasos**

- Crear un nuevo request de tipo POST CON LA URT (http://127.0.0.1:5000/generate_word)
- direccionar se Body > raw y pegar lo siguiente
- {
    "malla_curricular": "Asignatura: Programación Avanzada. Temas cubiertos: estructuras de datos, algoritmos complejos, y diseño orientado a objetos.",
    "silabo": "El sílabo cubre las técnicas avanzadas de programación, incluyendo recursividad, estructuras dinámicas, y algoritmos de búsqueda y ordenación.",
    "rubricas": "Unidad 1: Algoritmos de Búsqueda y Ordenación.",
    "tema": "Introducción a algoritmos"
  }
- Enviar el request

4. **Los archivos generados estaran en la carpeta genai**
