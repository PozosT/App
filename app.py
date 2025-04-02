# app.py    
import streamlit as st
import pandas as pd
from datetime import datetime
import sqlite3
import io
import os
from PIL import Image

# Configuración inicial de la página
st.set_page_config(page_title="Competencia prescritive analytics", layout="wide")

# Título y descripción
st.title("Competencia Prescritive Analytics")

# Botón de descarga del archivo de entrada
st.markdown("### Descargar archivo de entrada")
with open("generic_input_case.xlsx", "rb") as file:
    st.download_button(
        label="Descargar generic_input_case.xlsx",
        data=file,
        file_name="generic_input_case.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

st.markdown("""

## Objetivo
Evaluar las habilidades en resolver problemas de prescritive analytics del equipo que aspire a integrarse al equipo de Ciencia de Datos de una reconocida empresa multinacional, líder en soluciones sostenibles e innovadoras.
            
### Objetivos Específicos
1. Desarrollar un programa con las siguientes especificaciones:
   * Leer el archivo en formato .xlsx proporcionado.
   * Implementar un heurística o metaheurística que cumpla de forma correcta con las reglas de negocio establecidas.
   * Generar un archivo de salida en formato .xlsx o .csv que contenga la solución encontrada.
   * Utilizar preferentemente el lenguaje Python.
   * Emplear cualquier biblioteca que facilite la implementación de las reglas de negocio.

2. Elaborar un informe que incluya:
   * Instrucciones para ejecutar el programa.
   * la metodología para resolver el problema.
   * Las premisas asumidas y un análisis de las reglas de negocio.
   * Cualquier otra información que la(o) candidata(o) considere relevante.

## Definición del Problema
Las plantaciones de eucalipto de la empresa se distribuyen en diversas fazendas a lo largo del país. Cada hacienda se divide en Unidades Productivas (UPs). Tras la cosecha de cada UP se genera un volumen de madera que debe ser transportado a las fábricas. Dicho transporte debe planificarse con una granularidad diaria utilizando la flota de vehículos disponible, cumpliendo con un conjunto de premisas y buscando el mejor secuenciamiento posible.

El mejor secuenciamiento, entre todas las alternativas, es aquel que minimiza la variación diaria de la densidad básica (DB) de la madera que llega a la fábrica. La variación de la DB en el día \(t\) se define como:
$$
\Delta DB^t = DB^t_{max} - DB^t_{min}.
$$

### Premisas de Negocio

| **Entidad**    | **Premisa**                                  | **Descripción**                                                                                                                                                                  |
|----------------|----------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Fábrica        | Demanda diaria                               | El volumen de madera entregado diariamente debe respetar los intervalos definidos en el archivo de entrada.                                                                     |
| Fábrica        | Calidad de la madera                         | La media ponderada, basada en los volúmenes transportados diariamente, de la Relación Sólido/Polpa (RSP) de cada UP debe mantenerse dentro de los límites estipulados.       |
| Flujo          | Capacidad de vehículos                       | La capacidad de transporte diario se define por la caja de carga y el tiempo de ciclo entre la UP de origen y la fábrica de destino.                                              |
| Flujo          | Capacidad de grúas                           | Un transportador puede atender simultáneamente un número máximo de UPs igual al número de grúas disponibles.                                                                      |
| Transportador  | Asignación Transportador x Fazenda           | No se permite que un transportador opere simultáneamente en dos fazendas distintas.                                                                                             |
| Transportador  | Consumo de recursos                          | Se debe respetar el límite mínimo y máximo de equipos asignables a cada transportador.                                                                                          |
| Transportador  | Grúas                                        | Dado que un transportador puede atender diversas UPs (según las restricciones de flujo y capacidad de grúas), el número de vehículos asignados a cada UP debe cumplir con un porcentaje mínimo respecto al total de vehículos en actividad cada día. |
| Fazendas       | Transporte completo                          | Al iniciar el transporte de una fazenda, el transportador solo podrá cambiar de fazenda o interrumpir la actividad si completa el transporte del volumen total disponible en la fazenda. (Ver la primera ilustración a continuación.) |
| UPs            | Transporte completo                          | Al comenzar el transporte de una UP con volumen inferior a 7000 m³, el transportador solo podrá cambiar de UP o interrumpir la actividad si completa el transporte del volumen total disponible en dicha UP. (Ver la primera ilustración a continuación.) |
| UPs            | Transporte fraccionado                       | Una UP con volumen superior a 7000 m³ puede tener actividades de transporte discontinuas en el horizonte, permitiéndose hasta dos entradas. Es decir, puede existir hasta un intervalo sin actividad de cualquier transportador en la UP entre dos intervalos en los que se realice transporte. (Ver la segunda ilustración a continuación.) |

## Ilustraciones de las Premisas de Negocio
Las siguientes ilustraciones representan los comportamientos esperados según las premisas establecidas:

##### Haciendas y UPs con volúmenes inferiores a 7000 m³
""")

# Cargar y mostrar la primera imagen
image1 = Image.open('images/image_1.png')
st.image(image1, caption='Haciendas y UPs con volúmenes inferiores a 7000 m³')

st.markdown("""
##### UPs con volúmenes superiores a 7000 m³
""")

# Cargar y mostrar la segunda imagen
image2 = Image.open('images/image_2.png')
st.image(image2, caption='UPs con volúmenes superiores a 7000 m³')

st.markdown("""
## Descripción del Archivo de Entrada
El archivo de entrada consta de las siguientes pestañas: **HORIZONTE**, **BD_UP**, **FROTA**, **FABRICA**, **ROTA** y **GRUA**.

| **Pestaña** | **Descripción**                                                                                      | **Columnas**                                                                                                         |
|-------------|------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------|
| HORIZONTE   | Contempla el horizonte de días para la planificación.                                               | DIA, MES, ANO, CICLO_LENTO                                                                                            |
| BD_UP       | Contiene los datos de los volúmenes y la calidad de la madera cosechada en cada UP.                    | UP, FAZENDA, DB, VOLUME, RSP, DATA_COLHEITA, IDADE_FLORESTA, IMA, RD, RESERVADO, CLONE, ESPECIE, PRECIPITACAO       |
| FROTA       | Describe los transportadores disponibles, especificando el número mínimo y máximo de camiones a utilizar. | TRANSPORTADOR, DIA, FROTA_MIN, FROTA_MAX                                                                               |
| GRUA        | Proporciona información sobre las grúas que se emplearán para cargar la madera desde las UPs a los vehículos. | TRANSPORTADOR, QTD_GRUAS, PORCENTAGEM_VEICULOS_MIN                                                                     |
| FABRICA     | Presenta la demanda diaria de la fábrica junto con las restricciones de calidad de la madera basadas en el RSP. | DIA, FABRICA, DEMANDA_MIN, DEMANDA_MAX, RSP_MIN, RSP_MAX                                                               |
| ROTA        | Contiene los datos del tiempo de ciclo y la caja de carga para cada combinación posible de origen, destino y transportador. La origen siempre es una UP y el destino una fábrica. | ORIGEM, DESTINO, TRANSPORTADOR, CAIXA_CARGA, TEMPO_CICLO, CICLO_LENTO, Fazenda                                        |

## Descripción del Archivo de Salida
Se espera la generación de un archivo de salida en formato .csv o .xlsx, el cual deberá incluir todas las decisiones adoptadas por el optimizador para cada UP, transportador y día. A continuación se muestra un ejemplo:

| **UP**  | **FAZENDA** | **TRANSPORTADOR** | **DÍA** | **MES** | **DB** | **RSP** | **QTD_VEICULOS** | **VOLUME** |
|---------|-------------|-------------------|---------|---------|--------|---------|------------------|------------|
| UP_1    | FAZENDA_1   | T1                | 8       | 3       | 475    | 1,62    | 12               | 1400       |
| UP_2    | FAZENDA_1   | T1                | 9       | 3       | 475    | 1,53    | 9                | 1630       |
| UP_3    | FAZENDA_2   | T3                | 9       | 3       | 480    | 1,53    | 10               | 1368       |

## Glosario
* **Caja de carga:** Cantidad de volumen de madera que un camión puede transportar por viaje.
* **DB:** Densidad básica (\(m^3\)/kg) de la madera; es una propiedad intensiva que refleja la calidad de la madera evaluada en cada UP. Su variabilidad es indeseable debido al consumo de químicos en la producción de celulosa.
* **Grúa:** Equipo utilizado para cargar los camiones que transportan la madera; se emplea como sinónimo de grúa.
* **RD:** Rendimiento de la fábrica (%), que representa la cantidad de celulosa producida por tonelada de madera.
* **RSP:** Relación Sólido/Polpa (%), una propiedad intensiva de la calidad de la madera evaluada en cada UP, la cual debe mantenerse dentro de un rango de referencia para asegurar una alimentación adecuada que permita el control de la productividad de la fábrica.
* **Tiempo de ciclo (viaje/día):** Número de viajes que puede realizar cada camión en un día.
* **UP:** Unidad Productiva, la menor división de terreno destinada a la plantación de eucalipto en la que se organizan las fazendas.

""")

# Crear/conectar base de datos
conn = sqlite3.connect('competencia.db')
c = conn.cursor()

# Crear tabla si no existe
c.execute('''CREATE TABLE IF NOT EXISTS submissions 
            (equipo TEXT, BKS REAL, timestamp DATETIME, 
             codigo TEXT, archivo_solucion BLOB)''')
conn.commit()

# Formulario de envío
st.header("Enviar Solución")
with st.form("submission_form"):
    equipo = st.text_input("Nombre del Equipo")
    BKS = st.number_input("BKS obtenido", min_value=0.0)
    codigo = st.text_area("Código fuente")
    archivo = st.file_uploader("Archivo de solución")
    
    submitted = st.form_submit_button("Enviar")
    if submitted:
        if archivo is not None:
            archivo_bytes = archivo.getvalue()
        else:
            archivo_bytes = None
            
        c.execute("""INSERT INTO submissions 
                    (equipo, BKS, timestamp, codigo, archivo_solucion) 
                    VALUES (?, ?, ?, ?, ?)""", 
                    (equipo, BKS, datetime.now(), codigo, archivo_bytes))
        conn.commit()
        st.success("¡Solución enviada exitosamente!")

# Mostrar ranking
st.header("Ranking Actual")
df = pd.read_sql_query("""SELECT equipo, BKS, timestamp 
                          FROM submissions 
                          ORDER BY BKS ASC""", conn)
st.dataframe(df)

# Cerrar conexión
conn.close()
