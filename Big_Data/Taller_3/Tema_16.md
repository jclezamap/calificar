# Big Data
## Taller 3: Análisis EDA

### 🛠️ Instrucciones Previas
```python
# Configuración inicial del Taller
import calificar as cr
import numpy as np
import pandas as pd
import yfinance as yf
from scipy import stats

# Reemplace 'ID' por su código y 'G' por su número de grupo
taller = cr.taller('ID', G, 'taller3BD2026i', 6)
```

---
### 👤 Asignación: Tema 16

#### 📋 Enunciados del Taller

**1. Carga y Exploración Inicial:**   
   Cargue el archivo `Actividad2.xlsx` que contiene los precios de cierre.   
   **Instrucción:** Use el método `.loc` para encontrar el precio de cierre de la acción AAPL específicamente para el día '2024-02-01'.   
   **[0] ¿Cuál es el precio de cierre de AAPL ese día?**

**2. Imputación de Datos Faltantes:**   
   Las series financieras suelen tener vacíos por días no bursátiles.   
   **Instrucción:** Aplique el método `.ffill()` a todo el DataFrame para propagar el último precio válido hacia adelante.   
   **[1] Tras realizar la imputación, ¿cuál es el promedio (mean) de la columna MSFT?**

**3. Gestión de Outliers (Valores Atípicos):**   
   A veces existen errores de digitación que disparan los precios artificialmente.   
   **Instrucción:** Identifique los valores de 'AAPL' que sean mayores a 500 y reemplácelos por la mediana de esa misma columna usando `.loc`.   
   **[2] ¿Cuál es la desviación estándar (std) de AAPL después de corregir estos valores?**

**4. Asociación Lineal (Correlación):**   
   Es fundamental medir cómo se mueven las acciones líderes del sector tecnológico en conjunto.   
   **Instrucción:** Use el método `.corr()` para calcular el coeficiente de correlación de Pearson entre Apple (AAPL) y Microsoft (MSFT).   
   **[3] ¿Cuál es el valor del coeficiente de correlación obtenido?**

**5. Inferencia Estadística:**   
   Realice una comparación de medias para determinar si existen diferencias significativas entre ambos activos.   
   **Instrucción:** Utilice la función `stats.ttest_ind(df['AAPL'], df['MSFT'])` de la librería `scipy`.   
   **[4] ¿Cuál es el p-valor (p_val) resultante de esta prueba de hipótesis?**

**6. RETO DE PROGRAMACIÓN (Limpieza de Datos Crudos):**   
   Cargue el archivo `Reporte_Crudo.csv`. La columna 'Precio_BVC' requiere limpieza profunda.   
   **Instrucción:** Defina una función llamada `limpiar_precios(df_sucio)` que realice lo siguiente:   
   a) Elimine las filas que contengan el texto 'ERROR'.   
   b) Quite los símbolos de moneda '$' y los puntos de miles.   
   c) Convierta la columna a tipo flotante (`float`) y devuelva la suma total de dicha columna.   
   **Valide con evafunciones para obtener su código de éxito.**[5] ¿Cuál es el código de éxito de la validación?**


---
[⬅️ Volver al curso](../README.md)