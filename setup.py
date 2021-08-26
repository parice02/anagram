# -*- coding: utf-8 -*-

"""
@author: Muhammed Zeba (parice02)
"""

import sys
import os
from pathlib import Path
from cx_Freeze import setup, Executable
from datetime import date

from utility import load_license
from tk_ui import _config

__version__, __author__ = _config["version"], _config["author"]
__license__ = load_license()

# repertoire où est  installé python / environnement python
python_env_dir = Path.cwd() / "env"
# Récupération du packages tcl nécessaire le GUI
tcl_lib = python_env_dir / "tcl" / "tcl8.6"
# Récupération du packages tk nécessaire le GUI
tkl_lib = python_env_dir / "tcl" / "tk8.6"

os.environ["TCL_LIBRARY"] = tcl_lib.as_posix()
os.environ["TK_LIBRARY"] = tkl_lib.as_posix()


# OPTIONS PREPARATION
path = sys.path.append(python_env_dir)  # os.path.dirname(sys.executable)
includes = ["utility", "anagram", "tk_ui"]  # inclusion de modules créés sois-même
excludes = []  # exclusion de modules créés sois-même
# packages = ["config", "locales"]  # inclusion de packages créés sois-même
include_files = [
    "db.db",
    "favicon.png",
    "LICENSE",
    "config/",
    "locales/",
]  # inclusion de fichiers essentiels
options = {}

base = None
# TARGET PREPARATION
if sys.platform == "win32":
    tcl86_dll = Path()
    tk86_dll = Path()
    base = "Win32GUI"
    options["include_msvcr"] = True
    tk86_dll = python_env_dir / "DLLs" / "tk86t.dll"
    tcl86_dll = python_env_dir / "DLLs" / "tcl86t.dll"
    include_files.append(tcl86_dll)
    include_files.append(tk86_dll)
elif sys.platform.startswith("linux"):
    options["bin_path_includes"] = ["/usr/lib"]
else:
    # darwin => macOS
    # freebsd/netbsd/sunos...
    pass

app = Executable(
    script="main.py",
    base=base,
    copyright=f"Copyright (c) {date.year}",
    icon="favicon.png",
    target_name="Anagrameur",
    shortcut_dir="anagrameur",
    shortcut_name="anagrameur",
)

options["path"] = path
options["includes"] = includes
options["excludes"] = excludes
# options["packages"] = packages
options["optimize"] = 2
options["include_files"] = include_files
# options["build_exe"] = "build/anagrameur"  # nom du dossier d'installation
options["silent"] = True


# SETUP PREPARATION
long_description = str(
    "Application permettant de retrouver l'ensembles anagrammes d'un ensemble de lettres saisies."
)

setup(
    name="MyAnagram",
    version=__version__,
    description="Application pour trouver des anagrammes",
    long_description=long_description,
    author=__author__["name"],
    author_email=__author__["email"],
    maintainer=__author__["name"],
    maintainer_email=__author__["email"],
    download_url="",
    license=__license__,
    url=__author__["project"],
    options={"build_exe": options},
    executables=[app],
)
