# Big Data
## Taller 4: Taller No 4: NLP y k-NN

### 🛠️ Instrucciones Previas
```python
# Configuración inicial del Taller 4
import calificar as cr
import pandas as pd
import numpy as np
from sklearn.neighbors import KNeighborsClassifier

# Reemplace 'ID' por su código estudiantil, si son dos se separa por ;, así: '1026;1027' y 'G' por su número de grupo.
taller = cr.taller('ID', G, 'taller4BD2026i', 5)
#GIT para validación de funciones de este taller: https://raw.githubusercontent.com/jclezamap/calificar/refs/heads/main/Big_Data/Taller_4

#Nota: Los datos de su cliente están en el Excel, pero los puntos de comparación C1 y C2 son fijos para todo el curso: C1 = [0.2, 0.8] y C2 = [0.8, 0.2]. Úselos para entrenar su modelo de KNeighborsClassifier.
```

---
### 👤 Asignación: Tema 26

#### 📋 Enunciados del Taller 

**1. Longitud de Texto:**   
   a) Extraiga la variable 'Comentario_Cliente' de su pestaña 'Tema_26'.   
   b) Use el método `.lower()` para convertirlo a minúsculas.   
   **[0] ¿Cuál es la longitud total de caracteres (`len()`) del texto en minúsculas?**

**2. Análisis de Frecuencias con Pandas:**   
   a) Use `.split()` para separar el texto en palabras y conviértalo en una Serie de Pandas (`pd.Series`).   
   b) Aplique el método `.value_counts()` sobre esa serie.   
   **[1] ¿Cuántas veces aparece la palabra 'deuda'?**

**3. Identificación de la Moda:**   
   a) Identifique la palabra que más se repite en su serie de datos anterior.   
   **[2] ¿Cuál es esa palabra?**

**4. Ubicación en el Mapa de Riesgo:**   
   a) Su cliente tiene coordenadas Ingreso_X: 0.62 y Deuda_Y: 0.38.   
   b) Ubique los Nodos de referencia: C1 (Riesgo) en [0.2, 0.8] y C2 (Cumplido) en [0.8, 0.2].   
   **[3] ¿En qué número de cuadrante está su cliente? (Considere X > 0.5 o X <= 0.5)**

**5. Distancia al Nodo de Riesgo (C1):**   
   a) Use la fórmula de distancia: `sqrt((x2-x1)**2 + (y2-y1)**2)` entre su cliente y C1.   
   **[4] ¿Cuál es la distancia exacta? (4 decimales)**

**6. Predicción k-NN (Vecino más cercano):**   
   a) Calcule la distancia hacia C2 y compárela con la de C1.   
   **[5] ¿A qué nombre de nodo (C1 o C2) está más cerca su cliente?**

**7. Clasificación del Modelo:**   
   a) Si el cliente está más cerca de C1 la etiqueta es 1. Si es C2 la etiqueta es 0.   
   **[6] ¿Qué número de clasificación le corresponde?**

**8. Análisis Descriptivo con Pandas:**   
   a) Tome los 4 valores de 'Dato_Prueba' (1 al 4) de su pestaña y cree una Serie de Pandas.   
   b) Aplique el método `.describe()`.   
   **[7] ¿Cuál es el valor de la mediana (percentil 50%) de esos datos?**

**9. Indicador de Capacidad:**   
   a) Calcule el indicador usando la fórmula: `(Ingreso_X * 0.7) - (Deuda_Y * 0.3)`.   
   **[8] ¿Cuál es el resultado numérico? (4 decimales)**

**10. RETO: Función de Rentabilidad:**   
    a) Defina la función `es_rentable(valor)`. Si el valor es mayor a 0.5 retorne True, sino False.   
    b) **DATO DE EJEMPLO:** Si prueba su función con 0.8, el resultado DEBE ser True.   
    **[9] Valide con evafunciones para obtener su código de éxito.**


---
[⬅️ Volver al curso](../README.md)