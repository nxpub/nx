import sys
import shutil

from pathlib import Path

from nx.compiler import nx_compile
from nx.platforms.cloudflare import cf_bundle, cf_publish


def _prepare_build_dir(path: str) -> str:
    output_path = Path(path).parent / 'build'
    if output_path.exists():
        shutil.rmtree(output_path)
    output_path.mkdir()
    return str(output_path)


def run(args: list[str] | None = None):
    if not args:
        args = sys.argv[1:]
    if (cmd := args[0]) == 'publish':
        build_dir = _prepare_build_dir(args[1])
        nx_compile(args[1], build_dir)
        cf_bundle(build_dir)
        cf_publish('pytest', build_dir, args[2])
    else:
        raise NotImplementedError(f'Unknown command {cmd}')


if __name__ == '__main__':
    run([
        'publish', '../../nxhome/nxhome/main.py', 'nx.pub'
    ])
