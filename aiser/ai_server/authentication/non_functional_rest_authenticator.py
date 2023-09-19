from aiser.ai_server.authentication.rest_authenticator import RestAuthenticator, TokenVerificationCallable


class NonFunctionalRestAuthenticator(RestAuthenticator):
    def get_authentication_dependency(self) -> TokenVerificationCallable:
        async def verify_token() -> str:
            return ''

        return verify_token
