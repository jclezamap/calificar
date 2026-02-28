# Big Data
## Taller 1: Librería Numpy

### 🛠️ Instrucciones Previas
```python
Para realizar este taller, asegúrate de tener instalada las librerías numpy y calificar. 


    #!pip install calificar
    #Librerias para el Taller
    import calificar as cr
    import numpy as np
    
    Taller1=cr.taller('1026',1, 'taller1BD2026i',9)
    
    #Se cambia '1026' por su código estudiantil, si son dos se separa por ;, así: '1026;1027'
    #Se cambia 1 por el Número de su Grupo asignado. 

    

    #GIT para validación de funciones de este taller: https://raw.githubusercontent.com/jclezamap/calificar/refs/heads/main/Big_Data/Taller_1
```

---
### 👤 Asignación: Tema 1

#### 📋 Enunciados del Taller

1. **1.** Convierta la lista `[[2,2,4], [3,3,2], [1,4,3]]` en una matriz de 3x3. Réstele una matriz identidad y calcule la suma de todos los elementos. **[0]¿Cuál es el valor de la suma?**

2. **2.** Cree un vector que inicie en 0 y termine en 56. Genere un nuevo vector recortando los dos primeros elementos (del índice 2 al final). **[1]¿Cuál es el valor del elemento 47 de este vector recortado?**

3. **3.** Calcule la suma acumulada (`cumsum`) del vector anterior. **[2]¿Qué valor hay en la posición 40?**

4. **4.** Cree un vector con los enteros del 1 al 10. Use `.dtype` y conviértalo a string. **[3]¿Cuál es el tipo de datos?**

5. **5.** Cree una serie uniforme de 0 a 50 con 25 elementos.

6. **6.** Modifique la serie anterior colocando a los primeros 10 elementos (índice 0 al 9) el valor de 5. Luego, sume todos los elementos. **[4]¿Cuánto es el valor de la suma?**

7. **7.** Cree una matriz de 5x10 llena de ceros (tipo 'U256'). Use ciclos `for` y `.shape` para que cada celda contenga la fila y columna unidas como texto (ej: '00', '01'). **[5]¿Qué valor hay en la posición [0, 8]?**

8. **8.** De la matriz de textos anterior: **[6]¿Qué valor hay en la fila 1 y columna 1?**

9. **9. RETO FINAL:** Programe la función `mi_operacion(A, B)` que multiplique matrices elemento a elemento con ciclos `for` y sume el total. Matrices: A=[[1, 4], [1, 4]], B=[[1, 3], [1, 2]]. **Valide con evafunciones para obtener su código de éxito.**[7]¿Cuál es el resultado de la función?**.[8]¿Cuál es el código de la validación?


---
[⬅️ Volver al curso](../README.md)