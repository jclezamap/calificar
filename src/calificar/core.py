# -*- coding: utf-8 -*-

import requests
import numpy as np
import pandas as pd
import inspect
import hashlib
import sys
import os
import json
from html import escape as _esc


# =====================================================================
#  Utilidades de presentación (las usan taller y evacolab)
# =====================================================================
_VERDE = "#10b981"
_ROJO = "#ef4444"
_AMBAR = "#f59e0b"
_AZUL = "#1e3a8a"
_TARJETA = ("font-family:'Segoe UI',Arial,sans-serif;max-width:640px;"
            "background:#ffffff;color:#1c1917;border:1px solid #e7e5e4;"
            "border-radius:12px;padding:16px")


def _mostrar_html(contenido, texto_alterno=""):
    """Muestra HTML en Colab/Jupyter. Fuera de un notebook imprime texto plano."""
    try:
        from IPython import get_ipython
        from IPython.display import HTML, display
        if get_ipython() is not None:
            display(HTML(contenido))
            return
    except ImportError:
        pass
    print(texto_alterno or contenido)


def _etiqueta(texto, color, ancho=48):
    """Recuadro de color al estilo de 'Validación de las Respuestas' de la web."""
    return ("<span style='display:inline-block;min-width:%dpx;padding:5px 10px;"
            "border-radius:6px;background:%s;color:#ffffff;font-weight:700;"
            "text-align:center;border:1px solid rgba(0,0,0,.15)'>%s</span>"
            % (ancho, color, _esc(str(texto))))


