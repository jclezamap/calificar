# src/calificar/__init__.py

__version__ = "0.1.17"

#Se importa los módulos que están en core
from .core import taller, evafunciones


# Lo que importa cuando colocan 'from calificar import *'
__all__ = ["taller", "evafunciones"]



import numpy as np

print(f"Iniciando Calificar v{__version__} (Usando Numpy {np.__version__})")


