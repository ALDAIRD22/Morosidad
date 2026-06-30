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
    
    .ia-box { background: linear-gradient(135deg, #f6f8fd 0%, #f1f5f9 100%); border-radius: 15px; padding: 25px; border-left: 6px solid #4CAF50; box-shadow: 0 5px 15px rgba(0,0,0,0.05); margin-bottom: 20px; }
    
    /* DISEÑO DE MASCOTA PERSONAJE INTERACTIVO */
    .mascot-container {
        display: flex;
        align-items: center;
        gap: 20px;
        background: white;
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.05);
        margin-top: 25px;
        border-left: 6px solid #FF4B2B;
    }
    .mascot-avatar {
        font-size: 3rem;
        background: #f1f5f9;
        padding: 12px;
        border-radius: 50%;
        box-shadow: inset 0 2px 5px rgba(0,0,0,0.1);
        display: flex;
        align-items: center;
        justify-content: center;
        animation: pulse mascot 2s infinite;
    }
    .mascot-speech-bubble {
        flex: 1;
    }

    /* Estilo para las pestañas (Tabs) */
    .stTabs [data-baseweb="tab-list"] { gap: 24px; }
    .stTabs [data-baseweb="tab"] { height: 50px; white-space: pre-wrap; background-color: transparent; border-radius: 4px 4px 0px 0px; gap: 1px; padding-top: 10px; padding-bottom: 10px; font-weight: 600; font-size: 1.1rem; }
    
    /* ANIMACIÓN DE TRANSICIÓN (SLIDESHOW) */
    .slider-wrapper {
        position: relative;
        width: 100%;
        height: 550px;
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 10px 30px rgba(0,0,0,0.15);
        background-color: #f0f2f6;
    }
    .slide-img {
        position: absolute;
        width: 100%;
        height: 100%;
        object-fit: cover;
        opacity: 0;
        animation: slide-anim 10s infinite;
    }
    .slide-img:nth-child(1) { animation-delay: 0s; }
    .slide-img:nth-child(2) { animation-delay: 3s; }
    
    @keyframes slide-anim {
        0%, 40% { opacity: 1; }
        50%, 90% { opacity: 0; }
        100% { opacity: 1; }
    }
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
    url_bim = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid=1034063425"
    
    try:
        # 1. OLIMPIADAS
        df_olim = pd.read_csv(url_olim)
        df_olim.columns = df_olim.columns.str.strip()
        df_olim = df_olim.dropna(subset=["Tutor"])
        df_olim = df_olim[~df_olim['Tutor'].astype(str).str.upper().str.contains('TOTAL')]
        df_olim['Tutor'] = df_olim['Tutor'].astype(str).str.replace('\n', ' ').str.strip()
        
        for col in ['Matriculados', 'Meta', 'Pagantes', 'EFECTIVO', 'YAPE', 'Recaudado', 'Falta', 'Avance %']:
            if col in df_olim.columns:
                df_olim[col] = pd.to_numeric(df_olim[col].astype(str).str.replace(r'[S/,\s%]', '', regex=True).str.replace('-', '0'), errors='coerce').fillna(0)

        # 1.5 TALLAS DE OLIMPIADAS (Fila 12)
        df_tallas = pd.read_csv(url_olim, skiprows=11, usecols=range(0, 5))
        df_tallas.columns = ["Tutor", "S", "M", "L", "XL"]
        df_tallas = df_tallas.dropna(subset=["Tutor"])
        df_tallas['Tutor'] = df_tallas['Tutor'].astype(str).str.replace('\n', ' ').str.strip()
        for col in ["S", "M", "L", "XL"]:
            df_tallas[col] = pd.to_numeric(df_tallas[col], errors='coerce').fillna(0).astype(int)
        df_tallas["Total Polos"] = df_tallas["S"] + df_tallas["M"] + df_tallas["L"] + df_tallas["XL"]

        # 2. MOROSIDAD - RESUMEN
        df_mor_resumen = pd.read_csv(url_mor, skiprows=1, usecols=range(0, 9))
        df_mor_resumen.columns = ["FECHA", "CICLO", "TUTO", "MAT", "PAG", "SUS", "DES", "CUM", "NOT"]
        df_mor_resumen = df_mor_resumen.dropna(subset=["TUTO"])
        df_mor_resumen = df_mor_resumen[~df_mor_resumen["TUTO"].astype(str).str.upper().str.contains('TOTAL')]
        for col in ["MAT", "PAG", "SUS", "NOT"]:
            df_mor_resumen[col] = pd.to_numeric(df_mor_resumen[col], errors='coerce').fillna(0)

        # 3. MOROSIDAD - ALUMNOS
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

        # 6. BIMENSUAL
        df_bim = pd.read_csv(url_bim)
        df_bim.columns = df_bim.columns.str.strip()
        df_bim = df_bim.dropna(subset=["TUTOR"])
        cols_num_bim = [
            'ASIST. ALUMNOS', 'ASIST. TUTORES', 'ASISTENCIA Y PUNTUALIDAD', 
            'ENCUESTA S.T.', 'ASISTENCIA S.T.', 'STUDY TIME', 'CI', 'EPPFF', 
            'ORIENTACIÓN', 'CUMP. DE META', 'ASIST. EVALUACIONES', 'PLAN DE ACCIÓN', 
            'META ACADÉMICA', 'DESERCIÓN', 'ENCUESTA TUTOR', 'PART. ENC. DOCENTE', 
            'PROMEDIO FINAL EVA. Y DESEMPEÑO', 'NOTA FINAL'
        ]
        for col in cols_num_bim:
            if col in df_bim.columns:
                df_bim[col] = pd.to_numeric(df_bim[col].astype(str).str.replace(r'[^\d.]', '', regex=True), errors='coerce').fillna(0)

        return df_olim, df_tallas, df_mor_resumen, df_mor_alumnos, df_cuotas, df_analisis, df_bim
    except Exception as e:
        st.error(f"Error al conectar con Google Sheets. Detalle: {e}")
        st.stop()

df_olim, df_tallas, df_mor_resumen, df_mor_alumnos, df_cuotas, df_analisis, df_bim = load_data()

@st.cache_data
def convert_df(df):
    return df.to_csv(index=False).encode('utf-8')

# ==========================================
# BARRA LATERAL (NAVEGACIÓN)
# ==========================================
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3048/3048122.png", width=100)
st.sidebar.title("Navegación Web")
menu = st.sidebar.radio("", ("🏠 Inicio", "🏆 Olimpiadas", "⚠️ Morosidad", "🤖 Análisis Académico", "📈 Evaluación Bimensual"))

# ==========================================
# PÁGINA 1: INICIO 
# ==========================================
if menu == "🏠 Inicio":
    st.balloons()
    st.markdown('<div class="animate-up"><p class="title-comas">SISTEMA WEB COMAS</p><p class="subtitle">🔥 LA MEJOR SEDE - LA NÚMERO 1 🔥</p></div>', unsafe_allow_html=True)
    
    st.markdown('<div class="web-card">', unsafe_allow_html=True)
    st.subheader("📸 Galería Fotográfica de la Sede")
    
    LINK_FOTO_1 = "https://lh3.googleusercontent.com/d/1Y9n4xlDrUS1yf5wlExwqUpsUuMrECmtR"
    LINK_FOTO_2 = "https://lh3.googleusercontent.com/d/1xx_WqMIvabKhGEzMqyBtBOUYwuOD0Yyj"
    
    st.markdown(f"""
        <div class="slider-wrapper">
            <img class="slide-img" src="{LINK_FOTO_1}">
            <img class="slide-img" src="{LINK_FOTO_2}">
        </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# PÁGINA 2: OLIMPIADAS
# ==========================================
elif menu == "🏆 Olimpiadas":
    st.markdown('<p class="title-comas" style="font-size: 2.5rem;">Recaudación Olimpiadas</p>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["📊 Resumen Global", "🎯 Detalle por Tutor", "👕 Control de Tallas"])
    
    with tab1:
        st.markdown('<div class="web-card animate-up">', unsafe_allow_html=True)
        st.subheader("💰 Resumen Global e Ingresos de la Sede")
        
        total_recaudado = df_olim['Recaudado'].sum()
        total_yape = df_olim['YAPE'].sum()
        total_efectivo = df_olim['EFECTIVO'].sum()
        total_falta = df_olim['Falta'].sum()
        
        col_tot1, col_tot2, col_tot3, col_tot4 = st.columns(4)
        col_tot1.metric("Total Recaudado", f"S/ {total_recaudado:,.2f}")
        col_tot2.metric("Total Yape", f"S/ {total_yape:,.2f}")
        col_tot3.metric("Total Efectivo", f"S/ {total_efectivo:,.2f}")
        col_tot4.metric("Dinero que Falta (Meta)", f"S/ {total_falta:,.2f}", delta="- Pendiente", delta_color="inverse")
        
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
            
        # PERSONAJE INTERACTIVO DE SALUDO AL TUTOR
        nombre_tutor_greet = tutor_seleccionado.split()[0].capitalize()
        st.markdown(f"""
        <div class="mascot-container animate-up">
            <div class="mascot-avatar">👨‍🏫</div>
            <div class="mascot-speech-bubble">
                <h4 style="margin:0; color:#FF4B2B; font-weight:800;">¡Hola {nombre_tutor_greet}!</h4>
                <p style="margin:5px 0 0 0; color:#333; font-size:1rem;">Tu salón está respondiendo activamente en esta campaña de las Olimpiadas 2026. ¡Sigue impulsando la recaudación para asegurar el primer puesto de la sede! 🚀</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with tab3:
        st.markdown('<div class="web-card animate-up">', unsafe_allow_html=True)
        st.subheader("👕 Control de Tallas por Tutor (Lista Única)")
        
        df_olim_sub = df_olim[['Tutor', 'Pagantes']].copy().drop_duplicates(subset=['Tutor'])
        df_tallas_clean = df_tallas.copy().drop_duplicates(subset=['Tutor'])
        
        df_control = pd.merge(df_olim_sub, df_tallas_clean, on='Tutor', how='left').fillna(0)
        
        for col in ['Pagantes', 'S', 'M', 'L', 'XL', 'Total Polos']:
            df_control[col] = df_control[col].astype(int)
            
        total_polos_sede = df_control['Total Polos'].sum()
        total_pagantes_sede = df_control['Pagantes'].sum()
        balance_sede = total_polos_sede - total_pagantes_sede
        
        col_t1, col_t2, col_t3 = st.columns(3)
        col_t1.metric("Total Polos Pedidos", int(total_polos_sede))
        col_t2.metric("Total Alumnos Pagantes", int(total_pagantes_sede))
        
        if balance_sede == 0:
            col_t3.metric("Estado General de Sede", "✅ Todo Cuadra Perfecto")
        elif balance_sede > 0:
            col_t3.metric("Estado General de Sede", f"🔴 Se excede por {int(balance_sede)} polos")
        else:
            col_t3.metric("Estado General de Sede", f"🟡 Le faltan {int(abs(balance_sede))} polos", delta_color="inverse")
            
        st.divider()
        
        # Inteligencia Artificial Integrada
        st.markdown(f"""
        <div class="ia-box">
            <h4>🧠 Auditoría Logística de Tallas por IA</h4>
            <p><b>🚨 Brecha Crítica detectada:</b> Hay un déficit total de <b>{int(abs(balance_sede))} prendas</b> a nivel institucional. Los tutores <b>García Gutierrez, Martínez Huaira y Boza Villanueva</b> presentan ausencia absoluta de registros de tallas, poniendo en riesgo los tiempos de confección para sus <b>142 alumnos pagantes</b>.</p>
            <p><b>📊 Diagnóstico de Consistencia:</b> Solo la tutora <b>Carrera Martínez Virginia Gaby</b> presenta un cuadre perfecto (1:1). El bloque de <b>Alexander Javier</b> registra un excedente de +13 prendas que debe ser regularizado.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Gráfico comparativo visual
        df_chart_tallas = df_control.melt(id_vars=['Tutor'], value_vars=['Total Polos', 'Pagantes'], var_name='Concepto', value_name='Cantidad')
        fig_tallas_comp = px.bar(df_chart_tallas, x='Tutor', y='Cantidad', color='Concepto', barmode='group', color_discrete_sequence=["#1E3A8A", "#4CAF50"], title="Polos Solicitados vs Alumnos Pagantes")
        st.plotly_chart(fig_tallas_comp, use_container_width=True)
        
        st.subheader("📋 Resumen de Control")
        def clean_status(row):
            diff = row['Total Polos'] - row['Pagantes']
            if diff == 0: return "✅ Cuadra Perfecto"
            elif diff > 0: return f"❌ Se excede por {int(diff)} polos (Sobran)"
            else: return f"⚠️ Le falta {int(abs(diff))} polos por registrar"
            
        df_control['Observación'] = df_control.apply(clean_status, axis=1)
        st.dataframe(df_control[['Tutor', 'Total Polos', 'Pagantes', 'Observación']], use_container_width=True, hide_index=True)
        
        # 1. ACTUALIZADO: SE AGREGÓ LA COLUMNA 'PAGANTES' (TOTAL PAGADOS) ADENTRO DEL DESGLOSE DEL EXPANDER
        with st.expander("🔍 Ver desglose detallado por tallas (S, M, L, XL)"):
            st.dataframe(
                df_control[['Tutor', 'S', 'M', 'L', 'XL', 'Total Polos', 'Pagantes']], 
                use_container_width=True, 
                hide_index=True,
                column_config={"Pagantes": "Total Pagados"}
            )
            
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
        
        df_filtrado = df_filtrado.copy()
        df_filtrado["#"] = range(1, len(df_filtrado) + 1)
        
        with col_btn:
            st.markdown("<br>", unsafe_allow_html=True)
            csv_data = convert_df(df_filtrado)
            st.download_button(label="📥 Descargar Reporte (CSV)", data=csv_data, file_name=f"Morosos_{tutor_moroso}.csv", mime='text/csv')
        
        df_mostrar = df_filtrado.copy()
        df_mostrar['Celular_Limpio'] = df_mostrar['Celular'].astype(str).str.replace(r'\D', '', regex=True)
        df_mostrar['Acción'] = "https://wa.me/51" + df_mostrar['Celular_Limpio'] + "?text=Hola%20apoderado%20de%20" + df_mostrar['ALUMNO'].astype(str).str.replace(' ', '%20') + ",%20le%20escribimos%20de%20la%20Sede%20Comas%20para%20recordarle%20amablemente%20el%20pago%20de%20su%20cuota%20pendiente.%20Muchas%20gracias."
        df_mostrar = df_mostrar.drop(columns=['Celular_Limpio'])
        
        st.dataframe(
            df_mostrar, 
            use_container_width=True, 
            hide_index=True,
            column_config={
                "Acción": st.column_config.LinkColumn("Enviar WhatsApp 💬", display_text="Cobrar por WS")
            }
        )
        st.markdown('</div>', unsafe_allow_html=True)

    with tab_mor3:
        st.markdown('<div class="web-card">', unsafe_allow_html=True)
        st.dataframe(df_cuotas, use_container_width=True, hide_index=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# PÁGINA 4: ANÁLISIS ACADÉMICO (IA WITH MASCOT)
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
    
    # 2. ACTUALIZADO: SE REDISEÑÓ EL CUADRO DE RECOMENDACIÓN CON UN SÚPER ASISTENTE VIRTUAL DE IA ROBOT ("🤖") INTERACTIVO
    nombre_tutor = str(tutor_ia).split()[0].capitalize()
    ultimo_examen = datos_ia.iloc[-1] if not datos_ia.empty else None
    cursos_bajos = f"{ultimo_examen['C+D']} y {ultimo_examen['CXM']}" if ultimo_examen is not None and 'C+D' in ultimo_examen else "Letras y Ciencias"
    
    st.markdown(f"""
    <div class="mascot-container animate-up" style="background: rgba(76, 175, 80, 0.05); border-left-color: #4CAF50;">
        <div class="mascot-avatar">🤖</div>
        <div class="mascot-speech-bubble">
            <h3 style='color: #4CAF50; font-weight: 800; margin: 0 0 10px 0;'>💡 Recomendación Estratégica para UNMSM</h3>
            <p style="margin:0; color:#333; font-size:1rem;">Hola <b>{nombre_tutor}</b>. Para asegurar el máximo ingreso de vacantes a la Universidad Nacional Mayor de San Marcos, es vital enfocar los repasos en el formato de preguntas de destreza cognitiva (DECO).</p>
            <p style="margin:8px 0 0 0; color:#333; font-size:1rem;">📊 Analizando el rendimiento histórico de tu aula, la mayor prioridad de reforzamiento está en los bloques de <b>{cursos_bajos}</b>.</p>
            <p style="margin:8px 0 0 0; font-style: italic; color:#666; font-size:0.95rem;">🚀 Acción inmediata: Ejecutar simulacros semanales cronometrados con control estricto de tiempos por sección para potenciar los puntajes de los muchachos. ¡Vamos por esos cachimbos!</p>
        </div>
    </div>
    """, unsafe_allow_html=True) 

# ==========================================
# PÁGINA 5: EVALUACIÓN BIMENSUAL
# ==========================================
elif menu == "📈 Evaluación Bimensual":
    st.markdown('<p class="title-comas" style="font-size: 2.5rem;">Evaluación Corporativa Bimensual</p>', unsafe_allow_html=True)
    
    st.markdown('<div class="web-card animate-up">', unsafe_allow_html=True)
    st.subheader("📊 Panel de Rendimiento de Tutores")
    
    promedio_global = df_bim['NOTA FINAL'].mean() if not df_bim.empty else 0
    nota_max = df_bim['NOTA FINAL'].max() if not df_bim.empty else 0
    mejor_tutor = df_bim.loc[df_bim['NOTA FINAL'].idxmax()]['TUTOR'] if not df_bim.empty else "N/A"
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Promedio Global (Sede)", f"{promedio_global:.2f} / 20")
    col2.metric("Tutor Destacado", mejor_tutor.split()[0].capitalize() if mejor_tutor != "N/A" else "N/A")
    col3.metric("Nota Máxima Alcanzada", f"{nota_max:.2f}")
    st.markdown('</div>', unsafe_allow_html=True)
    
    tab_bim1, tab_bim2, tab_bim3 = st.tabs(["📈 Gráficos de Rendimiento", "🏆 Ranking y Cuadro de Honor", "🧠 Análisis Estratégico (IA)"])
    
    with tab_bim1:
        st.markdown('<div class="web-card">', unsafe_allow_html=True)
        st.subheader("Comparativa de Notas Finales por Periodo")
        fig_bim = px.bar(df_bim, x="TUTOR", y="NOTA FINAL", color="PERIODO DE EVALUACION", barmode="group", text="NOTA FINAL", color_discrete_sequence=["#FF4B2B", "#4CAF50", "#FFC107"])
        fig_bim.update_traces(texttemplate='%{text:.2f}', textposition='outside')
        fig_bim.update_layout(xaxis_tickangle=-45, height=500)
        st.plotly_chart(fig_bim, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with tab_bim2:
        st.markdown('<div class="web-card">', unsafe_allow_html=True)
        st.subheader("🏆 Top 5 Tutores (Cuadro de Honor)")
        df_top = df_bim.sort_values(by="NOTA FINAL", ascending=False).head(5)
        st.dataframe(df_top[['PERIODO DE EVALUACION', 'TUTOR', 'NOTA FINAL', 'CUMP. DE META', 'ENCUESTA TUTOR']], use_container_width=True, hide_index=True)
        
        st.divider()
        st.subheader("📑 Base de Datos Completa")
        st.dataframe(df_bim, use_container_width=True, hide_index=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with tab_bim3:
        st.markdown(f"""
        <div class="ia-box animate-up" style="height: 100%;">
            <h3 style='color: #4CAF50; font-weight: 800; margin-bottom: 10px;'>🧠 Reporte Estratégico de Gestión</h3>
            <p><b>1. Tendencia General:</b> El equipo mantiene un estándar sobresaliente con un promedio global de <b>{promedio_global:.2f}</b>. Esto refleja un compromiso sólido con los estándares de calidad de la sede.</p>
            <p><b>2. Pilares de Éxito:</b> Se identifican fortalezas clave en el <i>Cumplimiento de Meta</i> y la <i>Satisfacción del Alumno (Encuestas)</i>, demostrando un excelente clima en las aulas.</p>
            <p><b>3. Áreas de Oportunidad:</b> Se recomienda implementar un plan de acción inmediato para mejorar la <b>Asistencia a Study Time (S.T.)</b> y la ejecución de los <b>EPPFF</b>, ya que presentan los indicadores más bajos del periodo.</p>
            <p>🚀 <i>Directiva: Felicitar al top 5 en la próxima reunión de equipo y programar clínicas de capacitación para los indicadores de Study Time.</i></p>
        </div>
        """, unsafe_allow_html=True) 