# =====================================================================
#  Talleres con respuestas (economiafinanciera.com.co)
# =====================================================================
class taller:
    def __init__(self, integrante, grupo, taller, cant_respuestas=1, curso='0'):
        # Datos Iniciales
        self.integrante = integrante
        self.grupo = grupo
        self.taller = taller
        self.curso = curso
        self.resp = np.zeros(cant_respuestas, 'U256')  # No Modificar
        # Al crear el taller se muestra solo la nota y el mensaje (sin detalle por pregunta)
        self._resumen_inicial()

    def respuestas(self, indice, valor):
        try:
            self.resp[indice] = valor
            print(f"🔢 La respuesta {indice} se actualizó a {valor}.")
        except IndexError:
            print(f"❌ Error: El índice {indice} está fuera de rango.")

    def _preparar_respuestas(self):
        if hasattr(self.resp, 'tolist'):  # Si es un array de numpy
            return ';'.join(map(str, self.resp.tolist()))
        elif isinstance(self.resp, list):  # Si es una lista normal
            return ';'.join(map(str, self.resp))
        return str(self.resp)

    def _enviar(self, **extra):
        """Envía las respuestas al servidor y devuelve su respuesta separada por '|'."""
        datos = {
            'Integrantes': self.integrante,
            'Grupo': self.grupo,
            'Curso': self.curso,
            'Respuestas': self._preparar_respuestas(),
            'python': 1
        }
        datos.update(extra)
        url = f'https://www.economiafinanciera.com.co/index.php?app=excel&modulo=taller&accion=respuestas&Actividad={self.taller}'
        resp = requests.post(url, data=datos, timeout=60)
        return resp.text.split("|")

    @staticmethod
    def _leer(partes):
        """'1;0;0;| 0.6| Mensaje;' -> (['1','0','0'], '0.6', 'Mensaje')"""
        puntos = [p.strip() for p in partes[0].split(";") if p.strip()]
        nota = partes[1].strip()
        mensaje = partes[2][1:].strip().rstrip(";").strip()
        return puntos, nota, mensaje

    def _resumen_inicial(self):
        try:
            # 'inicio' le permite al servidor distinguir esta consulta de una calificación real
            partes = self._enviar(inicio=1)
            if len(partes) >= 3:
                _, nota, mensaje = self._leer(partes)
                self._mostrar_calificacion(nota, mensaje)
            else:
                print(f"Respuesta recibida: {partes[0]}")
        except Exception as e:
            print(f"❌ Error al conectar con el taller: {str(e)}")

    def calificar(self):
        try:
            partes = self._enviar()
            if len(partes) >= 3:
                puntos, nota, mensaje = self._leer(partes)
                self._mostrar_calificacion(nota, mensaje, puntos)
            else:
                print(f"Respuesta recibida: {partes[0]}")
        except Exception as e:
            print(f"❌ Error en calificación: {str(e)}")

    def _mostrar_calificacion(self, nota, mensaje, puntos=None):
        """Sin puntos: solo nota y mensaje. Con puntos: tabla vertical desde P0."""
        if puntos is None:
            html = """
<div style="%(tarjeta)s;display:inline-block;min-width:320px">
  <div style="font-weight:700;color:#374151">%(taller)s</div>
  <div style="font-size:28px;font-weight:700;color:%(azul)s;margin:8px 0 2px">Nota %(nota)s</div>
  <p style="margin:8px 0 0;font-size:13px;color:#57534e">%(mensaje)s</p>
</div>
""" % {"tarjeta": _TARJETA, "azul": _AZUL, "taller": _esc(str(self.taller)),
                "nota": _esc(nota), "mensaje": _esc(mensaje)}
            _mostrar_html(html, "Nota: %s\n%s" % (nota, mensaje))
            return

        filas, texto = [], []
        correctas = 0
        for i, p in enumerate(puntos):
            try:
                valor = float(p)
            except ValueError:
                valor = 0.0
            if valor >= 1:
                color, estado, icono = _VERDE, "Correcta", "✔"
                correctas += 1
            elif valor > 0:
                color, estado, icono = _AMBAR, "Parcial", "◐"
            else:
                color, estado, icono = _ROJO, "Incorrecta", "✘"

            enviada = str(self.resp[i]) if i < len(self.resp) else ""
            enviada = enviada if enviada.strip() else "—"

            filas.append(
                "<tr style='border-top:1px solid #f1f5f9'>"
                "<td style='padding:4px 8px'>%s</td>"
                "<td style='padding:4px 8px;color:#44403c'>%s</td>"
                "<td style='padding:4px 8px;color:%s;font-weight:600'>%s %s</td>"
                "</tr>" % (_etiqueta("P%d" % i, color), _esc(enviada), color, icono, estado)
            )
            texto.append("P%d  %-10s  %s" % (i, estado, enviada))

        html = """
<div style="%(tarjeta)s;display:inline-block;min-width:320px">
  <div style="font-weight:700;color:#374151">Validación de las respuestas</div>
  <div style="font-size:28px;font-weight:700;color:%(azul)s;margin:8px 0 2px">Nota %(nota)s</div>
  <div style="font-size:14px;color:#57534e">%(correctas)d de %(total)d preguntas correctas</div>
  <table style="border-collapse:collapse;margin-top:12px;font-size:14px">
    <thead><tr style="color:#57534e;text-align:left">
      <th style="padding:4px 8px">Pregunta</th>
      <th style="padding:4px 8px">Tu respuesta</th>
      <th style="padding:4px 8px">Resultado</th>
    </tr></thead>
    <tbody>%(filas)s</tbody>
  </table>
  <p style="margin:12px 0 0;font-size:13px;color:#57534e">%(mensaje)s</p>
</div>
""" % {
            "tarjeta": _TARJETA,
            "azul": _AZUL,
            "nota": _esc(nota),
            "correctas": correctas,
            "total": len(puntos),
            "filas": "".join(filas),
            "mensaje": _esc(mensaje),
        }
        alterno = "Nota: %s (%d de %d correctas)\n%s\n%s" % (
            nota, correctas, len(puntos), "\n".join(texto), mensaje)
        _mostrar_html(html, alterno)

    def validar(self):
        try:
            return self._enviar()[0].split(";")
        except Exception as e:
            return f"❌ Error en validación: {str(e)}"


