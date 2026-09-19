# src/calificar/__init__.py
 
__version__ = "0.1.21"
 
#Se importa los módulos que están en core
from .core import taller, evafunciones, evacolab
 
 
# Lo que importa cuando colocan 'from calificar import *'
__all__ = ["taller", "evafunciones", "evacolab"]
 
 
 
import numpy as np
 
print(f"Iniciando Calificar v{__version__} (Usando Numpy {np.__version__})")
 