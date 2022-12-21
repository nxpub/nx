import sys


def run(args: list[str] | None = None):
    if not args:
        args = sys.argv[1:]
    # Import .py, compile to wasm
    #  - binaryen to render wasm, source maps
    # Bundle the worker
    # Upload the worker to Cloudflare
    #  - CF API client
    raise NotImplementedError


if __name__ == '__main__':
    run([
        'publish', '/home/nxpub/dev/home/home/main.py', 'nx.pub'
    ])
