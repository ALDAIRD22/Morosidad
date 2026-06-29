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
# CARGA DE DATOS
# ==========================================
@st.cache_data
def load_data():
    # 1. Olimpiadas
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
    
    # 2. Morosidad - Resumen Exacto
    df_mor_resumen = pd.DataFrame({
        "FECHA": ["20-06-2026", "20-06-2026", "20-06-2026", "27-06-2026", "27-06-2026", "27-06-2026", "27-06-2026", "27-06-2026", "04-07-2026", "04-07-2026", "04-07-2026", "04-07-2026"],
        "CICLO": ["SAN EN", "MATE SABATINO", "CIENCIAS 0", "SAN ABRIL", "INT ABRIL", "SAN MAYO", "INT MAYO", "MATE 0", "INT MARZO", "SAN MAR A", "SAN MAR B", "ESCOLARES"],
        "TUTO": ["LESLY", "MAJA", "MAJA", "ALEXANDER", "GABY", "RODRIGO", "RODRIGO", "MAJA", "CINTHYA", "NATALY", "MARIANA", "MAJA"],
        "MAT": [63, 46, 23, 48, 32, 84, 25, 6, 78, 74, 62, 11],
        "PAG": [59, 37, 15, 29, 32, 59, 5, 6, 78, 74, 62, 11],
        "SUS": [4, 9, 8, 19, 0, 25, 20, 0, 0, 0, 0, 0],
        "DES": ["6.3%", "19.6%", "34.8%", "39.6%", "0.0%", "29.8%", "80.0%", "0.0%", "0.0%", "0.0%", "0.0%", "0.0%"],
        "CUM": ["93.7%", "80.4%", "65.2%", "60.4%", "100.0%", "70.2%", "20.0%", "100.0%", "100.0%", "100.0%", "100.0%", "100.0%"],
        "NOT": [20, 10, 10, 10, 20, 10, 10, 20, 20, 20, 20, 20]
    })
    
    # 3. Morosidad - Alumnos (Rango X2:AC200)
    # NOTA: Aquí debes pegar los datos de tus 200 alumnos separados por comas.
    df_mor_alumnos = pd.DataFrame({
        "DNI": ["72831111", "75302957", "73565909", "61423613", "72053356"], # <-- Pega los 200 DNIs aquí
        "ALUMNO": ["CASTILLO VARGAS JOANN", "MENDOZA ARONI FABRICIO", "SANGAMA RAMIREZ ISAIAS", "SALAZAR TORRES ESTHEFANY", "SAAVEDRA CHAVEZ DARIANA"], # <-- Pega los 200 Nombres aquí
        "Tutor": ["LESLY", "LESLY", "ALEXANDER", "RODRIGO", "RODRIGO"], # <-- Pega los 200 Tutores aquí
        "CONDICIÓN PAGO": ["PAGA VIERNES", "SUSPENDIDO", "DEBE 1 CUOTA", "RETIRO", "PAGA VIERNES"] # <-- Pega las 200 Condiciones aquí
    })
    
    # 4. Cuotas (L3:U11 Exacto)
    df_cuotas = pd.DataFrame({
        "CUOTA": [1, 2, 3, 4, 5, 6, 7],
        "SAN MAR": ["16-mar", "11-abr", "9-may", "6-jun", "4-jul", "8-ago", "5-sep"],
        "INT MAR": ["16-mar", "11-abr", "9-may", "6-jun", "4-jul", "8-ago", "5-sep"],
        "SAN ABR": ["6-abr", "2-may", "30-may", "27-jun", "1-ago", "29-ago", "20-jun"],
        "INT ABR": ["6-abr", "2-may", "30-may", "27-jun", "31-oct", "28-nov", "-"],
        "SAN MAY": ["4-may", "30-may", "27-jun", "1-ago", "31-oct", "28-nov", "-"],
        "INT MAY": ["4-may", "30-may", "27-jun", "1-ago", "25-abr", "23-may", "-"],
        "SAN JUL": ["6-jul", "8-ago", "5-sep", "3-oct", "-", "-", "-"],
        "REP JUL": ["6-jul", "8-ago", "5-sep", "3-oct", "-", "-", "-"],
        "SAN ENE": ["2-ene", "31-ene", "28-feb", "28-mar", "25-abr", "23-may", "-"]
    })
    
    # 5. Análisis Académico (Datos exactos de Lesly con variaciones en %)
    df_analisis = pd.DataFrame({
        "TUTOR": ["GARCIA LESLY", "GARCIA LESLY", "GARCIA LESLY", "GARCIA LESLY", "GARCIA LESLY"],
        "CÓDIGO": ["SMSAN0126P9A", "SMSAN0126P9A", "SMSAN0126P9A", "SMSAN0126P9A", "SMSAN0126P9A"],
        "EXAMEN": ["EXSA 1", "EXSA 2", "EXSA 3", "EXSA 4", "EXSA 5"],
        "ASISTENCIA": [60, 54, 52, 53, 57],
        "FALTA": [3, 9, 11, 10, 6],
        "NOTA": [1071.7, 998.99, 1076.06, 1091.84, 1052.9],
        "VARIACION": ["100.0%", "-6.8%", "7.7%", "1.5%", "-3.6%"],
        "SICA": [10, 5, 8, 10, 9],
        "C+D": ["AC - RV - CI", "IG-CI-LI", "AC-RV-EC", "HU-AC-LI", "HU-RV-PS"],
        "CXM": ["QUI - FI - GEF-MAT", "HP-FI-AR", "QU-RM-AL", "GF-TR-HP", "QU-AL-FI"]
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
    
    total_mat = df_mor_resumen["MAT"].sum()
    total_pag = df_mor_resumen["PAG"].sum()
    total_sus = df_mor_resumen["SUS"].sum()
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
        st.subheader("🚨 Lista de Morosos Filtrada (X2:AC200)")
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
        <p>Se registran un total de <b>{total_faltas} faltas</b> acumuladas en los exámenes recientes.</p>
        <p><b>💡 Recomendación de la IA:</b> {"Excelente trabajo, el puntaje es alto. Mantener el ritmo en los simulacros." if diagnostico == "Sobresaliente" else "Reforzar los temas del último examen y hacer seguimiento a las inasistencias."}</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    # Gráfica de evolución de exámenes (EXSA, EXSI, etc.)
    st.subheader(f"📈 Evolución de Notas por Examen - {tutor_ia}")
    fig_notas = px.line(datos_ia, x="EXAMEN", y="NOTA", markers=True, text="NOTA", title="Tendencia de Puntaje")
    fig_notas.update_traces(textposition="top center")
    st.plotly_chart(fig_notas, use_container_width=True)
    
    st.subheader(f"📑 Base de Datos Analizada: {tutor_ia}")
    st.dataframe(datos_ia, use_container_width=True, hide_index=True) 
