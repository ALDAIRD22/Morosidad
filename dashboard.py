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
        
        # CORRECCIÓN PRINCIPAL: Normalizar cabecera TUTOR a Tutor
        if "TUTOR" in df_olim.columns:
            df_olim.rename(columns={"TUTOR": "Tutor"}, inplace=True)
            
        df_olim = df_olim.dropna(subset=["Tutor"])
        df_olim = df_olim[~df_olim['Tutor'].astype(str).str.upper().str.contains('TOTAL')]
        df_olim['Tutor'] = df_olim['Tutor'].astype(str).str.replace('\n', ' ').str.strip()
        
        for col in ['Matriculados', 'Meta', 'Pagantes', 'EFECTIVO', 'YAPE', 'Recaudado', 'Falta', 'Avance %']:
            if col in df_olim.columns:
                df_olim[col] = pd.to_numeric(df_olim[col].astype(str).str.replace(r'[S/,\s%]', '', regex=True).str.replace('-', '0'), errors='coerce').fillna(0)
        
        # 1.5 TALLAS CORREGIDO: Salta a la fila 14 (skiprows=13) y lee las 6 tallas del cuadro (usecols de 0 a 7)
        df_tallas = pd.read_csv(url_olim, skiprows=13, header=None, usecols=range(0, 7))
        df_tallas.columns = ["Tutor", "T14", "T16", "S", "M", "L", "XL"]
        df_tallas = df_tallas.dropna(subset=["Tutor"])
        df_tallas['Tutor'] = df_tallas['Tutor'].astype(str).str.replace('\n', ' ').str.strip()
        df_tallas = df_tallas[~df_tallas['Tutor'].astype(str).str.upper().str.contains('TOTAL')]
        
        for col in ["T14", "T16", "S", "M", "L", "XL"]:
            df_tallas[col] = pd.to_numeric(df_tallas[col], errors='coerce').fillna(0).astype(int)
            
        df_tallas["Total Polos"] = df_tallas["T14"] + df_tallas["T16"] + df_tallas["S"] + df_tallas["M"] + df_tallas["L"] + df_tallas["XL"]
        
        # 2. MOROSIDAD - RESUMEN
        df_mor_resumen = pd.read_csv(url_mor, skiprows=1, usecols=range(0, 9))
        df_mor_resumen.columns = ["FECHA", "CICLO", "TUTO", "MAT", "PAG", "SUS", "DES", "CUM", "NOT"]
        df_mor_resumen = df_mor_resumen.dropna(subset=["TUTO"])
        df_mor_resumen = df_mor_resumen[~df_mor_resumen["TUTO"].astype(str).str.upper().str.contains('TOTAL')]
        df_mor_resumen['TUTO_CICLO'] = df_mor_resumen['TUTO'].astype(str) + " (" + df_mor_resumen['CICLO'].astype(str) + ")"
        
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
            'ASIST. ALUMNOS', 'ASIST. TUTORES', 'ASISTENCIA Y PUNTUALIDAD', 'ENCUESTA S.T.',
            'ASISTENCIA S.T.', 'STUDY TIME', 'CI', 'EPPFF', 'ORIENTACIÓN', 'CUMP. DE META',
            'ASIST. EVALUACIONES', 'PLAN DE ACCIÓN', 'META ACADÉMICA', 'DESERCIÓN',
            'ENCUESTA TUTOR', 'PART. ENC. DOCENTE', 'PROMEDIO FINAL EVA. Y DESEMPEÑO', 'NOTA FINAL'
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
st.sidebar.title("Sede Comas 2026")
menu = st.sidebar.radio("", ("🏠 Inicio", "🏆 Olimpiadas", "⚠️ Morosidad", "🤖 Análisis Académico", "📈 Evaluación Bimensual"))

# ==========================================
# PÁGINA 1: INICIO
# ==========================================
if menu == "🏠 Inicio":
    st.balloons()
    st.title("🔥 SISTEMA WEB COMAS - LA SEGUNDA SEDE NÚMERO 1 🔥")
    st.subheader("📸 Panel Fotográfico General")
    st.info("Bienvenido al ecosistema unificado de control de metas, cobranzas y rendimiento.")

