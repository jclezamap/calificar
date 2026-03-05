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
        self.url_base = url_base
        self.num_tema = f"tema_{num_tema}"
        self.respuestas = self._cargar_respuestas()

    def _cargar_respuestas(self):
        try:
            # Se descarga el JSON de respuestas del profesor
            r = requests.get(f"{self.url_base}/respuestas.json", timeout=10)
            r.raise_for_status() 
            return r.json()
        except Exception as e:
            print(f"❌ Error al cargar respuestas: {e}")
            return None

    def _generar_verificador(self, n_secreto, salt="2026i"):
        # Genera el código hash final para el estudiante
        hash_obj = hashlib.sha256(f"{n_secreto}{salt}{self.num_tema}".encode())
        return hash_obj.hexdigest()[:8].upper()

    def obtener_funcion_estudiante(self, nombre_funcion):
        # Busca la función definida por el alumno en su entorno local
        frame = inspect.stack()[1]
        modulo = inspect.getmodule(frame[0])
        funcion = getattr(modulo, nombre_funcion, None)
        
        if funcion is None:
            main_mod = sys.modules.get('__main__')
            funcion = getattr(main_mod, nombre_funcion, None)
            
        return funcion

    def validar(self, nombre_funcion):
        if not self.respuestas:
            print("❌ No hay respuestas cargadas.")
            return

        tema_data = self.respuestas.get(self.num_tema)
        if not tema_data:
            print(f"❌ No existe el {self.num_tema} en el JSON.")
            return

        datos_reto = tema_data.get(nombre_funcion)
        if not datos_reto:
            print(f"❌ El ejercicio '{nombre_funcion}' no existe para este tema.")
            return

        inputs_del_reto = datos_reto['inputs']
        esperado_raw = datos_reto['expected']
        codigo_base = datos_reto.get('codigo_oculto', '0000')

        # --- AJUSTE: CONVERSIÓN Y EXTRACCIÓN POR POSICIÓN ---
        lista_argumentos = []
        for valor in inputs_del_reto.values():
            if isinstance(valor, dict):
                # Convertimos el diccionario del JSON en un DataFrame real
                lista_argumentos.append(pd.DataFrame(valor))
            else:
                lista_argumentos.append(valor)
        # ----------------------------------------------------

        funcion_estudiante = self.obtener_funcion_estudiante(nombre_funcion)
         
        if not funcion_estudiante:
            print(f"❌ No se encontró la función '{nombre_funcion}' definida.")
            return
        
        try:
            # --- CAMBIO CLAVE ---
            # Pasamos los argumentos por POSICIÓN (*lista_argumentos)
            # Esto ignora si el alumno llamó al parámetro 'df', 'df_retos' o 'x'
            resultado_estudiante = funcion_estudiante(*lista_argumentos)
            
            es_correcto = False

            # Validación de DataFrames
            if isinstance(resultado_estudiante, pd.DataFrame):
                df_esperado = pd.DataFrame(esperado_raw)
                pd.testing.assert_frame_equal(
                    resultado_estudiante, 
                    df_esperado, 
                    check_dtype=False, 
                    check_like=True,    
                    check_exact=False,  
                    atol=1e-5           
                )
                es_correcto = True
            
            # Validación de Series
            elif isinstance(resultado_estudiante, pd.Series):
                serie_esperada = pd.Series(esperado_raw)
                pd.testing.assert_series_equal(resultado_estudiante, serie_esperada, check_dtype=False)
                es_correcto = True
                
            # Validación de escalares (números)
            else:
                es_correcto = np.allclose(resultado_estudiante, esperado_raw, atol=1e-5)

            if es_correcto:
                codigo_final = self._generar_verificador(codigo_base)
                print(f"✅ ¡Validación exitosa para '{nombre_funcion}'!")
                print(f"🔢 TU CÓDIGO DE ÉXITO: {codigo_final}")
                return codigo_final
                
        except AssertionError:
            print(f"❌ El resultado de '{nombre_funcion}' no coincide con lo esperado.")
        except TypeError as e:
            print(f"⚠️ Error de argumentos: Revisa que la función reciba el número correcto de parámetros.")
            print(f"ℹ️ Detalle: {e}")
        except Exception as e:
            print(f"⚠️ Error al ejecutar la función: {type(e).__name__}: {e}")