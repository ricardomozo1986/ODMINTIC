import streamlit as st
import pandas as pd
import io
import datetime

st.set_page_config(page_title="Evaluador de Datos Abiertos", layout="wide")
st.title("📊 Evaluador Inteligente de Datos Abiertos")
st.subheader("Diagnóstico de calidad de los datos cargados")

# --- MÓDULO 2: Evaluación extendida ---
def evaluar_calidad_interoperabilidad(df, uploaded_file):
    st.markdown("## 🧪 Evaluación de calidad e interoperabilidad extendida")
    resultados = {}

    accesibilidad = 100 if uploaded_file.name.endswith((".csv", ".xlsx")) and df.columns.notnull().all() else 0
    resultados["Accesibilidad"] = accesibilidad

    completitud = 100 - (df.isnull().sum().sum() / (df.shape[0] * df.shape[1])) * 100
    resultados["Completitud"] = round(completitud, 2)

    inconsistencias = sum(df[col].map(type).nunique() > 1 for col in df.columns)
    consistencia = 100 - (inconsistencias / df.shape[1]) * 100
    resultados["Consistencia"] = round(consistencia, 2)

    posibles_invalidos = 0
    for col in df.select_dtypes(include='number').columns:
        if df[col].min() < 0 or df[col].max() > 10000:
            posibles_invalidos += 1
    exactitud = 100 - (posibles_invalidos / df.shape[1]) * 100
    resultados["Exactitud"] = round(exactitud, 2)

    posibles_fechas = df.columns[df.columns.str.contains("fecha|date", case=False, regex=True)]
    if len(posibles_fechas) > 0:
        validez_total = 0
        for col in posibles_fechas:
            fechas_validas = pd.to_datetime(df[col], errors='coerce')
            porcentaje_validas = fechas_validas.notnull().sum() / len(fechas_validas) * 100
            validez_total += porcentaje_validas
        resultados["Validez"] = round(validez_total / len(posibles_fechas), 2)
    else:
        resultados["Validez"] = "No aplica"

    if len(posibles_fechas) > 0:
        max_fecha = pd.to_datetime(df[posibles_fechas[0]], errors='coerce').max()
        if pd.isnull(max_fecha):
            resultados["Actualización"] = "No disponible"
        else:
            dias = (datetime.datetime.now() - max_fecha).days
            resultados["Actualización"] = f"{dias} días desde última actualización"
    else:
        resultados["Actualización"] = "No aplica"

    # --- LÍNEA CORREGIDA ---
    portabilidad = 100 if all(col.replace(" ", "").isidentifier() for col in df.columns) else 50
    resultados["Portabilidad"] = portabilidad

    nombres_claros = sum(df.columns.str.len() > 3)
    comprensibilidad = (nombres_claros / df.shape[1]) * 100
    resultados["Comprensibilidad"] = round(comprensibilidad, 2)

    confidenciales = ["nombre", "documento", "correo", "teléfono"]
    contiene_sensibles = sum(col.lower() in confidenciales for col in df.columns)
    confidencialidad = 100 if contiene_sensibles == 0 else 0
    resultados["Confidencialidad"] = confidencialidad

    disponibilidad = 100 if df.shape[0] > 0 and df.shape[1] > 0 else 0
    resultados["Disponibilidad"] = disponibilidad

    columnas_claves = ["codigo_dane", "departamento", "municipio", "valor", "tipo"]
    detectadas = sum(1 for col in df.columns if col.lower() in columnas_claves)
    relevancia = detectadas / len(columnas_claves) * 100
    resultados["Relevancia"] = round(relevancia, 2)

    st.markdown("### 🔎 Resultados extendidos")
    for criterio, valor in resultados.items():
        st.write(f"**{criterio}**: {valor}")

