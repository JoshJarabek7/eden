from datetime import datetime
from enum import Enum, IntEnum
from typing import Literal

from pydantic import BaseModel, EmailStr, field_validator


class Keys(BaseModel):
    """An object that defines a single JSON Web Key.

    Attributes:
        alg (str): The encryption algorithm used to encrypt the token.
        e (str): The exponent value for the RSA public key.
        kid (str): A 10-character identifier key, obtained from your developer account.
        kty (str): The key type parameter setting. You must set to 'RSA'.
        n (str): The modulus value for the RSA public key.
        use (str): The intended use for the public key.
    """

    alg: str
    e: str
    kid: str
    kty: str
    n: str
    use: str


class JWKSet(BaseModel):
    """A set of JSON Web Key objects.

    Attributes:
        keys (list[Keys]): An array that contains JSON Web Key objects.
    """

    keys: list[Keys]


class ASUserDetectionStatusEnum(IntEnum):
    """User detection status.

    Attributes:
        UNSUPPORTED (int): The device doesn't support real user status determination.
        UNKNOWN (int): The real user status couldn't be determined.
        LIKELY_REAL (int): The user appears to be a real person.
    """

    UNSUPPORTED = 0
    UNKNOWN = 1
    LIKELY_REAL = 2


class IdentityToken(BaseModel):
    """The identity token containing the user's information.

    Attributes:
        iss (str): The issuer identifier.
        sub (str): The unique identifier for the user.
        aud (str): Your client identifier.
        iat (datetime): Issued at timestamp.
        exp (datetime): Expiration timestamp.
        nonce (str | None): A nonce value.
        nonce_supported (bool | None): Indicates if the nonce is supported.
        email (EmailStr | None): The user's email address.
        email_verified (bool | str | None): Whether the email is verified.
        is_private_email (bool | str | None): Whether the email is a private relay.
        real_user_status (ASUserDetectionStatusEnum | None): The user's real status.
        transfer_sub (str | None): The identifier for user migration.
    """

    iss: str
    sub: str
    aud: str
    iat: datetime
    exp: datetime
    nonce: str | None = None
    nonce_supported: bool | None = None
    email: EmailStr | None = None
    email_verified: bool | str | None = None
    is_private_email: bool | str | None = None
    real_user_status: ASUserDetectionStatusEnum | None = None
    transfer_sub: str | None = None

    @field_validator("email_verified", "is_private_email", mode="before")
    def str_to_bool(cls, value):
        if isinstance(value, str):
            return value.lower() == "true"
        return value


class TokenResponse(BaseModel):
    """The response token object returned on a successful request.

    Attributes:
        access_token (str): A token used to access allowed data.
        expires_in (int): The amount of time, in seconds, before the access token expires.
        id_token (str): A JSON Web Token (JWT) that contains the user's identity information.
        refresh_token (str): The refresh token used to regenerate new access tokens.
        token_type (Literal['bearer']): The type of access token, which is always 'bearer'.
    """

    access_token: str
    expires_in: int
    id_token: str
    refresh_token: str
    token_type: Literal["bearer"]


class ErrorType(str, Enum):
    """Enum representing possible error values for an unsuccessful request.

    Attributes:
        INVALID_REQUEST: The request is malformed, typically because it's missing a parameter, contains an unsupported parameter,
            includes multiple credentials, or uses more than one mechanism for authenticating the client.
        INVALID_CLIENT: The client authentication failed, typically due to a mismatched or invalid client identifier, invalid client secret
            (expired token, malformed claims, or invalid signature), or mismatched or invalid redirect URI.
        INVALID_GRANT: The authorization grant or refresh token is invalid, typically due to a mismatched or invalid client identifier,
            invalid code (expired or previously used authorization code), or invalid refresh token.
        UNAUTHORIZED_CLIENT: The client isn't authorized to use this authorization grant type.
        UNSUPPORTED_GRANT_TYPE: The authenticated client isn't authorized to use this grant type.
        INVALID_SCOPE: The requested scope is invalid.
    """

    INVALID_REQUEST = "invalid_request"
    INVALID_CLIENT = "invalid_client"
    INVALID_GRANT = "invalid_grant"
    UNAUTHORIZED_CLIENT = "unauthorized_client"
    UNSUPPORTED_GRANT_TYPE = "unsupported_grant_type"
    INVALID_SCOPE = "invalid_scope"


class ErrorResponse(BaseModel):
    """The error object returned after an unsuccessful request.

    Attributes:
        error (ErrorType): A string that describes the reason for the unsuccessful request.
            It contains exactly one of the specified allowed values.
        error_description (str | None): A human-readable explanation of the error.
        error_uri (str | None): A URI identifying a human-readable web page with information about the error.
    """

    error: ErrorType
    error_description: str | None = None
    error_uri: str | None = None

