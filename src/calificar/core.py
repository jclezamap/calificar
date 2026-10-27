# -*- coding: utf-8 -*-

import requests
import numpy as np
import pandas as pd
import inspect
import hashlib
import math
import sys
import os
import json
from html import escape as _esc


SITIO = os.environ.get("CALIFICAR_SITIO", "https://economiafinanciera.com.co").rstrip("/")
COLAB = os.environ.get("VALIDARCOLAB_URL", "https://colab.economiafinanciera.com.co").rstrip("/")
TIEMPO = 60  # segundos de espera por respuesta


# =====================================================================
#  Utilidades de presentación (las usan taller, parcial y evacolab)
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


def _formatear(valor):
    """La respuesta como la manda la macro de Excel.

    Los números van con 15 cifras significativas, como los muestra Excel.
    Antes viajaban con todas las cifras de Python (0.1 + 0.2 llegaba como
    0.30000000000000004) y no coincidían con la respuesta guardada.
    """
    if valor is None:
        return ""
    if isinstance(valor, (bool, np.bool_)):
        return str(bool(valor))
    if isinstance(valor, (np.integer,)):
        return str(int(valor))
    if isinstance(valor, (float, np.floating)):
        v = float(valor)
        if math.isnan(v) or math.isinf(v):
            return str(v)
        if v.is_integer() and abs(v) < 1e15:
            return str(int(v))
        return format(v, ".15g")
    return str(valor).strip()


def _aviso_html(texto):
    """¿Respondió el hosting con una página (bloqueo, captcha) en vez del sistema?"""
    t = (texto or "").lstrip().lower()
    return t.startswith("<!doctype") or t.startswith("<html") or "<body" in t[:500]


def _post(url, datos):
    """POST al sistema de notas. Devuelve el texto o lanza RuntimeError legible."""
    try:
        resp = requests.post(url, data=datos, timeout=TIEMPO,
                             headers={"User-Agent": "calificar-python"})
    except requests.exceptions.Timeout:
        raise RuntimeError("El servidor tardó demasiado en responder. Intenta de nuevo.")
    except requests.exceptions.RequestException:
        raise RuntimeError("No hay conexión con economiafinanciera.com.co.")
    texto = resp.text or ""
    if resp.status_code >= 500 or _aviso_html(texto):
        raise RuntimeError("El servidor no pudo atender la calificación (código %s). "
                           "Tu nota anterior no cambió; intenta en un momento." % resp.status_code)
    return texto


def _tabla_calificacion(titulo, nota, mensaje, puntos, enviadas, subtitulo=""):
    """Tarjeta con nota, conteo y tabla vertical desde P0 (igual que la web)."""
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

        enviada = str(enviadas[i]) if i < len(enviadas) else ""
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
  <div style="font-weight:700;color:#374151">%(titulo)s</div>
  %(subtitulo)s
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
        "titulo": _esc(titulo),
        "subtitulo": ("<div style='font-size:13px;color:#57534e'>%s</div>" % _esc(subtitulo)) if subtitulo else "",
        "nota": _esc(nota),
        "correctas": correctas,
        "total": len(puntos),
        "filas": "".join(filas),
        "mensaje": _esc(mensaje),
    }
    alterno = "Nota: %s (%d de %d correctas)\n%s\n%s" % (
        nota, correctas, len(puntos), "\n".join(texto), mensaje)
    _mostrar_html(html, alterno)


def _resumen(titulo, nota, mensaje, subtitulo=""):
    html = """
<div style="%(tarjeta)s;display:inline-block;min-width:320px">
  <div style="font-weight:700;color:#374151">%(titulo)s</div>
  %(subtitulo)s
  <div style="font-size:28px;font-weight:700;color:%(azul)s;margin:8px 0 2px">Nota %(nota)s</div>
  <p style="margin:8px 0 0;font-size:13px;color:#57534e">%(mensaje)s</p>
</div>
""" % {"tarjeta": _TARJETA, "azul": _AZUL, "titulo": _esc(str(titulo)),
       "subtitulo": ("<div style='font-size:14px;font-weight:600;color:%s'>%s</div>" % (_AZUL, _esc(subtitulo))) if subtitulo else "",
       "nota": _esc(nota), "mensaje": _esc(mensaje)}
    _mostrar_html(html, "%s\n%sNota: %s\n%s" % (titulo, (subtitulo + "\n") if subtitulo else "", nota, mensaje))


