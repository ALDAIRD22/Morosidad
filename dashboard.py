import streamlit as st
import pandas as pd
import plotly.express as px
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
# CARGA DE DATOS (Simulados con tus datos reales)
# ==========================================
@st.cache_data
def load_data():
    # 1. Datos de Olimpiadas (Tus datos reales)
    df_olim = pd.DataFrame({
        "Tutor": ["GARCIA GUTIERREZ LESLY SABINITA", "MARTINEZ HUAIRA NATALY YANDIRA", "BOZA VILLANUEVA MARIANA ADELAIDA", "SANCHEZ RAMOS CINTHYA JUNET", "ALCARRAZ TEJEDA ALEXANDER JAVIER", "CARRERA MARTINEZ VIRGINIA GABY", "ESPADA ARAOZ RODRIGO PAOLO"],
        "Ciclo": ["SEMI ANUAL ENERO-A", "SEMI ANUAL MARZO-A", "SEMI ANUAL MARZO-B", "INTENSIVO MARZO-A", "SEMI ABRIL -A", "INTENSIVO ABRIL-A", "SAN JUNIO"],
        "Matriculados": [63, 74, 62, 78, 48, 32, 109],
        "Meta": [51, 59, 51, 62, 38, 26, 82],
        "Pagantes": [51, 60, 31, 63, 20, 26, 34],
        "Meta Dinero": [1530, 1770, 1530, 1860, 1140, 780, 2460],
        "EFECTIVO": [588, 390, 210, 705.5, 250, 140, 210],
        "YAPE": [942, 1410, 720, 1184.5, 350, 640, 795],
        "Recaudado": [1530, 1800, 930, 1890, 600, 780, 1005],
        "Falta": [0, -30, 600, -30, 540, 0, 1455],
        "Avance %": [100, 102, 61, 102, 53, 100, 41]
    })
    
    # 2. Datos de Morosidad - Resumen (A2:I15)
    df_mor_resumen = pd.DataFrame({
        "FECHA": ["15/06", "15/06", "15/06", "15/06"],
        "CICLO": ["SEMI ENERO", "SEMI MARZO-A", "INTENSIVO MARZO", "SEMI MARZO-B"],
        "TUTO": ["LESLY", "NATALY", "CINTHYA", "MARIANA"],
        "MAT": [63, 74, 78, 62],
        "PAG": [59, 70, 75, 50],
        "SUS": [4, 4, 3, 12],
        "DES": ["6.3%", "5.4%", "3.8%", "19.3%"],
        "CUM": ["93.7%", "94.6%", "96.2%", "80.7%"],
        "NOT": [20, 20, 20, 10]
    })
    
    # 3. Datos de Morosidad - Alumnos (X2:AC86)
    df_mor_alumnos = pd.DataFrame({
        "DNI": ["72831111", "75302957", "73565909", "61423613"],
        "ALUMNO": ["CASTILLO VARGAS JOANN", "MENDOZA ARONI FABRICIO", "SANGAMA RAMIREZ ISAIAS", "SALAZAR TORRES ESTHEFANY"],
        "Tutor": ["LESLY", "LESLY", "NATALY", "MARIANA"],
        "CONDICIÓN PAGO": ["PAGA VIERNES", "SUSPENDIDO", "RETIRO", "DEBE 1 CUOTA"]
    })
    
    # 4. Datos de Cuotas (L3:U11)
    df_cuotas = pd.DataFrame({
        "CUOTA": [1, 2, 3, 4, 5, 6, 7],
        "SAN MAR": ["16-mar", "11-abr", "9-may", "6-jun", "4-jul", "8-ago", "5-sep"],
        "INT MAR": ["23-mar", "18-abr", "16-may", "13-jun", "11-jul", "15-ago", "-"],
        "SAN ABR": ["6-abr", "2-may", "30-may", "27-jun", "1-ago", "29-ago", "-"],
        "INT ABR": ["13-abr", "9-may", "6-jun", "4-jul", "8-ago", "-", "-"],
        "SAN MAY": ["4-may", "30-may", "27-jun", "1-ago", "-", "-", "-"],
        "INT MAY": ["11-may", "6-jun", "4-jul", "8-ago", "-", "-", "-"],
        "SAN JUL": ["-", "-", "-", "-", "-", "-", "-"],
        "REP JUL": ["-", "-", "-", "-", "-", "-", "-"],
        "SAN ENE": ["-", "-", "-", "-", "-", "-", "-"]
    })
    
    # 5. Datos de Análisis Académico (A1:J1000)
    df_analisis = pd.DataFrame({
        "TUTOR": ["LESLY", "LESLY", "NATALY", "CINTHYA", "MARIANA"],
        "CÓDIGO": ["A001", "A002", "A003", "A004", "A005"],
        "EXAMEN": ["EX1", "EX1", "EX1", "EX1", "EX1"],
        "ASISTENCIA": [100, 80, 95, 100, 60],
        "FALTA": [0, 2, 1, 0, 4],
        "NOTA": [18, 12, 15, 20, 9],
        "VARIACION": ["+2", "-1", "0", "+4", "-3"],
        "SICA": ["SI", "NO", "SI", "SI", "NO"],
        "C+D": [15, 10, 14, 18, 8],
        "CXM": [12, 8, 11, 15, 6]
    })
    
    return df_olim, df_mor_resumen, df_mor_alumnos, df_cuotas, df_analisis

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
    
    # Ranking de Tutores por Porcentaje
    st.subheader("🥇 Ranking de Tutores (Porcentaje de Avance)")
    df_ranking = df_olim.sort_values(by="Avance %", ascending=True) # Ascending para que el mayor quede arriba en Plotly
    fig_ranking = px.bar(df_ranking, x="Avance %", y="Tutor", orientation='h', text="Avance %", color="Avance %", color_continuous_scale="Viridis")
    fig_ranking.update_traces(texttemplate='%{text}%', textposition='outside')
    st.plotly_chart(fig_ranking, use_container_width=True)
    
    st.divider()
    
    st.subheader("🔎 Detalle Interactivo por Tutor")
    tutor_seleccionado = st.selectbox("Elegir Tutor:", df_olim["Tutor"].unique())
    
    datos_tutor = df_olim[df_olim["Tutor"] == tutor_seleccionado].iloc[0]
    avance = datos_tutor['Avance %']
    
    # Mensaje dinámico según porcentaje
    if avance >= 100:
        st.success(f"🌟 ¡Excelente, llegaste a la meta! ({avance}%)")
    elif avance >= 80:
        st.info(f"👍 ¡Buen trabajo! Estás muy cerca de la meta. ({avance}%)")
    elif avance >= 50:
        st.warning(f"⚠️ ¡Vamos! Aún falta para llegar a la meta. ({avance}%)")
    else:
        st.error(f"🚨 ¡Alerta! Porcentaje bajo, se necesita acción inmediata. ({avance}%)")
        
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Matriculados vs Meta", f"{datos_tutor['Matriculados']} / {datos_tutor['Meta']}")
    col2.metric("Pagantes", datos_tutor['Pagantes'])
    col3.metric("Recaudado Total", f"S/ {datos_tutor['Recaudado']}", f"Falta: S/ {datos_tutor['Falta']}")
    col4.metric("Avance %", f"{avance}%")
    
    fig_pie = px.pie(values=[datos_tutor["YAPE"], datos_tutor["EFECTIVO"]], names=["Yape", "Efectivo"], hole=0.5, title=f"Distribución de Pagos - {tutor_seleccionado}")
    st.plotly_chart(fig_pie, use_container_width=True)

