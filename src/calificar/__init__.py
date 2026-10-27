# src/calificar/__init__.py

__version__ = "0.2.0"

# Se importa los módulos que están en core
from .core import taller, parcial, evafunciones, evacolab

# Lo que importa cuando colocan 'from calificar import *'
__all__ = ["taller", "parcial", "evafunciones", "evacolab"]

import numpy as np

print(f"Iniciando Calificar v{__version__} (Usando Numpy {np.__version__})")