class _ConRespuestas:
    """Lo común a taller y parcial: el vector de respuestas."""

    def respuestas(self, indice, valor):
        try:
            self.resp[indice] = _formatear(valor)
            print(f"🔢 La respuesta {indice} se actualizó a {self.resp[indice]}.")
        except IndexError:
            print(f"❌ Error: El índice {indice} está fuera de rango (hay {len(self.resp)} preguntas: 0 a {len(self.resp) - 1}).")

    def _preparar_respuestas(self):
        if hasattr(self.resp, 'tolist'):  # Si es un array de numpy
            return ';'.join(_formatear(x) if not isinstance(x, str) else x for x in self.resp.tolist())
        elif isinstance(self.resp, list):  # Si es una lista normal
            return ';'.join(map(_formatear, self.resp))
        return str(self.resp)


# =====================================================================
#  Talleres con respuestas (economiafinanciera.com.co)
# =====================================================================
class taller(_ConRespuestas):
    def __init__(self, integrante, grupo, taller, cant_respuestas=1, curso='0'):
        # Datos Iniciales
        self.integrante = str(integrante).strip()
        self.grupo = grupo
        self.taller = str(taller).strip()
        self.curso = curso
        self.resp = np.zeros(cant_respuestas, 'U256')  # No Modificar
        self.resp[:] = ""
        # Al crear el taller se muestra solo la nota y el mensaje (sin detalle por pregunta)
        self._resumen_inicial()

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
        url = f'{SITIO}/index.php?app=excel&modulo=taller&accion=respuestas&Actividad={self.taller}'
        return _post(url, datos).split("|")

    @staticmethod
    def _leer(partes):
        """'1;0;0;| 0.6| Mensaje;' -> (['1','0','0'], '0.6', 'Mensaje')"""
        puntos = [p.strip() for p in partes[0].split(";") if p.strip()]
        nota = partes[1].strip()
        mensaje = partes[2][1:].strip().rstrip(";").strip() if len(partes) > 2 else ""
        return puntos, nota, mensaje

    def _resumen_inicial(self):
        try:
            # 'inicio' le permite al servidor distinguir esta consulta de una calificación real
            partes = self._enviar(inicio=1)
            if len(partes) >= 3:
                _, nota, mensaje = self._leer(partes)
                self._mostrar_calificacion(nota, mensaje)
            else:
                print(f"Respuesta recibida: {partes[0][:300]}")
        except Exception as e:
            print(f"❌ Error al conectar con el taller: {str(e)}")

    def calificar(self):
        try:
            partes = self._enviar()
            if len(partes) >= 3:
                puntos, nota, mensaje = self._leer(partes)
                self._mostrar_calificacion(nota, mensaje, puntos)
            else:
                print(f"Respuesta recibida: {partes[0][:300]}")
        except Exception as e:
            print(f"❌ Error en calificación: {str(e)}")

    def _mostrar_calificacion(self, nota, mensaje, puntos=None):
        """Sin puntos: solo nota y mensaje. Con puntos: tabla vertical desde P0."""
        if puntos is None:
            _resumen(self.taller, nota, mensaje)
            return
        _tabla_calificacion("Validación de las respuestas", nota, mensaje, puntos, list(self.resp))

    def validar(self):
        try:
            return self._enviar()[0].split(";")
        except Exception as e:
            return f"❌ Error en validación: {str(e)}"


