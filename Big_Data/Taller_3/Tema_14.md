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
### 👤 Asignación: Tema 14

#### 📋 Enunciados del Taller

1. **Exploración de Series Temporales:** Cargue el archivo `Actividad2.xlsx` y, utilizando el método `.loc`, extraiga el precio de cierre de la acción **AAPL** para la fecha exacta de **'2024-01-30'**.   
   **[0] ¿Cuál es el valor del precio de cierre encontrado?**

2. **Tratamiento de Datos Faltantes:** Aplique el método `.ffill()` (forward fill) a todo el DataFrame para asegurar la continuidad de los datos.   
   **[1] Tras la imputación, ¿cuál es el promedio (mean) de la columna MSFT?**

3. **Gestión de Outliers:** Identifique los valores de **AAPL** superiores a 500 y reemplácelos por la mediana (`.median()`) de esa misma columna utilizando asignación con `.loc`.   
   **[2] ¿Cuál es la desviación estándar (std) de AAPL después de la corrección?**

4. **Análisis de Asociación:** Determine la fuerza de la relación lineal entre Apple (AAPL) y Microsoft (MSFT) mediante el coeficiente de correlación de Pearson usando el método `.corr()`.   
   **[3] ¿Cuál es el valor del coeficiente de correlación obtenido?**

5. **Inferencia Estadística:** Utilice la función `stats.ttest_ind()` de la librería `scipy.stats` para realizar una prueba de hipótesis independiente entre las series de AAPL y MSFT.   
   **[4] ¿Cuál es el p-valor (p_val) resultante de la prueba?**

6. **RETO DE PROGRAMACIÓN (Limpieza):** Defina una función llamada `limpiar_precios(df_sucio)`. Debe eliminar filas con 'ERROR', quitar '$' y puntos de miles en 'Precio_BVC' y devolver la suma total como float.   
   **Valide con evafunciones para obtener su código de éxito.** [5] ¿Cuál es el código de éxito?**


---
[⬅️ Volver al curso](../README.md)