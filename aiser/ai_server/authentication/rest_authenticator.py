from abc import ABC, abstractmethod
import typing

TokenVerifyCoroutine = typing.Coroutine[typing.Any, typing.Any, str]
TokenVerificationCallable = typing.Callable[[...], TokenVerifyCoroutine]


class RestAuthenticator(ABC):
    @abstractmethod
    def get_authentication_dependency(self) -> TokenVerificationCallable:
        raise NotImplementedError
