import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import time
import io

# ==========================================
# CONFIGURACIÓN DE LA PÁGINA Y FUENTES
# ==========================================
st.set_page_config(page_title="Dashboard Comas 2026", page_icon="🔥", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;800&display=swap');
    
    html, body, [class*="css"] { font-family: 'Poppins', sans-serif; }
    
    @keyframes fadeInUp { 0% { opacity: 0; transform: translateY(20px); } 100% { opacity: 1; transform: translateY(0); } }
    .animate-up { animation: fadeInUp 0.6s ease-out; }
    
    .title-comas { font-size: 3.5rem; font-weight: 800; background: linear-gradient(45deg, #FF4B2B, #FF416C); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-align: center; padding: 10px; margin-bottom: 0; }
    .subtitle { text-align: center; color: #555; font-size: 1.2rem; font-weight: 300; margin-bottom: 30px; }
    
    .web-card { background: white; padding: 25px; border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.08); margin-bottom: 25px; border-top: 5px solid #FF4B2B; transition: transform 0.3s ease; }
    .web-card:hover { transform: translateY(-5px); }
    
    .hall-of-fame { background: linear-gradient(135deg, #FFD700, #FDB931); padding: 20px; border-radius: 15px; color: white; text-align: center; box-shadow: 0 10px 20px rgba(255, 215, 0, 0.3); margin-bottom: 25px; }
    .hall-of-fame h3 { color: white; font-weight: 800; margin:0; }
    .tutor-star { font-size: 1.2rem; font-weight: 600; background: rgba(255,255,255,0.2); padding: 5px 15px; border-radius: 20px; display: inline-block; margin: 5px; }
    
    .ia-box { background: linear-gradient(135deg, #f6f8fd 0%, #f1f5f9 100%); border-radius: 15px; padding: 25px; border-left: 6px solid #4CAF50; box-shadow: 0 5px 15px rgba(0,0,0,0.05); }
    
    .greeting { font-size: 1.1rem; font-weight: 400; color: #333; text-align: left; margin-top: 30px; padding: 25px; background: rgba(255, 75, 43, 0.05); border-radius: 15px; border-left: 6px solid #FF4B2B;}
    
    /* Estilo para las pestañas (Tabs) */
    .stTabs [data-baseweb="tab-list"] { gap: 24px; }
    .stTabs [data-baseweb="tab"] { height: 50px; white-space: pre-wrap; background-color: transparent; border-radius: 4px 4px 0px 0px; gap: 1px; padding-top: 10px; padding-bottom: 10px; font-weight: 600; font-size: 1.1rem; }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# CARGA DE DATOS (CONECTADO EN VIVO)
# ==========================================
@st.cache_data(ttl=300)
def load_data():
    sheet_id = "1ABAEjZLFfVASDJGgYeSmikt0KmqAgNZiQzmlO8smMKY"
    url_olim = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid=272338387"
    url_mor = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid=0"
    url_ana = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid=2004118335"
    
    try:
        # 1. OLIMPIADAS
        df_olim = pd.read_csv(url_olim)
        df_olim.columns = df_olim.columns.str.strip()
        df_olim = df_olim.dropna(subset=["Tutor"])
        df_olim = df_olim[~df_olim['Tutor'].astype(str).str.upper().str.contains('TOTAL')]
        for col in ['Matriculados', 'Meta', 'Pagantes', 'EFECTIVO', 'YAPE', 'Recaudado', 'Falta', 'Avance %']:
            if col in df_olim.columns:
                df_olim[col] = pd.to_numeric(df_olim[col].astype(str).str.replace(r'[S/,\s%]', '', regex=True).str.replace('-', '0'), errors='coerce').fillna(0)

        # 2. MOROSIDAD - RESUMEN
        df_mor_resumen = pd.read_csv(url_mor, skiprows=1, usecols=range(0, 9))
        df_mor_resumen.columns = ["FECHA", "CICLO", "TUTO", "MAT", "PAG", "SUS", "DES", "CUM", "NOT"]
        df_mor_resumen = df_mor_resumen.dropna(subset=["TUTO"])
        df_mor_resumen = df_mor_resumen[~df_mor_resumen["TUTO"].astype(str).str.upper().str.contains('TOTAL')]
        for col in ["MAT", "PAG", "SUS", "NOT"]:
            df_mor_resumen[col] = pd.to_numeric(df_mor_resumen[col], errors='coerce').fillna(0)

        # 3. MOROSIDAD - ALUMNOS (AHORA LEE HASTA LA COLUMNA DE CELULAR)
        # range(23, 30) lee desde la columna X hasta la AD
        df_mor_alumnos = pd.read_csv(url_mor, skiprows=1, usecols=range(23, 30))
        df_mor_alumnos.columns = ["#", "DNI", "ALUMNO", "CORTE", "Tutor", "CONDICIÓN PAGO", "Celular"]
        df_mor_alumnos = df_mor_alumnos.dropna(subset=["DNI", "ALUMNO"])

        # 4. CUOTAS
        df_cuotas = pd.read_csv(url_mor, skiprows=3, usecols=range(11, 21))
        df_cuotas.columns = ["CUOTA", "SAN MAR", "INT MAR", "SAN ABR", "INT ABR", "SAN MAY", "INT MAY", "SAN JUL", "REP JUL", "SAN ENE"]
        df_cuotas = df_cuotas.dropna(subset=["CUOTA"])

        # 5. ANÁLISIS ACADÉMICO
        df_analisis = pd.read_csv(url_ana)
        df_analisis.columns = df_analisis.columns.str.strip()
        df_analisis = df_analisis.dropna(subset=["TUTOR", "NOTA"])
        for col in ["NOTA", "ASISTENCIA", "FALTA", "SICA"]:
            if col in df_analisis.columns:
                df_analisis[col] = pd.to_numeric(df_analisis[col].astype(str).str.replace('%', ''), errors='coerce').fillna(0)

        return df_olim, df_mor_resumen, df_mor_alumnos, df_cuotas, df_analisis
    except Exception as e:
        st.error(f"Error al conectar con Google Sheets. Detalle: {e}")
        st.stop()

df_olim, df_mor_resumen, df_mor_alumnos, df_cuotas, df_analisis = load_data()

@st.cache_data
def convert_df(df):
    return df.to_csv(index=False).encode('utf-8')

# ==========================================
# BARRA LATERAL (NAVEGACIÓN)
# ==========================================
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3048/3048122.png", width=100)
st.sidebar.title("Navegación Web")
menu = st.sidebar.radio("", ("🏠 Inicio", "🏆 Olimpiadas", "⚠️ Morosidad", "🤖 Análisis Académico"))

# ==========================================
# PÁGINA 1: INICIO
# ==========================================
if menu == "🏠 Inicio":
    st.balloons()
    st.markdown('<div class="animate-up"><p class="title-comas">SISTEMA WEB COMAS</p><p class="subtitle">🔥 LA MEJOR SEDE - LA NÚMERO 1 🔥</p></div>', unsafe_allow_html=True)
    
    st.markdown('<div class="web-card">', unsafe_allow_html=True)
    st.subheader("📸 Portada de la Sede")
    imagen_subida = st.file_uploader("Sube una imagen de tu equipo (JPG/PNG)", type=["jpg", "png", "jpeg"])
    if imagen_subida is not None:
        st.image(imagen_subida, use_column_width=True, caption="Sede Comas - Oficial")
    else:
        st.image("https://images.unsplash.com/photo-1522202176988-66273c2fd55f?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80", use_column_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# PÁGINA 2: OLIMPIADAS
# ==========================================
elif menu == "🏆 Olimpiadas":
    st.markdown('<p class="title-comas" style="font-size: 2.5rem;">Recaudación Olimpiadas</p>', unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["📊 Resumen Global", "🎯 Detalle por Tutor"])
    
    with tab1:
        st.markdown('<div class="web-card animate-up">', unsafe_allow_html=True)
        st.subheader("💰 Resumen Global de la Sede")
        col_tot1, col_tot2, col_tot3 = st.columns(3)
        col_tot1.metric("Total Recaudado", f"S/ {df_olim['Recaudado'].sum():,.2f}")
        col_tot2.metric("Total Yape", f"S/ {df_olim['YAPE'].sum():,.2f}")
        col_tot3.metric("Total Efectivo", f"S/ {df_olim['EFECTIVO'].sum():,.2f}")
        
        st.divider()
        st.subheader("🥇 Ranking de Tutores (Avance %)")
        df_ranking = df_olim.sort_values(by="Avance %", ascending=True)
        fig_ranking = px.bar(df_ranking, x="Avance %", y="Tutor", orientation='h', text="Avance %", color="Avance %", color_continuous_scale="Sunsetdark")
        fig_ranking.update_traces(texttemplate='%{text}%', textposition='outside')
        st.plotly_chart(fig_ranking, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with tab2:
        st.markdown('<div class="web-card animate-up">', unsafe_allow_html=True)
        st.subheader(f"🔎 Panel de Control del Tutor")
        tutor_seleccionado = st.selectbox("Selecciona un Tutor:", df_olim["Tutor"].unique())
        
        datos_tutor = df_olim[df_olim["Tutor"] == tutor_seleccionado].iloc[0]
        avance = datos_tutor['Avance %']
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Matriculados vs Meta", f"{int(datos_tutor['Matriculados'])} / {int(datos_tutor['Meta'])}")
        col2.metric("Pagantes", int(datos_tutor['Pagantes']))
        col3.metric("Recaudado Total", f"S/ {datos_tutor['Recaudado']:,.2f}")
        col4.metric("Falta Recaudar", f"S/ {datos_tutor['Falta']:,.2f}")
        
        st.divider()
        
        col_graf1, col_graf2 = st.columns(2)
        
        with col_graf1:
            fig_gauge = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = avance,
                title = {'text': "Velocímetro de Avance %"},
                gauge = {
                    'axis': {'range': [None, 120]},
                    'bar': {'color': "#FF4B2B"},
                    'steps': [
                        {'range': [0, 50], 'color': "#ffebee"},
                        {'range': [50, 80], 'color': "#fff9c4"},
                        {'range': [80, 120], 'color': "#e8f5e9"}],
                    'threshold': {'line': {'color': "green", 'width': 4}, 'thickness': 0.75, 'value': 100}
                }
            ))
            st.plotly_chart(fig_gauge, use_container_width=True)
            
        with col_graf2:
            fig_pie = px.pie(values=[datos_tutor["YAPE"], datos_tutor["EFECTIVO"]], names=["Yape", "Efectivo"], hole=0.5, title="Distribución de Pagos")
            st.plotly_chart(fig_pie, use_container_width=True)
            
        st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# PÁGINA 3: MOROSIDAD
# ==========================================
elif menu == "⚠️ Morosidad":
    st.markdown('<p class="title-comas" style="font-size: 2.5rem;">Panel de Morosidad</p>', unsafe_allow_html=True)
    
    total_mat = df_mor_resumen['MAT'].sum()
    total_sus = df_mor_resumen['SUS'].sum()
    pct_morosidad = (total_sus / total_mat * 100) if total_mat > 0 else 0
    
    st.markdown('<div class="web-card animate-up">', unsafe_allow_html=True)
    col_m1, col_m2, col_m3 = st.columns(3)
    col_m1.metric("Población Total", int(total_mat))
    col_m2.metric("Morosos (Suspendidos)", int(total_sus))
    col_m3.metric("Índice de Morosidad", f"{pct_morosidad:.1f}%", delta="- Crítico" if pct_morosidad > 15 else "Estable", delta_color="inverse")
    st.markdown('</div>', unsafe_allow_html=True)
    
    tutores_20 = df_mor_resumen[df_mor_resumen['NOT'] == 20]['TUTO'].unique()
    if len(tutores_20) > 0:
        estrellas_html = "".join([f"<span class='tutor-star'>⭐ {t}</span>" for t in tutores_20])
        st.markdown(f"<div class='hall-of-fame animate-up'><h3>🏆 SALÓN DE LA FAMA - NOTA 20 🏆</h3><p>¡Gestión perfecta!</p>{estrellas_html}</div>", unsafe_allow_html=True)

    tab_mor1, tab_mor2, tab_mor3 = st.tabs(["📊 Deuda por Salón", "🚨 Lista Interactiva de Morosos", "📅 Cronograma de Cuotas"])
    
    with tab_mor1:
        st.markdown('<div class="web-card">', unsafe_allow_html=True)
        df_mor_resumen['DEUDA_SALON'] = df_mor_resumen['SUS'] * 510
        fig_deuda = px.bar(df_mor_resumen, x="TUTO", y="DEUDA_SALON", text="DEUDA_SALON", color="DEUDA_SALON", color_continuous_scale="Reds", title="Deuda Acumulada por Salón (S/)")
        fig_deuda.update_traces(texttemplate='S/ %{text:,.2f}', textposition='outside')
        st.plotly_chart(fig_deuda, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with tab_mor2:
        st.markdown('<div class="web-card">', unsafe_allow_html=True)
        col_filtro, col_btn = st.columns([3, 1])
        with col_filtro:
            tutor_moroso = st.selectbox("Filtrar alumnos por tutor:", ["Todos"] + list(df_mor_alumnos["Tutor"].unique()))
            
        df_filtrado = df_mor_alumnos if tutor_moroso == "Todos" else df_mor_alumnos[df_mor_alumnos["Tutor"] == tutor_moroso]
        
        with col_btn:
            st.markdown("<br>", unsafe_allow_html=True)
            csv_data = convert_df(df_filtrado)
            st.download_button(label="📥 Descargar Reporte (CSV)", data=csv_data, file_name=f"Morosos_{tutor_moroso}.csv", mime='text/csv')
        
        # =========================================================================================
        # BOTÓN DE WHATSAPP DINÁMICO (LEE LA COLUMNA CELULAR DE TU EXCEL)
        # =========================================================================================
        df_mostrar = df_filtrado.copy()
        
        # Limpia la columna celular (elimina espacios o símbolos que hayas puesto por error en el Excel)
        df_mostrar['Celular_Limpio'] = df_mostrar['Celular'].astype(str).str.replace(r'\D', '', regex=True)
        
        # Genera el enlace de WhatsApp usando el número de cada alumno
        df_mostrar['Acción'] = "https://wa.me/" + df_mostrar['Celular_Limpio'] + "?text=Hola%20apoderado%20de%20" + df_mostrar['ALUMNO'].astype(str).str.replace(' ', '%20') + ",%20le%20escribimos%20de%20la%20Sede%20Comas%20para%20recordarle%20amablemente%20el%20pago%20de%20su%20cuota%20pendiente.%20Muchas%20gracias."
        
        # Ocultamos la columna temporal para que la tabla se vea limpia
        df_mostrar = df_mostrar.drop(columns=['Celular_Limpio'])
        
        st.dataframe(
            df_mostrar, 
            use_container_width=True, 
            hide_index=True,
            column_config={
                "Acción": st.column_config.LinkColumn("Enviar WhatsApp 💬", display_text="Cobrar por WS")
            }
        )
        st.info("💡 Haz clic en 'Cobrar por WS' para abrir el chat directamente con el número que pusiste en tu Excel.")
        st.markdown('</div>', unsafe_allow_html=True)

    with tab_mor3:
        st.markdown('<div class="web-card">', unsafe_allow_html=True)
        st.dataframe(df_cuotas, use_container_width=True, hide_index=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# PÁGINA 4: ANÁLISIS ACADÉMICO (IA)
# ==========================================
elif menu == "🤖 Análisis Académico":
    st.markdown('<p class="title-comas" style="font-size: 2.5rem;">Inteligencia Académica</p>', unsafe_allow_html=True)
    
    st.markdown('<div class="web-card">', unsafe_allow_html=True)
    tutor_ia = st.selectbox("Selecciona un tutor para analizar:", df_analisis["TUTOR"].unique())
    datos_ia = df_analisis[df_analisis["TUTOR"] == tutor_ia]
    
    with st.spinner(f"Analizando métricas de {tutor_ia}..."):
        time.sleep(1)
        
    promedio_general = datos_ia["NOTA"].mean()
    promedio_asistencia = datos_ia["ASISTENCIA"].mean()
    promedio_sica = datos_ia["SICA"].mean() if "SICA" in datos_ia.columns else 0
    
    df_exsa = datos_ia[datos_ia['EXAMEN'].astype(str).str.contains('EXSA', case=False, na=False)]
    df_exsi = datos_ia[datos_ia['EXAMEN'].astype(str).str.contains('EXSI', case=False, na=False)]
    prom_exsa = df_exsa["NOTA"].mean() if not df_exsa.empty else 0
    prom_exsi = df_exsi["NOTA"].mean() if not df_exsi.empty else 0
    
    col_ia1, col_ia2 = st.columns([1, 1])
    
    with col_ia1:
        st.markdown(f"""
        <div class="ia-box animate-up" style="height: 100%;">
            <h4>🧠 Reporte IA para {tutor_ia}</h4>
            <p>Se han procesado los registros académicos. El salón mantiene un promedio general de <b>{promedio_general:.1f} puntos</b>.</p>
            <div style="display:flex; gap:10px; margin-top:15px;">
                <div style="background:white; padding:10px; border-radius:10px; border-bottom: 4px solid #FF4B2B; width:50%; text-align:center;">
                    <small>Promedio EXSA</small><br><b style="font-size:1.2rem;">{prom_exsa:.1f} pts</b>
                </div>
                <div style="background:white; padding:10px; border-radius:10px; border-bottom: 4px solid #4CAF50; width:50%; text-align:center;">
                    <small>Promedio EXSI</small><br><b style="font-size:1.2rem;">{prom_exsi:.1f} pts</b>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    with col_ia2:
        val_nota = min((promedio_general / 2000) * 100, 100) 
        val_asist = min(promedio_asistencia, 100)
        val_sica = min(promedio_sica * 10, 100) 
        
        fig_radar = go.Figure(data=go.Scatterpolar(
          r=[val_asist, val_nota, val_sica, 85, val_asist], 
          theta=['Asistencia', 'Notas', 'SICA', 'Participación', 'Asistencia'],
          fill='toself',
          line_color='#FF4B2B'
        ))
        fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])), showlegend=False, margin=dict(l=20, r=20, t=20, b=20), height=250)
        st.plotly_chart(fig_radar, use_container_width=True)

    st.divider()
    
    st.subheader(f"📈 Evolución de Notas (Pasa el cursor sobre los puntos)")
    fig_notas = px.line(datos_ia, x="EXAMEN", y="NOTA", markers=True, hover_data=["ASISTENCIA", "FALTA", "VARIACION", "SICA", "C+D", "CXM"])
    fig_notas.update_traces(marker=dict(size=10, color='#FF4B2B'), line=dict(width=3))
    st.plotly_chart(fig_notas, use_container_width=True)
    
    st.subheader("📑 Cuadro Resumen de Notas")
    columnas_mostrar = [col for col in ['EXAMEN', 'ASISTENCIA', 'FALTA', 'NOTA', 'VARIACION', 'SICA', 'C+D', 'CXM'] if col in datos_ia.columns]
    st.dataframe(datos_ia[columnas_mostrar], use_container_width=True, hide_index=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    nombre_tutor = str(tutor_ia).split()[0].capitalize()
    ultimo_examen = datos_ia.iloc[-1] if not datos_ia.empty else None
    cursos_bajos = f"{ultimo_examen['C+D']} y {ultimo_examen['CXM']}" if ultimo_examen is not None and 'C+D' in ultimo_examen else "Letras y Ciencias"
    
    st.markdown(f"""
    <div class='greeting animate-up'>
        <h3 style='color: #FF4B2B; font-weight: 800; margin-bottom: 10px;'>💡 Recomendación IA para UNMSM</h3>
        <p>Hola <b>{nombre_tutor}</b>. Para asegurar vacantes en San Marcos, te sugerimos enfocar los repasos en preguntas DECO.</p>
        <p>📊 Según el último examen, debes reforzar urgentemente <b>{cursos_bajos}</b>.</p>
        <p>🚀 <i>Estrategia: Aplica simulacros cronometrados semanales y tutorías personalizadas. ¡Vamos por esos cachimbos!</i></p>
    </div>
    """, unsafe_allow_html=True)
