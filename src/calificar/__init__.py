# src/calificar/__init__.py

__version__ = "0.1.10"

#Se importa los módulos que están en core
from .core import taller, evafunciones


# Lo que importa cuando colocan 'from calificar import *'
__all__ = ["taller", "evafunciones"]



import numpy as np

print(f"Iniciando Calificar v0.1.0 (Usando Numpy {np.__version__})")


