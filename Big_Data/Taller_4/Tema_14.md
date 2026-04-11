# Big Data
## Taller 4: NLP y k-NN

### 🛠️ Instrucciones Previas
```python
# Configuración inicial del Taller 4
import calificar as cr
import pandas as pd
import numpy as np
from sklearn.neighbors import KNeighborsClassifier

# Reemplace 'ID' por su código estudiantil, si son dos se separa por ;, así: '1026;1027' y 'G' por su número de grupo.
taller = cr.taller('ID', G, 'taller4BD2026i', 10)
#GIT para validación de funciones de este taller: https://raw.githubusercontent.com/jclezamap/calificar/refs/heads/main/Big_Data/Taller_4
#Para usar la libreria evafunciones, se coloca la URL dada y el Grupo.
#Para validar una función se guarda el resultado en una variable y la función a validar entrecomillas:  codigo = Eva.validar('es_rentable')
Eva = cr.evafunciones(URL, G)



#Nota: Los datos de su cliente están en el Excel, pero los puntos de comparación C1 y C2 son fijos para todo el curso: C1 = [0.2, 0.8] y C2 = [0.8, 0.2]. Úselos para entrenar su modelo de KNeighborsClassifier.
```

---
### 👤 Asignación: Tema 14

#### 📋 Enunciados del Taller 

**1. Procesamiento de Lenguaje Natural (NLP):**   
   a) Abra el archivo `Datos_Taller_4_NLP_KNN.xlsx` en la pestaña 'Tema_14'.   
   b) Extraiga la celda 'Comentario_Cliente' y conviértala a minúsculas usando el método `.lower()`.   
   **[0] ¿Cuál es el número total de caracteres (longitud) de ese texto resultante?**

**2. Minería de Textos con Pandas:**   
   a) Tome el texto en minúsculas y sepárelo en una lista de palabras usando `.split()`.   
   b) Convierta esa lista en una Serie de Pandas (`pd.Series`).   
   c) Utilice el método `.value_counts()` para contar las repeticiones de cada palabra.   
   **[1] ¿Cuántas veces aparece exactamente la palabra 'deuda'?**

**3. Análisis de Moda:**   
   a) Usando la serie de conteos anterior, aplique el método `.idxmax()` para identificar la palabra más frecuente.   
   **[2] ¿Qué palabra es la que presenta la mayor frecuencia en su comentario?**

**4. Ubicación de Cliente (Features):**   
   a) Identifique los valores 'Ingreso_X' y 'Deuda_Y' en su pestaña de Excel.   
   b) Determine el cuadrante de su cliente: Si Ingreso_X es menor o igual a 0.5 y Deuda_Y es mayor a 0.5, el cliente es 'Cuadrante 2'. Si Ingreso_X es mayor a 0.5 y Deuda_Y es menor o igual a 0.5, es 'Cuadrante 4'.   
   **[3] ¿En qué número de cuadrante quedó ubicado su cliente?**

**5. Distancia al Nodo de Riesgo (C1):**   
   a) Definimos el Nodo C1 (Riesgo Alto) en las coordenadas [0.2, 0.8].   
   b) Calcule la distancia euclidiana entre su cliente y C1 usando la fórmula: `np.sqrt(np.sum((punto_cliente - nodo_c1)**2))`.   
   **[4] ¿Cuál es el valor de la distancia obtenida? (Reporte con 4 decimales).**

**6. Clasificación k-NN (Vecino más cercano):**   
   a) Ahora calcule la distancia de su cliente al Nodo C2 (Cumplido) ubicado en [0.8, 0.2].   
   b) Compare ambas distancias: ¿Es menor la distancia a C1 o a C2?   
   **[5] Escriba el nombre del nodo (C1 o C2) al que su cliente se encuentra más cerca.**

**7. Etiqueta del Modelo:**   
   a) Si el vecino más cercano es C1, la etiqueta es 1 (Riesgo). Si el más cercano es C2, la etiqueta es 0 (Cumplido).   
   **[6] ¿Qué etiqueta numérica le asignó el modelo a su cliente?**

**8. Estadísticos Descriptivos:**   
   a) Tome los 4 valores numéricos marcados como 'D1', 'D2', 'D3' y 'D4' en su Excel.   
   b) Cree una Serie de Pandas con esos datos y aplique el método `.describe()`.   
   **[7] ¿Cuál es el valor que aparece en el percentil 50% (la mediana) de sus datos?**

**9. Indicador de Capacidad de Pago:**   
   a) Aplique la siguiente fórmula ponderada: `(Ingreso_X * 0.7) - (Deuda_Y * 0.3)`.   
   **[8] ¿Cuál es el resultado de este indicador? (Reporte con 4 decimales).**

**10. RETO FINAL (Funciones):**   
    a) Defina la función `es_rentable(valor)`.   
    b) Dentro de la función, use un `if`: si el valor es mayor a 0.5 debe retornar `True`, de lo contrario `False`.   
    c) **Ejemplo de prueba:** Si usa `es_rentable(0.8)` el resultado debe ser `True`.   
    **[9] Valide con evafunciones para obtener su código de éxito.**


---
[⬅️ Volver al curso](../README.md)