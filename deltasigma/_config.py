# -*- coding: utf-8 -*-
# _config.py
# Module providing configuration switches
# Copyright 2013 Giuseppe Venturini
# This file is part of python-deltasigma.
#
# python-deltasigma is a 1:1 Python replacement of Richard Schreier's
# MATLAB delta sigma toolbox (aka "delsigma"), upon which it is heavily based.
# The delta sigma toolbox is (c) 2009, Richard Schreier.
#
# python-deltasigma is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# LICENSE file for the licensing terms.

"""Module providing configuration switches.
"""

import os
import sys
from warnings import warn

import numpy as np

# NOTE: numpy.distutils was removed in NumPy 2.0. 
# We no longer import get_info.

# should synthesizeNTF run the optimization routine?
optimize_NTF = True

# how many iterations should be allowed in NTF synthesis?
# see synthesizeNTF() for more
itn_limit = 500

# debug
_debug = False

# get blas information to compile the cython extensions
# Since NumPy 2.0 removed distutils, we manually search for cblas.h
# in standard locations and the active Python environment.

candidate_paths = []

# 1. User Override (Environment Variable)
if "BLAS_H" in os.environ:
    candidate_paths.append(os.environ["BLAS_H"])

# 2. Current Python Environment (Conda/Virtualenv)
candidate_paths.append(os.path.join(sys.prefix, 'include'))
if sys.platform == 'win32':
    candidate_paths.append(os.path.join(sys.prefix, 'Library', 'include'))

# 3. System Paths (Linux/Darwin)
if 'linux' in sys.platform or 'darwin' in sys.platform:
    candidate_paths.append('/usr/include')
    candidate_paths.append('/usr/local/include')

# Find the first path that actually contains cblas.h
found_blas_path = None
for path in candidate_paths:
    if path and os.path.isfile(os.path.join(path, 'cblas.h')):
        found_blas_path = path
        break

if not found_blas_path and _debug:
    warn("Could not detect cblas.h in standard system locations.")

# wrap it up: user-set environment var or a lucky guess is needed 
# to get the cblas.h header path. If not found, simulateDSM() will use
# a CPython implementation (slower).
setup_args = {"script_args":(["--compiler=mingw32"]
                             if sys.platform == 'win32' else [])}

lib_include = [np.get_include()]

if found_blas_path:
    lib_include.append(found_blas_path)
elif 'nt' not in os.name:
    # Only warn on non-Windows systems if we fail (consistent with original logic)
    warn("Cannot find the path for 'cblas.h'. You may set it using the environment variable "
         "BLAS_H.\nNOTE: You need to pass the path to the directories where the "
         "header files are, not the path to the files.")

setup_args.update({"include_dirs": list(set(lib_include))})
