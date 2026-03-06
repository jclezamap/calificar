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
    def __init__(self, url_base, num_tema):
        self.url = url_base.rstrip('/') + '/respuestas.json'
        self.num_tema = f"tema_{num_tema}"
        self.respuestas = self._cargar_respuestas()

    def _cargar_respuestas(self):
        try:
            raw_url = self.url.replace("github.com", "raw.githubusercontent.com").replace("/blob/", "/")
            response = requests.get(raw_url)
            return response.json()
        except Exception as e:
            print(f"❌ Error al cargar el JSON: {e}")
            return None

    def validar(self, nombre_funcion):
        if not self.respuestas: return None
        
        tema_data = self.respuestas.get(self.num_tema)
        reto = tema_data.get(nombre_funcion)
        if not reto: return None

        meta = reto.get('meta', {})
        inputs_raw = reto['inputs']
        esperado_raw = reto['expected']
        codigo_exito = reto['codigo_oculto']

        # 1. PREPARAR INPUTS
        args_est = []
        for val in inputs_raw.values():
            if isinstance(val, dict):
                df_in = pd.DataFrame(val)
                if meta.get('index_col'):
                    col_idx = meta['index_col']
                    if meta.get('is_datetime'):
                        df_in[col_idx] = pd.to_datetime(df_in[col_idx])
                    df_in.set_index(col_idx, inplace=True)
                args_est.append(df_in)
            else:
                args_est.append(val)

        # 2. EJECUCIÓN Y VALIDACIÓN
        try:
            import __main__
            func = getattr(__main__, nombre_funcion)
            res_est = func(*args_est)
            
            # --- CASO A: ESCALARES (Números simples) ---
            if meta.get('type') == 'scalar' or isinstance(res_est, (int, float, np.number)):
                if np.isclose(float(res_est), float(esperado_raw)):
                    print(f"✅ ¡Correcto! Código: {codigo_exito}")
                    return codigo_exito

            # --- CASO B: SERIES ---
            elif isinstance(res_est, pd.Series):
                ser_esp = pd.Series(esperado_raw)
                # Sincronizar índice si es necesario
                if len(ser_esp) == len(res_est):
                    ser_esp.index = res_est.index
                
                pd.testing.assert_series_equal(res_est, ser_esp, check_dtype=False, check_names=False)
                print(f"✅ ¡Correcto! Código: {codigo_exito}")
                return codigo_exito

            # --- CASO C: DATAFRAMES ---
            elif isinstance(res_est, pd.DataFrame):
                df_esp = pd.DataFrame(esperado_raw)
                if meta.get('index_col') and len(df_esp) == len(res_est):
                    df_esp.index = res_est.index

                pd.testing.assert_frame_equal(res_est, df_esp, check_dtype=False, check_like=True)
                print(f"✅ ¡Correcto! Código: {codigo_exito}")
                return codigo_exito

        except Exception as e:
            print(f"⚠️ Error en '{nombre_funcion}': {e}")
        return None