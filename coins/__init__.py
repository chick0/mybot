from os import path, listdir

__all__ = [file_name[:-3] for file_name in listdir(path.dirname(__file__))
           if file_name.endswith(".py") and not file_name.startswith("_")]

from coins import *
del path, listdir