# =====================================================================
#  Validación de notebooks de Colab contra la rúbrica (colab.economiafinanciera.com.co)
# =====================================================================
class evacolab:
    """Envía el notebook de Colab actual a la plataforma y muestra nota y rúbrica.

    Uso en Colab:
        ev = evacolab(codigo="1026", actividad=3)
        ev.validar()

    codigo: cédula o código estudiantil (debe estar en la lista del curso)
    actividad: id numérico o nombre de la actividad
    El resultado completo queda en ev.resultado por si se necesita.
    """
    SERVIDOR = "https://colab.economiafinanciera.com.co"

    def __init__(self, codigo, actividad, servidor=None, filename="colab.ipynb"):
        self.codigo = str(codigo).strip()
        self.actividad = actividad
        self.servidor = (servidor or os.environ.get("VALIDARCOLAB_URL")
                         or self.SERVIDOR).rstrip("/")
        self.filename = filename
        self.resultado = None

    @staticmethod
    def _notebook_actual():
        try:
            from google.colab import _message  # type: ignore
            data = _message.blocking_request("get_ipynb", request="", timeout_sec=30)
            if data and data.get("ipynb"):
                return data["ipynb"]
        except Exception:
            pass
        for nombre in os.listdir("."):
            if nombre.endswith(".ipynb") and not nombre.startswith("."):
                with open(nombre, "r", encoding="utf-8") as f:
                    return json.load(f)
        raise RuntimeError("No se encontró el notebook. Ejecuta esto desde Google Colab.")

    def validar(self):
        try:
            nb = self._notebook_actual()
        except RuntimeError as e:
            print(f"❌ {e}")
            return

        payload = json.dumps({
            "identificacion": self.codigo,  # clave que espera la API del servidor
            "actividad": self.actividad,
            "filename": self.filename,
            "notebook": nb,
        }).encode("utf-8")

        try:
            r = requests.post(self.servidor + "/api/colab", data=payload,
                              headers={"Content-Type": "application/json"}, timeout=60)
        except Exception as e:
            print(f"❌ No se pudo conectar con la plataforma: {e}")
            return

        try:
            data = r.json()
        except ValueError:
            print(f"❌ El servidor respondió {r.status_code}: {r.text[:300]}")
            return

        if data.get("status") == "error":
            print(f"❌ {data.get('message') or 'Error al validar'}")
            return

        self.resultado = data
        _mostrar_html(self._html(data), self._texto(data))
        # Sin return: así Colab no imprime el diccionario debajo de la tarjeta.

    @staticmethod
    def _html(data):
        filas = []
        for d in data.get("detalle") or []:
            cumple = str(d.get("cumple") or "")
            filas.append(
                "<tr style='border-top:1px solid #f1f5f9'>"
                "<td style='padding:4px 8px;color:#57534e'>%s</td>"
                "<td style='padding:4px 8px'>%s</td>"
                "<td style='padding:4px 8px;text-align:center'>%s</td>"
                "</tr>" % (_esc(str(d.get("categoria") or "")),
                           _esc(str(d.get("requisito") or "")),
                           _etiqueta(cumple, _VERDE if cumple == "SI" else _ROJO, 40))
            )

        alerta = data.get("alertaCopia") or ""
        aviso = (
            "<p style='margin:10px 0;padding:8px 10px;background:#fffbeb;"
            "border:1px solid #fcd34d;border-radius:8px;color:#b45309'>"
            "<b>Posible copia (%s).</b> El docente verá el detalle.</p>" % _esc(str(alerta))
            if alerta else ""
        )

        obs = data.get("observaciones") or []
        obs_html = (
            "<ul style='margin:8px 0;padding-left:18px;font-size:13px;color:#57534e'>"
            + "".join("<li>%s</li>" % _esc(str(o)) for o in obs) + "</ul>"
            if obs else ""
        )

        ok = data.get("requisitosOk")
        total = data.get("requisitosTotal")
        resumen = ("%s de %s requisitos cumplidos (%.1f%%)"
                   % (ok, total, float(data.get("cumplimiento") or 0))
                   if ok is not None and total is not None
                   else "%.1f%% de cumplimiento" % float(data.get("cumplimiento") or 0))

        return """
<div style="%(tarjeta)s">
  <div style="font-weight:700;font-size:18px;color:%(azul)s">%(actividad)s</div>
  <div style="font-size:14px;color:#57534e">%(estudiante)s, %(identificacion)s</div>
  <div style="font-size:28px;font-weight:700;color:%(azul)s;margin:10px 0 2px">Nota %(nota).1f</div>
  <div style="font-size:14px;color:#57534e">%(resumen)s</div>
  %(aviso)s
  %(obs)s
  <table style="width:100%%;border-collapse:collapse;margin-top:12px;font-size:14px">
    <thead><tr style="color:#57534e;text-align:left">
      <th style="padding:4px 8px">Categoría</th>
      <th style="padding:4px 8px">Requisito</th>
      <th style="padding:4px 8px;text-align:center">Cumple</th>
    </tr></thead>
    <tbody>%(filas)s</tbody>
  </table>
</div>
""" % {
            "tarjeta": _TARJETA,
            "azul": _AZUL,
            "actividad": _esc(str(data.get("actividad") or "")),
            "estudiante": _esc(str(data.get("estudiante") or "")),
            "identificacion": _esc(str(data.get("identificacion") or "")),
            "nota": float(data.get("nota") or 0),
            "resumen": _esc(resumen),
            "aviso": aviso,
            "obs": obs_html,
            "filas": "".join(filas),
        }

    @staticmethod
    def _texto(data):
        lineas = ["%s - %s (%s)" % (data.get("actividad"), data.get("estudiante"),
                                     data.get("identificacion")),
                  "Nota %.1f" % float(data.get("nota") or 0)]
        if data.get("alertaCopia"):
            lineas.append("Posible copia (%s)" % data.get("alertaCopia"))
        for d in data.get("detalle") or []:
            lineas.append("  [%s] %s: %s" % (d.get("cumple"), d.get("categoria"), d.get("requisito")))
        return "\n".join(lineas)


