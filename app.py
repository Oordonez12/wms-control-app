import streamlit as st
import pandas as pd
from google import genai

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(
    page_title="WMS AI Assistant",
    page_icon="🤖",
    layout="wide"
)

# --- CONFIGURACIÓN DE LA API DE IA (GEMINI) ---
st.sidebar.title("⚙️ Configuración")
api_key_input = st.sidebar.text_input("Ingresa tu Google Gemini API Key", type="password")

if api_key_input:
    client = genai.Client(api_key=api_key_input)
else:
    client = None

# --- MARCA DE AGUA Y ESTILO ---
st.markdown("""
    <style>
    .watermark {
        position: fixed; bottom: 10px; right: 15px;
        background-color: rgba(0, 0, 0, 0.8); color: #00ffcc;
        padding: 5px 12px; border-radius: 8px; font-size: 12px;
        font-family: monospace; z-index: 99999; pointer-events: none;
    }
    </style>
    <div class="watermark">🔒 Creado por [Tu Nombre] | WMS AI Analytics</div>
""", unsafe_allow_html=True)

st.title("⚡ WMS Scale: Panel Inteligente con IA")
st.markdown("Automatiza el análisis de recibos, inventarios, surtido y reabastos sin pasar horas en Excel.")

# --- CARGA DE ARCHIVO O DATOS DE PRUEBA ---
uploaded_file = st.sidebar.file_uploader("Sube tu reporte de Manhattan WMS (Excel/CSV)", type=["csv", "xlsx"])

if uploaded_file is not None:
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)
    st.sidebar.success("¡Reporte cargado correctamente!")
else:
    st.sidebar.info("💡 Mostrando datos de prueba. Sube tu archivo real en la parte superior.")
    data = {
        "Area": ["Recibo", "Recibo", "Surtido", "Surtido", "Reabasto"],
        "Proceso": ["Carga/Descarga", "Aduanado", "QC Error", "Surtido Normal", "Reabasto Local"],
        "Tiempo_Minutos": [45, 30, 15, 120, 25],
        "Eficiencia_O_Precision": [0.95, 0.98, 0.85, 0.99, 1.0],
        "Operador": ["Carlos M.", "Carlos M.", "Ana L.", "Juan P.", "Ana L."]
    }
    df = pd.DataFrame(data)

# --- PESTAÑAS DE ANÁLISIS ---
tab1, tab2, tab3 = st.tabs(["📊 Vista General y Datos", "🤖 Análisis Inteligente (IA)", "📈 Reporte Ejecutivo"])

with tab1:
    st.subheader("Datos Procesados (Sin ruido de WMS)")
    st.dataframe(df, use_container_width=True)

with tab2:
    st.subheader("Pregúntale a la IA sobre tu operación")
    st.markdown("Hazle preguntas directas a los datos procesados (ej: *'¿Qué operador tuvo más retrasos en recibo?'* o *'¿Cuáles fueron los principales errores de QC?'*)")
    
    pregunta_usuario = st.text_input("Escribe tu consulta operativa:")
    
    if st.button("Analizar con IA"):
        if not client:
            st.warning("⚠️ Por favor ingresa tu API Key de Gemini en la barra lateral.")
        else:
            with st.spinner("La IA está analizando los datos..."):
                data_text = df.to_string()
                prompt = f"""
                Eres un experto en logística y operaciones de almacén usando Manhattan WMS. 
                Basándote en los siguientes datos operativos:
                {data_text}
                
                Responde de forma profesional, clara y directa a la siguiente pregunta o requerimiento del supervisor:
                "{pregunta_usuario}"
                """
                
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=prompt
                )
                st.success("Análisis completado:")
                st.markdown(response.text)

with tab3:
    st.subheader("Generación de Resumen Ejecutivo para Jefes")
    st.markdown("Genera un reporte redactado automáticamente para enviar por correo o WhatsApp a la gerencia.")
    
    if st.button("✨ Generar Informe Ejecutivo Automático"):
        if not client:
            st.warning("⚠️ Por favor ingresa tu API Key de Gemini en la barra lateral.")
        else:
            with st.spinner("Redactando informe ejecutivo..."):
                data_text = df.to_string()
                prompt = f"""
                Actúa como el coordinador de operaciones y redacta un resumen ejecutivo formal y conciso 
                para los jefes de área, basándote en estos datos de WMS:
                {data_text}
                
                Destaca tiempos clave, eficiencias y áreas de oportunidad detectadas.
                """
                
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=prompt
                )
                st.markdown(response.text)
