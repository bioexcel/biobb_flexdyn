""" Common functions for package biobb_flexdyn.flexdyn """
import os
from pathlib import Path
from typing import Optional


def concoord_lib(concoord_lib_path: Optional[str]) -> Path:
    """Go from the concoord_lib_path property to the CONCOORD library folder: the property, else the
    CONCOORDLIB environment variable. ValueError if neither is set."""
    lib = concoord_lib_path or os.getenv("CONCOORDLIB")
    if not lib:
        raise ValueError("No CONCOORD library folder: set the concoord_lib_path property or the CONCOORDLIB environment variable")
    return Path(lib)