# ==========================================
# PÁGINA 2: OLIMPIADAS
# ==========================================
elif menu == "🏆 Olimpiadas":
    st.title("🏆 Control e Ingresos de Olimpiadas")
    tab1, tab2, tab3 = st.tabs(["📊 Resumen Global", "🎯 Detalle por Tutor", "👕 Control de Tallas"])
    
    with tab1:
        total_recaudado = df_olim['Recaudado'].sum()
        total_yape = df_olim['YAPE'].sum()
        total_efectivo = df_olim['EFECTIVO'].sum()
        total_falta = df_olim['Falta'].sum()
        
        col_tot1, col_tot2, col_tot3, col_tot4 = st.columns(4)
        col_tot1.metric("Total Recaudado", f"S/ {total_recaudado:,.2f}")
        col_tot2.metric("Total Yape", f"S/ {total_yape:,.2f}")
        col_tot3.metric("Total Efectivo", f"S/ {total_efectivo:,.2f}")
        col_tot4.metric("Monto Pendiente (Falta)", f"S/ {total_falta:,.2f}", delta="- Restante", delta_color="inverse")
        
        st.divider()
        st.subheader("🥇 Ranking de Cumplimiento de Metas (Avance %)")
        df_ranking = df_olim.sort_values(by="Avance %", ascending=True)
        fig_ranking = px.bar(df_ranking, x="Avance %", y="Tutor", orientation='h', text="Avance %", color="Avance %", color_continuous_scale="Viridis")
        fig_ranking.update_traces(texttemplate='%{text}%', textposition='outside')
        st.plotly_chart(fig_ranking, use_container_width=True)

    with tab2:
        st.subheader("🔎 Panel de Control por Tutor")
        tutor_seleccionado = st.selectbox("Selecciona un Tutor:", df_olim["Tutor"].unique())
        datos_tutor = df_olim[df_olim["Tutor"] == tutor_seleccionado].iloc[0]
        avance = datos_tutor['Avance %']
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Matriculados vs Meta", f"{int(datos_tutor['Matriculados'])} / {int(datos_tutor['Meta'])}")
        col2.metric("Pagantes", int(datos_tutor['Pagantes']))
        col3.metric("Recaudado", f"S/ {datos_tutor['Recaudado']:,.2f}")
        col4.metric("Falta", f"S/ {datos_tutor['Falta']:,.2f}")
        
        st.divider()
        
        # CORRECCIÓN: Tallas integradas leyendo la nueva matriz de 6 tallas reales
        st.subheader("👕 Distribución de Polos de este Salón")
        tallas_tutor = df_tallas[df_tallas['Tutor'] == tutor_seleccionado]
        if not tallas_tutor.empty:
            t_data = tallas_tutor.iloc[0]
            t_pedidos = int(t_data['Total Polos'])
            t_pagantes = int(datos_tutor['Pagantes'])
            t_diff = t_pedidos - t_pagantes
            
            c_t1, c_t2, c_t3, c_t4, c_t5, c_t6, c_t7, c_t8 = st.columns(8)
            c_t1.metric("T. 14", int(t_data['T14']))
            c_t2.metric("T. 16", int(t_data['T16']))
            c_t3.metric("T. S", int(t_data['S']))
            c_t4.metric("T. M", int(t_data['M']))
            c_t5.metric("T. L", int(t_data['L']))
            c_t6.metric("T. XL", int(t_data['XL']))
            c_t7.metric("Total Pedidos", t_pedidos)
            
            if t_diff == 0:
                c_t8.metric("Logística", "✅ Cuadra")
            elif t_diff > 0:
                c_t8.metric("Logística", f"🔴 +{t_diff} Sobran", delta_color="inverse")
            else:
                c_t8.metric("Logística", f"🟡 {t_diff} Faltan", delta_color="inverse")
        else:
            st.warning("⚠️ Sin registros específicos de tallas cargados para este tutor.")

    with tab3:
        st.subheader("📊 Auditoría de Inventario de Camisetas")
        df_olim_sub = df_olim[['Tutor', 'Pagantes']].copy()
        df_control = pd.merge(df_olim_sub, df_tallas, on='Tutor', how='inner')
        st.dataframe(df_control, use_container_width=True, hide_index=True)

# ==========================================
# PÁGINA 3: MOROSIDAD
# ==========================================
elif menu == "⚠️ Morosidad":
    st.title("⚠️ Control y Gestión de Carteras de Morosidad")
    st.dataframe(df_mor_resumen, use_container_width=True, hide_index=True)

# ==========================================
# PÁGINA 4: ANÁLISIS ACADÉMICO
# ==========================================
elif menu == "🤖 Análisis Académico":
    st.title("🤖 Inteligencia de Notas y Rendimiento")
    tutor_ia = st.selectbox("Selecciona un tutor para evaluar:", df_analisis["TUTOR"].unique())
    datos_ia = df_analisis[df_analisis["TUTOR"] == tutor_ia]
    st.dataframe(datos_ia, use_container_width=True, hide_index=True)

# ==========================================
# PÁGINA 5: EVALUACIÓN BIMENSUAL
# ==========================================
elif menu == "📈 Evaluación Bimensual":
    st.title("📈 Matriz Corporativa de Desempeño Bimensual")
    st.dataframe(df_bim, use_container_width=True, hide_index=True)
