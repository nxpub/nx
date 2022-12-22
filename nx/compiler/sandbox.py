import ast
import importlib

from importlib.util import spec_from_loader, module_from_spec
from importlib.machinery import SourceFileLoader
from functools import partial
from types import CodeType

from nx.compiler.target.wasm import render


def nx_compile(path: str, output_dir: str, platform: str = 'cloudflare') -> None:
    nx_import(path)
    raise NotImplementedError


def nx_import(path: str):
    with open(path) as py_file:
        code = compile(
            source=(py_source := py_file.read()), filename='<target>', mode='exec',
            flags=ast.PyCF_ALLOW_TOP_LEVEL_AWAIT, dont_inherit=True, optimize=0
        )
        nx_exec(code, py_source)


def nx_exec(code_obj: CodeType, py_source: str):
    # TODO: Get rid of dis usage
    import dis
    # TODO: Parse exception table
    # TODO: code_object._varname_from_oparg can be helpful
    code, ext_arg = code_obj.co_code, 0
    for idx in range(0, len(code), 2):
        opcode = code[idx]
        # TODO: Do we want to also get a deoptimized opcode?
        if opcode >= dis.HAVE_ARGUMENT:
            oparg = code[idx + 1] | ext_arg
            ext_arg = (oparg << 8) if opcode == dis.EXTENDED_ARG else 0
        else:
            oparg = None
            ext_arg = 0
    breakpoint()
