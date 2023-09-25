import typing
import jwt
import httpx
import time
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2

from aiser.ai_server.authentication.rest_authenticator import RestAuthenticator, TokenVerificationCallable
from aiser.utils import base64_to_pem
from aiser.models.dtos import PublicKeyInfo
from aiser.ai_server_consumer import AiServerConsumer


class PublicKeyInfoClient:
    def __init__(self, consumer: AiServerConsumer):
        self._consumer = consumer

    async def fetch_public_key_info(self) -> PublicKeyInfo:
        async with httpx.AsyncClient() as client:
            url = str(self._consumer.publicKeyInfoUrl)
            response = await client.get(url)
            response.raise_for_status()
            public_key_info = PublicKeyInfo(**response.json())
            return public_key_info


class PublicKeyInfoGetter:
    def __init__(
            self,
            public_key_info_client: PublicKeyInfoClient,
            refresh_interval_in_seconds: float = 60,
    ):
        self._public_key_info_client = public_key_info_client
        self._public_key_info: typing.Optional[PublicKeyInfo] = None
        self._last_refresh_timestamp: float = 0
        self._refresh_interval_in_seconds = refresh_interval_in_seconds

    async def get_public_key_info(self) -> PublicKeyInfo:
        if (self._public_key_info is None
                or (time.time() - self._last_refresh_timestamp) > self._refresh_interval_in_seconds):
            self._public_key_info = await self._public_key_info_client.fetch_public_key_info()
            self._last_refresh_timestamp = time.time()
        return self._public_key_info


class AsymmetricJwtRestAuthenticator(RestAuthenticator):
    def __init__(
            self,
            complete_server_url: typing.Optional[str],
            consumer: AiServerConsumer
    ):
        self._complete_server_url = complete_server_url
        self._consumer = consumer

        public_key_info_client = PublicKeyInfoClient(consumer=self._consumer)
        public_key_info_getter = PublicKeyInfoGetter(public_key_info_client=public_key_info_client)

        auth_scheme = OAuth2()

        async def verify_token(token: str = Depends(auth_scheme)) -> str:
            try:
                token_without_prefix = token.split(" ")[1]
                public_key = (await public_key_info_getter.get_public_key_info()).publicKey
                public_key_pem = base64_to_pem(public_key)
                decoded_jwt = jwt.decode(jwt=token_without_prefix, key=public_key_pem, algorithms=["RS256"], options={
                    "verify_signature": True,
                    "verify_exp": True,
                    "verify_nbf": True,
                    "verify_iat": True,
                    "verify_aud": False,
                })

                if (self._complete_server_url is not None) and (decoded_jwt['aud'] != self._complete_server_url):
                    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
            except jwt.exceptions.InvalidTokenError as error:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
            return token

        self._verify_token = verify_token

    def get_authentication_dependency(self) -> TokenVerificationCallable:
        return self._verify_token
