# Big Data
## Taller_2: Modelos de Regresión Avanzados

### 🛠️ Instrucciones Previas
```python
# Configuración inicial del Taller 5
import pandas as pd
import numpy as np
import calificar as cr
import pandas as pd
import numpy as np
import json
import hashlib
import os
import joblib
from sklearn.datasets import fetch_openml
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import recall_score, f1_score, roc_auc_score  
from statsmodels.stats.outliers_influence import variance_inflation_factor

import calificar as cr


# Reemplace 'ID' por su código estudiantil, si son dos se separa por ;, así: '1026;1027' y 'G' por su número de grupo.
taller5 = cr.taller('ID', G, 'taller5BD2026i', 10)



#Nota: Este taller recopila todo lo que hemos visto en clase.
```

---
### 👤 Asignación: Tema 22

#### 📋 Enunciados del Taller 

**1. Análisis de Multicolinealidad (VIF) y Selección:**   
   a) Cargue el dataset 'credit-g' usando `fetch_openml(name='credit-g', version=1, as_frame=True)`.   
   b) Filtre únicamente las variables numéricas base: `['duration', 'credit_amount', 'age']`.   
   c) Calcule el Factor de Inflación de la Varianza (VIF) para cada una de estas variables.   
   **[0] ¿Cuál es el valor del VIF calculated para la variable 'credit_amount'? (Exprese con 4 decimales)**

**2. Diagnóstico y Balanceo de Clases:**   
   a) Mapee la variable 'class' para crear una variable objetivo binaria (`target`) donde 'bad' equivale a 1 y 'good' a 0.   
   b) Calcule la proporción (porcentaje) de la clase minoritaria (1) en todo el conjunto de datos original.   
   **[1] ¿Qué porcentaje (%) de los datos pertenece a la clase minoritaria (1)? (Exprese con 2 decimales, ej: 30.00)**

**3. Transformación de Variables Asimétricas:**   
   a) Genere una copia de la columna 'credit_amount' y aplique una transformación logarítmica natural: `np.log(df['credit_amount'])`.   
   b) Calcule el coeficiente de asimetría (*skewness*) de esta variable transformada usando el método `.skew()`.   
   **[2] ¿Cuál es el coeficiente de asimetría de 'credit_amount' después de aplicar el logaritmo natural?**

**4. Tratamiento de Outliers (Rango Intercuartílico - IQR):**   
   a) Calcule el Límite Superior de valores atípicos para la variable 'duration' usando la fórmula estricta: `Q3 + 1.5 * IQR`.   
   b) Determine cuántos registros de la columna 'duration' exceden de forma estricta este límite en el dataset completo.   
   **[3] ¿Cuántos registros atípicos (outliers) superiores se identificaron en la columna 'duration'?**

**5. Construcción del ColumnTransformer:**   
   a) Defina las variables numéricas como `['duration', 'credit_amount', 'age']` y las categóricas como `['checking_status', 'purpose']`.   
   b) Diseñe un preprocesador usando `ColumnTransformer` que aplique:   
      - Para numéricas: Un pipeline con `SimpleImputer(strategy='median')` y `StandardScaler()`.   
      - Para categóricas: Un pipeline con `SimpleImputer(strategy='most_frequent')` y `OneHotEncoder(handle_unknown='ignore', sparse_output=False)`.   
   c) Separe sus variables en `X` (las 5 características indicadas) e `y` (`target`), y realice un split con `test_size=0.2` y `random_state=2250`.   
   d) Ajuste (`fit_transform`) el preprocesador ÚNICAMENTE con los datos de entrenamiento `X_train`.   
   **[4] ¿Cuántas columnas totales tiene la matriz resultante de entrenamiento preprocesada?**

**6. Pipeline Completo de Clasificación Base:**   
   a) Construya un objeto `Pipeline` que integre el preprocesador del punto anterior como primer paso, y un modelo base `LogisticRegression(random_state=2250, max_iter=1000)`.   
   b) Entrene el pipeline usando `X_train` e `y_train`. Calcule la predicción sobre el conjunto de prueba `X_test`.   
   **[5] ¿Cuál es la precisión global (*accuracy_score*) obtenida por este pipeline base en el conjunto de prueba?**

**7. Métricas de Evaluación de la Matriz de Confusión:**   
   a) Genere la matriz de confusión o use métricas directas sobre el conjunto de prueba evaluado con el pipeline anterior.   
   b) Calcule el valor exacto de la sensibilidad (*Recall*) enfocado en la clase de riesgo (clase 1).   
   **[6] ¿Cuál es el valor del Recall obtenido para la clase 1 en el conjunto de prueba? (Exprese con 4 decimales)**

**8. Selección del Mejor Modelo (Competencia F1-Score):**   
   a) Instancie un segundo modelo competitivo reemplazando el clasificador por un `DecisionTreeClassifier(random_state=2250)` dentro de una nueva estructura de Pipeline idéntica.   
   b) Entrene y evalúe este árbol en el conjunto de prueba. Extraiga el valor de `f1_score` para la clase 1 de ambos modelos.   
   **[7] ¿Cuál es el F1-Score más alto para la clase 1 obtenido entre la Regresión Logística y el Árbol de Decisión?**

**9. Sintonización de Hiperparámetros (Grid Search con Validación Cruzada):**   
   a) Tome el pipeline que contiene el `DecisionTreeClassifier` y configure una búsqueda usando `GridSearchCV`.   
   b) Defina exactamente la siguiente rejilla de parámetros: `classifier__max_depth: [3, 5, 10]` y `classifier__min_samples_split: [2, 5]`.   
   c) Configure la búsqueda con validación cruzada `cv=3` y optimizando la métrica `scoring='f1'`. Entrene sobre `X_train`.   
   **[8] ¿Cuál es el valor del mejor parámetro 'max_depth' seleccionado por la búsqueda en rejilla?**

**10. Evaluación del Pipeline Final Optimizado:**   
    a) Extraiga el mejor estimador sintonizado del Grid Search (`grid.best_estimator_`) y prediga las probabilidades del conjunto de prueba.   
    b) Calcule la métrica del Área Bajo la Curva ROC (`roc_auc_score`) en el conjunto de prueba.   
    **[9] ¿Cuál es el valor del AUC-ROC en el conjunto de prueba para el árbol optimizado? (Exprese con 4 decimales)**


---
[⬅️ Volver al curso](../README.md)