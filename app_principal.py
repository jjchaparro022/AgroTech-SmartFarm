import streamlit as st
#from componente_datos import cargar_y_validar_datos_agro
#from componente_metricas import calcular_kpis_agro
#from componente_prediccion import estimar_necesidad_riego

#Configuracion de la Pagina 
st.set_page_config(page_title="AgroTech SmartFarm", layout="wide")

st.title("AgroTech SmartFarm")
st.subheader("Bienvenido a la plataforma de gestión agrícola inteligente")

# Sidebar para subir archivo CSV
with st.sidebar:
    st.header("⚙️ Configuración")
    archivo_subido = st.file_uploader("Sube tu archivo de datos agrícolas (CSV)", type=["csv"])
    
if archivo_subido is not None:
    try:
        st.session_state['datos_agro'] = cargar_y_validar_datos_agro(archivo_subido)
        st.sidebar.success("Archivo cargado y validado correctamente.")
    except Exception as error:
        st.error(f"Error al cargar los datos: {error}")
        if 'datos_agro' in st.session_state:
            del st.session_state['datos_agro']

if 'datos_agro' not in st.session_state:
    st.warning("No se han cargado datos. Por favor, sube un archivo CSV para continuar.")
    st.stop()
    
try:
    #Le pasamos el DataFrame limpio y guardamos en session_state
    kpis = calcular_kpis_agro(st.session_state['datos_agro'])
    
    st.subheader("📊 Métricas Clave de Rendimiento (KPIs)")
    
    with st.container():
        col1, col2, col3 = st.columns(3)
        col1.metric(label=" Humedad media", value=f"{kpis[0]:.1f}% ")
        col2.metric(label=" Temperatura Maxima", value=f"{kpis[1]:.1f}°C")
        col3.metric(label=" Parcelas Criticas", value=kpis[2])    
except Exception as e:
    st.error(f"Error al calcular los KPIs: {e}")
    
st.markdown("---")
st.subheader("💧 Estimación de Necesidad de Riego")

try:
    # 1. Recuperamos el DataFrame de la sesión
    df_actual = st.session_state['datos_agro']
    
    # 2. Implementamos el selector de parcela que exige la guía
    lista_parcelas = df_actual['id_parcela'].unique()
    parcela_seleccionada = st.selectbox("Selecciona una parcela específica:", lista_parcelas)
    
    # 3. Llamamos a la función (recuerda: solo devuelve un número float correspondiente a los litros o 0)
    litros_recomendados = estimar_necesidad_riego(df_actual)
    
    litros_recomendados = estimar_necesidad_riego(df_filtrado)
    
    with st.container():
        # Reducimos a 2 columnas ya que la función no nos da 3 datos distintos
        col1, col2 = st.columns(2)
        
        col1.metric(label="📍 Parcela en Visualización", value=parcela_seleccionada)
        
        # Mostramos la recomendación dependiendo del valor retornado
        if litros_recomendados > 0:
            col2.metric(label="⚠️ Litros a Regar", value=f"{litros_recomendados:.2f} L")
        else:
            col2.metric(label="✅ Estado Óptimo", value="0.0 L (Sin riego)")
            
    # 4. Arreglamos el gráfico de líneas
    st.write("📈 Tendencia de humedad en la parcela seleccionada:")
    
    # Filtramos los datos para mostrar solo la gráfica de la parcela elegida
    df_filtrado = df_actual[df_actual['id_parcela'] == parcela_seleccionada]
    
    # Preparamos los datos poniendo el timestamp como índice para el gráfico
    datos_grafico = df_filtrado.set_index('timestamp')['humedad_suelo_pct']
    
    # Dibujamos el gráfico (corregida la variable y la indentación)
    st.line_chart(datos_grafico)

except Exception as e:
    st.error(f"Error en el módulo de predicción: {e}")