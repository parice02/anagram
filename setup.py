# -*- coding: utf-8 -*-

'''
@author: Muhammed Zeba (parice02)
'''

import sys
import os
from pathlib import Path
from cx_Freeze import setup, Executable
from datetime import date

# repertoire où est  installé python / environnement python
python_env_dir = Path.cwd() / 'env'
# Récupération du packages tcl nécessaire le GUI
tcl_lib = python_env_dir / "tcl" / 'tcl8.6'
# Récupération du packages tk nécessaire le GUI
tkl_lib = python_env_dir / 'tcl' / 'tk8.6'

os.environ['TCL_LIBRARY'] = tcl_lib.as_posix()
os.environ['TK_LIBRARY'] = tkl_lib.as_posix()


# OPTIONS PREPARATION
path = sys.path.append(python_env_dir)    # os.path.dirname(sys.executable)
includes = ['outils', 'anagram']  # inclusion de modules créés sois-même
excludes = []  # exclusion de modules créés sois-même
packages = ['config', 'locales']  # inclusion de packages créés sois-même
include_files = ['ana.db', 'favicon.png']  # inclusion de fichiers essentiels
options = {}


# TARGET PREPARATION
base = None
tcl86_dll = Path()
tk86_dll = Path()
binpathincludes = []
if sys.platform == "win32":  # and $$WINCONS$$:
    base = "Win32GUI"
    options["include_msvcr"] = True
    tk86_dll = python_env_dir / 'DLLs' / 'tk86t.dll'
    tcl86_dll = python_env_dir / 'DLLs' / 'tcl86t.dll'
    include_files.append(tcl86_dll)
    include_files.append(tk86_dll)
elif sys.platform == "linux2":
    binpathincludes = ["/usr/lib"]
    options['bin_path_includes'] = binpathincludes
    pass
else:
    pass

app = Executable(
    "tk_ui.py",
    base=base,
    copyright=f"Copyright (c) {date.year}",
    icon="favicon.png"
)

options['path'] = path
options['includes'] = includes
options['excludes'] = excludes
options['packages'] = packages
options['optimize'] = 2
options['include_files'] = include_files
# options['create_shared_zip'] = False # Non reconnu sous cx_Freeze 5.1.1
# options['append_script_to_exe'] = True  # Non reconnu sous cx_Freeze 5.1.1
# options['include_in_shared_zip'] = False  # Non reconnu sous cx_Freeze 5.1.1


# SETUP PREPARATION
long_description = str(
    "Application permettant de retrouver l'ensembles anagrammes d'un ensemble de lettres saisies.")

setup(
    name="MyAnagram",
    version="0.0.2",
    description="application pour trouver des anagrammes",
    long_description=long_description,
    author="Muhammed Zeba",
    author_email="parice02@hotmail.com",
    maintainer="Muhammed Zeba",
    maintainer_email="parice02@hotmail.com",
    download_url='',
    license='Libre & Gratuit',
    url="",
    options={"build_exe": options},
    executables=[app]
)
