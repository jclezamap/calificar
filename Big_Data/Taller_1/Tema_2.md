# Big Data
## Taller_1: Librería Numpy

### 🛠️ Instrucciones Previas
```python
# Configuración inicial del Taller 1
#si no tiene instalada la libreria ejecute este código
!pip install calificar
#Luego Importa las librerías
import calificar as cr
import pandas as pd
import numpy as np


# Reemplace 'ID' por su código estudiantil, si son dos se separa por ;, así: '20261026;20261027' y 'G' por su número de grupo.
taller = cr.taller('ID', G, 'taller1BD2026ii', 10)
#GIT para validación de funciones de este taller: https://raw.githubusercontent.com/jclezamap/calificar/refs/heads/main/Big_Data/Taller_1
#Para usar la libreria evafunciones, se coloca la URL dada y el Grupo.
#Para validar una función se guarda el resultado en una variable y la función a validar entrecomillas:  codigo = Eva.validar('es_rentable')
Eva = cr.evafunciones(URL, G)
```

---
### 👤 Asignación: Tema 2

#### 📋 Enunciados del Taller 

**1.** Convierta la lista `[[3,4,2], [3,1,2], [3,1,2]]` en una matriz de 3x3. Réstele una matriz identidad y calcule la suma de todos los elementos. **[0]¿Cuál es el valor de la suma?**

**2.** Cree un vector que inicie en 0 y termine en 57. Genere un nuevo vector recortando los dos primeros elementos (del índice 2 al final). **[1]¿Cuál es el valor del elemento 47 de este vector recortado?**

**3.** Calcule la suma acumulada (`cumsum`) del vector anterior (vector recortado). **[2]¿Qué valor hay en la posición 40?**

**4.** Cree un vector con los enteros del 2 al 11. Use `.dtype` y conviértalo a string. **[3]¿Cuál es el tipo de datos?**

**5.** Cree una serie uniforme de 0 a 50 con 25 elementos.

**6.** Modifique la serie anterior colocando a los primeros 10 elementos (índice 0 al 9) el valor de 5. Luego, sume todos los elementos. **[4]¿Cuánto es el valor de la suma?**

**7.** Cree una matriz de 5x10 llena de ceros (tipo 'U256'). Use ciclos `for` y `.shape` para que cada celda contenga la fila y columna unidas como texto (ej: '00', '01'). **[5]¿Qué valor hay en la posición [0, 8]?**

**8.** De la matriz de textos anterior: **[6]¿Qué valor hay en la fila 2 y columna 2?**

**9. RETO FINAL:** Programe la función `mi_operacion(A, B)` que multiplique matrices elemento a elemento con ciclos `for` y sume el total. Matrices: A=[[1, 1], [1, 3]], B=[[3, 3], [1, 4]]. **Valide con evafunciones para obtener su código de éxito.**[7]¿Cuál es el resultado de la función?**.[8]¿Cuál es el código de la validación?


---
[⬅️ Volver al curso](../README.md)