# -*- coding: utf-8 -*-

import requests
import numpy as np
import pandas as pd
import inspect
import hashlib 
import sys


class taller:
    def __init__(self, integrante, grupo, taller, cant_respuestas=1, curso='0'):
        # Datos Inicialess
        self.integrante = integrante
        self.grupo = grupo
        self.taller = taller
        self.curso = curso
        self.resp=np.zeros(cant_respuestas,'U256') #No Modificar
    
    def respuestas(self, indice, valor):
        try:
            self.resp[indice] = valor
            print(f"🔢 La respuesta {indice} se actualizó a {valor}.")
            
        except IndexError:
            print(f"❌ Error: El índice {indice} está fuera de rango.")  
    
    def _preparar_respuestas(self):
        
        if hasattr(self.resp, 'tolist'): # Si es un array de numpy
            return ';'.join(map(str, self.resp.tolist()))
        elif isinstance(self.resp, list): # Si es una lista normal
            return ';'.join(map(str, self.resp))
        return str(self.resp)

    def calificar(self):
        respuestas_str = self._preparar_respuestas()
        datos = {
            'Integrantes': self.integrante, 
            'Grupo': self.grupo,
            'Curso': self.curso,
            'Respuestas': respuestas_str, 
            'python': 1
        }
        try:
            url = f'https://www.economiafinanciera.com.co/indexdes.php?app=excel&modulo=taller&accion=respuestas&Actividad={self.taller}'
            resp = requests.post(url, data=datos)
            partes = resp.text.split("|")
            if len(partes) >= 3:
                return print(f"🔢 Validación de Puntos: {partes[0]} \n Nota: {partes[1]} \n Mensaje: {partes[2][1:]}")
            else:
                print(f"Respuesta recibida: {partes[0]}")
                
        except Exception as e:
            return print(f"❌ Error en calificación: {str(e)}")

    def validar(self):
        respuestas_str = self._preparar_respuestas()
        datos = {
            'Integrantes': self.integrante, 
            'Grupo': self.grupo,
            'Curso': self.curso,
            'Respuestas': respuestas_str, 
            'python': 1
        }
        try:
            url = f'https://www.economiafinanciera.com.co/indexdes.php?app=excel&modulo=taller&accion=respuestas&Actividad={self.taller}'
            resp = requests.post(url, data=datos)
            return resp.text.split("|")[0].split(";")
        except Exception as e:
            return f"❌ Error en validación: {str(e)}"


class evafunciones:
    def __init__(self, url_repo, num_tema):
        self.url = url_repo
        self.num_tema = f"tema_{num_tema}"
        self.respuestas = self._cargar_respuestas()

    def _cargar_respuestas(self):
        try:
            response = requests.get(self.url)
            return response.json()
        except Exception as e:
            print(f"❌ Error al cargar el JSON: {e}")
            return None

    def validar(self, nombre_funcion):
        if not self.respuestas:
            return "Error de conexión"

        tema_data = self.respuestas.get(self.num_tema)
        datos_reto = tema_data.get(nombre_funcion)
        inputs_raw = datos_reto['inputs']
        esperado_raw = datos_reto['expected']
        codigo_exito = datos_reto['codigo_oculto']

        # 1. RECONSTRUIR INPUTS (Detección de Fecha/Periodo)
        args_para_estudiante = []
        for val in inputs_raw.values():
            if isinstance(val, dict):
                df_input = pd.DataFrame(val)
                # Buscamos columnas temporales
                cols_t = [c for c in df_input.columns if c.lower() in ['fecha', 'periodo'] or 'fecha' in c.lower()]
                if cols_t:
                    df_input[cols_t[0]] = pd.to_datetime(df_input[cols_t[0]])
                    df_input.set_index(cols_t[0], inplace=True)
                    df_input.index.name = 'Fecha'
                args_para_estudiante.append(df_input)
            else:
                args_para_estudiante.append(val)

        # 2. EJECUTAR FUNCIÓN DEL ESTUDIANTE
        try:
            import __main__
            func = getattr(__main__, nombre_funcion)
            resultado_estudiante = func(*args_para_estudiante)
            
            # 3. VALIDACIÓN ESPECIAL PARA DATAFRAMES
            if isinstance(resultado_estudiante, pd.DataFrame):
                df_esperado = pd.DataFrame(esperado_raw)
                
                # Normalizar fechas en el esperado si existen
                cols_e = [c for c in df_esperado.columns if c.lower() in ['fecha', 'periodo'] or 'fecha' in c.lower()]
                if cols_e:
                    df_esperado[cols_e[0]] = pd.to_datetime(df_esperado[cols_e[0]])
                    df_esperado.set_index(cols_e[0], inplace=True)
                    df_esperado.index.name = 'Fecha'

                # --- ELIMINAR ERROR DE ÍNDICES Y SHAPE ---
                # Forzamos al esperado a tener el MISMO índice que el alumno para comparar solo DATA
                if len(df_esperado) == len(resultado_estudiante):
                    df_esperado.index = resultado_estudiante.index
                
                pd.testing.assert_frame_equal(
                    resultado_estudiante, 
                    df_esperado, 
                    check_dtype=False,
                    check_column_type=False,
                    check_like=True 
                )
                print(f"✅ ¡Correcto! Código: {codigo_exito}")
                return codigo_exito

            # VALIDACIÓN PARA ESCALARES (reporte_pares)
            elif isinstance(resultado_estudiante, (int, float, np.number)):
                if np.isclose(resultado_estudiante, float(esperado_raw)):
                    print(f"✅ ¡Correcto! Código: {codigo_exito}")
                    return codigo_exito

        except AssertionError as e:
            print(f"⚠️ Error: Los datos no coinciden.\nℹ️ Detalle: {e}")
        except Exception as e:
            print(f"⚠️ Error inesperado: {e}")
        
        return None