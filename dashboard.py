import streamlit as st
import pandas as pd
import plotly.express as px
import os

# ==========================================
# 1. CONFIGURACIÓN DE LA PÁGINA
# ==========================================
st.set_page_config(
    page_title="Dashboard Siniestralidad Vial",
    page_icon="🚦",
    layout="wide"
)

# Título y Descripción
st.title("🚦 Tablero de Control: Siniestralidad Vial en Colombia")
st.markdown("""
Este dashboard permite analizar los **sectores críticos de siniestralidad** priorizando recursos 
basado en evidencia. Se exploran variables clave como **Fallecidos**, **Ubicación** y **Tendencia Temporal**.
""")

# ==========================================
# 2. CARGA DE DATOS
# ==========================================
@st.cache_data
def load_data():
    # Rutas dinámicas para encontrar el archivo data/dataset_enriquecido.csv
    # Asumimos que corres esto desde la raíz del proyecto
    file_path = "data/dataset_enriquecido.csv"
    
    if not os.path.exists(file_path):
        st.error(f"No se encontró el archivo en: {file_path}. ¡Ejecuta primero el script de la Etapa 2!")
        return None
    
    df = pd.read_csv(file_path)
    # Convertir fecha a datetime
    df['fecha'] = pd.to_datetime(df['fecha'])
    return df

df = load_data()

if df is not None:
    # ==========================================
    # 3. BARRA LATERAL (FILTROS)
    # ==========================================
    st.sidebar.header("🎛️ Filtros de Análisis")
    
    # Filtro Año
    years = sorted(df['anio'].unique())
    selected_years = st.sidebar.multiselect("Seleccionar Año(s)", years, default=years)
    
    # Filtro Departamento
    deptos = sorted(df['departamento'].unique())
    selected_deptos = st.sidebar.multiselect("Seleccionar Departamento(s)", deptos, default=deptos[:5]) # Pre-selecciona los primeros 5
    
    # Aplicar Filtros
    df_filtered = df.copy()
    
    if selected_years:
        df_filtered = df_filtered[df_filtered['anio'].isin(selected_years)]
        
    if selected_deptos:
        df_filtered = df_filtered[df_filtered['departamento'].isin(selected_deptos)]

    # ==========================================
    # 4. KPIs (INDICADORES CLAVE)
    # ==========================================
    st.subheader("📊 Métricas Generales")
    col1, col2, col3, col4 = st.columns(4)
    
    total_fallecidos = df_filtered['fallecidos'].sum()
    total_sectores = len(df_filtered)
    promedio_giz = df_filtered['gizscore'].mean()
    max_fallecidos = df_filtered['fallecidos'].max()
    
    col1.metric("Total Fallecidos", f"{total_fallecidos:,.0f}", delta_color="inverse")
    col2.metric("Sectores Críticos", total_sectores)
    col3.metric("Intensidad Prom. (GiZ)", f"{promedio_giz:.2f}")
    col4.metric("Máx. Fallecidos (1 sector)", max_fallecidos)
    
    st.markdown("---")

    # ==========================================
    # 5. VISUALIZACIONES PRINCIPALES
    # ==========================================
    
    # FILA 1: Mapa y Tendencia Temporal
    c1, c2 = st.columns((2, 2))
    
    with c1:
        st.subheader("🗺️ Mapa de Calor (Sectores Críticos)")
        # Usamos Plotly para un mapa interactivo usando Latitud y Longitud
        fig_map = px.scatter_mapbox(
            df_filtered, 
            lat="latitud", 
            lon="longitud", 
            color="fallecidos",
            size="fallecidos",
            hover_name="municipio",
            hover_data=["departamento", "tramo", "gizscore"],
            color_continuous_scale=px.colors.sequential.Reds,
            zoom=4, 
            mapbox_style="open-street-map",
            height=400
        )
        st.plotly_chart(fig_map, use_container_width=True)

    with c2:
        st.subheader("📈 Tendencia Temporal (Fallecidos)")
        # Agrupar por mes/año para la línea de tiempo
        df_time = df_filtered.groupby(['fecha', 'anio'])['fallecidos'].sum().reset_index().sort_values('fecha')
        
        fig_line = px.line(
            df_time, 
            x='fecha', 
            y='fallecidos',
            markers=True,
            title="Evolución de Fallecidos en el Tiempo"
        )
        fig_line.update_layout(height=400)
        st.plotly_chart(fig_line, use_container_width=True)

    # FILA 2: Análisis por Categoría (Barras)
    c3, c4 = st.columns(2)
    
    with c3:
        st.subheader("🏙️ Top Municipios Críticos")
        df_muni = df_filtered.groupby('municipio')['fallecidos'].sum().reset_index().nlargest(10, 'fallecidos')
        fig_bar_muni = px.bar(
            df_muni, 
            x='fallecidos', 
            y='municipio', 
            orientation='h',
            color='fallecidos',
            color_continuous_scale='Viridis',
            title="Municipios con mayor siniestralidad"
        )
        fig_bar_muni.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig_bar_muni, use_container_width=True)
        
    with c4:
        st.subheader("🔍 Correlación: Estadistica vs Realidad")
        fig_scatter = px.scatter(
            df_filtered,
            x="gizscore",
            y="fallecidos",
            color="departamento",
            size="fallecidos",
            hover_data=["municipio"],
            title="Relación GiZScore vs Fallecidos"
        )
        st.plotly_chart(fig_scatter, use_container_width=True)

    # ==========================================
    # 6. TABLA DE DATOS
    # ==========================================
    with st.expander("📂 Ver Datos Detallados (Tabla)"):
        st.dataframe(df_filtered)