# --- MÓDULO 3: Sugerencias automáticas ---
def sugerencias_automaticas(df):
    st.markdown("## 🧠 Sugerencias automáticas de mejora")
    sugerencias = []
    for col in df.columns:
        if df[col].dtype == object:
            if df[col].str.contains(r"[^\x00-\x7F]", na=False).any():
                sugerencias.append(f"🟡 Convertir caracteres especiales en columna '{col}'")
            if df[col].str.lower().isin(["sí", "no"]).sum() > 0:
                sugerencias.append(f"🔄 Normalizar valores binarios en '{col}' (Sí/No → 1/0)")
        if df[col].dtype != object and df[col].nunique() == 1:
            sugerencias.append(f"⚠️ Eliminar columna '{col}' por baja variabilidad")

    if sugerencias:
        for s in sugerencias:
            st.markdown(s)
    else:
        st.success("No se encontraron sugerencias relevantes.")

# --- MÓDULO 4: Metadatos asistidos ---
def construir_metadatos(df):
    st.markdown("## 🧾 Construcción asistida de metadatos")
    with st.form("metadata_form"):
        titulo = st.text_input("Título del conjunto de datos")
        descripcion = st.text_area("Descripción")
        fuente = st.text_input("Fuente de los datos")
        cobertura = st.text_input("Cobertura geográfica (municipio, departamento)")
        frecuencia = st.selectbox("Frecuencia de actualización", ["Única", "Diaria", "Mensual", "Trimestral", "Anual"])
        licencia = st.selectbox("Licencia", ["Datos Abiertos", "Creative Commons", "Dominio Público", "Otra"])

        st.markdown("### Diccionario de datos detectado:")
        for col in df.columns:
            st.write(f"🔹 **{col}**: tipo {df[col].dtype}")

        enviado = st.form_submit_button("Guardar metadatos")
        if enviado:
            st.success("✅ Metadatos guardados exitosamente (simulado).")

# --- MÓDULO 5: Ajustes técnicos sugeridos ---
def ajustes_tecnicos(df):
    st.markdown("## 🔧 Ajustes técnicos sugeridos")
    st.markdown("Sugerencias para preparar los datos para publicación o análisis avanzado:")

    recomendaciones = []

    # 1. Renombrar columnas con espacios o caracteres especiales
    if any(df.columns.str.contains(" |\.|,|;|\(|\)", regex=True)):
        recomendaciones.append("🔄 Renombrar columnas con espacios o caracteres especiales para mayor interoperabilidad.")

    # 2. Codificación estándar de texto
    recomendaciones.append("✅ Asegurar codificación UTF-8 al exportar.")

    # 3. Separar fechas y horas
    for col in df.columns:
        if "fecha" in col.lower() and df[col].dtype == 'object':
            recomendaciones.append(f"🕓 Revisar formato de fecha en '{col}' y separar si contiene hora.")

    # 4. Normalizar nombres de columnas (snake_case)
    if not all(df.columns.str.match("^[a-z0-9_]+$")):
        recomendaciones.append("💡 Normalizar nombres de columnas a formato snake_case (ej: tipo_dato).")

    # 5. Estandarizar valores categóricos
    for col in df.select_dtypes(include='object').columns:
        if df[col].nunique() < 10:
            recomendaciones.append(f"📚 Revisar valores en columna '{col}' y aplicar dominio controlado si aplica.")

    for rec in set(recomendaciones):
        st.markdown(rec)
    
# --- MÓDULO 6: Evaluación de uso potencial con IA ---
def evaluar_uso_con_ia(df):
    st.markdown("## 🤖 Evaluación de uso potencial con IA")

    uso_sugerido = []

    if "latitud" in df.columns.str.lower().tolist() and "longitud" in df.columns.str.lower().tolist():
        uso_sugerido.append("📍 Visualización geoespacial y análisis de mapas")

    if df.select_dtypes(include="number").shape[1] >= 2:
        uso_sugerido.append("📈 Modelos de predicción y regresión multivariada")

    if df.select_dtypes(include="object").shape[1] > 0 and df.shape[0] > 100:
        uso_sugerido.append("🧠 Clasificación y segmentación con machine learning")

    if "fecha" in ''.join(df.columns).lower():
        uso_sugerido.append("🕒 Series de tiempo y proyecciones")

    if len(uso_sugerido) == 0:
        st.warning("No se detectaron características suficientes para sugerir uso con IA.")
    else:
        for u in uso_sugerido:
            st.markdown(u)

