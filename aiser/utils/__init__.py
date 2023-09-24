from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
import base64
from .version import get_aiser_version


def base64_to_pem(base64_key) -> str:
    decoded_key = base64.b64decode(base64_key)
    public_key = serialization.load_der_public_key(decoded_key, backend=default_backend())
    pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    return pem.decode()
