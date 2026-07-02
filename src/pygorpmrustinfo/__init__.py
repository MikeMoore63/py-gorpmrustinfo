from __future__ import annotations

from ._pyinstaller import get_hook_dirs, get_PyInstaller_tests

__all__ = [
    "get_hook_dirs",
    "get_PyInstaller_tests",
    "get_rpm_db_info",
    "get_rust_audit",
    "get_go_build_info",
    "get_go_mod",
    "get_go_sum",
]

import ctypes
import json
import os
from pathlib import Path
from sysconfig import get_config_var


here = Path(__file__).absolute().parent
ext_suffix = get_config_var("EXT_SUFFIX")
so_file = os.path.join(here, ("_pygorpmrustinfo" + ext_suffix))

so = ctypes.cdll.LoadLibrary(so_file)

rpmdb_info_so = so.getrpmdbInfo
rpmdb_info_so.argtypes = [ctypes.c_char_p]
rpmdb_info_so.restype = ctypes.c_void_p

rust_audit_so = so.getrustAudit
rust_audit_so.argtypes = [ctypes.c_char_p]
rust_audit_so.restype = ctypes.c_void_p

go_build_info_so = so.getgobuildinfo
go_build_info_so.argtypes = [ctypes.c_char_p]
go_build_info_so.restype = ctypes.c_void_p

go_mod_so = so.getgomod
go_mod_so.argtypes = [ctypes.c_char_p]
go_mod_so.restype = ctypes.c_void_p

free = so.free
free.argtypes = [ctypes.c_void_p]


def _call_go_function(func, file_name):
    res = func(file_name.encode("utf-8"))
    if res is None:
        return {"error": "empty response"}
    try:
        return json.loads(ctypes.string_at(res).decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        return {"error": "Error converting result to json"}
    finally:
        free(res)


def get_rpm_db_info(file_name):
    return _call_go_function(rpmdb_info_so, file_name)


def get_rust_audit(file_name):
    return _call_go_function(rust_audit_so, file_name)


def get_go_build_info(file_name):
    return _call_go_function(go_build_info_so, file_name)


def get_go_mod(file_name):
    return _call_go_function(go_mod_so, file_name)


def get_go_sum(file_name):
    result = {"error": "not a valid go sum file"}
    if not os.path.isfile(file_name):
        return result
    with open(file_name, mode="rt", encoding="utf-8") as handle:
        data = {}
        for line in handle.readlines():
            sumfields = line.strip().split()
            if len(sumfields) < 3:
                continue
            if sumfields[1].endswith("/go.mod"):
                sumfields[1] = sumfields[1][:-7]
            data[sumfields[0]] = {"Version": sumfields[1], "Sum": sumfields[2]}
        if data:
            return {
                "Deps": [
                    {"Path": k, "Version": data[k]["Version"], "Sum": data[k]["Sum"]}
                    for k in data
                ]
            }
    return result
