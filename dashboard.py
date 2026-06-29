import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import time

# ==========================================
# CONFIGURACIÓN DE LA PÁGINA
# ==========================================
st.set_page_config(page_title="Dashboard Comas 2026", page_icon="🔥", layout="wide")

st.markdown("""
    <style>
    @keyframes fadeIn { 0% { opacity: 0; transform: scale(0.9); } 100% { opacity: 1; transform: scale(1); } }
    .fade-in-text { animation: fadeIn 1s ease-in-out; text-align: center; }
    .title-comas { font-size: 3rem; font-weight: 900; background: -webkit-linear-gradient(45deg, #FF4B2B, #FF416C); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-align: center; padding: 20px; }
    div[data-testid="metric-container"] { background-color: #ffffff; border-left: 5px solid #FF4B2B; padding: 15px; border-radius: 5px; box-shadow: 2px 2px 10px rgba(0,0,0,0.1); transition: transform 0.3s; }
    div[data-testid="metric-container"]:hover { transform: translateY(-5px); }
    .ia-box { background-color: #f0f2f6; border-radius: 10px; padding: 20px; border-left: 5px solid #4CAF50; font-style: italic; }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# CARGA DE DATOS (CONECTADO EN VIVO A GOOGLE SHEETS)
# ==========================================
# ttl=300 actualiza los datos automáticamente cada 5 minutos
@st.cache_data(ttl=300)
def load_data():
    sheet_id = "1ABAEjZLFfVASDJGgYeSmikt0KmqAgNZiQzmlO8smMKY"
    
    # Enlaces a cada pestaña de tu Google Sheets
    url_olim = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid=272338387"
    url_mor = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid=0"
    url_ana = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid=2004118335"
    
    try:
        # 1. OLIMPIADAS
        df_olim = pd.read_csv(url_olim)
        df_olim.columns = df_olim.columns.str.strip() # Limpia espacios en los títulos
        df_olim = df_olim.dropna(subset=["Tutor"])
        
        # Limpiar símbolos de moneda y porcentaje para poder sumar y graficar
        cols_numericas_olim = ['Matriculados', 'Meta', 'Pagantes', 'EFECTIVO', 'YAPE', 'Recaudado', 'Falta', 'Avance %']
        for col in cols_numericas_olim:
            if col in df_olim.columns:
                df_olim[col] = pd.to_numeric(df_olim[col].astype(str).str.replace(r'[S/,\s%]', '', regex=True).str.replace('-', '0'), errors='coerce').fillna(0)

        # 2. MOROSIDAD - RESUMEN (A2:I15)
        df_mor_resumen = pd.read_csv(url_mor, skiprows=1, usecols=range(0, 9))
        df_mor_resumen.columns = ["FECHA", "CICLO", "TUTO", "MAT", "PAG", "SUS", "DES", "CUM", "NOT"]
        df_mor_resumen = df_mor_resumen.dropna(subset=["TUTO"])
        df_mor_resumen = df_mor_resumen[df_mor_resumen["TUTO"] != "TOTAL"] # Excluir fila de totales si existe
        for col in ["MAT", "PAG", "SUS"]:
            df_mor_resumen[col] = pd.to_numeric(df_mor_resumen[col], errors='coerce').fillna(0)

        # 3. MOROSIDAD - ALUMNOS (X2:AC200)
        df_mor_alumnos = pd.read_csv(url_mor, skiprows=1, usecols=range(23, 29))
        df_mor_alumnos.columns = ["#", "DNI", "ALUMNO", "CORTE", "Tutor", "CONDICIÓN PAGO"]
        df_mor_alumnos = df_mor_alumnos.dropna(subset=["DNI", "ALUMNO"])

        # 4. CUOTAS (L3:U11)
        df_cuotas = pd.read_csv(url_mor, skiprows=2, usecols=range(11, 21))
        df_cuotas.columns = ["CUOTA", "SAN MAR", "INT MAR", "SAN ABR", "INT ABR", "SAN MAY", "INT MAY", "SAN JUL", "REP JUL", "SAN ENE"]
        df_cuotas = df_cuotas.dropna(subset=["CUOTA"])

        # 5. ANÁLISIS ACADÉMICO
        df_analisis = pd.read_csv(url_ana)
        df_analisis.columns = df_analisis.columns.str.strip()
        df_analisis = df_analisis.dropna(subset=["TUTOR", "NOTA"])
        for col in ["NOTA", "ASISTENCIA", "FALTA"]:
            if col in df_analisis.columns:
                df_analisis[col] = pd.to_numeric(df_analisis[col].astype(str).str.replace('%', ''), errors='coerce').fillna(0)

        return df_olim, df_mor_resumen, df_mor_alumnos, df_cuotas, df_analisis
    
    except Exception as e:
        st.error(f"Error al conectar con Google Sheets. Asegúrate de que el archivo sea público (Cualquier usuario que tenga el vínculo). Detalle: {e}")
        st.stop()

# Cargar los datos
df_olim, df_mor_resumen, df_mor_alumnos, df_cuotas, df_analisis = load_data()

# ==========================================
# BARRA LATERAL (NAVEGACIÓN)
# ==========================================
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3048/3048122.png", width=100)
st.sidebar.title("Menú Principal")
menu = st.sidebar.radio("Navegación:", ("🏠 Inicio", "🏆 Olimpiadas", "⚠️ Morosidad", "🤖 Análisis Académico"))

# ==========================================
# PÁGINA 1: INICIO
# ==========================================
if menu == "🏠 Inicio":
    st.balloons()
    st.markdown('<div class="fade-in-text"><p class="title-comas">¡BIENVENIDO A LA SEDE COMAS!</p><h2>🔥 LA MEJOR SEDE - LA NÚMERO 1 🔥</h2></div>', unsafe_allow_html=True)
    
    st.subheader("Sube tu propia imagen de la sede aquí:")
    imagen_subida = st.file_uploader("Elige una imagen (JPG/PNG)", type=["jpg", "png", "jpeg"])
    
    if imagen_subida is not None:
        st.image(imagen_subida, use_column_width=True, caption="Sede Comas - Oficial")
    else:
        st.image("https://images.unsplash.com/photo-1522202176988-66273c2fd55f?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80", use_column_width=True, caption="Sube una foto arriba para cambiar esta imagen")

# ==========================================
# PÁGINA 2: OLIMPIADAS
# ==========================================
elif menu == "🏆 Olimpiadas":
    st.title("🏆 Recaudación Olimpiadas")
    
    st.subheader("🥇 Ranking de Tutores (Porcentaje de Avance)")
    df_ranking = df_olim.sort_values(by="Avance %", ascending=True)
    fig_ranking = px.bar(df_ranking, x="Avance %", y="Tutor", orientation='h', text="Avance %", color="Avance %", color_continuous_scale="Viridis")
    fig_ranking.update_traces(texttemplate='%{text}%', textposition='outside')
    st.plotly_chart(fig_ranking, use_container_width=True)
    
    st.divider()
    
    st.subheader("🔎 Detalle Interactivo por Tutor")
    tutor_seleccionado = st.selectbox("Elegir Tutor:", df_olim["Tutor"].unique())
    
    datos_tutor = df_olim[df_olim["Tutor"] == tutor_seleccionado].iloc[0]
    avance = datos_tutor['Avance %']
    
    if avance >= 100:
        st.success(f"🌟 ¡Excelente, llegaste a la meta! ({avance}%)")
    elif avance >= 80:
        st.info(f"👍 ¡Buen trabajo! Estás muy cerca de la meta. ({avance}%)")
    elif avance >= 50:
        st.warning(f"⚠️ ¡Vamos! Aún falta para llegar a la meta. ({avance}%)")
    else:
        st.error(f"🚨 ¡Alerta! Porcentaje bajo, se necesita acción inmediata. ({avance}%)")
        
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Matriculados vs Meta", f"{int(datos_tutor['Matriculados'])} / {int(datos_tutor['Meta'])}")
    col2.metric("Pagantes", int(datos_tutor['Pagantes']))
    col3.metric("Recaudado Total", f"S/ {datos_tutor['Recaudado']:,.2f}", f"Falta: S/ {datos_tutor['Falta']:,.2f}")
    col4.metric("Avance %", f"{avance}%")
    
    fig_pie = px.pie(values=[datos_tutor["YAPE"], datos_tutor["EFECTIVO"]], names=["Yape", "Efectivo"], hole=0.5, title=f"Distribución de Pagos - {tutor_seleccionado}")
    st.plotly_chart(fig_pie, use_container_width=True)

# ==========================================
# PÁGINA 3: MOROSIDAD
# ==========================================
elif menu == "⚠️ Morosidad":
    st.title("⚠️ Panel de Morosidad y Pagos")
    
    total_mat = int(df_mor_resumen["MAT"].sum())
    total_pag = int(df_mor_resumen["PAG"].sum())
    total_sus = int(df_mor_resumen["SUS"].sum())
    deuda_acumulada = total_sus * 510
    
    st.subheader("Resumen Global de la Sede")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Matriculados (TOTAL)", total_mat)
    col2.metric("Pagantes (TOTAL)", total_pag)
    col3.metric("Suspendidos/Deserción", total_sus)
    col4.metric("Deuda Acumulada", f"S/ {deuda_acumulada:,.2f}", "- Crítico", delta_color="inverse")
    
    st.divider()
    
    col_izq, col_der = st.columns([1, 1])
    
    with col_izq:
        st.subheader("📊 Rendimiento por Tutor")
        st.dataframe(df_mor_resumen, use_container_width=True, hide_index=True)
        
    with col_der:
        st.subheader("🚨 Lista de Morosos Filtrada")
        tutor_moroso = st.selectbox("Filtrar alumnos del tutor:", ["Todos"] + list(df_mor_alumnos["Tutor"].unique()))
        
        if tutor_moroso == "Todos":
            st.dataframe(df_mor_alumnos, use_container_width=True, hide_index=True)
        else:
            df_filtrado = df_mor_alumnos[df_mor_alumnos["Tutor"] == tutor_moroso]
            st.dataframe(df_filtrado, use_container_width=True, hide_index=True)
            
    st.divider()
    st.subheader("📅 Cuadro Completo de Cuotas")
    st.dataframe(df_cuotas, use_container_width=True, hide_index=True)

# ==========================================
# PÁGINA 4: ANÁLISIS ACADÉMICO (IA)
# ==========================================
elif menu == "🤖 Análisis Académico":
    st.title("🤖 Asistente de Análisis Académico")
    st.markdown("Selecciona un tutor para ver su evolución en todos los exámenes (EXSA, EXSI, etc.).")
    
    tutor_ia = st.selectbox("Analizar rendimiento académico del tutor:", df_analisis["TUTOR"].unique())
    datos_ia = df_analisis[df_analisis["TUTOR"] == tutor_ia]
    
    with st.spinner(f"La IA está analizando los registros de {tutor_ia}..."):
        time.sleep(1.5)
        
    promedio_nota = datos_ia["NOTA"].mean()
    promedio_asistencia = datos_ia["ASISTENCIA"].mean()
    total_faltas = datos_ia["FALTA"].sum()
    
    diagnostico = "Sobresaliente" if promedio_nota >= 1000 else "Regular" if promedio_nota >= 800 else "Deficiente"
    
    st.markdown(f"""
    <div class="ia-box">
        <h4>🧠 Insight Generado por IA para {tutor_ia}</h4>
        <p><strong>Diagnóstico Académico:</strong> Nivel {diagnostico}</p>
        <p>Se han analizado los registros del tutor <b>{tutor_ia}</b>. 
        El promedio de notas de sus alumnos es de <b>{promedio_nota:.1f} puntos</b>, con una asistencia promedio de <b>{promedio_asistencia:.1f} alumnos por examen</b>.</p>
        <p>Se registran un total de <b>{int(total_faltas)} faltas</b> acumuladas en los exámenes recientes.</p>
        <p><b>💡 Recomendación de la IA:</b> {"Excelente trabajo, el puntaje es alto. Mantener el ritmo en los simulacros." if diagnostico == "Sobresaliente" else "Reforzar los temas del último examen y hacer seguimiento a las inasistencias."}</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    st.subheader(f"📈 Evolución de Notas por Examen - {tutor_ia}")
    fig_notas = px.line(datos_ia, x="EXAMEN", y="NOTA", markers=True, text="NOTA", title="Tendencia de Puntaje")
    fig_notas.update_traces(textposition="top center")
    st.plotly_chart(fig_notas, use_container_width=True)
    
    st.subheader(f"📑 Base de Datos Analizada: {tutor_ia}")
    st.dataframe(datos_ia, use_container_width=True, hide_index=True)