# =====================================================================
#  Parciales (economiafinanciera.com.co) — igual que el libro de Excel
# =====================================================================
class parcial(_ConRespuestas):
    """Parcial de Economía Financiera presentado desde Python.

    Uso:
        p = cr.parcial('CODIGO', ID_PARCIAL, 'CLAVE', NUM_PREGUNTAS)
        p.respuestas(0, valor)
        p.calificar()

    Igual que el libro de Excel: al crearlo, Economía Financiera te asigna el
    tema (queda en p.tema) y ese primer envío cuenta como intento. Cada
    calificar() es un intento; se respetan apertura, cierre e intentos, y
    cuenta la nota más alta.
    """

    def __init__(self, integrante, id_parcial, clave, cant_respuestas=1):
        self.integrante = str(integrante).strip()
        self.id_parcial = str(id_parcial).strip()
        self.clave = str(clave).strip()
        self.resp = np.zeros(cant_respuestas, 'U256')
        self.resp[:] = ""
        self.tema = None
        self.nombre = "Parcial %s" % self.id_parcial
        self.cierre = None
        self._abrir()

    def _enviar(self, respuestas):
        datos = {
            "ID": self.id_parcial,
            "clave": self.clave,
            "Integrantes": self.integrante,
            "Respuestas": respuestas,
        }
        texto = _post(f"{SITIO}/index.php?app=parcial&modulo=calificar", datos).strip()
        partes = texto.split("|")
        if len(partes) < 8:
            # El sistema responde un solo mensaje cuando no califica
            # (clave, apertura, plazo, identificación, intentos agotados).
            raise RuntimeError(texto[:300] or "El sistema no respondió.")
        # Nombre | Mensaje final | Tema | Fecha actual | Fecha final | Puntos | Nota | Observaciones
        self.nombre = partes[0].strip() or self.nombre
        self.tema = partes[2].strip() or self.tema
        self.cierre = partes[4].strip() or self.cierre
        puntos = [p.strip() for p in partes[5].split(";") if p.strip()]
        return puntos, partes[6].strip(), "|".join(partes[7:]).strip().rstrip(";").strip()

    def _abrir(self):
        try:
            _, nota, mensaje = self._enviar("")
            _resumen(self.nombre, nota, mensaje, subtitulo="Tema %s" % self.tema if self.tema else "")
        except Exception as e:
            print(f"❌ {str(e)}")

    def calificar(self):
        try:
            puntos, nota, mensaje = self._enviar(self._preparar_respuestas())
            _tabla_calificacion(self.nombre, nota, mensaje, puntos, list(self.resp),
                                subtitulo="Tema %s" % self.tema if self.tema else "")
        except Exception as e:
            print(f"❌ {str(e)}")


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
    SERVIDOR = COLAB

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
                              headers={"Content-Type": "application/json"}, timeout=TIEMPO)
        except Exception as e:
            print(f"❌ No se pudo conectar con la plataforma: {e}")
            return

        try:
            data = r.json()
        except ValueError:
            print(f"❌ El servidor respondió {r.status_code}.")
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
#  Evaluación de funciones
# =====================================================================
def _armar_entradas(inputs_raw, meta):
    """Reconstruye los argumentos de la función (DataFrames incluidos)."""
    args = []
    for val in inputs_raw.values():
        if isinstance(val, dict):
            df_in = pd.DataFrame(val)
            if meta.get('index_col'):
                col_idx = meta['index_col']
                if meta.get('is_datetime'):
                    df_in[col_idx] = pd.to_datetime(df_in[col_idx])
                df_in.set_index(col_idx, inplace=True)
            args.append(df_in)
        else:
            args.append(val)
    return args


def _a_json(v):
    """Valor de numpy/pandas → algo que JSON entiende (NaN → None)."""
    if isinstance(v, (np.bool_, bool)):
        return bool(v)
    if isinstance(v, np.integer):
        return int(v)
    if isinstance(v, (np.floating, float)):
        f = float(v)
        return None if math.isnan(f) else f
    if isinstance(v, (pd.Timestamp,)):
        return str(v)
    if isinstance(v, (list, tuple, np.ndarray)):
        return [_a_json(x) for x in list(v)]
    if isinstance(v, dict):
        return {str(k): _a_json(x) for k, x in v.items()}
    return v


