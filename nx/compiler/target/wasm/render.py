import binaryen as asm

from typing import Optional


def sandbox(
    *, wasm_path: str,
    wat_path: Optional[str] = None,
    source_map_path: Optional[str] = None,
    source_map_url: Optional[str] = None
) -> None:
    source_map_url = ''
    module = asm.ModuleCreate()
    # Create imports
    asm.AddFunctionImport(module, b'~/lib/bindings/dom/console.log', b'env', b'console.log', asm.TypeInt32(), asm.TypeNone())
    # Create types (order?)
    # asm.TypeCreate()
    # Iterate over exported Python functions
    # for _ in ():
    #     func_name = params = results = var_types = []
    #     relooper = asm.RelooperCreate(module)
    #     block = asm.RelooperAddBlock(relooper, _)
    #     func_body = asm.RelooperRenderAndDispose(relooper, block, 0)
    #     func_ref = asm.AddFunction(module, func_name, params, results, var_types, len(var_types), func_body)
    #     # TODO: Add function
    literal = asm.LiteralInt32(1056)
    asm.AddFunction(
        module, b'$worker/fetch', asm.TypeNone(), asm.TypeInt32(), asm.ffi.NULL, 0,
        asm.Const(module, literal.i32)
    )
    asm.AddFunction(
        module, b'$worker/scheduled', asm.TypeNone(), asm.TypeNone(), asm.ffi.NULL, 0,
        asm.Const(module, asm.LiteralInt32(1184))
    )
    asm.AddFunction(
        module, b'$worker/email', asm.TypeNone(), asm.TypeNone(), asm.ffi.NULL, 0,
        asm.Const(module, asm.LiteralInt32(1248))
    )
    # Export functions
    asm.AddFunctionExport(module, b'$worker/fetch', b'fetch')
    # Export memory
    # TODO: asm.AddMemoryExport(module, b'memory', b'memory')
    # Render module
    if asm.ModuleValidate(module):
        if wat_path:
            wat_body = asm.ModuleAllocateAndWriteText(module)  # wat
            with open(wat_path, 'wb') as wat_file:
                wat_file.write(asm.ffi.string(wat_body))
        result = asm.ModuleAllocateAndWrite(module, source_map_url.encode())  # wasm + source_maps
        if source_map_path:
            with open(source_map_path, 'wb') as map_file:
                map_file.write(asm.ffi.string(result.sourceMap))
        with open(wasm_path, 'wb') as wasm_file:
            wasm_file.write(asm.ffi.buffer(result.binary, result.binaryBytes))
    else:
        raise Exception('TODO')
    asm.ModuleDispose(module)


if __name__ == '__main__':
    sandbox(
        wasm_path='/home/nxpub/dev/nxhome/replica/worker.wasm',
        wat_path='/home/nxpub/dev/nxhome/replica/worker.wat',
        source_map_path='/home/nxpub/dev/nxhome/replica/worker.map',
        source_map_url='https://nx.pub',
    )
