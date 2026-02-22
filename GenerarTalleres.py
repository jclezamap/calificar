import pandas as pd
import json
import os
from datetime import datetime

def actualizar_sistema_talleres(df_nuevo, subtitulo="", instruccion_principal=""):
    nombre_json = 'enunciados.json'
    fecha_hoy = datetime.now().strftime("%d/%m/%Y")
    
    if os.path.exists(nombre_json):
        with open(nombre_json, 'r', encoding='utf-8') as f:
            banco_datos = json.load(f)
    else:
        banco_datos = {}

    for (curso, taller, tema), grupo in df_nuevo.groupby(['Curso', 'Taller', 'Tema']):
        if curso not in banco_datos:
            banco_datos[curso] = {}
        
        taller_id = f"Taller_{taller}"
        
        # Inicializar taller si no existe
        if taller_id not in banco_datos[curso]:
            banco_datos[curso][taller_id] = {"temas": {}}
        
        # Actualizamos siempre estos campos por si el usuario los cambió en el script
        banco_datos[curso][taller_id]["fecha"] = fecha_hoy
        banco_datos[curso][taller_id]["subtitulo"] = subtitulo
        banco_datos[curso][taller_id]["instruccion"] = instruccion_principal
        
        tema_id = f"{tema}".replace(" ", "_")
        banco_datos[curso][taller_id]["temas"][tema_id] = grupo['Enunciado'].tolist()

    with open(nombre_json, 'w', encoding='utf-8') as f:
        json.dump(banco_datos, f, indent=4, ensure_ascii=False)

    construir_archivos_desde_diccionario(banco_datos)
    print(f"✅ Sistema actualizado con instrucciones para el taller.")

def construir_archivos_desde_diccionario(datos):
    # Generar Menú Principal
    with open("TALLERES.md", "w", encoding="utf-8") as f_main:
        f_main.write("# 📚 Portal Global de Talleres\n\n Seleccione su curso:\n\n")
        
        for curso, talleres in datos.items():
            f_main.write(f"## 🏫 [{curso.replace('_', ' ')}](./{curso}/README.md)\n")
            os.makedirs(curso, exist_ok=True)
            
            # Generar README del Curso
            ruta_readme_curso = os.path.join(curso, "README.md")
            with open(ruta_readme_curso, "w", encoding="utf-8") as f_curso:
                f_curso.write(f"# Talleres de {curso.replace('_', ' ')}\n\n")
                
                for t_id in sorted(talleres.keys(), key=lambda x: int(x.split('_')[1])):
                    f_curso.write(f"### 📝 {t_id.replace('_', ' ')} (Asignado: {talleres[t_id]['fecha']})\n")
                    
                    sub = talleres[t_id].get("subtitulo", "")
                    inst = talleres[t_id].get("instruccion", "")
                    
                    ruta_taller = os.path.join(curso, t_id)
                    os.makedirs(ruta_taller, exist_ok=True)
                    
                    for tema_id, enunciados in talleres[t_id]["temas"].items():
                        nombre_archivo = f"{tema_id}.md"
                        ruta_archivo_md = os.path.join(ruta_taller, nombre_archivo)
                        
                        with open(ruta_archivo_md, "w", encoding="utf-8") as f_tema:
                            f_tema.write(f"# {curso.replace('_', ' ')}\n")
                            f_tema.write(f"## {t_id.replace('_', ' ')}: {sub}\n\n")
                            
                            if inst:
                                f_tema.write(f"### 🛠️ Instrucciones Previas\n{inst}\n\n")
                            
                            f_tema.write(f"--- \n### 👤 Asignación: {tema_id.replace('_', ' ')}\n")
                            f_tema.write("| # | Enunciado |\n|---|---|\n")
                            for i, texto in enumerate(enunciados, 1):
                                f_tema.write(f"| {i} | {texto} |\n")
                            f_tema.write(f"\n\n[⬅️ Volver al curso](../README.md)")
                        
                        f_curso.write(f"- [{tema_id.replace('_', ' ')}](./{t_id}/{nombre_archivo})\n")
                    f_curso.write("\n---\n")

# --- EJECUCIÓN ---
if __name__ == "__main__":
    df_semana = pd.DataFrame({
        'Curso': ['Big_Data'] * 30,
        'Taller': [1] * 30, 
        'Tema': sorted([f"Grupo {i}" for i in range(1, 11)] * 3),
        'Enunciado': [f"Analizar dataset fila {i}" for i in range(1, 31)]
    })
    
    sub_t = "Taller 1. Librería Numpy"
    inst_p = """Para realizar este taller, asegúrate de tener instalada las librerías numpy y calificar. \n\n
    \n
    #!pip install calificar
    \n
    \n
    #Librerias para el Taller \n
    import calificar as cr \n
    import numpy as np \n
    Taller1=cr.taller('1026',1, 'taller1BD2026i',6) \n
    \n
    Se cambia '1026' por su código estudiantil, si son dos se separa por ;, así: '1026;1027' \n
    Se cambia 1 por el Número de su Grupo asignado. \n
    \n
    """

actualizar_sistema_talleres(df_semana, subtitulo=sub_t, instruccion_principal=inst_p)


