# Big Data
## Taller 2: Introducción a la Librería Pandas

### 🛠️ Instrucciones Previas
```python
Para realizar este taller, asegúrate de tener instalada las librerías numpy, pandas y calificar. 


    #!pip install calificar
    #Librerias para el Taller
    import calificar as cr
    import numpy as np
    import pandas as pd
    
    Taller2=cr.taller('1026',1, 'taller2BD2026i',11)
    
    #Se cambia '1026' por su código estudiantil, si son dos se separa por ;, así: '1026;1027'
    #Se cambia 1 por el Número de su Grupo asignado. 

    

    #GIT para validación de funciones de este taller: https://raw.githubusercontent.com/jclezamap/calificar/refs/heads/main/Big_Data/Taller_2
```

---
### 👤 Asignación: Tema 6

#### 📋 Enunciados del Taller

**1. Creación de la Tabla Principal:**   
   a) Antes de iniciar, coloque la siguiente función en python para generar números aleatorios con una semilla establecida  `np.random.seed(650)`.   
   b) Cree un rango de fechas (`pd.date_range`) que inicie en '2022-01-01', con 12 períodos y frecuencia de inicio de mes (`freq='MS'`).   
   c) Genere una matriz de números aleatorios enteros (`np.random.randint`) entre 10 y 100, con un tamaño de 12 filas y 4 columnas.   
   d) Construya el DataFrame `Nuevo1` usando esa matriz, las fechas como índice y nombre las columnas como 'Col1', 'Col2', 'Col3' y 'Col4'.   
   **[0] ¿Cuál es el resultado de sumar todos los valores obtenidos al aplicar `.describe()` a la columna 'Col1'?**

**2. Cargar archivo en Excel** Abra el archivo `Actividad1.xlsx` en la hoja llamada '6'. Extraiga únicamente las primeras 4 filas (utilice `.iloc[0:4]`) y seleccione la columna 'B'. **[1] ¿Cuál es el promedio (mean) de esos 4 valores?**

**3. Filtro y Reordenar:** De la tabla `Nuevo1`, seleccione el rango de fechas de Octubre a Diciembre de 2022 (pista: use `.loc['2022-10-01':'2022-12-01']`). Transponga los datos con `.T`. Luego, use `.sort_values` para ordenar la tabla de mayor a menor (falso en ascendente) basándose en los valores de la columna de la última fecha disponible. **[2] ¿Qué valor numérico quedó en la fila 'Col2' para esa fecha final?**

**4. Producto Punto:** En el archivo `Actividad1.xlsx` (hoja '6'), identifique las últimas 3 filas de la tabla (puede usar `.tail(3)`). Realice la operación de producto punto con el método `.dot()` entre la columna 'A' y la columna 'C'. **[3] ¿Cuál es el resultado final de esta operación?**

**5. Análisis de Datos de Combustibles:** Cargue el archivo CSV desde la URL 'https://economiafinanciera.com.co/download/Combustibles.csv'. Siga este orden:   
   a) Convierta 'fecha_despacho' a formato fecha con `pd.to_datetime`.   
   b) Cree la columna 'Año' usando `.dt.year` y la columna 'Mes' usando `.dt.month`.   
   c) Filtre la tabla para dejar solo los registros donde 'municipio_proveedor' sea exactamente 'BOGOTA, D.C.'.   
   d) Agrupe por 'Año' y 'Mes', sume el 'volumen_despachado' y aplique `.reset_index()` al final.   
   **[4] ¿Cuál fue el volumen total despachado en Bogotá durante Diciembre (12) de 2022?**

**6. Resumen Estadístico:** Cargue el archivo `Resultados2.xlsx` que está en su carpeta del taller en Github. Seleccione la columna 'TD' y aplique `.describe()`.   
**[5] ¿Cuál es el valor de la desviación estándar?** (Es el dato que aparece en la posición física [2] del resultado).

**7. RETO LIMPIEZA (Funciones):** Crea una función llamada `limpiar_nulos(df)`.   
Dentro de la función, use el método `.fillna(0)` para que todos los valores vacíos se conviertan en cero. La función debe terminar con `return` seguido de la tabla modificada. Use `datos_reto.csv` que se encuentra en la carpeta de Github para probar que funcione. **Valide con evafunciones para obtener su código de éxito.**[6]¿Cuál es el código de la validación?**

**8. RETO OPERACIÓN (Funciones):** Defina una función llamada `nueva_moneda(df)`.   
Dentro, cree la columna 'Dolares' dividiendo 'Col1' entre 4000. No olvide el `return`. **Valide con evafunciones para obtener su código de éxito.**[7]¿Cuál es el código de la validación?**

**9. Cálculos Comparativos:** Usando la tabla `Nuevo1`, obtenga el promedio de 'Col1' y el promedio de 'Col2'. Reste ambos resultados: `promedio_col1 - promedio_col2`. **[8] ¿Cuál es el valor de esa diferencia?**

**10. RETO FINAL (Filtrado Avanzado):** Defina la función `reporte_pares(df)`.   
   a) Identifique los meses pares usando el operador módulo en el índice: `df.index.month % 2 == 0`.   
   b) Filtre la tabla original con esa condición.   
   c) Sume los valores de la columna 'Col3' de esa tabla filtrada y use `return` para devolver el resultado.   
   **[9] ¿Cuánto es la suma de la columna 'Col3'?**   **Valide con evafunciones para obtener su código de éxito.**[10]¿Cuál es el código de la validación?**


---
[⬅️ Volver al curso](../README.md)