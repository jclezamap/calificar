# Big Data
## Parcial 1: Primer Parcial

### 🛠️ Instrucciones Previas
```python
# Configuración inicial del Parcial
import calificar as cr
import numpy as np
import pandas as pd
import yfinance as yf
from scipy import stats

# Reemplace 'ID' por su código estudiantil, si son dos se separa por ;, así: '1026;1027' y 'G' por su número de grupo.
taller = cr.taller('ID', G, 'parcial1BD2026i', 5)
#GIT para validación de funciones de este taller: https://raw.githubusercontent.com/jclezamap/calificar/refs/heads/main/Big_Data/Parcial_1
```

---
### 👤 Asignación: Tema 8

#### 📋 Enunciados del Taller Parcial

**1. Uso de Numpy:**   
   Cree una matriz de identidad de 4x4. Multiplíquela por el escalar 18.   
   Posteriormente, cambie el valor de la posición [2, 2] por 0.   
   **[0] ¿Cuál es la suma total de todos los elementos de la matriz resultante?**

**2. Uso de Pandas:**   
   Cree un DataFrame con un índice de fechas que inicie el '2025-01-01' para 24 meses (freq='MS').   
   Llene una columna llamada 'Datos' con una secuencia lineal de 1 a 24.   
   **[1] ¿Cuál es el valor de la columna 'Datos' para la fecha '2025-09-01'?**

**3. Análisis de Archivos en excel:**   
   Cargue el archivo `Actividad_Final.xlsx` en la hoja '8'. El archivo contiene columnas 'A' y 'B'.   
   **Instrucción:** Calcule el producto de la columna 'A' por la columna 'B' fila a fila, y luego obtenga el valor máximo de ese resultado.   
   **[2] ¿Cuál es el valor máximo obtenido?**

**4. Limpieza y Transformación:**   
   De la tabla del punto 2, extraiga los meses correspondientes al segundo semestre del año 2025 (Julio a Diciembre).   
   **Instrucción:** Calcule el promedio de estos 6 meses y réstele 10 unidades como ajuste de auditoría.   
   **[3] ¿Cuál es el resultado final tras el ajuste?**

**5. RETO DE INTEGRACIÓN (Funciones):**   
   Defina la función `analisis_vulnerabilidad(lista_precios)`.   
   a) Convierta la lista en una serie de Pandas.   
   b) Identifique los valores que están por debajo del promedio de la serie.   
   c) Devuelva la cantidad (count) de elementos que cumplieron esa condición.   
   Use lista_precios_test = [100, 200, 300, 400, 500] como Ejemplo de validación  
   **Valide con evafunciones para obtener su código de éxito.** [4] ¿Cuál es el código de éxito?**


---
[⬅️ Volver al curso](../README.md)