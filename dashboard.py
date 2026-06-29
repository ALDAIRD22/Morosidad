import streamlit as st
import pandas as pd
import plotly.express as px
import time

# ==========================================
# CONFIGURACIÓN DE LA PÁGINA
# ==========================================
st.set_page_config(page_title="Dashboard Académico 2026", page_icon="📊", layout="wide")

# ==========================================
# ESTILOS CSS PARA TRANSICIONES VISUALES
# ==========================================
st.markdown("""
    <style>
    /* Animación de entrada (Fade In y deslizamiento) */
    @keyframes slideIn {
        0% { opacity: 0; transform: translateY(20px); }
        100% { opacity: 1; transform: translateY(0); }
    }
    .main .block-container {
        animation: slideIn 0.8s ease-out;
    }
    /* Estilo para tarjetas de métricas */
    div[data-testid="metric-container"] {
        background-color: #f8f9fa;
        border: 1px solid #e9ecef;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.05);
        transition: transform 0.3s;
    }
    div[data-testid="metric-container"]:hover {
        transform: translateY(-5px);
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# FUNCIÓN PARA CARGAR DATOS (Simulados basados en tu Excel)
# ==========================================
@st.cache_data
def load_data():
    # En producción, aquí conectarías con pd.read_csv() o la API de Google Sheets.
    # Simulamos los datos basados en tu estructura:
    
    df_olimpiadas = pd.DataFrame({
        "Tutor": ["GARCIA", "MARTINEZ", "BOZA", "SANCHEZ", "ALCARRAZ", "CARRERA", "ESPADA"],
        "Ciclo": ["SEMI ENERO", "SEMI MARZO-A", "SEMI MARZO-B", "INT MARZO-A", "SEMI ABRIL-A", "INT ABRIL-A", "SAN JUNIO"],
        "Meta Dinero": [1530, 1770, 1530, 1860, 1140, 780, 2460],
        "Recaudado": [1530, 1800, 930, 1890, 600, 780, 1005],
        "Avance %": [100, 102, 61, 102, 53, 100, 41]
    })
    
    df_analisis = pd.DataFrame({
        "Tutor": ["GARCIA", "MARTINEZ", "BOZA", "SANCHEZ", "ALCARRAZ"] * 10,
        "Nota": [15, 12, 18, 14, 10, 16, 11, 19, 13, 9] * 5,
        "Asistencia": [100, 80, 95, 85, 70, 100, 75, 90, 80, 60] * 5
    })
    
    return df_olimpiadas, df_analisis

df_olim, df_ana = load_data()

# ==========================================
# BARRA LATERAL (NAVEGACIÓN)
# ==========================================
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3048/3048122.png", width=100)
st.sidebar.title("Navegación")
menu = st.sidebar.radio(
    "Selecciona un módulo:",
    ("🏆 Olimpiadas (Finanzas)", "⚠️ Morosidad", "📈 Análisis Académico")
)

# ==========================================
# PÁGINA 1: OLIMPIADAS (FINANZAS)
# ==========================================
if menu == "🏆 Olimpiadas (Finanzas)":
    st.title("Recaudación y Metas Financieras")
    st.markdown("Seguimiento de pagos, yape y efectivo por tutor.")
    
    # Cuadros Estadísticos
    col1, col2, col3 = st.columns(3)
    total_meta = df_olim["Meta Dinero"].sum()
    total_recaudado = df_olim["Recaudado"].sum()
    avance_global = (total_recaudado / total_meta) * 100
    
    col1.metric("Meta Total", f"S/ {total_meta:,.2f}")
    col2.metric("Recaudado Total", f"S/ {total_recaudado:,.2f}", f"S/ {total_recaudado - total_meta:,.2f}")
    col3.metric("Avance Global", f"{avance_global:.1f}%")
    
    st.divider()
    
    # Gráfico interactivo con Plotly (Transiciones automáticas)
    st.subheader("Avance de Recaudación por Tutor")
    fig1 = px.bar(
        df_olim, 
        x="Tutor", 
        y=["Meta Dinero", "Recaudado"], 
        barmode="group",
        color_discrete_sequence=["#1f77b4", "#2ca02c"],
        text_auto='.2s'
    )
    fig1.update_layout(transition_duration=500) # Animación nativa de Plotly
    st.plotly_chart(fig1, use_container_width=True)

# ==========================================
# PÁGINA 2: MOROSIDAD
# ==========================================
elif menu == "⚠️ Morosidad":
    st.title("Estado de Pagos y Morosidad")
    st.markdown("Control de alumnos con cuotas pendientes y suspensiones.")
    
    # Simulador de carga para efecto visual
    with st.spinner('Cargando registros de morosidad...'):
        time.sleep(0.5)
    
    # Cuadros Estadísticos diferentes
    col1, col2, col3 = st.columns(3)
    col1.metric("Alumnos en Riesgo", "45", "+5 esta semana", delta_color="inverse")
    col2.metric("Deuda Acumulada", "S/ 4,500.00")
    col3.metric("Suspendidos", "12")
    
    st.divider()
    
    # Gráfico de Anillo
    st.subheader("Distribución por Condición de Pago")
    labels = ['Al Día', 'Debe 1 Cuota', 'Debe 2+ Cuotas', 'Suspendidos']
    values = [350, 80, 24, 12]
    fig2 = px.pie(names=labels, values=values, hole=0.4, color_discrete_sequence=px.colors.sequential.RdBu_r)
    fig2.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig2, use_container_width=True)

# ==========================================
# PÁGINA 3: ANÁLISIS ACADÉMICO
# ==========================================
elif menu == "📈 Análisis Académico":
    st.title("Asistencia y Rendimiento")
    st.markdown("Relación entre la asistencia a clases y las notas de los exámenes.")
    
    col1, col2 = st.columns(2)
    col1.metric("Promedio General (Notas)", f"{df_ana['Nota'].mean():.1f} / 20")
    col2.metric("Asistencia Promedio", f"{df_ana['Asistencia'].mean():.1f}%")
    
    st.divider()
    
    # Gráfico de dispersión (Scatter plot)
    st.subheader("Impacto de la Asistencia en la Nota")
    fig3 = px.scatter(
        df_ana, 
        x="Asistencia", 
        y="Nota", 
        color="Tutor", 
        size="Nota",
        hover_data=['Tutor'],
        trendline="ols" # Línea de tendencia
    )
    st.plotly_chart(fig3, use_container_width=True)
    
    # Mostrar tabla de datos con estilo
    st.subheader("Detalle de Registros")
    st.dataframe(df_ana.head(10), use_container_width=True)
