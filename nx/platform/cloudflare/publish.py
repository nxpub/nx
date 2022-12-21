import os
import json
import requests

from pathlib import Path
from dataclasses import dataclass
from urllib.parse import urljoin
from requests_toolbelt import MultipartEncoder

__all__ = [
    'bundle', 'publish',
]

CF_API_URL = os.getenv('CF_API_URL', 'https://api.cloudflare.com/client/v4/')

# TODO: Figure out the order (credentials file vs env)
CF_API_TOKEN = os.getenv('CF_API_TOKEN', None)
CF_ACCOUNT_ID = os.getenv('CF_ACCOUNT_ID', None)
CF_ZONE_ID = os.getenv('CF_ZONE_ID', None)

DEFAULT_CREDENTIALS_PATH = Path('~/.nx/credentials.json').expanduser()


@dataclass
class Credentials:
    api_token: str
    account_id: str
    zone_id: str


def read_credentials(path: Path | str = DEFAULT_CREDENTIALS_PATH) -> Credentials:
    with open(path) as cred_file:
        return Credentials(**json.load(cred_file))


def bundle():
    raise NotImplementedError


def publish(*, worker_name: str, bundle_path: str, domain_name: str):
    creds = read_credentials()
    session = requests.Session()
    session.headers.update({
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {creds.api_token}',
    })

    # Upload the worker module first
    # TODO: Do we need to remove hardcoded names and have some Bundle dataclass instead?
    mp_encoder = MultipartEncoder(
        fields={
            'metadata': json.dumps({
                'main_module': 'shim.mjs',
            }),
            'shim.mjs': (
                'shim.mjs', open(os.path.join(bundle_path, 'shim.mjs'), 'rb'),
                'application/javascript+module'
            ),
            'generated.js': (
                'generated.js', open(os.path.join(bundle_path, 'generated.js'), 'rb'),
                'application/javascript+module'
            ),
            'worker.wasm': (
                'worker.wasm', open(os.path.join(bundle_path, 'worker.wasm'), 'rb'),
                'application/wasm'
            ),
        }
    )
    resp = session.put(
        url=urljoin(CF_API_URL, f'accounts/{creds.account_id}/workers/scripts/{worker_name}'),
        data=mp_encoder, headers={'Content-Type': mp_encoder.content_type},
    )
    resp.raise_for_status()

    # Attach Custom Domain to the worker
    resp = session.put(
        url=urljoin(CF_API_URL, f'accounts/{creds.account_id}/workers/domains'),
        json={
            # TODO: Allow to customize the env
            'environment': 'production',
            'hostname': domain_name,
            'service': worker_name,
            'zone_id': creds.zone_id,
        },
    )
    resp.raise_for_status()


if __name__ == '__main__':
    publish(
        worker_name='surrogate',
        bundle_path='../../../home/surrogate/',
        domain_name='nx.pub',
    )
