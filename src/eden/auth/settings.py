from pydantic_settings import BaseSettings, SettingsConfigDict


class AppleSignInConfig(BaseSettings):
    """
    Configuration settings for Sign in with Apple integration.

    Environment Prefix is 'SIWA_'.

    Attributes:
        client_id (str): Your Service ID registered with Apple.
        team_id (str): Your Apple Developer Team ID.
        key_id (str): The Key ID of your private key.
        private_key (str): The private key in PEM format.
        redirect_uri (str): The redirect URI after authentication.
        scope (str): Scopes to request from the user.
        response_mode (str): How the authorization response is returned.
        response_type (str): The type of response desired.
        state (str | None): Optional state parameter to prevent CSRF.

    """

    client_id: str
    team_id: str
    key_id: str
    private_key: str
    redirect_uri: str
    scope: str = "email name"
    response_mode: str = "form_post"
    response_type: str = "code id_token"
    state: str | None = None

    model_config = SettingsConfigDict(env_prefix="SIWA_")
