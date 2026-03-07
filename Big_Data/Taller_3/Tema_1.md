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

# Reemplace 'ID' por su código estudiantil, si son dos se separa por ;, así: '1026;1027' y 'G' por su número de grupo.
taller = cr.taller('ID', G, 'taller3BD2026i', 6)
#GIT para validación de funciones de este taller: https://raw.githubusercontent.com/jclezamap/calificar/refs/heads/main/Big_Data/Taller_3
```

---
### 👤 Asignación: Tema 1

#### 📋 Enunciados del Taller

1. **Extracción de Datos Específicos:** Cargue el archivo Excel llamado `Actividad2.xlsx`. Utilice el método `.loc` sobre el índice de fechas para extraer el precio de cierre de la acción **AAPL** correspondiente al día **'2024-01-10'**.   
   **[0] ¿Cuál es el valor exacto del precio de cierre para esa fecha?**

2. **Limpieza de Datos Faltantes:** Las series financieras suelen tener valores nulos (NaN) en días no hábiles. Cargue el DataFrame completo de `Actividad2.xlsx` y aplique el método `.ffill()` (forward fill) para completar los espacios vacíos con el último valor disponible.   
   **[1] Tras realizar la imputación, ¿cuál es el promedio (mean) de la columna 'MSFT'?**

3. **Tratamiento de Valores Atípicos (Outliers):** En la columna **AAPL**, identifique todos los registros cuyo valor sea superior a 500. Reemplace estos valores atípicos por la mediana (`.median()`) de esa misma columna utilizando la función `.loc`.   
   **[2] ¿Cuál es la desviación estándar (std) de la columna AAPL después de corregir los valores?**

4. **Análisis de Correlación:** Utilice el método `.corr()` de Pandas para calcular el coeficiente de correlación de Pearson entre las series de precios de 'AAPL' y 'MSFT'. Este valor indica el grado de asociación lineal entre ambas acciones.   
   **[3] ¿Cuál es el resultado del coeficiente de correlación obtenido?**

5. **Inferencia Estadística (Prueba T):** Importe la librería `from scipy import stats`. Realice una prueba de hipótesis para muestras independientes usando `stats.ttest_ind()` comparando las series de 'AAPL' y 'MSFT' (asegúrese de no tener valores nulos).   
   **[4] ¿Cuál es el valor del p-valor (p_val) arrojado por la prueba estadística?**

6. **RETO DE PROGRAMACIÓN (Limpieza de Datos Crudos):** Localice el archivo `Reporte_Crudo.csv` en su carpeta de trabajo. Defina una función llamada `limpiar_precios(df_sucio)` que procese la columna 'Precio_BVC' de la siguiente manera:   
   a) Filtre el DataFrame para eliminar las filas que contienen la palabra 'ERROR'.   
   b) En los valores restantes, elimine el símbolo de moneda '$' y los puntos de miles (ej: de '$150.500' a '150500').   
   c) Transforme la columna a tipo numérico (float) y retorne la suma total de dicha columna con `return`.   
   **Valide su función con la librería evafunciones para obtener su código de éxito.** [5] ¿Cuál es el código de éxito?**


---
[⬅️ Volver al curso](../README.md)