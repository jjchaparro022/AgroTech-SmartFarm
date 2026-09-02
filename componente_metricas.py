import pandas as pd

def calcular_kpis_agro(df: pd.DataFrame) -> dict:
    #Vamos a calcular los KPIS que nos piden a partir del Dataframe
    #Devolveremos un diccionario con lo solicitado
    
    if df.empty:
        return {
            "humedad_promedio" : 0.0,
            "temp_maxima" : 0.0,
            "parcelas_criticas" : 0
        }
    
    #Usamos .mean para obtener un promedio    
    humedad_promedio = float(df['humedad_suelo_pct'].mean())
    #Usamos .max para el maximo
    temp_maxima = float(df['temp_ambiente_c'].max())
    #Usaremos .nunique ya que nos solicitan parcelas diferentes estan en estado critico
    parcelas_criticas = int(df[df['humedad_suelo_pct'] < 30.0]['id_parcela'].nunique())
    
    return {
        "humedad_promedio": humedad_promedio,
        "temp_maxima": temp_maxima,
        "parcelas_criticas": parcelas_criticas
    }