import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import time
import random

# ==========================================
# CONFIGURACIÓN DE LA PÁGINA
# ==========================================
st.set_page_config(page_title="Dashboard Comas 2026", page_icon="🔥", layout="wide")

# ==========================================
# ESTILOS CSS AVANZADOS
# ==========================================
st.markdown("""
    <style>
    @keyframes fadeIn {
        0% { opacity: 0; transform: scale(0.9); }
        100% { opacity: 1; transform: scale(1); }
    }
    .fade-in-text {
        animation: fadeIn 1s ease-in-out;
        text-align: center;
    }
    .title-comas {
        font-size: 3rem;
        font-weight: 900;
        background: -webkit-linear-gradient(45deg, #FF4B2B, #FF416C);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding: 20px;
    }
    div[data-testid="metric-container"] {
        background-color: #ffffff;
        border-left: 5px solid #FF4B2B;
        padding: 15px;
        border-radius: 5px;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
        transition: transform 0.3s;
    }
    div[data-testid="metric-container"]:hover {
        transform: translateY(-5px);
    }
    .ia-box {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 20px;
        border-left: 5px solid #4CAF50;
        font-style: italic;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# CARGA DE DATOS (Basado en tus hojas)
# ==========================================
@st.cache_data
def load_data():
    # 1. Datos de Olimpiadas
    df_olim = pd.DataFrame({
        "Tutor": ["LESLY", "MAJA", "RODRIGO", "ALEXANDER", "GABY", "CINTHYA", "NATALY", "MARIANA"],
        "Ciclo": ["SAN EN", "MATE SABATINO", "SAN MAYO", "SAN ABRIL", "INT ABRIL", "INT MARZO", "SAN MAR A", "SAN MAR B"],
        "Matriculados": [63, 46, 84, 48, 32, 78, 74, 62],
        "Meta": [60, 45, 80, 45, 30, 75, 70, 60],
        "Pagantes": [59, 37, 59, 29, 32, 78, 74, 62],
        "EFECTIVO": [1000, 500, 1200, 400, 600, 1500, 1400, 1100],
        "YAPE": [500, 240, 800, 180, 360, 840, 820, 760]
    })
    df_olim["Recaudado"] = df_olim["EFECTIVO"] + df_olim["YAPE"]
    df_olim["Meta Dinero"] = df_olim["Meta"] * 30 # Asumiendo cuota olimpiadas
    
    # 2. Datos de Morosidad - Resumen
    df_mor_resumen = pd.DataFrame({
        "Tutor": ["LESLY", "MAJA", "RODRIGO", "ALEXANDER", "GABY", "CINTHYA", "NATALY", "MARIANA"],
        "MAT": [63, 46, 84, 48, 32, 78, 74, 62],
        "PAG": [59, 37, 59, 29, 32, 78, 74, 62],
        "SUS": [4, 9, 25, 19, 0, 0, 0, 0],
        "DES": ["6.3%", "19.6%", "29.8%", "39.6%", "0.0%", "0.0%", "0.0%", "0.0%"],
        "CUM": ["93.7%", "80.4%", "70.2%", "60.4%", "100%", "100%", "100%", "100%"],
        "NOT": [20, 10, 10, 10, 20, 20, 20, 20]
    })
    
    # 3. Datos de Morosidad - Alumnos
    df_mor_alumnos = pd.DataFrame({
        "DNI": ["72831111", "75302957", "73565909", "61423613", "72053356", "61462066"],
        "ALUMNO": ["CASTILLO VARGAS JOANN", "MENDOZA ARONI FABRICIO", "SANGAMA RAMIREZ ISAIAS", "SALAZAR TORRES ESTHEFANY", "SAAVEDRA CHAVEZ DARIANA", "LOBATO SALDIVAR ERIKA"],
        "Tutor": ["Lesly", "Lesly", "Rodrigo", "Rodrigo", "Rodrigo", "Rodrigo"],
        "CONDICIÓN PAGO": ["PAGA VIERNES", "PAGA VIERNES", "PAGA VIERNES", "PAGA VIERNES", "PAGA VIERNES", "RETIRO"]
    })
    
    # 4. Datos de Cuotas
    df_cuotas = pd.DataFrame({
        "CUOTA": [1, 2, 3, 4, 5, 6, 7],
        "SAN MAR": ["16-mar", "11-abr", "9-may", "6-jun", "4-jul", "8-ago", "5-sep"],
        "SAN ABR": ["6-abr", "2-may", "30-may", "27-jun", "1-ago", "29-ago", "-"],
        "SAN MAY": ["4-may", "30-may", "27-jun", "1-ago", "-", "-", "-"]
    })
    
    return df_olim, df_mor_resumen, df_mor_alumnos, df_cuotas

df_olim, df_mor_resumen, df_mor_alumnos, df_cuotas = load_data()

# ==========================================
# BARRA LATERAL (NAVEGACIÓN)
# ==========================================
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3048/3048122.png", width=100)
st.sidebar.title("Menú Principal")
menu = st.sidebar.radio(
    "Navegación:",
    ("🏠 Inicio", "🏆 Olimpiadas", "⚠️ Morosidad", "🤖 Análisis Académico")
)

# ==========================================
# PÁGINA 1: INICIO
# ==========================================
if menu == "🏠 Inicio":
    st.balloons()
    st.markdown('<div class="fade-in-text">', unsafe_allow_html=True)
    st.markdown('<p class="title-comas">¡BIENVENIDO A LA SEDE COMAS!</p>', unsafe_allow_html=True)
    st.markdown('<h2>🔥 LA MEJOR SEDE - LA NÚMERO 1 🔥</h2>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.image("https://images.unsplash.com/photo-1522202176988-66273c2fd55f?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80", use_column_width=True)
    st.info("💡 Selecciona un módulo en el menú de la izquierda para comenzar a analizar los datos de la sede.")

# ==========================================
# PÁGINA 2: OLIMPIADAS
# ==========================================
elif menu == "🏆 Olimpiadas":
    st.title("🏆 Recaudación Olimpiadas")
    
    # Gráfico general
    fig = px.bar(df_olim, x="Tutor", y=["YAPE", "EFECTIVO"], title="Recaudación Total por Tutor (Yape vs Efectivo)", text_auto=True)
    st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("🔎 Detalle Interactivo por Tutor")
    st.write("Selecciona un tutor para ver su rendimiento específico:")
    
    tutor_seleccionado = st.selectbox("Elegir Tutor:", ["Todos"] + list(df_olim["Tutor"].unique()))
    
    if tutor_seleccionado != "Todos":
        datos_tutor = df_olim[df_olim["Tutor"] == tutor_seleccionado].iloc[0]
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Matriculados vs Meta", f"{datos_tutor['Matriculados']} / {datos_tutor['Meta']}")
        col2.metric("Pagantes", datos_tutor['Pagantes'])
        col3.metric("Recaudado Total", f"S/ {datos_tutor['Recaudado']}")
        
        # Desglose Yape vs Efectivo
        fig_pie = px.pie(values=[datos_tutor["YAPE"], datos_tutor["EFECTIVO"]], names=["Yape", "Efectivo"], hole=0.5, title=f"Distribución de Pagos - {tutor_seleccionado}")
        st.plotly_chart(fig_pie, use_container_width=True)

# ==========================================
# PÁGINA 3: MOROSIDAD
# ==========================================
elif menu == "⚠️ Morosidad":
    st.title("⚠️ Panel de Morosidad y Pagos")
    
    # Cálculos globales (Basados en fila TOTAL de tu Excel: MAT 552, PAG 467, SUS 85)
    total_mat = df_mor_resumen["MAT"].sum()
    total_pag = df_mor_resumen["PAG"].sum()
    total_sus = df_mor_resumen["SUS"].sum()
    deuda_acumulada = total_sus * 510 # Suspendidos/Deserción x 510
    
    st.subheader("Resumen Global de la Sede")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Matriculados (MAT)", total_mat)
    col2.metric("Pagantes (PAG)", total_pag)
    col3.metric("Suspendidos (SUS/DES)", total_sus)
    col4.metric("Deuda Acumulada", f"S/ {deuda_acumulada:,.2f}", "- Crítico", delta_color="inverse")
    
    st.divider()
    
    col_izq, col_der = st.columns([1.5, 1])
    
    with col_izq:
        st.subheader("📅 Cuadro de Pagos (Fechas)")
        st.dataframe(df_cuotas, use_container_width=True, hide_index=True)
        
        st.subheader("📊 Rendimiento por Tutor (MAT, PAG, CUM, NOT)")
        st.dataframe(df_mor_resumen, use_container_width=True, hide_index=True)

    with col_der:
        st.subheader("🚨 Alumnos Morosos")
        st.write("Despliega para ver la lista de alumnos que no pagan:")
        with st.expander("Ver Lista Completa de Morosos 🔽", expanded=True):
            st.dataframe(df_mor_alumnos, use_container_width=True, hide_index=True)

# ==========================================
# PÁGINA 4: ANÁLISIS ACADÉMICO (IA)
# ==========================================
elif menu == "🤖 Análisis Académico":
    st.title("🤖 Asistente de Análisis de Rendimiento")
    st.markdown("Selecciona un tutor para que la IA genere un análisis automático de su salón.")
    
    tutor_ia = st.selectbox("Analizar salón a cargo de:", df_mor_resumen["Tutor"].unique())
    datos_ia = df_mor_resumen[df_mor_resumen["Tutor"] == tutor_ia].iloc[0]
    
    with st.spinner("La IA está analizando los datos del tutor..."):
        time.sleep(1.5) # Simula tiempo de procesamiento de IA
        
    # Generación de texto dinámico "Tipo IA"
    cumplimiento = float(datos_ia["CUM"].replace("%", ""))
    nota = datos_ia["NOT"]
    
    diagnostico = "Excelente" if cumplimiento >= 85 else "Regular" if cumplimiento >= 60 else "Crítico"
    recomendacion = "Mantener las estrategias de retención actuales." if diagnostico == "Excelente" else "Se requiere intervención urgente. Llamar a los apoderados de los alumnos suspendidos para negociar pagos."
    
    st.markdown(f"""
    <div class="ia-box">
        <h4>🧠 Insight Generado por IA para {tutor_ia}</h4>
        <p><strong>Diagnóstico de Salón:</strong> Nivel {diagnostico}</p>
        <p>El salón del tutor <b>{tutor_ia}</b> tiene actualmente <b>{datos_ia['MAT']}</b> alumnos matriculados. 
        Se registra un total de <b>{datos_ia['SUS']}</b> alumnos suspendidos/desertores, lo que representa una tasa de deserción del <b>{datos_ia['DES']}</b>.</p>
        <p>El nivel de cumplimiento de pagos es del <b>{datos_ia['CUM']}</b> y la nota de evaluación de gestión es <b>{nota}/20</b>.</p>
        <p><b>💡 Recomendación de la IA:</b> {recomendacion}</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    # Gráfico interactivo tipo Radar para el tutor
    st.subheader(f"Perfil de Gestión: {tutor_ia}")
    categorias = ['Matriculados', 'Pagantes', 'Cumplimiento (%)', 'Nota (x5)']
    valores = [datos_ia['MAT'], datos_ia['PAG'], cumplimiento, nota * 5] # Multiplicado para igualar escala visual
    
    fig_radar = go.Figure(data=go.Scatterpolar(
      r=valores,
      theta=categorias,
      fill='toself',
      line_color='#FF4B2B'
    ))
    fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])), showlegend=False)
    st.plotly_chart(fig_radar, use_container_width=True)