# =====================================================================
#  Evaluación de funciones con respuestas en GitHub
# =====================================================================
class evafunciones:
    def __init__(self, url_base, num_tema):
        self.url = url_base.rstrip('/') + '/respuestas.json'
        self.num_tema = f"tema_{num_tema}"
        self.salt_seguridad = "2026i"  # Debe coincidir con tu script de profesor
        self.respuestas = self._cargar_respuestas()

    def _cargar_respuestas(self):
        try:
            # 1. LIMPIEZA TOTAL DE URL (Inmune a Colab)
            # Pasamos de 'github.com' a 'raw.githubusercontent.com'
            # Y eliminamos los segmentos que causan el error de HTML
            raw_url = self.url.replace("github.com", "raw.githubusercontent.com") \
                              .replace("/blob/", "/") \
                              .replace("/tree/", "/") \
                              .replace("/refs/heads/", "/") \
                              .replace("/refs/branch/", "/")

            # 2. PETICIÓN CON CABECERAS DE TEXTO PLANO
            # Forzamos a GitHub a entender que queremos el contenido crudo
            headers = {'Accept': 'application/json'}
            response = requests.get(raw_url, headers=headers)

            # 3. VERIFICACIÓN DE ESTADO
            if response.status_code != 200:
                print(f"❌ Error {response.status_code}: No se pudo acceder al JSON.")
                print(f"🔗 Ruta fallida: {raw_url}")
                return None

            # 4. PRUEBA DE CONTENIDO (Antes de convertir)
            contenido = response.text.strip()
            if not contenido.startswith("{"):
                print("❌ Error: El servidor no devolvió un JSON válido.")
                print(f"📝 Inicio del contenido recibido: {contenido[:50]}")
                return None

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
        base_code = reto['codigo_oculto']  # El número base (ej: 7001)

        # 1. RECONSTRUCCIÓN DE INPUTS
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

        # 2. VALIDACIÓN TÉCNICA
        exito = False
        try:
            import __main__
            func = getattr(__main__, nombre_funcion)
            res_est = func(*args_est)

            # --- Validación Escalar ---
            if meta.get('type') == 'scalar' or isinstance(res_est, (int, float, np.number)):
                if np.isclose(float(res_est), float(esperado_raw)):
                    exito = True

            # --- Validación Serie ---
            elif isinstance(res_est, pd.Series):
                ser_esp = pd.Series(esperado_raw)
                if len(ser_esp) == len(res_est):
                    ser_esp.index = res_est.index
                pd.testing.assert_series_equal(res_est, ser_esp, check_dtype=False, check_names=False)
                exito = True

            # --- Validación DataFrame ---
            elif isinstance(res_est, pd.DataFrame):
                df_esp = pd.DataFrame(esperado_raw)
                if meta.get('index_col') and len(df_esp) == len(res_est):
                    df_esp.index = res_est.index
                pd.testing.assert_frame_equal(res_est, df_esp, check_dtype=False, check_like=True)
                exito = True
            # --- Validación de modelos ----
            elif hasattr(res_est, 'predict') and meta.get('type') == 'model_validation':
                # res_est es el (modelo, scaler) retornado por el alumno
                modelo, scaler = res_est

                # Reconstruimos X_prueba desde el JSON
                X_prueba = inputs_raw.get('X_prueba')

                # Predecimos y comparamos
                X_proc = scaler.transform(X_prueba)
                preds = modelo.predict(X_proc).tolist()

                # Comparamos con esperado_raw (predicciones)
                if preds == esperado_raw.get('predicciones'):
                    exito = True
            # 3. GENERACIÓN DEL HASH (Solo si pasó la validación)
            if exito:
                # Aplicamos tu fórmula exacta
                hash_estudiante = hashlib.sha256(
                    f"{base_code}{self.salt_seguridad}{self.num_tema}".encode()
                ).hexdigest()[:8].upper()

                print(f"✅ ¡Correcto! Código de éxito: {hash_estudiante}")
                return hash_estudiante

        except Exception as e:
            # Si hay error en la comparación, no se genera el hash
            pass

        return None