def _empaquetar(res_est, meta, inputs_raw):
    """El resultado de la función del estudiante, listo para enviarlo."""
    if meta.get('type') == 'model_validation':
        modelo, scaler = res_est if isinstance(res_est, tuple) else (res_est, None)
        X = inputs_raw.get('X_prueba')
        X_proc = scaler.transform(X) if scaler is not None else X
        return {"tipo": "predicciones", "valores": _a_json(modelo.predict(X_proc).tolist())}
    if isinstance(res_est, pd.DataFrame):
        return {"tipo": "tabla", "columnas": [str(c) for c in res_est.columns],
                "datos": {str(c): _a_json(res_est[c].tolist()) for c in res_est.columns}}
    if isinstance(res_est, pd.Series):
        return {"tipo": "serie", "valores": _a_json(res_est.tolist())}
    if meta.get('type') == 'scalar' or isinstance(res_est, (int, float, bool, np.number, np.bool_)):
        return {"tipo": "escalar", "valor": _a_json(float(res_est))}
    return {"tipo": "otro", "valor": _a_json(res_est)}


class evafunciones:
    """Valida una función de Python y entrega el código de éxito.

    Nuevo (seguro):    Eva = cr.evafunciones('T2BD2026ii', G)
        El primer dato es el identificador del taller (el mismo de cr.taller).
        Los datos de prueba se piden a colab.economiafinanciera.com.co, tu
        función se ejecuta aquí y el resultado se compara en el servidor. La
        respuesta y el código nunca se publican.

    Anterior:          Eva = cr.evafunciones('https://github.com/...', G)
        Sigue funcionando para los talleres que ya están en GitHub.
    """

    def __init__(self, url_base, num_tema):
        self.num_tema = f"tema_{num_tema}"
        self.tema = num_tema
        ref = str(url_base).strip()
        self.en_servidor = not ref.lower().startswith(("http://", "https://")) and "github" not in ref.lower()
        if self.en_servidor:
            self.actividad = ref
            self.respuestas = None
        else:
            self.url = ref.rstrip('/') + '/respuestas.json'
            self.salt_seguridad = "2026i"  # Debe coincidir con tu script de profesor
            self.respuestas = self._cargar_respuestas()

    # ---------------- modo nuevo: el servidor compara ----------------
    def _validar_en_servidor(self, nombre_funcion):
        try:
            r = requests.get(COLAB + "/api/funciones", timeout=TIEMPO,
                             params={"actividad": self.actividad, "tema": self.tema, "funcion": nombre_funcion})
            info = r.json()
        except (requests.exceptions.RequestException, ValueError):
            print("❌ No se pudo conectar con colab.economiafinanciera.com.co.")
            return None
        if info.get("status") != "ok":
            print(f"❌ {info.get('message') or 'No se encontró la función.'}")
            return None

        meta = info.get("meta") or {}
        inputs_raw = info.get("inputs") or {}
        try:
            import __main__
            func = getattr(__main__, nombre_funcion)
        except AttributeError:
            print(f"❌ No encontré la función {nombre_funcion}. Ejecuta primero la celda donde la defines.")
            return None
        try:
            casos = info.get("casos")
            if casos:
                # Varias entradas de prueba: la función tiene que acertar todas.
                resultado = {"tipo": "casos", "valores": [
                    _empaquetar(func(*_armar_entradas(c, meta)), meta, c) for c in casos]}
            else:
                resultado = _empaquetar(func(*_armar_entradas(inputs_raw, meta)), meta, inputs_raw)
        except Exception as e:
            print(f"❌ Tu función {nombre_funcion} falló con los datos de prueba: {type(e).__name__}: {str(e)[:200]}")
            return None

        try:
            r = requests.post(COLAB + "/api/funciones/validar", timeout=TIEMPO, json={
                "actividad": self.actividad, "tema": self.tema,
                "funcion": nombre_funcion, "resultado": resultado,
            })
            data = r.json()
        except (requests.exceptions.RequestException, ValueError):
            print("❌ No se pudo conectar con colab.economiafinanciera.com.co.")
            return None
        if data.get("status") != "ok":
            print(f"❌ {data.get('message') or 'No se pudo validar.'}")
            return None
        if not data.get("correcto"):
            print(f"❌ {nombre_funcion} no da el resultado esperado"
                  + (" en todos los casos de prueba." if info.get("casos") else "."))
            return None
        print(f"✅ ¡Correcto! Código de éxito: {data['codigo']}")
        return data["codigo"]

    # ---------------- modo anterior: GitHub ----------------
    def _cargar_respuestas(self):
        try:
            # Pasamos de 'github.com' a 'raw.githubusercontent.com'
            raw_url = self.url.replace("github.com", "raw.githubusercontent.com") \
                              .replace("/blob/", "/") \
                              .replace("/tree/", "/") \
                              .replace("/refs/heads/", "/") \
                              .replace("/refs/branch/", "/")
            raw_url = raw_url.replace("raw.raw.githubusercontent.com", "raw.githubusercontent.com")
            response = requests.get(raw_url, headers={'Accept': 'application/json'}, timeout=TIEMPO)
            if response.status_code != 200:
                print(f"❌ Error {response.status_code}: No se pudo acceder al JSON.")
                return None
            contenido = response.text.strip()
            if not contenido.startswith("{"):
                print("❌ Error: El servidor no devolvió un JSON válido.")
                return None
            return response.json()
        except Exception as e:
            print(f"❌ Error al cargar el JSON: {e}")
            return None

    def validar(self, nombre_funcion):
        if self.en_servidor:
            return self._validar_en_servidor(nombre_funcion)
        if not self.respuestas:
            return None

        tema_data = self.respuestas.get(self.num_tema) or {}
        reto = tema_data.get(nombre_funcion)
        if not reto:
            return None

        meta = reto.get('meta', {})
        inputs_raw = reto['inputs']
        esperado_raw = reto['expected']
        base_code = reto['codigo_oculto']

        exito = False
        try:
            import __main__
            func = getattr(__main__, nombre_funcion)
            res_est = func(*_armar_entradas(inputs_raw, meta))

            if meta.get('type') == 'model_validation':
                modelo, scaler = res_est if isinstance(res_est, tuple) else (res_est, None)
                X_prueba = inputs_raw.get('X_prueba')
                X_proc = scaler.transform(X_prueba) if scaler is not None else X_prueba
                if modelo.predict(X_proc).tolist() == esperado_raw.get('predicciones'):
                    exito = True
            elif meta.get('type') == 'scalar' or isinstance(res_est, (int, float, np.number)):
                if np.isclose(float(res_est), float(esperado_raw)):
                    exito = True
            elif isinstance(res_est, pd.Series):
                ser_esp = pd.Series(esperado_raw)
                if len(ser_esp) == len(res_est):
                    ser_esp.index = res_est.index
                pd.testing.assert_series_equal(res_est, ser_esp, check_dtype=False, check_names=False)
                exito = True
            elif isinstance(res_est, pd.DataFrame):
                df_esp = pd.DataFrame(esperado_raw)
                if meta.get('index_col') and len(df_esp) == len(res_est):
                    df_esp.index = res_est.index
                pd.testing.assert_frame_equal(res_est, df_esp, check_dtype=False, check_like=True)
                exito = True

            if exito:
                hash_estudiante = hashlib.sha256(
                    f"{base_code}{self.salt_seguridad}{self.num_tema}".encode()
                ).hexdigest()[:8].upper()
                print(f"✅ ¡Correcto! Código de éxito: {hash_estudiante}")
                return hash_estudiante

        except Exception:
            pass

        return None