# --- MÓDULO 7: Exportación de resultados y resumen general ---
def exportar_resultados(df):
    st.markdown("## 📤 Exportación y resumen final")
    st.markdown("Puedes descargar los datos junto con los resultados de los análisis anteriores.")

    # Generar resumen de columnas
    resumen = {
        "columnas": df.columns.tolist(),
        "tipos": [str(df[col].dtype) for col in df.columns],
        "nulos": df.isnull().sum().tolist(),
        "únicos": df.nunique().tolist()
    }
    resumen_df = pd.DataFrame(resumen)

    st.markdown("### 📝 Resumen del conjunto de datos")
    st.dataframe(resumen_df)

    st.download_button(
        label="📄 Descargar resumen en CSV",
        data=resumen_df.to_csv(index=False).encode("utf-8"),
        file_name="resumen_diagnostico.csv",
        mime="text/csv"
    )

    # Descarga final
    st.markdown("### Descargar tabla original (Excel)")
    output = io.BytesIO()
    df.to_excel(output, index=False)
    st.download_button(
        label="💾 Descargar datos",
        data=output.getvalue(),
        file_name="datos_cargados.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

# --- CARGUE DE ARCHIVO ---
uploaded_file = st.file_uploader("Cargar archivo CSV o Excel", type=["csv", "xlsx"])

if uploaded_file is not None:
    try:
        file_type = uploaded_file.name.split(".")[-1]
        if file_type == "csv":
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        st.success("Archivo cargado exitosamente.")
        st.markdown("### Vista preliminar de los datos")
        st.dataframe(df.head(100), use_container_width=True)

        # Diagnóstico básico
        st.markdown("## 🔍 Diagnóstico básico de calidad")
        n_filas, n_columnas = df.shape
        n_celdas = n_filas * n_columnas
        n_valores_nulos = df.isnull().sum().sum()
        porcentaje_nulos = (n_valores_nulos / n_celdas) * 100
        duplicados = df.duplicated().sum()
        tipos_columnas = df.dtypes.apply(lambda x: str(x)).value_counts()

        st.write(f"🔢 Filas: {n_filas} | Columnas: {n_columnas}")
        st.write(f"⚠️ Celdas vacías: {n_valores_nulos} ({porcentaje_nulos:.1f}%)")
        st.write(f"📎 Filas duplicadas: {duplicados}")
        st.write("📁 Tipos de dato detectados:")
        st.json(tipos_columnas.to_dict())

        # Errores por columna
        st.markdown("### Problemas detectados por columna")
        problemas = []
        for col in df.columns:
            if df[col].isnull().sum() > 0:
                problemas.append(f"🔴 Columna **'{col}'** tiene valores nulos")
            if df[col].dtype == 'object' and df[col].str.contains(r'[^ - ]', na=False).any():
                problemas.append(f"🟡 Columna **'{col}'** contiene caracteres especiales")
            if df[col].dtype != object and df[col].nunique() <= 1:
                problemas.append(f"⚠️ Columna **'{col}'** tiene solo un valor único")
        if problemas:
            for p in problemas:
                st.markdown(p)
        else:
            st.success("No se detectaron problemas evidentes.")

        # Módulos funcionales
        evaluar_calidad_interoperabilidad(df, uploaded_file)
        sugerencias_automaticas(df)
        construir_metadatos(df)
        ajustes_tecnicos(df)
        evaluar_uso_con_ia(df)
        exportar_resultados(df)

    except Exception as e:
        st.error(f"Ocurrió un error al procesar el archivo: {e}")
