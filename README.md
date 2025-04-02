# Competencia Prescriptive Analytics

Aplicación web para la competencia de Prescriptive Analytics desarrollada con Streamlit.

## Requisitos

- Python 3.8 o superior
- Las dependencias listadas en `requirements.txt`

## Instalación

1. Clona este repositorio:
```bash
git clone [URL_DEL_REPOSITORIO]
```

2. Instala las dependencias:
```bash
pip install -r requirements.txt
```

3. Ejecuta el script para crear la base de datos:
```bash
python crear_db.py
```

4. Inicia la aplicación:
```bash
streamlit run app.py
```

## Uso

La aplicación estará disponible en `http://localhost:8501` por defecto.

## Estructura del Proyecto

- `app.py`: Aplicación principal de Streamlit
- `crear_db.py`: Script para inicializar la base de datos
- `requirements.txt`: Lista de dependencias del proyecto
- `images/`: Directorio con las imágenes utilizadas en la aplicación
- `.streamlit/`: Configuración de Streamlit
- `generic_input_case.xlsx`: Archivo de datos de entrada

## Notas

- La base de datos se crea localmente al ejecutar `crear_db.py`
- Asegúrate de tener el archivo `generic_input_case.xlsx` en el directorio raíz 