# ==========================================
# PÁGINA 3: MOROSIDAD
# ==========================================
elif menu == "⚠️ Morosidad":
    st.title("⚠️ Panel de Morosidad y Pagos")
    
    total_sus = df_mor_resumen["SUS"].sum()
    deuda_acumulada = total_sus * 510
    
    st.subheader("Resumen Global de la Sede")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Matriculados (MAT)", df_mor_resumen["MAT"].sum())
    col2.metric("Pagantes (PAG)", df_mor_resumen["PAG"].sum())
    col3.metric("Suspendidos/Deserción", total_sus)
    col4.metric("Deuda Acumulada", f"S/ {deuda_acumulada:,.2f}", "- Crítico", delta_color="inverse")
    
    st.divider()
    
    col_izq, col_der = st.columns([1, 1])
    
    with col_izq:
        st.subheader("📊 Rendimiento por Tutor (A2:I15)")
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
    st.subheader("📅 Cuadro Completo de Cuotas (L3:U11)")
    st.dataframe(df_cuotas, use_container_width=True, hide_index=True)

# ==========================================
# PÁGINA 4: ANÁLISIS ACADÉMICO (IA)
# ==========================================
elif menu == "🤖 Análisis Académico":
    st.title("🤖 Asistente de Análisis Académico (A1:J1000)")
    st.markdown("Selecciona un tutor para generar un análisis basado en su hoja de notas.")
    
    tutor_ia = st.selectbox("Analizar rendimiento académico del tutor:", df_analisis["TUTOR"].unique())
    datos_ia = df_analisis[df_analisis["TUTOR"] == tutor_ia]
    
    with st.spinner(f"La IA está analizando los registros de {tutor_ia}..."):
        time.sleep(1.5)
        
    promedio_nota = datos_ia["NOTA"].mean()
    promedio_asistencia = datos_ia["ASISTENCIA"].mean()
    total_faltas = datos_ia["FALTA"].sum()
    
    diagnostico = "Sobresaliente" if promedio_nota >= 15 else "Regular" if promedio_nota >= 11 else "Deficiente"
    
    st.markdown(f"""
    <div class="ia-box">
        <h4>🧠 Insight Generado por IA para {tutor_ia}</h4>
        <p><strong>Diagnóstico Académico:</strong> Nivel {diagnostico}</p>
        <p>Se han analizado los registros del tutor <b>{tutor_ia}</b>. 
        El promedio de notas de sus alumnos es de <b>{promedio_nota:.1f}/20</b>, con una asistencia promedio del <b>{promedio_asistencia:.1f}%</b>.</p>
        <p>Se registran un total de <b>{total_faltas} faltas</b> acumuladas en los exámenes recientes.</p>
        <p><b>💡 Recomendación de la IA:</b> {"Excelente trabajo, continuar con los repasos de SICA." if diagnostico == "Sobresaliente" else "Reforzar los temas del último examen y hacer seguimiento a las inasistencias."}</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.subheader(f"Datos Analizados: {tutor_ia}")
    st.dataframe(datos_ia, use_container_width=True, hide_index=True)
