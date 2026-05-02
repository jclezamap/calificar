# Big Data
## Parcial_2: Evaluación de Modelos de Clasificación

### 🛠️ Instrucciones Previas
```python
# Configuración inicial del Parcial 2
import pandas as pd
import numpy as np
from sklearn.datasets import fetch_openml
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.inspection import permutation_importance
from sklearn.metrics import recall_score

import calificar as cr


# Reemplace 'ID' por su código estudiantil, si son dos se separa por ;, así: '1026;1027' y 'G' por su número de grupo.
parcial2 = cr.taller('ID', G, 'parcial2BD2026i', 10)



#Nota: Este parcial toma cosas que hemos hecho en clase y en las actividades.
```

---
### 👤 Asignación: Tema 2

#### 📋 Enunciados del Parcial 

**1. Preparación de Datos y Feature Engineering:**   
   a) Cargue el dataset 'credit-g' usando `fetch_openml(name='credit-g', version=1, as_frame=True)`.   
   b) Cree la variable objetivo `target` mapeando 'good' a 1 y 'bad' a 0 de la columna 'class'.   
   c) Calcule una nueva variable llamada `Cuota_Estimada` como: `(credit_amount / duration) + (age * 10)`.   
   d) Defina sus variables independientes como: `X = df[['duration', 'credit_amount', 'age', 'Cuota_Estimada']]`.   
   **[0] ¿Cuál es la desviación estándar de la nueva columna 'Cuota_Estimada'?**

**2. Partición de Datos:**   
   a) Use `train_test_split` con un `test_size=0.2`.   
   b) Es OBLIGATORIO usar la semilla aleatoria `random_state=250`.   
   **[1] ¿Cuántos registros quedaron en el conjunto de entrenamiento (X_train)?**

**3. Estandarización:**   
   a) Cree un objeto `StandardScaler()`.   
   b) Ajuste el escalador SOLO con los datos de entrenamiento (`fit_transform`) y transforme los de prueba (`transform`).   
   **[2] ¿Cuál es el valor máximo obtenido en la columna 'duration' después de estandarizar X_train?**

**4. Árbol de Decisión (Optimización):**   
   a) Use `GridSearchCV` con el modelo `DecisionTreeClassifier(random_state=250)`.   
   b) Pruebe los parámetros `max_depth: [3, 5, 10]` y `criterion: ['gini', 'entropy']`.   
   c) Configure `scoring='recall'` y `cv=3`.   
   **[3] ¿Cuál fue el mejor 'max_depth' encontrado por la búsqueda?**

**5. Naive Bayes y Probabilidades:**   
   a) Entrene un modelo `GaussianNB()` con los datos escalados de entrenamiento.   
   b) Para el primer registro de su conjunto de prueba (`X_test_scaled[0]`), calcule la probabilidad de ser 'buen crédito' (clase 1).   
   **[4] ¿Cuál es esa probabilidad? (Exprese con 4 decimales)**

**6. Importancia de Variables (Bayes):**   
   a) Calcule la importancia de variables para Naive Bayes usando la diferencia absoluta de las medias: `np.abs(modelo.theta_[1] - modelo.theta_[0])`.   
   b) Identifique el valor resultante para la variable 'age' (posición [2]).   
   **[5] ¿Cuál es el valor de importancia para 'age'?**

**7. k-NN y Permutación:**   
   a) Entrene un `KNeighborsClassifier(n_neighbors=5)` con los datos escalados.   
   b) Calcule la importancia por permutación usando `permutation_importance` con `random_state=250` sobre el conjunto de prueba.   
   **[6] ¿Cuál es el valor de 'importances_mean' para la variable 'credit_amount'?**

**8. Selección del Mejor Modelo (Recall):**   
   a) Calcule el `recall_score` en el conjunto de prueba para los 3 modelos entrenados (Árbol optimizado, Bayes y k-NN).   
   **[7] ¿Cuál es el Recall más alto obtenido entre los tres modelos?**

**9. Predicción de Nuevos Casos:**   
   a) Use el mejor modelo (el del punto anterior) para predecir el siguiente caso: `[[24, 2500, 35, 200]]` (Recuerde escalarlos primero).   
   **[8] ¿Cuál es la probabilidad de que este cliente sea Clase 1?**

**10. Análisis de Impacto Relativo:**   
   a) Tome los datos para predecir `[[24, 2500, 35, 200]]`.   
   b) Calcule la importancia relativa: `abs(datos) / abs(datos).sum()`.   
   c) Determine el impacto del factor principal: `porcentaje = importancia_relativa.max() * 100`.   
   **[9] ¿Qué porcentaje (%) de impacto tiene el factor más influyente en este registro?**


---
[⬅️ Volver al curso](../README.md)